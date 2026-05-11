# Notebook guidance

Use notebooks to inspect decision-support scorecards, not to hide certified metric logic.

Recommended pattern:

1. Run `python/decision_support_scorecard.py`.
2. Load `outputs/bi_decision_support_manifest_python.json`.
3. Inspect dashboard decision-support scores, metric trust scores, alert response, and traceability.
4. Compare certified dashboards against reviewed, uncertified, and deprecated dashboards.
5. Keep exploratory analysis separate from official BI reporting logic.
