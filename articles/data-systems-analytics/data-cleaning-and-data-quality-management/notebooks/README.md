# Notebook guidance

Use notebooks to inspect quality evidence, not to hide official cleaning logic.

Recommended pattern:

1. Run `python/data_quality_scorecard.py`.
2. Load `outputs/data_quality_manifest_python.json`.
3. Inspect cleaned records, rejects, lineage, survivorship review, rule scorecard, dimension summary, incidents, and root causes.
4. Compare repairs against disclosures and stewardship review items.
5. Preserve unresolved uncertainty before downstream reporting, modeling, or publication.
