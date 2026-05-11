# Notebook guidance

Use notebooks to inspect access and privacy scorecards, not to hide security logic.

Recommended pattern:

1. Run `python/security_privacy_access_scorecard.py`.
2. Load `outputs/security_privacy_access_manifest_python.json`.
3. Inspect asset-level governance score, residual risk, entitlement drift, privacy-purpose review, and anomaly flags.
4. Compare classification, policy, entitlement, and audit signals.
5. Keep exploratory analysis separate from official access-control logic.
