# ledger-api

Payments microservice for tokenising PANs and serving transaction metadata.
Deployed on Kubernetes in the `payments` namespace.

## Endpoints

| Method | Path            | Description                          |
|--------|-----------------|-------------------
| GET    | `/health`       | Liveness check                       |
| POST   | `/tokenize`     | `{"pan": "..."}` → opaque token      |
| GET    | `/transactions` | Recent transaction records           |
| POST   | `/import`       | Import a YAML configuration blob     |
| GET    | `/fetch?url=`   | Fetch a remote resource by URL       |
# Ledger API DevSecOps Security Assessment

This repository contains my solutions for the DevSecOps assessment. The implementation focuses on Kubernetes security hardening, secure CI/CD, GitOps, Zero Trust networking with Istio, and an authorized security assessment.

## Repository Structure

- `task-1/` – Kubernetes Security Hardening
- `task-2/` – Secure CI/CD Pipeline & GitOps
- `task-3/` – Zero Trust Networking with Istio
- `task-4/` – Reconnaissance & Penetration Testing

---

# Task 1 – Kubernetes Security Hardening

**Location:** `task-1/`

Implemented:
- Hardened Dockerfile
- Non-root containers
- Read-only root filesystem
- Dropped Linux capabilities
- RuntimeDefault seccomp profile
- RBAC
- Kubernetes NetworkPolicies
- Kyverno admission policies
- ConfigMap-based configuration

---

# Task 2 – Secure Delivery

**Location:** `task-2/`

Implemented:
- GitHub Actions CI/CD
- Gitleaks secret scanning
- Semgrep SAST
- Trivy filesystem and container image scanning
- Docker image build
- GitHub Container Registry (GHCR)
- Cosign image signing
- GitHub Artifact Attestations
- ArgoCD GitOps deployment

---

# Task 3 – Zero Trust & Networking

**Location:** `task-3/`

Implemented:
- Istio Service Mesh
- STRICT mTLS
- PeerAuthentication
- AuthorizationPolicy
- Kubernetes NetworkPolicy
- SPIFFE workload identities
- Authorized and unauthorized access verification

---

# Task 4 – Offensive Security Assessment

**Location:** `task-4/`

Included:
- Passive reconnaissance
- Technology fingerprinting
- Vulnerability assessment
- Proof of Concept (PoC)
- CVSS scoring
- Remediation recommendations
- Final penetration testing report

---

## Evidence

Each task contains an `evidence/` directory with supporting outputs, screenshots, and verification artifacts.

## Author

Bandela Priyanka
