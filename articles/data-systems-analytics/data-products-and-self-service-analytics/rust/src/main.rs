use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/data_products.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let owner_idx = headers.iter().position(|x| *x == "owner").unwrap();
    let lifecycle_idx = headers.iter().position(|x| *x == "lifecycle_status").unwrap();

    let mut owner_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut lifecycle_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *owner_counts.entry(cols[owner_idx].to_string()).or_default() += 1;
        *lifecycle_counts.entry(cols[lifecycle_idx].to_string()).or_default() += 1;
    }

    println!("Rust ownership inventory:");
    for (owner, count) in owner_counts {
        println!("owner:{}={}", owner, count);
    }

    println!("Rust lifecycle inventory:");
    for (status, count) in lifecycle_counts {
        println!("status:{}={}", status, count);
    }

    Ok(())
}
