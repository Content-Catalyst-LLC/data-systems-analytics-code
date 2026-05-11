# Notebook guidance

Use notebooks to inspect metadata trust, catalog use, lineage depth, and provenance, not to hide official catalog or lineage logic.

Recommended pattern:

1. Run `python/metadata_catalog_lineage_scorecard.py`.
2. Load `outputs/metadata_catalog_lineage_manifest_python.json`.
3. Inspect asset-level metadata trust, evidence gaps, metadata quality, policy enforcement, lineage depth, and provenance completeness.
4. Compare certified, reviewed, uncertified, and legacy assets.
5. Keep exploratory metadata analysis separate from official governance rules and catalog certification.
