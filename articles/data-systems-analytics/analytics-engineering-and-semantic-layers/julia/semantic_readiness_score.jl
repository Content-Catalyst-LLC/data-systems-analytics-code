# Semantic readiness scoring example using Julia standard libraries.

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

metrics = read_csv_simple("data/semantic_metrics.csv")

cert_weight = Dict("certified" => 1.0, "reviewed" => 0.7, "uncertified" => 0.2)

mkpath("outputs")
open("outputs/semantic_readiness_julia.csv", "w") do io
    println(io, "metric_id,metric_name,domain,semantic_readiness_score")
    for row in metrics
        certification = get(cert_weight, row["certification_status"], 0.0)
        grain_score = row["grain"] == "mixed" ? 0.0 : 1.0
        version_value = parse(Float64, row["version"])
        version_score = min(version_value / 1.0, 1.0)
        criticality_bonus = row["decision_critical"] == "true" ? 1.0 : 0.8
        score = round(0.45certification + 0.25grain_score + 0.15version_score + 0.15criticality_bonus, digits=3)
        println(io, "$(row["metric_id"]),$(row["metric_name"]),$(row["domain"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=semantic-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "metric_count=$(length(metrics))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia semantic readiness scoring complete")
