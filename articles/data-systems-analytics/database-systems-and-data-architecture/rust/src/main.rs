use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/system_inventory.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let type_idx = headers.iter().position(|x| *x == "system_type").unwrap();
    let storage_idx = headers.iter().position(|x| *x == "storage_model").unwrap();
    let status_idx = headers.iter().position(|x| *x == "certification_status").unwrap();

    let mut type_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut storage_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *type_counts.entry(cols[type_idx].to_string()).or_default() += 1;
        *storage_counts.entry(cols[storage_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
    }

    println!("Rust database architecture inventory:");
    for (system_type, count) in type_counts {
        println!("system_type:{}={}", system_type, count);
    }
    for (storage_model, count) in storage_counts {
        println!("storage_model:{}={}", storage_model, count);
    }
    for (status, count) in status_counts {
        println!("certification_status:{}={}", status, count);
    }

    Ok(())
}
