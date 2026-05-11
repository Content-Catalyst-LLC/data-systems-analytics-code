# Pipeline readiness scoring example using Julia standard libraries.

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

gates = read_csv_simple("data/quality_gates.csv")
severity_penalty = Dict("medium" => 0.10, "high" => 0.20, "critical" => 0.45)
status_weight = Dict("pass" => 1.0, "warn" => 0.45, "fail" => 0.0)

scores = Float64[]
for row in gates
    observed = parse(Float64, row["observed_value"])
    threshold = parse(Float64, row["threshold"])
    base = min(1.0, observed / threshold)
    penalty = row["status"] == "pass" ? 0.0 : get(severity_penalty, row["severity"], 0.1)
    push!(scores, max(0.0, min(base, get(status_weight, row["status"], 0.5)) - penalty))
end

readiness = round(sum(scores) / length(scores), digits=3)

mkpath("outputs")
open("outputs/pipeline_readiness_julia.csv", "w") do io
    println(io, "quality_gate_count,mean_quality_gate_score")
    println(io, "$(length(scores)),$(readiness)")
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=pipeline-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "quality_gate_count=$(length(scores))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia pipeline readiness scoring complete")
