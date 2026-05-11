use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/dashboard_inventory.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let type_idx = headers.iter().position(|x| *x == "dashboard_type").unwrap();
    let status_idx = headers.iter().position(|x| *x == "status").unwrap();

    let mut type_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *type_counts.entry(cols[type_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
    }

    println!("Rust dashboard type inventory:");
    for (dashboard_type, count) in type_counts {
        println!("dashboard_type:{}={}", dashboard_type, count);
    }

    println!("Rust dashboard status inventory:");
    for (status, count) in status_counts {
        println!("status:{}={}", status, count);
    }

    Ok(())
}
