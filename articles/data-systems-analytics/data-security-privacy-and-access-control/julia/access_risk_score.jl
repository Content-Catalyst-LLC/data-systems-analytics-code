# Privacy exposure and access-risk scoring example using Julia standard libraries.

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

classification_weight = Dict(
    "public" => 0.1,
    "internal" => 0.35,
    "confidential" => 0.7,
    "restricted" => 0.9,
    "secret" => 1.0
)

mkpath("outputs")
open("outputs/access_risk_julia.csv", "w") do io
    println(io, "asset_id,classification,contains_personal_data,access_risk_score")
    for row in assets
        sensitivity = parse(Float64, row["sensitivity_score"])
        classification = get(classification_weight, row["classification"], 0.5)
        personal = row["contains_personal_data"] == "true" ? 1.0 : 0.0
        identifiers = row["contains_direct_identifiers"] == "true" ? 1.0 : 0.0
        score = round(0.45sensitivity + 0.25classification + 0.15personal + 0.15identifiers, digits=3)
        println(io, "$(row["asset_id"]),$(row["classification"]),$(row["contains_personal_data"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=privacy-exposure-access-risk-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "asset_count=$(length(assets))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia privacy exposure and access-risk scoring complete")
