-- 1. Source records by system, domain, and entity type.
SELECT
    source_system,
    domain,
    entity_type,
    COUNT(*) AS record_count
FROM source_records
GROUP BY source_system, domain, entity_type
ORDER BY domain, source_system;

-- 2. Candidate matches requiring steward review.
SELECT
    candidate_id,
    left_record_id,
    right_record_id,
    entity_type,
    match_method,
    match_score,
    recommended_action,
    review_required
FROM candidate_matches
WHERE review_required = 'true'
ORDER BY match_score DESC;

-- 3. Master entity linkage confidence.
SELECT
    m.master_entity_id,
    m.master_name,
    m.domain,
    COUNT(c.record_id) AS linked_record_count,
    ROUND(AVG(c.confidence), 3) AS average_confidence,
    SUM(CASE WHEN c.link_status = 'review' THEN 1 ELSE 0 END) AS review_links
FROM master_entities m
LEFT JOIN entity_crosswalk c ON m.master_entity_id = c.master_entity_id
GROUP BY m.master_entity_id, m.master_name, m.domain
ORDER BY review_links DESC, average_confidence DESC;

-- 4. Survivorship rules that require human review.
SELECT
    entity_type,
    attribute_name,
    authority_rule,
    primary_source,
    secondary_source,
    conflict_action
FROM survivorship_rules
WHERE review_required = 'true'
ORDER BY entity_type, attribute_name;

-- 5. Stewardship backlog by priority and status.
SELECT
    priority,
    status,
    review_type,
    COUNT(*) AS review_count
FROM stewardship_queue
GROUP BY priority, status, review_type
ORDER BY priority DESC, status;

-- 6. External identifiers and verification status.
SELECT
    e.master_entity_id,
    m.master_name,
    e.identifier_type,
    e.identifier_value,
    e.issuing_authority,
    e.verification_status
FROM external_identifiers e
JOIN master_entities m ON e.master_entity_id = m.master_entity_id
ORDER BY e.verification_status, e.identifier_type;

-- 7. Identity-linkage privacy risks requiring review.
SELECT
    risk_id,
    master_entity_id,
    entity_type,
    linked_record_count,
    contains_personal_data,
    reidentification_risk,
    linkage_sensitivity,
    purpose_review_status,
    mitigation
FROM privacy_identity_risk
WHERE purpose_review_status <> 'approved'
   OR reidentification_risk = 'high'
   OR linkage_sensitivity = 'high'
ORDER BY linkage_sensitivity DESC, reidentification_risk DESC;
