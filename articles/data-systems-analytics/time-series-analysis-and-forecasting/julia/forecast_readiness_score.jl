# Forecast readiness scoring example using Julia standard libraries.

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

models = read_csv_simple("data/forecast_model_registry.csv")

status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "planned" => 0.45, "needs_revision" => 0.15)
validation_weight = Dict("rolling_origin" => 1.0, "static_holdout" => 0.45)

mkpath("outputs")
open("outputs/forecast_readiness_julia.csv", "w") do io
    println(io, "model_id,model_family,validation_design,status,forecast_readiness_score")
    for row in models
        score = round(
            0.60 * get(validation_weight, row["validation_design"], 0.5) +
            0.40 * get(status_weight, row["status"], 0.5),
            digits=3
        )
        println(io, "$(row["model_id"]),$(row["model_family"]),$(row["validation_design"]),$(row["status"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=forecast-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "model_count=$(length(models))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia forecast readiness scoring complete")
