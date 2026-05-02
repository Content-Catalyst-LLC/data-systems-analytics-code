PRAGMA foreign_keys = ON;

.mode csv
.import --skip 1 data/reference/domains.csv domains
.import --skip 1 data/reference/articles.csv articles
.import --skip 1 data/raw/entities.csv dim_systems
.import --skip 1 data/raw/observations.csv stg_observations
