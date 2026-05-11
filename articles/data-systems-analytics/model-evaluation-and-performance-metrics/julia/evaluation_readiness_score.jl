# Model evaluation readiness scoring example using Julia standard libraries.

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
scorecard = read_csv_simple("data/metric_scorecard.csv")

status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "watch" => 0.55, "needs_revision" => 0.2)
risk_weight = Dict("low" => 1.0, "medium" => 0.8, "high" => 0.6)

scorecard_by_model = Dict{String,Vector{Dict{String,String}}}()
for row in scorecard
    push!(get!(scorecard_by_model, row["model_id"], Vector{Dict{String,String}}()), row)
end

mkpath("outputs")
open("outputs/evaluation_readiness_julia.csv", "w") do io
    println(io, "model_id,task_type,status,risk_level,evaluation_readiness_score")
    for row in models
        metrics = get(scorecard_by_model, row["model_id"], Vector{Dict{String,String}}())
        metric_status = length(metrics) == 0 ? 0.0 : sum(get(status_weight, m["status"], 0.5) for m in metrics) / length(metrics)
        model_status = get(status_weight, row["status"], 0.5)
        risk_factor = get(risk_weight, row["risk_level"], 0.7)
        score = round(0.45metric_status + 0.35model_status + 0.20risk_factor, digits=3)
        println(io, "$(row["model_id"]),$(row["task_type"]),$(row["status"]),$(row["risk_level"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=evaluation-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "model_count=$(length(models))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia evaluation readiness scoring complete")
