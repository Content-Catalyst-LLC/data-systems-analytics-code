-- 1. Source systems by domain and type.
SELECT
    domain,
    system_type,
    COUNT(*) AS system_count
FROM source_systems
GROUP BY domain, system_type
ORDER BY domain, system_type;

-- 2. Mapping risk and review status.
SELECT
    semantic_risk,
    status,
    COUNT(*) AS mapping_count
FROM schema_mappings
GROUP BY semantic_risk, status
ORDER BY semantic_risk, status;

-- 3. Interoperability check status by layer.
SELECT
    layer,
    status,
    COUNT(*) AS check_count,
    ROUND(AVG(observed_value), 3) AS average_observed_value
FROM interoperability_checks
GROUP BY layer, status
ORDER BY layer, status;

-- 4. Entity crosswalk confidence.
SELECT
    entity_type,
    match_method,
    COUNT(*) AS linked_entities,
    ROUND(AVG(confidence), 3) AS average_confidence
FROM entity_crosswalk
GROUP BY entity_type, match_method
ORDER BY entity_type, average_confidence DESC;

-- 5. Payloads that are syntactically valid but semantically weak.
SELECT
    payload_id,
    source_system,
    message_type,
    syntax_valid,
    semantic_valid,
    minimized_payload,
    consumer_ready
FROM message_payloads
WHERE syntax_valid = 'true'
  AND semantic_valid <> 'true'
ORDER BY source_system;
