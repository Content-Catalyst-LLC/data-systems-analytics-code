CREATE TABLE IF NOT EXISTS causal_study_registry (
    study_id TEXT PRIMARY KEY,
    study_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    causal_question TEXT NOT NULL,
    intervention TEXT NOT NULL,
    comparison TEXT NOT NULL,
    outcome TEXT NOT NULL,
    unit_of_analysis TEXT NOT NULL,
    design_type TEXT NOT NULL,
    estimand TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS experiment_units (
    unit_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    block TEXT NOT NULL,
    treatment INTEGER NOT NULL,
    outcome REAL NOT NULL,
    pre_score REAL NOT NULL,
    propensity_score REAL NOT NULL,
    assignment_score REAL NOT NULL,
    time_period TEXT NOT NULL,
    group_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS did_panel (
    unit_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    group_name TEXT NOT NULL,
    time_period TEXT NOT NULL,
    treatment_group INTEGER NOT NULL,
    post INTEGER NOT NULL,
    outcome REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS rdd_units (
    unit_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    running_variable REAL NOT NULL,
    cutoff REAL NOT NULL,
    treatment INTEGER NOT NULL,
    outcome REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS assumption_checks (
    check_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    assumption TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence TEXT NOT NULL,
    remediation TEXT NOT NULL
);
