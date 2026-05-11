# Causal design readiness scoring example using Julia standard libraries.

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

studies = read_csv_simple("data/causal_study_registry.csv")
design_weight = Dict(
    "randomized_experiment" => 1.0,
    "regression_discontinuity" => 0.82,
    "difference_in_differences" => 0.78,
    "target_trial_emulation" => 0.72,
    "observational_regression" => 0.35
)
status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "planned" => 0.45, "needs_revision" => 0.15)

mkpath("outputs")
open("outputs/causal_readiness_julia.csv", "w") do io
    println(io, "study_id,design_type,estimand,status,causal_readiness_score")
    for row in studies
        score = round(0.65 * get(design_weight, row["design_type"], 0.5) + 0.35 * get(status_weight, row["status"], 0.5), digits=3)
        println(io, "$(row["study_id"]),$(row["design_type"]),$(row["estimand"]),$(row["status"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=causal-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "study_count=$(length(studies))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia causal readiness scoring complete")
