# Data quality readiness scoring example using Julia standard libraries.

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

rules = read_csv_simple("data/quality_rules.csv")
severity_weight = Dict("low" => 0.90, "medium" => 0.80, "high" => 0.65, "critical" => 0.50)
status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "needs_revision" => 0.15)

scores = Float64[]
for row in rules
    push!(scores, get(status_weight, row["status"], 0.5) * get(severity_weight, row["severity"], 0.75))
end

readiness = round(sum(scores) / length(scores), digits=3)

mkpath("outputs")
open("outputs/data_quality_readiness_julia.csv", "w") do io
    println(io, "quality_rule_count,mean_rule_governance_score")
    println(io, "$(length(scores)),$(readiness)")
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=data-quality-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "rule_count=$(length(scores))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia data quality readiness scoring complete")
