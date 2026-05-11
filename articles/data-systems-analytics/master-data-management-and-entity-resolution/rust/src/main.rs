use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/source_records.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let source_idx = headers.iter().position(|x| *x == "source_system").unwrap();
    let entity_idx = headers.iter().position(|x| *x == "entity_type").unwrap();

    let mut source_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut entity_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *source_counts.entry(cols[source_idx].to_string()).or_default() += 1;
        *entity_counts.entry(cols[entity_idx].to_string()).or_default() += 1;
    }

    println!("Rust MDM source-system inventory:");
    for (source, count) in source_counts {
        println!("source_system:{}={}", source, count);
    }

    println!("Rust entity-type inventory:");
    for (entity_type, count) in entity_counts {
        println!("entity_type:{}={}", entity_type, count);
    }

    Ok(())
}
