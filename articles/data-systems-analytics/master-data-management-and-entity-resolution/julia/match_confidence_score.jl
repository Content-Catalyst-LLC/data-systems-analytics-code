# Match confidence and merge-action scoring example using Julia standard libraries.

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

candidates = read_csv_simple("data/candidate_matches.csv")

action_risk = Dict(
    "merge" => 0.15,
    "link" => 0.30,
    "steward_review" => 0.45,
    "possible_link" => 0.65,
    "block" => 0.90
)

mkpath("outputs")
open("outputs/match_confidence_julia.csv", "w") do io
    println(io, "candidate_id,entity_type,match_score,recommended_action,governance_action_risk")
    for row in candidates
        score = parse(Float64, row["match_score"])
        risk = get(action_risk, row["recommended_action"], 0.50)
        review_penalty = row["review_required"] == "true" ? 0.10 : 0.0
        governance_risk = round((1.0 - score) * 0.60 + risk * 0.30 + review_penalty, digits=3)
        println(io, "$(row["candidate_id"]),$(row["entity_type"]),$(score),$(row["recommended_action"]),$(governance_risk)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=match-confidence-governance-action-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "candidate_count=$(length(candidates))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia match confidence scoring complete")
