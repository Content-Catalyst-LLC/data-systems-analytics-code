# Methodology: Data Lifecycle Management and Retention

This companion workflow treats lifecycle governance as a structured evidence problem.

## Core fields

- `asset_id`: stable identifier for the data asset.
- `system`: platform or system where the asset is stored.
- `owner`: accountable business, technical, or stewardship owner.
- `classification`: privacy, confidentiality, regulatory, or analytical classification.
- `retention_category`: category used to assign schedule logic.
- `trigger_date`: date from which retention begins.
- `legal_hold`: flag that suspends ordinary disposition.
- `archival_value`: low, medium, or high value for preservation review.
- `downstream_dependencies`: number of known dependent reports, models, tables, extracts, or workflows.

## Lifecycle statuses

- `active_retain`: asset remains within active retention.
- `inactive_monitor_for_future_disposition`: asset is inactive but not yet expired.
- `eligible_for_disposition`: asset is expired and has no major blockers.
- `review_dependencies_before_disposition`: asset is expired but has downstream dependencies.
- `archive_review_required`: asset has high archival value or preservation significance.
- `retain_legal_hold`: asset is blocked from ordinary disposition.
- `assign_owner_before_disposition`: ownership must be resolved before lifecycle action.

## Governance interpretation

The workflows are not legal advice. They are scaffolds for making retention logic visible, reproducible, and auditable.
