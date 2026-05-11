use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/schema_mappings.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let source_idx = headers.iter().position(|x| *x == "source_system").unwrap();
    let risk_idx = headers.iter().position(|x| *x == "semantic_risk").unwrap();

    let mut source_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut risk_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *source_counts.entry(cols[source_idx].to_string()).or_default() += 1;
        *risk_counts.entry(cols[risk_idx].to_string()).or_default() += 1;
    }

    println!("Rust source mapping inventory:");
    for (source, count) in source_counts {
        println!("source:{}={}", source, count);
    }

    println!("Rust semantic risk inventory:");
    for (risk, count) in risk_counts {
        println!("risk:{}={}", risk, count);
    }

    Ok(())
}
