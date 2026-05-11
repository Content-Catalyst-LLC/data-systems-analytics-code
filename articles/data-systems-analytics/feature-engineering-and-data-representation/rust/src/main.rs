use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/feature_registry.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let family_idx = headers.iter().position(|x| *x == "feature_family").unwrap();
    let status_idx = headers.iter().position(|x| *x == "status").unwrap();

    let mut family_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *family_counts.entry(cols[family_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
    }

    println!("Rust feature family inventory:");
    for (family, count) in family_counts {
        println!("feature_family:{}={}", family, count);
    }

    println!("Rust feature status inventory:");
    for (status, count) in status_counts {
        println!("status:{}={}", status, count);
    }

    Ok(())
}
