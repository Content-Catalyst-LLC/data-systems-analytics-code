# Data product readiness scoring example using Julia standard libraries.

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

products = read_csv_simple("data/data_products.csv")

status_weight = Dict(
    "certified" => 1.0,
    "reviewed" => 0.7,
    "uncertified" => 0.2
)

lifecycle_weight = Dict(
    "active" => 1.0,
    "beta" => 0.7,
    "deprecated" => 0.2,
    "retired" => 0.0
)

mkpath("outputs")
open("outputs/product_readiness_julia.csv", "w") do io
    println(io, "product_id,domain,readiness_score")
    for row in products
        q = parse(Float64, row["quality_score"])
        s = get(status_weight, row["semantic_status"], 0.0)
        l = get(lifecycle_weight, row["lifecycle_status"], 0.5)
        score = round(0.5q + 0.3s + 0.2l, digits=3)
        println(io, "$(row["product_id"]),$(row["domain"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=data-product-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "product_count=$(length(products))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia product readiness scoring complete")
