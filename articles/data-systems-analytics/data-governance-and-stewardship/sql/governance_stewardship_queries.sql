-- 1. Assets by domain, classification, and certification status.
SELECT
    domain,
    classification,
    certification_status,
    COUNT(*) AS asset_count
FROM data_assets
GROUP BY domain, classification, certification_status
ORDER BY domain, classification;

-- 2. Open or in-review quality issues by steward.
SELECT
    q.issue_id,
    a.asset_name,
    q.issue_type,
    q.severity,
    q.status,
    q.assigned_steward,
    q.days_open,
    q.consumer_notified
FROM quality_issues q
JOIN data_assets a ON q.asset_id = a.asset_id
WHERE q.status <> 'resolved'
ORDER BY q.severity DESC, q.days_open DESC;

-- 3. High-risk access reviews and outcomes.
SELECT
    ar.access_id,
    a.asset_name,
    ar.requester_group,
    ar.purpose,
    ar.access_level,
    ar.risk_level,
    ar.decision,
    ar.approver_role,
    ar.expiry_days
FROM access_reviews ar
JOIN data_assets a ON ar.asset_id = a.asset_id
WHERE ar.risk_level = 'high'
ORDER BY ar.decision, ar.asset_id;

-- 4. Policies with weak or review enforcement.
SELECT
    policy_id,
    policy_name,
    policy_domain,
    policy_type,
    owner,
    enforcement_status,
    linked_assets
FROM policy_register
WHERE enforcement_status <> 'enforced'
ORDER BY enforcement_status, policy_domain;

-- 5. Lifecycle controls that are overdue or require disposal.
SELECT
    lc.control_id,
    a.asset_name,
    lc.lifecycle_stage,
    lc.control_type,
    lc.status,
    lc.owner,
    lc.retention_rule,
    lc.disposal_required
FROM lifecycle_controls lc
JOIN data_assets a ON lc.asset_id = a.asset_id
WHERE lc.status <> 'current'
   OR lc.disposal_required = 'true'
ORDER BY lc.status, a.asset_name;

-- 6. Responsible-use risks not fully approved.
SELECT
    r.risk_id,
    a.asset_name,
    r.use_case,
    r.risk_type,
    r.severity,
    r.review_status,
    r.mitigation,
    r.review_owner
FROM responsible_use_risks r
JOIN data_assets a ON r.asset_id = a.asset_id
WHERE r.review_status <> 'approved'
ORDER BY r.severity DESC, r.review_status;
