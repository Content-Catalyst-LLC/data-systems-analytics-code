# Vendor-neutral dependency scoring example using Julia standard libraries.

using Dates

components_path = "data/stack_components.csv"
pipelines_path = "data/pipeline_catalog.csv"

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

components = read_csv_simple(components_path)
pipelines = read_csv_simple(pipelines_path)

layer_criticality = Dict{String,Int}()

for row in components
    weight = row["criticality"] == "high" ? 2 : 1
    layer_criticality[row["layer"]] = get(layer_criticality, row["layer"], 0) + weight
end

mkpath("outputs")
open("outputs/layer_criticality_julia.csv", "w") do io
    println(io, "layer,criticality_score")
    for layer in sort(collect(keys(layer_criticality)))
        println(io, "$(layer),$(layer_criticality[layer])")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=cloud-data-platform-dependency-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "component_count=$(length(components))")
    println(io, "pipeline_count=$(length(pipelines))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia dependency scoring complete")
