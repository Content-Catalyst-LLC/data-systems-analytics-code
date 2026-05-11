-- 1. Dashboards by mode, status, and refresh cadence.
SELECT
    dashboard_type,
    status,
    refresh_cadence,
    COUNT(*) AS dashboard_count
FROM dashboard_inventory
GROUP BY dashboard_type, status, refresh_cadence
ORDER BY dashboard_type, status;

-- 2. Dashboards with potential clutter risk.
SELECT
    dashboard_id,
    dashboard_title,
    dashboard_type,
    view_count,
    filter_count,
    status
FROM dashboard_inventory
WHERE view_count > 3
   OR filter_count > 5
ORDER BY view_count DESC, filter_count DESC;

-- 3. KPIs lacking context.
SELECT
    d.dashboard_title,
    k.kpi_name,
    k.definition_status,
    k.baseline_present,
    k.target_present,
    k.trend_present,
    k.denominator_present,
    k.certification_status
FROM kpi_definitions k
JOIN dashboard_inventory d ON k.dashboard_id = d.dashboard_id
WHERE k.baseline_present <> 'true'
   OR k.trend_present <> 'true'
   OR k.denominator_present <> 'true'
   OR k.definition_status NOT IN ('approved', 'review');

-- 4. Filters likely to create friction.
SELECT
    d.dashboard_title,
    f.filter_name,
    f.filter_type,
    f.default_state_visible,
    f.reset_available,
    f.consumer_relevant,
    f.complexity_level
FROM filter_controls f
JOIN dashboard_inventory d ON f.dashboard_id = d.dashboard_id
WHERE f.default_state_visible <> 'true'
   OR f.reset_available <> 'true'
   OR f.consumer_relevant <> 'true'
   OR f.complexity_level = 'high'
ORDER BY d.dashboard_title, f.complexity_level DESC;

-- 5. Accessibility issues.
SELECT
    d.dashboard_title,
    a.check_type,
    a.status,
    a.severity,
    a.notes
FROM accessibility_checks a
JOIN dashboard_inventory d ON a.dashboard_id = d.dashboard_id
WHERE a.status <> 'pass'
ORDER BY a.severity DESC, d.dashboard_title;

-- 6. Governance blocking issues.
SELECT
    d.dashboard_title,
    g.check_type,
    g.status,
    g.owner,
    g.blocking_issue,
    g.notes
FROM governance_checks g
JOIN dashboard_inventory d ON g.dashboard_id = d.dashboard_id
WHERE g.blocking_issue = 'true'
   OR g.status = 'needs_revision'
ORDER BY g.blocking_issue DESC, d.dashboard_title;
