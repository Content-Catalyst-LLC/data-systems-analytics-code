use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/data_assets.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let zone_idx = headers.iter().position(|x| *x == "architecture_zone").unwrap();
    let format_idx = headers.iter().position(|x| *x == "file_or_table_format").unwrap();
    let schema_idx = headers.iter().position(|x| *x == "schema_strategy").unwrap();

    let mut zone_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut format_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut schema_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *zone_counts.entry(cols[zone_idx].to_string()).or_default() += 1;
        *format_counts.entry(cols[format_idx].to_string()).or_default() += 1;
        *schema_counts.entry(cols[schema_idx].to_string()).or_default() += 1;
    }

    println!("Rust warehouse/lake inventory:");
    for (zone, count) in zone_counts {
        println!("architecture_zone:{}={}", zone, count);
    }
    for (format, count) in format_counts {
        println!("format:{}={}", format, count);
    }
    for (schema, count) in schema_counts {
        println!("schema_strategy:{}={}", schema, count);
    }

    Ok(())
}
