# BI decision-support readiness scoring example using Julia standard libraries.

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

status_weight = Dict("certified" => 1.0, "reviewed" => 0.7, "uncertified" => 0.2)
lifecycle_weight = Dict("active" => 1.0, "beta" => 0.7, "deprecated" => 0.2, "retired" => 0.0)

mkpath("outputs")
open("outputs/bi_readiness_julia.csv", "w") do io
    println(io, "dashboard_id,domain,decision_function,readiness_score")
    for row in dashboards
        c = get(status_weight, row["certification_status"], 0.0)
        l = get(lifecycle_weight, row["lifecycle_status"], 0.5)
        f = parse(Float64, row["refresh_sla_hours"])
        freshness_score = max(0.0, min(1.0, 1.0 - (f / 168.0)))
        score = round(0.45c + 0.35l + 0.20freshness_score, digits=3)
        println(io, "$(row["dashboard_id"]),$(row["domain"]),$(row["decision_function"]),$(score)")
    end
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=bi-decision-support-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "dashboard_count=$(length(dashboards))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia BI readiness scoring complete")
