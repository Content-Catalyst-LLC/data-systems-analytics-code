# Inference readiness scoring example using Julia standard libraries.

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

models = read_csv_simple("data/model_registry.csv")
status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "needs_revision" => 0.15)
assumption_weight = Dict(
    "independent_samples" => 0.8,
    "linear_independent_errors" => 0.75,
    "linear_additive_errors" => 0.7,
    "unclear_assumptions" => 0.2
)

mkpath("outputs")
open("outputs/inference_readiness_julia.csv", "w") do io
    println(io, "model_id,model_family,estimand,status,inference_readiness_score")
    for row in models
        score = round(
            0.50 * get(status_weight, row["status"], 0.5) +
            0.50 * get(assumption_weight, row["assumption_profile"], 0.5),
            digits=3
        )
        println(io, "$(row["model_id"]),$(row["model_family"]),$(row["estimand"]),$(row["status"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=inference-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "model_count=$(length(models))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia inference readiness scoring complete")
