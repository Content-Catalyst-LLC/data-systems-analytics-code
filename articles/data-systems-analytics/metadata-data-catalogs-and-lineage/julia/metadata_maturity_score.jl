# Metadata maturity scoring example using Julia standard libraries.

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

catalog = read_csv_simple("data/catalog_entries.csv")

mkpath("outputs")
open("outputs/metadata_maturity_julia.csv", "w") do io
    println(io, "asset_id,trust_label,metadata_maturity_score")
    for row in catalog
        flags = [
            row["discoverable"] == "true",
            row["description_complete"] == "true",
            row["owner_visible"] == "true",
            row["quality_visible"] == "true",
            row["lineage_visible"] == "true",
            row["policy_visible"] == "true",
            row["usage_visible"] == "true"
        ]
        score = round(sum(flags) / length(flags), digits=3)
        println(io, "$(row["asset_id"]),$(row["trust_label"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=metadata-maturity-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "catalog_entry_count=$(length(catalog))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia metadata maturity scoring complete")
