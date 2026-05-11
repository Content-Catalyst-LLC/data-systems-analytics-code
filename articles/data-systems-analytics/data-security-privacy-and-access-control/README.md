# Data Security, Privacy, and Access Control

This companion code models security, privacy, and access control as architectural governance over data power rather than as a narrow permissions checklist.

The examples use small security classification, access-policy, entitlement, privacy-purpose, audit-log, and data-flow datasets to show how a governed data platform can evaluate least privilege, privacy risk, overexposure, entitlement drift, purpose limitation, auditability, and sensitive-data propagation.

## Included languages and examples

- `python/` — security/privacy/access scorecard, entitlement drift review, and manifest
- `r/` — classification, access, privacy-purpose, and audit summaries
- `julia/` — privacy exposure and access-risk scoring
- `sql/` — schema and access-governance queries
- `go/` — access policy contract validation utility
- `rust/` — entitlement and classification inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for access policy files
- `cpp/` — sensitive-data flow adjacency example
- `typescript/` — typed data asset, policy, and access-decision contracts
- `terraform/` — non-deploying placeholder for security and access-control resource categories
- `bash/` — orchestration wrapper
- `docs/` — security/privacy canvas, access review checklist, and data-classification checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Security, privacy, and access control should be evaluated as a connected governance system:

```text
classified assets → access policies → identities and entitlements
        → purpose limitation + minimization + masking/tokenization
        → audit logs + monitoring + entitlement review
```

A trustworthy data system does not only ask whether data can be queried. It asks whether access is justified, minimized, auditable, proportionate, and aligned with legitimate purpose.
