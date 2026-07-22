import hashlib
import ipaddress
import os
import socket
from urllib.parse import urlparse

import requests
import yaml
from flask import Flask, jsonify, request

app = Flask(__name__)

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

ALLOWED_FETCH_HOSTS = {
    "example.com",
    "api.example.com",
}

LEDGER = [
    {
        "id": "txn_1001",
        "pan": "4242424242424242",
        "amount": 1200,
        "currency": "USD",
    },
    {
        "id": "txn_1002",
        "pan": "5555555555554444",
        "amount": 2500,
        "currency": "USD",
    },
]


def is_valid_pan(pan: str) -> bool:
    return pan.isdigit() and 12 <= len(pan) <= 19


def mask_pan(pan: str) -> str:
    return f"**** **** **** {pan[-4:]}"


def is_safe_url(url: str) -> bool:
    try:
        parsed_url = urlparse(url)

        if parsed_url.scheme != "https":
            return False

        hostname = parsed_url.hostname

        if not hostname or hostname not in ALLOWED_FETCH_HOSTS:
            return False

        resolved_ip = socket.gethostbyname(hostname)
        ip_address = ipaddress.ip_address(resolved_ip)

        if (
            ip_address.is_private
            or ip_address.is_loopback
            or ip_address.is_link_local
            or ip_address.is_reserved
            or ip_address.is_multicast
        ):
            return False

        return True

    except (ValueError, socket.gaierror):
        return False


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="healthy"), 200


@app.route("/tokenize", methods=["POST"])
def tokenize():
    request_data = request.get_json(silent=True) or {}
    pan = str(request_data.get("pan", "")).strip()

    if not is_valid_pan(pan):
        return jsonify(error="Invalid PAN"), 400

    token = hashlib.sha256(pan.encode("utf-8")).hexdigest()

    return jsonify(token=token), 200


@app.route("/transactions", methods=["GET"])
def transactions():
    safe_transactions = [
        {
            "id": transaction["id"],
            "pan": mask_pan(transaction["pan"]),
            "amount": transaction["amount"],
            "currency": transaction["currency"],
        }
        for transaction in LEDGER
    ]

    return jsonify(transactions=safe_transactions), 200


@app.route("/import", methods=["POST"])
def import_config():
    try:
        config = yaml.safe_load(request.data) or {}
    except yaml.YAMLError:
        return jsonify(error="Invalid YAML"), 400

    if not isinstance(config, dict):
        return jsonify(error="YAML must contain an object"), 400

    return jsonify(config=config), 200


@app.route("/fetch", methods=["GET"])
def fetch():
    url = request.args.get("url", "").strip()

    if not is_safe_url(url):
        return jsonify(error="URL is not allowed"), 400

    try:
# URL is restricted to HTTPS, an explicit hostname allowlist,
# and validated against private, loopback, link-local and reserved IPs.
# nosemgrep: python.flask.security.injection.ssrf-requests.ssrf-requests
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False,
        )
        response.raise_for_status()
    except requests.RequestException:
        return jsonify(error="Unable to fetch URL"), 502

    return jsonify(
        status_code=response.status_code,
        content=response.text[:1000],
    ), 200
