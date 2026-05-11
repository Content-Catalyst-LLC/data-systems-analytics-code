# Terraform placeholder

This folder intentionally does not provision real cloud resources.

A production metadata, catalog, and lineage platform might include Terraform modules for:

- metadata service accounts
- catalog workspaces
- lineage collection jobs
- data quality metadata stores
- OpenLineage-compatible backends
- glossary and taxonomy services
- policy-tag propagation
- audit logs
- catalog access groups
- notification channels for ownership review

Keep provider-specific infrastructure outside this article scaffold unless a deployment target is explicitly selected.
