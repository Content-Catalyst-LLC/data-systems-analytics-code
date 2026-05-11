# Exploration readiness scoring example using Julia standard libraries.

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

checks = read_csv_simple("data/exploration_checks.csv")
status_weight = Dict("pass" => 1.0, "in_review" => 0.7, "warn" => 0.45, "fail" => 0.0)
severity_penalty = Dict("low" => 0.05, "medium" => 0.10, "high" => 0.20, "critical" => 0.40)

scores = Float64[]
for row in checks
    base = get(status_weight, row["status"], 0.5)
    penalty = row["status"] == "pass" ? 0.0 : get(severity_penalty, row["severity"], 0.1)
    push!(scores, max(0.0, base - penalty))
end

readiness = round(sum(scores) / length(scores), digits=3)

mkpath("outputs")
open("outputs/exploration_readiness_julia.csv", "w") do io
    println(io, "check_count,mean_check_score")
    println(io, "$(length(scores)),$(readiness)")
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=exploration-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "check_count=$(length(scores))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia exploration readiness scoring complete")
