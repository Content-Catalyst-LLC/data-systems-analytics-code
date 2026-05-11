# Visualization readiness scoring example using Julia standard libraries.

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

visuals = read_csv_simple("data/visualization_inventory.csv")

status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "needs_revision" => 0.25)
surface_weight = Dict("report" => 1.0, "technical_report" => 0.9, "policy_memo" => 0.9, "dashboard" => 0.8)

mkpath("outputs")
open("outputs/visualization_readiness_julia.csv", "w") do io
    println(io, "visual_id,visualization_context,status,visualization_readiness_score")
    for row in visuals
        status = get(status_weight, row["status"], 0.5)
        surface = get(surface_weight, row["publication_surface"], 0.6)
        reviewed = row["last_reviewed_at_utc"] == "" ? 0.0 : 1.0
        score = round(0.50 * status + 0.25 * surface + 0.25 * reviewed, digits=3)
        println(io, "$(row["visual_id"]),$(row["visualization_context"]),$(row["status"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=visualization-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "visual_count=$(length(visuals))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia visualization readiness scoring complete")
