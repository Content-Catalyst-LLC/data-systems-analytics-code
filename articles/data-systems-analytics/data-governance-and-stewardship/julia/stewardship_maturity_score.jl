# Stewardship maturity scoring example using Julia standard libraries.

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

assets = read_csv_simple("data/data_assets.csv")

criticality_weight = Dict("high" => 1.0, "medium" => 0.7, "low" => 0.4)
certification_weight = Dict("certified" => 1.0, "reviewed" => 0.7, "uncertified" => 0.2)
lifecycle_weight = Dict("active" => 1.0, "deprecated" => 0.3, "retired" => 0.1)

mkpath("outputs")
open("outputs/stewardship_maturity_julia.csv", "w") do io
    println(io, "asset_id,domain,criticality,stewardship_priority_score")
    for row in assets
        criticality = get(criticality_weight, row["criticality"], 0.5)
        certification = get(certification_weight, row["certification_status"], 0.5)
        lifecycle = get(lifecycle_weight, row["lifecycle_status"], 0.5)
        score = round(0.45criticality + 0.35certification + 0.20lifecycle, digits=3)
        println(io, "$(row["asset_id"]),$(row["domain"]),$(row["criticality"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=stewardship-maturity-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "asset_count=$(length(assets))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia stewardship maturity scoring complete")
