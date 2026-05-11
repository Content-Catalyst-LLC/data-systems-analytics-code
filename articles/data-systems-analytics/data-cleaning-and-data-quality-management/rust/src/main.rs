use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/raw_customer_records.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let source_idx = headers.iter().position(|x| *x == "source_system").unwrap();
    let country_idx = headers.iter().position(|x| *x == "country_code").unwrap();
    let status_idx = headers.iter().position(|x| *x == "status").unwrap();

    let mut source_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut country_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *source_counts.entry(cols[source_idx].to_string()).or_default() += 1;
        *country_counts.entry(cols[country_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
    }

    println!("Rust data quality inventory:");
    for (source, count) in source_counts {
        println!("source_system:{}={}", source, count);
    }
    for (country, count) in country_counts {
        println!("country_code:{}={}", country, count);
    }
    for (status, count) in status_counts {
        println!("status:{}={}", status, count);
    }

    Ok(())
}
