use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/model_registry.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let task_idx = headers.iter().position(|x| *x == "task_type").unwrap();
    let status_idx = headers.iter().position(|x| *x == "status").unwrap();
    let risk_idx = headers.iter().position(|x| *x == "risk_level").unwrap();

    let mut task_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut risk_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *task_counts.entry(cols[task_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
        *risk_counts.entry(cols[risk_idx].to_string()).or_default() += 1;
    }

    println!("Rust model task inventory:");
    for (task, count) in task_counts {
        println!("task_type:{}={}", task, count);
    }

    println!("Rust model status inventory:");
    for (status, count) in status_counts {
        println!("status:{}={}", status, count);
    }

    println!("Rust model risk inventory:");
    for (risk, count) in risk_counts {
        println!("risk_level:{}={}", risk, count);
    }

    Ok(())
}
