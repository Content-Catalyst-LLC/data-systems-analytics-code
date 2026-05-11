# Dataset reliability scoring example using Julia standard libraries.

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

registry = read_csv_simple("data/dataset_registry.csv")

criticality_weight = Dict("high" => 1.0, "medium" => 0.7, "low" => 0.4)
cert_weight = Dict("certified" => 1.0, "reviewed" => 0.7, "uncertified" => 0.2)

mkpath("outputs")
open("outputs/dataset_reliability_julia.csv", "w") do io
    println(io, "dataset_id,domain,criticality,reliability_priority_score")
    for row in registry
        criticality = get(criticality_weight, row["criticality"], 0.5)
        certification = get(cert_weight, row["certification_status"], 0.0)
        consumer_count = parse(Float64, row["consumer_count"])
        consumer_score = min(consumer_count / 20.0, 1.0)
        score = round(0.45criticality + 0.30certification + 0.25consumer_score, digits=3)
        println(io, "$(row["dataset_id"]),$(row["domain"]),$(row["criticality"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=dataset-reliability-priority-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "dataset_count=$(length(registry))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia dataset reliability scoring complete")
