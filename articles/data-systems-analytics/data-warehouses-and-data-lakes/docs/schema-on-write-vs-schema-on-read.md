# Schema-on-write and schema-on-read notes

Schema-on-write applies structure before or during loading into a governed analytical target. It is useful for repeated reporting, governed KPIs, dimensional models, and high-trust downstream consumption.

Schema-on-read stores data first and applies structure at consumption time. It is useful for raw retention, exploratory analytics, heterogeneous data, machine learning, and cases where downstream questions are not yet fixed.

Most mature estates use both:

- raw lake retention
- bronze standardization
- silver refined assets
- gold data products
- warehouse marts
- feature layers
- archives
