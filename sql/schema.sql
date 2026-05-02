PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS domains (
    domain_key TEXT PRIMARY KEY,
    domain_name TEXT NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 3
);

CREATE TABLE IF NOT EXISTS articles (
    slug TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('published','planned','drafting','archived')),
    domain_key TEXT NOT NULL,
    priority INTEGER DEFAULT 3,
    FOREIGN KEY (domain_key) REFERENCES domains(domain_key)
);

CREATE TABLE IF NOT EXISTS dim_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    criticality TEXT NOT NULL,
    owner TEXT,
    refresh_frequency TEXT
);

CREATE TABLE IF NOT EXISTS stg_observations (
    observation_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_system TEXT NOT NULL,
    quality_flag TEXT,
    FOREIGN KEY (system_id) REFERENCES dim_systems(system_id)
);

CREATE TABLE IF NOT EXISTS data_quality_results (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_name TEXT NOT NULL,
    check_status TEXT NOT NULL,
    failed_records INTEGER DEFAULT 0,
    checked_at TEXT DEFAULT CURRENT_TIMESTAMP
);
