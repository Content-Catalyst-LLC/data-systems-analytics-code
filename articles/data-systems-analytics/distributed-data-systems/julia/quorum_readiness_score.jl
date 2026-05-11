# Distributed quorum readiness scoring example using Julia standard libraries.

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

policies = read_csv_simple("data/quorum_policies.csv")

scores = Float64[]
for row in policies
    n = parse(Int, row["replication_factor"])
    r = parse(Int, row["read_quorum"])
    w = parse(Int, row["write_quorum"])
    intersects = (r + w > n) ? 1.0 : 0.0
    write_majority = (w > n / 2) ? 1.0 : 0.0
    approved = row["status"] == "approved" ? 1.0 : 0.65
    push!(scores, 0.45 * intersects + 0.35 * write_majority + 0.20 * approved)
end

readiness = round(sum(scores) / length(scores), digits=3)

mkpath("outputs")
open("outputs/quorum_readiness_julia.csv", "w") do io
    println(io, "quorum_policy_count,mean_quorum_readiness")
    println(io, "$(length(scores)),$(readiness)")
end

open("outputs/julia_manifest.txt", "w") do io
    println(io, "workflow=quorum-readiness-score")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "policy_count=$(length(scores))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia quorum readiness scoring complete")
