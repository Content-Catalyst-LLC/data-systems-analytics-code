-- 1. Layer coverage.
SELECT
    layer,
    COUNT(*) AS component_count
FROM stack_components
GROUP BY layer
ORDER BY layer;

-- 2. Pipeline dependency graph.
SELECT
    pipeline_id,
    source_layer || ' -> ' || target_layer AS dependency_edge,
    latency_pattern,
    expected_frequency,
    owner,
    quality_gate
FROM pipeline_catalog
ORDER BY pipeline_id;

-- 3. Governance and observability coverage.
SELECT
    COUNT(*) AS total_components,
    SUM(CASE WHEN governance_control IS NOT NULL AND governance_control <> '' THEN 1 ELSE 0 END) AS governed_components,
    SUM(CASE WHEN observability_control IS NOT NULL AND observability_control <> '' THEN 1 ELSE 0 END) AS observed_components
FROM stack_components;

-- 4. Cost by service category.
SELECT
    service_category,
    ROUND(SUM(estimated_cost), 2) AS estimated_cost
FROM cost_events
GROUP BY service_category
ORDER BY estimated_cost DESC;

-- 5. High-sensitivity policies.
SELECT
    policy_id,
    scope,
    principal_type,
    access_pattern,
    control_type
FROM access_policies
WHERE sensitivity = 'high'
ORDER BY scope;
