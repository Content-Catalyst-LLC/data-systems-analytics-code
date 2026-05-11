# Architecture notes

This example treats a modern cloud data platform as a layered architecture rather than a fixed vendor stack.

A useful reference model includes:

1. **Sources**
   - operational databases
   - SaaS platforms
   - files and APIs
   - event streams
   - logs and telemetry

2. **Ingestion**
   - batch loading
   - change data capture
   - streaming
   - API pulls
   - file arrival monitoring

3. **Storage**
   - raw zones
   - curated zones
   - warehouses
   - lakehouse tables
   - purpose-built stores

4. **Transformation**
   - versioned SQL models
   - code-based transformations
   - tests
   - quality gates
   - deployment discipline

5. **Orchestration**
   - scheduling
   - dependency management
   - retries
   - backfills
   - run metadata

6. **Metadata and lineage**
   - catalog registration
   - glossary terms
   - provenance records
   - downstream dependency visibility

7. **Governance and identity**
   - role-based access
   - attribute- or tag-based controls
   - audit logs
   - classification
   - retention policy

8. **Semantic and consumption layers**
   - governed metrics
   - certified dimensions
   - dashboards
   - APIs
   - notebooks
   - AI and feature-serving interfaces
