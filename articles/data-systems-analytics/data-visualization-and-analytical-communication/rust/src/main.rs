use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/visualization_inventory.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let context_idx = headers.iter().position(|x| *x == "visualization_context").unwrap();
    let status_idx = headers.iter().position(|x| *x == "status").unwrap();

    let mut context_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *context_counts.entry(cols[context_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
    }

    println!("Rust visualization context inventory:");
    for (context, count) in context_counts {
        println!("visualization_context:{}={}", context, count);
    }

    println!("Rust visualization status inventory:");
    for (status, count) in status_counts {
        println!("status:{}={}", status, count);
    }

    Ok(())
}
