# Reproducible Analytics and Versioned Data Workflows

This article companion code demonstrates how a data system can preserve analytical trust by connecting versioned inputs, versioned logic, workflow execution, data fingerprints, environment records, outputs, and provenance metadata.

The examples are intentionally small, portable, and inspectable. Each language implementation reads the same sample dataset and produces summary outputs or workflow metadata so the article can show reproducibility as a systems property rather than as a single-tool habit.

## Folder structure

- `data/` — small sample input data and generated immutable snapshots
- `python/` — standard-library workflow runner with fingerprints, manifest, and summary output
- `r/` — base R reproducible summary example
- `julia/` — Julia workflow summary and manifest example
- `sql/` — schema, run manifest table, and reproducibility queries
- `go/` — compiled reproducible summary example
- `rust/` — Cargo project for reproducible CSV summary
- `c/` — C example for lightweight file fingerprinting
- `cpp/` — C++ example for reproducible grouping and fingerprinting
- `bash/` — orchestration wrapper
- `configs/` — declarative workflow metadata
- `docs/` — provenance model and reproducibility checklist
- `notebooks/` — notebook guidance
- `outputs/` — generated outputs and manifests
- `ci/` — GitHub Actions workflow template

## Basic run

```bash
bash bash/run_all.sh
```

The script runs the portable Python workflow and then attempts the other language examples when local toolchains are available.

## Design idea

A reproducible analytics run should preserve at least this chain:

```text
input data snapshot + code version + environment + parameters + execution timestamp
        → workflow run id
        → output artifacts
        → manifest and lineage record
```

That chain makes results inspectable, rerunnable, comparable, and auditable.
