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

    let domain_idx = headers.iter().position(|x| *x == "domain").unwrap();
    let class_idx = headers.iter().position(|x| *x == "classification").unwrap();

    let mut domain_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut classification_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *domain_counts.entry(cols[domain_idx].to_string()).or_default() += 1;
        *classification_counts.entry(cols[class_idx].to_string()).or_default() += 1;
    }

    println!("Rust metadata domain inventory:");
    for (domain, count) in domain_counts {
        println!("domain:{}={}", domain, count);
    }

    println!("Rust classification inventory:");
    for (classification, count) in classification_counts {
        println!("classification:{}={}", classification, count);
    }

    Ok(())
}
