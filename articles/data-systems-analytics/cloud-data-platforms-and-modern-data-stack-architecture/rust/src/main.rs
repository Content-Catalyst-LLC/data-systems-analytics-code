use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/pipeline_catalog.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();
    let owner_idx = headers.iter().position(|x| *x == "owner").unwrap();

    let mut owner_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        let owner = cols[owner_idx].to_string();
        *owner_counts.entry(owner).or_default() += 1;
    }

    println!("Rust pipeline owner inventory:");
    for (owner, count) in owner_counts {
        println!("{}={}", owner, count);
    }

    Ok(())
}
