"""
Data Lifecycle Management and Retention
Python workflow: classify data assets, apply retention rules, respect legal holds,
and generate disposition review evidence.

This workflow is intentionally compact and educational. Real retention schedules
should be reviewed by legal, records-management, privacy, security, archival,
and business stakeholders.
"""

from pathlib import Path
import json
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = pd.Timestamp("2026-03-31")

ASSET_PATH = DATA_DIR / "retention_assets.csv"
RULE_PATH = DATA_DIR / "retention_rules.csv"

assets = pd.read_csv(ASSET_PATH)
rules = pd.read_csv(RULE_PATH)

date_columns = ["created_date", "trigger_date", "last_accessed_date"]

for column in date_columns:
    assets[column] = pd.to_datetime(assets[column])

assets["legal_hold"] = assets["legal_hold"].astype(bool)
rules["requires_archival_review"] = rules["requires_archival_review"].astype(bool)

inventory = assets.merge(
    rules,
    on="retention_category",
    how="left",
    validate="many_to_one"
)

if inventory["retention_years"].isna().any():
    missing = inventory.loc[inventory["retention_years"].isna(), "retention_category"].unique()
    raise ValueError(f"Missing retention rules for categories: {missing}")

inventory["retention_expiration_date"] = inventory.apply(
    lambda row: row["trigger_date"] + pd.DateOffset(years=int(row["retention_years"])),
    axis=1
)

inventory["days_since_last_access"] = (
    TODAY - inventory["last_accessed_date"]
).dt.days

inventory["retention_expired"] = TODAY > inventory["retention_expiration_date"]
inventory["ownership_gap"] = inventory["owner"].isna() | (inventory["owner"].astype(str).str.strip() == "")

def determine_lifecycle_status(row: pd.Series) -> str:
    """Assign a lifecycle status from retention, ownership, hold, and archival metadata."""
    if row["legal_hold"]:
        return "retain_legal_hold"

    if row["ownership_gap"]:
        return "assign_owner_before_disposition"

    if row["requires_archival_review"] and row["archival_value"] == "high":
        return "archive_review_required"

    if row["retention_expired"] and row["downstream_dependencies"] > 0:
        return "review_dependencies_before_disposition"

    if row["retention_expired"]:
        return "eligible_for_disposition"

    if row["days_since_last_access"] > 365 and row["archival_value"] == "low":
        return "inactive_monitor_for_future_disposition"

    return "active_retain"

inventory["lifecycle_status"] = inventory.apply(determine_lifecycle_status, axis=1)

review_statuses = [
    "eligible_for_disposition",
    "review_dependencies_before_disposition",
    "archive_review_required",
    "retain_legal_hold",
    "assign_owner_before_disposition"
]

disposition_register = inventory[
    inventory["lifecycle_status"].isin(review_statuses)
].copy()

next_step_map = {
    "eligible_for_disposition": "Approve deletion, anonymization, or secure sanitization and record evidence",
    "review_dependencies_before_disposition": "Review lineage and downstream dependencies before disposal",
    "archive_review_required": "Evaluate long-term preservation, restricted access, or archival transfer",
    "retain_legal_hold": "Suspend normal disposition until hold is released",
    "assign_owner_before_disposition": "Assign accountable owner before lifecycle decision"
}

disposition_register["recommended_next_step"] = disposition_register["lifecycle_status"].map(next_step_map)

evidence_template = disposition_register.assign(
    review_date=TODAY.date().isoformat(),
    reviewer="pending_assignment",
    disposition_authority="pending_policy_reference",
    disposition_method="pending_decision",
    verification_required=True
)

inventory_output = OUTPUT_DIR / "lifecycle_inventory.csv"
register_output = OUTPUT_DIR / "disposition_review_register.csv"
evidence_output = OUTPUT_DIR / "disposition_evidence_template.csv"
summary_output = OUTPUT_DIR / "lifecycle_summary.json"

inventory.to_csv(inventory_output, index=False)
disposition_register.to_csv(register_output, index=False)
evidence_template.to_csv(evidence_output, index=False)

summary = {
    "article": "Data Lifecycle Management and Retention",
    "run_date": TODAY.date().isoformat(),
    "asset_count": int(len(inventory)),
    "expired_assets": int(inventory["retention_expired"].sum()),
    "legal_hold_assets": int(inventory["legal_hold"].sum()),
    "ownership_gaps": int(inventory["ownership_gap"].sum()),
    "archive_review_assets": int((inventory["lifecycle_status"] == "archive_review_required").sum()),
    "disposition_review_assets": int(len(disposition_register)),
    "total_storage_gb": float(inventory["storage_gb"].sum()),
    "outputs": {
        "lifecycle_inventory": str(inventory_output.relative_to(BASE_DIR)),
        "disposition_review_register": str(register_output.relative_to(BASE_DIR)),
        "disposition_evidence_template": str(evidence_output.relative_to(BASE_DIR))
    }
}

summary_output.write_text(json.dumps(summary, indent=2))

print("Lifecycle inventory written to:", inventory_output)
print("Disposition register written to:", register_output)
print("Evidence template written to:", evidence_output)
print("Summary written to:", summary_output)
print(json.dumps(summary, indent=2))
