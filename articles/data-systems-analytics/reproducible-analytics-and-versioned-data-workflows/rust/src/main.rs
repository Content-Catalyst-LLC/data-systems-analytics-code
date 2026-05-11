use std::collections::BTreeMap;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, Write};

#[derive(Default)]
struct Summary {
    records: u32,
    total: i32,
}

fn main() -> std::io::Result<()> {
    let input_path = "../data/sample_events.csv";
    let output_path = "../outputs/run_summary_rust.csv";

    let file = File::open(input_path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header = lines.next().unwrap()?;
    let headers: Vec<&str> = header.split(',').collect();

    let system_idx = headers.iter().position(|x| *x == "system").unwrap();
    let value_idx = headers.iter().position(|x| *x == "value").unwrap();

    let mut summaries: BTreeMap<String, Summary> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        let system = cols[system_idx].to_string();
        let value: i32 = cols[value_idx].parse().unwrap();

        let entry = summaries.entry(system).or_default();
        entry.records += 1;
        entry.total += value;
    }

    fs::create_dir_all("../outputs")?;
    let mut out = File::create(output_path)?;
    writeln!(out, "system,records,total_value,average_value")?;

    for (system, summary) in summaries {
        let average = summary.total as f64 / summary.records as f64;
        writeln!(out, "{},{},{},{:.2}", system, summary.records, summary.total, average)?;
    }

    println!("Rust workflow complete: {}", output_path);
    Ok(())
}
