# Warehouse/lake readiness scoring example using Julia standard libraries.

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

controls = read_csv_simple("data/governance_controls.csv")

function status_score(value)
    scores = Dict(
        "certified" => 1.0,
        "approved" => 1.0,
        "pass" => 1.0,
        "registered" => 0.75,
        "in_review" => 0.60,
        "warn" => 0.40,
        "missing" => 0.10,
        "unknown" => 0.15,
        "unregistered" => 0.10
    )
    return get(scores, value, 0.5)
end

scores = Float64[]
for row in controls
    metadata = parse(Float64, row["metadata_coverage"])
    lineage = parse(Float64, row["lineage_coverage"])
    owner = row["owner_assigned"] == "1" ? 1.0 : 0.0
    classification = row["classification_applied"] == "1" ? 1.0 : 0.0
    quality = status_score(row["quality_status"])
    access = status_score(row["access_policy_status"])
    lifecycle = status_score(row["lifecycle_status"])
    certification = status_score(row["certification_status"])
    push!(scores, 0.18metadata + 0.18lineage + 0.10owner + 0.10classification + 0.14quality + 0.12access + 0.08lifecycle + 0.10certification)
end

readiness = round(sum(scores) / length(scores), digits=3)

mkpath("outputs")
open("outputs/warehouse_lake_readiness_julia.csv", "w") do io
    println(io, "asset_control_count,mean_governance_readiness")
    println(io, "$(length(scores)),$(readiness)")
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=warehouse-lake-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "asset_control_count=$(length(scores))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia warehouse/lake readiness scoring complete")
