# Normalization and analytical denormalization

Normalization protects transactional state from redundancy, update anomalies, and unclear dependencies.

Analytical systems may later denormalize selected structures for reporting, dimensional modeling, and query performance.

Review:

- Is the table representing one fact pattern?
- Does every non-key attribute depend on the key, the whole key, and nothing but the key?
- Are repeated groups or embedded lists present?
- Are reference concepts modeled as separate tables?
- Are analytical denormalizations documented as views, marts, or materialized outputs?
