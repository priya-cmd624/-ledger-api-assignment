# Task 1 – Harden the Ledger API

## Objective

Deploy the Ledger API locally on Kubernetes and harden the original insecure workload using container and Kubernetes security best practices.

## Implemented Security Controls

### Container hardening

- Runs the application as a non-root user
- Prevents privilege escalation
- Uses a read-only root filesystem
- Drops unnecessary Linux capabilities
- Uses a hardened Dockerfile

### Kubernetes workload security

- Resource requests and limits
- Liveness and readiness probes
- Kubernetes Secret for application configuration
- Restricted RBAC permissions
- NetworkPolicy for traffic restriction

### Admission control

Kyverno was used to enforce non-root container execution.

An intentionally insecure deployment was applied to verify the policy. Kyverno rejected the workload, proving that the admission policy was working.

### Ingress

An Ingress resource was configured to expose the Ledger API locally. The `/health` endpoint was tested successfully through the Ingress.

## Folder Structure

```text
task-1/
├── hardened/
│   ├── Dockerfile
│   ├── deployment.yaml
│   └── networkpolicy.yaml
├── insecure/
│   ├── Dockerfile.insecure
│   ├── deployment.yaml
│   ├── namespace.yaml
│   ├── neighbour.yaml
│   └── service.yaml
├── ingress/
│   └── ledger-api-ingress.yaml
├── kyverno/
│   └── require-nonroot.yaml
├── rbac/
│   └── ledger-api-rbac.yaml
├── secrets/
│   └── ledger-api-secret.yaml
└── evidence/
```

## Evidence

The `evidence/` folder contains proof of:

- Ingress creation
- Ingress configuration
- Successful access to the health endpoint
- Kyverno policy installation
- Rejection of an insecure Kubernetes workload

## Verification Commands

```bash
kubectl get pods -n payments
kubectl get deployments -n payments
kubectl get ingress -n payments
kubectl get networkpolicy -n payments
kubectl get clusterpolicy
kubectl describe deployment ledger-api -n payments
```

## Security Note

No real credentials are stored in this repository. The Kubernetes Secret manifest contains only a test or placeholder value and must be replaced securely during deployment.
