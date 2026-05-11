-- 1. Assets by domain and certification status.
SELECT
    domain,
    asset_type,
    certification_status,
    COUNT(*) AS asset_count
FROM data_assets
GROUP BY domain, asset_type, certification_status
ORDER BY domain, certification_status;

-- 2. Missing or stale metadata requiring review.
SELECT
    a.asset_name,
    m.metadata_type,
    m.element_name,
    m.quality_status,
    m.source,
    m.review_required
FROM metadata_elements m
JOIN data_assets a ON m.asset_id = a.asset_id
WHERE m.quality_status IN ('missing', 'stale', 'review')
   OR m.review_required = 'true'
ORDER BY a.asset_name, m.metadata_type;

-- 3. Catalog trust signals.
SELECT
    a.asset_name,
    c.trust_label,
    c.description_complete,
    c.quality_visible,
    c.lineage_visible,
    c.policy_visible,
    c.usage_visible
FROM catalog_entries c
JOIN data_assets a ON c.asset_id = a.asset_id
ORDER BY c.trust_label, a.asset_name;

-- 4. High-impact lineage edges.
SELECT
    edge_id,
    upstream_asset,
    downstream_asset,
    relationship_type,
    lineage_granularity,
    observed_by
FROM lineage_edges
WHERE impact_level = 'high'
ORDER BY upstream_asset, downstream_asset;

-- 5. Incomplete provenance records.
SELECT
    event_id,
    asset_id,
    prov_entity,
    prov_activity,
    prov_agent,
    version_id,
    notes
FROM provenance_events
WHERE provenance_complete <> 'true'
ORDER BY event_time_utc;

-- 6. Policy tags with weak or review enforcement.
SELECT
    a.asset_name,
    p.tag_type,
    p.tag_value,
    p.policy_owner,
    p.enforcement_status
FROM policy_tags p
JOIN data_assets a ON p.asset_id = a.asset_id
WHERE p.enforcement_status <> 'enforced'
ORDER BY p.enforcement_status, a.asset_name;
