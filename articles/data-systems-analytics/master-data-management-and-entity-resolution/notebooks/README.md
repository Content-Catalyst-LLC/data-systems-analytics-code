# Notebook guidance

Use notebooks to inspect candidate matches, stewardship queues, and hierarchy risks, not to hide official match or survivorship logic.

Recommended pattern:

1. Run `python/mdm_entity_resolution_scorecard.py`.
2. Load `outputs/mdm_entity_resolution_manifest_python.json`.
3. Inspect candidate match risk, master entity governance scores, crosswalk confidence, survivorship review, hierarchy edges, and privacy-risk records.
4. Compare deterministic, probabilistic, hybrid, and steward-reviewed actions.
5. Keep exploratory linkage analysis separate from approved mastered relationships.
