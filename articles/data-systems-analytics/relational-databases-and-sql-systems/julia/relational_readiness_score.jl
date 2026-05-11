# Relational SQL readiness scoring example using Julia standard libraries.

using Dates

function read_csv_simple(path)
    lines = readlines(path)
    header = split(lines[1], ",")
    rows = Vector{Dict{String,String}}()
    for line in lines[2:end]
        vals = split(line, ",")
        push!(rows, Dict(header[i] => vals[i] for i in eachindex(header)))
    end
    return rows
end

constraints = read_csv_simple("data/constraint_inventory.csv")

function status_score(value)
    scores = Dict(
        "approved" => 1.0,
        "certified" => 1.0,
        "pass" => 1.0,
        "in_review" => 0.60,
        "watch" => 0.45,
        "warn" => 0.40,
        "missing" => 0.10
    )
    return get(scores, value, 0.5)
end

function severity_weight(value)
    weights = Dict("low" => 0.05, "medium" => 0.15, "high" => 0.30, "critical" => 0.50)
    return get(weights, value, 0.15)
end

scores = Float64[]
for row in constraints
    relationship_complete = row["constraint_type"] == "foreign_key" ? (row["referenced_table"] != "" ? 1.0 : 0.0) : 1.0
    rule_present = row["rule_expression"] != "" ? 1.0 : 0.0
    push!(scores, 0.45 * status_score(row["status"]) + 0.25 * relationship_complete + 0.15 * (1.0 - severity_weight(row["severity"])) + 0.15 * rule_present)
end

readiness = round(sum(scores) / length(scores), digits=3)

mkpath("outputs")
open("outputs/relational_constraint_readiness_julia.csv", "w") do io
    println(io, "constraint_count,mean_constraint_readiness")
    println(io, "$(length(scores)),$(readiness)")
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=relational-constraint-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "constraint_count=$(length(scores))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia relational constraint readiness scoring complete")
