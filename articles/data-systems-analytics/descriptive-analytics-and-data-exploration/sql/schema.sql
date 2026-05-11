CREATE TABLE IF NOT EXISTS exploration_dataset (
    record_id TEXT PRIMARY KEY,
    segment TEXT NOT NULL,
    region TEXT NOT NULL,
    period TEXT NOT NULL,
    value REAL,
    volume REAL NOT NULL,
    quality_score REAL NOT NULL,
    response_time REAL NOT NULL,
    missing_flag INTEGER NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS variable_profile (
    variable_name TEXT PRIMARY KEY,
    variable_type TEXT NOT NULL,
    expected_domain TEXT NOT NULL,
    nullable TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exploration_checks (
    check_id TEXT PRIMARY KEY,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence TEXT NOT NULL,
    remediation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exploration_questions (
    question_id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    analysis_mode TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL
);
