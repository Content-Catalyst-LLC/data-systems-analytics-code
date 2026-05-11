-- 1. Visualizations by context, status, and publication surface.
SELECT
    visualization_context,
    status,
    publication_surface,
    COUNT(*) AS visual_count
FROM visualization_inventory
GROUP BY visualization_context, status, publication_surface
ORDER BY visualization_context, status;

-- 2. Chart choices that may not fit the analytical task.
SELECT
    v.visual_title,
    c.chart_type,
    c.analytical_task,
    c.chart_fit,
    c.comparison_supported,
    c.distribution_visible,
    c.trend_visible
FROM chart_assessments c
JOIN visualization_inventory v ON c.visual_id = v.visual_id
WHERE c.chart_fit <> 'high'
ORDER BY c.chart_fit, v.visual_title;

-- 3. Encodings with color dependency or weak perceptual accuracy.
SELECT
    v.visual_title,
    e.primary_encoding,
    e.scale_type,
    e.axis_baseline_appropriate,
    e.sorting_appropriate,
    e.label_quality,
    e.color_dependency,
    e.perceptual_accuracy
FROM encoding_assessments e
JOIN visualization_inventory v ON e.visual_id = v.visual_id
WHERE e.color_dependency = 'true'
   OR e.perceptual_accuracy <> 'high'
   OR e.label_quality <> 'approved'
ORDER BY v.visual_title;

-- 4. High-materiality uncertainty not near the claim.
SELECT
    v.visual_title,
    u.uncertainty_type,
    u.visual_form,
    u.near_claim,
    u.materiality,
    u.statement_quality
FROM uncertainty_elements u
JOIN visualization_inventory v ON u.visual_id = v.visual_id
WHERE u.materiality = 'high'
  AND u.near_claim <> 'true'
ORDER BY v.visual_title;

-- 5. Accessibility issues.
SELECT
    v.visual_title,
    a.check_type,
    a.status,
    a.severity,
    a.notes
FROM accessibility_checks a
JOIN visualization_inventory v ON a.visual_id = v.visual_id
WHERE a.status <> 'pass'
ORDER BY a.severity DESC, v.visual_title;

-- 6. Visual outputs without publication controls.
SELECT
    v.visual_title,
    o.output_format,
    o.versioned,
    o.archived,
    o.hash_recorded,
    o.publication_channel
FROM visual_outputs o
JOIN visualization_inventory v ON o.visual_id = v.visual_id
WHERE o.versioned <> 'true'
   OR o.archived <> 'true'
   OR o.hash_recorded <> 'true'
ORDER BY v.visual_title;
