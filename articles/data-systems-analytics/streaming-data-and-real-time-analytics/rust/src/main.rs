use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/event_stream.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let type_idx = headers.iter().position(|x| *x == "event_type").unwrap();
    let source_idx = headers.iter().position(|x| *x == "source_system").unwrap();
    let region_idx = headers.iter().position(|x| *x == "region").unwrap();

    let mut type_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut source_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut region_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *type_counts.entry(cols[type_idx].to_string()).or_default() += 1;
        *source_counts.entry(cols[source_idx].to_string()).or_default() += 1;
        *region_counts.entry(cols[region_idx].to_string()).or_default() += 1;
    }

    println!("Rust streaming event inventory:");
    for (event_type, count) in type_counts {
        println!("event_type:{}={}", event_type, count);
    }
    for (source, count) in source_counts {
        println!("source_system:{}={}", source, count);
    }
    for (region, count) in region_counts {
        println!("region:{}={}", region, count);
    }

    Ok(())
}
