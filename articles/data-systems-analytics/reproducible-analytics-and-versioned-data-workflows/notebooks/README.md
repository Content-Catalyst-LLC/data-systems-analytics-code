# Notebook guidance

For this article, notebooks should be treated as an interface over a reproducible workflow, not as the workflow itself.

Recommended notebook pattern:

1. Call `python/reproducible_workflow.py` rather than duplicating hidden logic.
2. Read generated outputs from `outputs/`.
3. Display the manifest and fingerprints.
4. Compare two run manifests to show whether a result changed because of code, data, parameters, or environment.
5. Keep exploratory cells separate from promoted workflow logic.
