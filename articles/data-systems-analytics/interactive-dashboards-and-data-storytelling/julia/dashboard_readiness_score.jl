# Dashboard readiness scoring example using Julia standard libraries.

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

dashboards = read_csv_simple("data/dashboard_inventory.csv")

status_weight = Dict("approved" => 1.0, "in_review" => 0.7, "needs_revision" => 0.25)
type_weight = Dict(
    "monitoring" => 1.0,
    "operational_monitoring" => 1.0,
    "guided_story" => 0.9,
    "exploratory" => 0.8,
    "legacy_reporting" => 0.3
)

mkpath("outputs")
open("outputs/dashboard_readiness_julia.csv", "w") do io
    println(io, "dashboard_id,dashboard_type,status,dashboard_readiness_score")
    for row in dashboards
        status = get(status_weight, row["status"], 0.5)
        mode = get(type_weight, row["dashboard_type"], 0.6)
        view_count = parse(Int, row["view_count"])
        filter_count = parse(Int, row["filter_count"])
        view_focus = view_count <= 3 ? 1.0 : max(0.25, 1.0 - 0.12 * (view_count - 3))
        filter_focus = filter_count <= 4 ? 1.0 : max(0.25, 1.0 - 0.08 * (filter_count - 4))
        score = round(0.35status + 0.25mode + 0.20view_focus + 0.20filter_focus, digits=3)
        println(io, "$(row["dashboard_id"]),$(row["dashboard_type"]),$(row["status"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=dashboard-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "dashboard_count=$(length(dashboards))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia dashboard readiness scoring complete")
