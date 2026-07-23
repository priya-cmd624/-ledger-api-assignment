# Task 3 – Service Mesh & Zero Trust (Istio)

## Objective

The goal of this task was to secure communication between Kubernetes workloads using Istio Service Mesh and implement Zero Trust security principles by enforcing mutual TLS (mTLS), workload identity-based authorization, and Kubernetes NetworkPolicies.

---

# Istio Installation

Istio was installed using the demo profile.

```bash
istioctl install --set profile=demo -y
```

The application namespace was enabled for automatic sidecar injection.

```bash
kubectl label namespace payments istio-injection=enabled
```

Pods were restarted so that the Envoy proxy sidecars were injected.

---

# Mutual TLS (mTLS)

A PeerAuthentication policy was configured in STRICT mode.

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication

spec:
  mtls:
    mode: STRICT
```

STRICT mode forces every workload to communicate only over encrypted mutual TLS.

Verification command:

```bash
istioctl authn tls-check
```

Evidence is available in the evidence folder.

---

# Authorization Policy

A default-deny AuthorizationPolicy was created.

Only workloads running with the authorized Kubernetes ServiceAccount are allowed to access ledger-api.

Example SPIFFE identity:

```
spiffe://cluster.local/ns/payments/sa/reporting-sa
```

Any workload without the permitted identity is denied automatically.

---

# Unauthorized Access Test

A test pod was deployed without the required ServiceAccount.

The request to ledger-api was denied.

This demonstrates Zero Trust access control based on workload identity instead of IP address.

---

# Authorized Access

The reporting service running with the approved ServiceAccount successfully communicated with ledger-api.

---

# Workload Identity (SPIFFE)

Istio assigns every workload a unique SPIFFE identity.

Example:

```
spiffe://cluster.local/ns/payments/sa/reporting-sa
```

AuthorizationPolicy evaluates this identity before allowing requests.

---

# Workload Certificates

Istio automatically issues X.509 certificates to workloads through Istiod.

Certificate lifecycle:

1. Workload starts.
2. Envoy contacts Istiod.
3. Istiod issues a signed certificate.
4. Envoy stores the certificate.
5. Certificates are rotated automatically before expiry.

No manual certificate management is required.

---

# Trust Root

The trust root is the Istio Certificate Authority (CA) managed by Istiod.

Every workload trusts certificates signed by this CA.

---

# Kubernetes NetworkPolicy

A default-deny NetworkPolicy was implemented.

Only explicitly allowed traffic can reach ledger-api.

NetworkPolicy protects Layer 3/Layer 4 communication.

---

# Defense in Depth

Istio AuthorizationPolicy and Kubernetes NetworkPolicy protect different layers.

## AuthorizationPolicy

- Layer 7
- Uses workload identity
- Understands HTTP/gRPC
- Enforces Zero Trust

## NetworkPolicy

- Layer 3/4
- Uses Pods/IPs/Ports
- Controls network connectivity
- Blocks unauthorized network traffic

Using both together provides defense in depth.

---

# Evidence

Implementation evidence is available under:

```
task-3/evidence/
```

Configuration manifests:

```
task-3/istio/
```

---

# Bonus

The assessment also mentions:

- Istio Ingress Gateway
- TLS termination
- Canary deployment using VirtualService and DestinationRule

These were not implemented as part of the core task.
