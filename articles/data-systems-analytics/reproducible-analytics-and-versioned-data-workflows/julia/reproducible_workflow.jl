# Julia reproducible workflow example using only standard libraries.

using Dates
using SHA

input_path = "data/sample_events.csv"
output_path = "outputs/run_summary_julia.csv"
manifest_path = "outputs/run_manifest_julia.txt"

function file_sha256(path)
    open(path, "r") do io
        return bytes2hex(sha256(io))
    end
end

lines = readlines(input_path)
header = split(lines[1], ",")
rows = [split(line, ",") for line in lines[2:end]]

idx_system = findfirst(==("system"), header)
idx_value = findfirst(==("value"), header)

totals = Dict{String, Int}()
counts = Dict{String, Int}()

for row in rows
    key = row[idx_system]
    value = parse(Int, row[idx_value])
    totals[key] = get(totals, key, 0) + value
    counts[key] = get(counts, key, 0) + 1
end

mkpath("outputs")
open(output_path, "w") do io
    println(io, "system,records,total_value,average_value")
    for key in sort(collect(keys(totals)))
        avg = totals[key] / counts[key]
        println(io, "$(key),$(counts[key]),$(totals[key]),$(round(avg, digits=2))")
    end
end

open(manifest_path, "w") do io
    println(io, "workflow=reproducible-analytics-and-versioned-data-workflows")
    println(io, "runtime=Julia")
    println(io, "julia_version=$(VERSION)")
    println(io, "input_path=$(input_path)")
    println(io, "input_sha256=$(file_sha256(input_path))")
    println(io, "output_path=$(output_path)")
    println(io, "output_sha256=$(file_sha256(output_path))")
    println(io, "row_count=$(length(rows))")
    println(io, "run_time_utc=$(Dates.format(now(UTC), dateformat\"yyyy-mm-ddTHH:MM:SS.sZ\"))")
end

println("Julia workflow complete")
