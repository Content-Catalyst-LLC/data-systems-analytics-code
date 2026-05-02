# Lightweight Julia workflow for simple time-series transformation.
# Run from repository root:
# julia julia/time_series_workflow.jl

using Dates
using Statistics
using DelimitedFiles

input_path = "data/raw/observations.csv"
lines = readlines(input_path)
header = split(lines[1], ",")

rows = [split(line, ",") for line in lines[2:end]]
metric_idx = findfirst(==("metric_value"), header)
system_idx = findfirst(==("system_id"), header)

systems = unique(row[system_idx] for row in rows)
open("outputs/julia-system-summary.csv", "w") do io
    println(io, "system_id,n,mean_metric_value")
    for system in systems
        values = [parse(Float64, row[metric_idx]) for row in rows if row[system_idx] == system]
        println(io, "$(system),$(length(values)),$(round(mean(values), digits=4))")
    end
end

println("Wrote outputs/julia-system-summary.csv")
