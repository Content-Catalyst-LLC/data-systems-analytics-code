use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/exploration_dataset.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let segment_idx = headers.iter().position(|x| *x == "segment").unwrap();
    let region_idx = headers.iter().position(|x| *x == "region").unwrap();
    let category_idx = headers.iter().position(|x| *x == "category").unwrap();

    let mut segment_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut region_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut category_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *segment_counts.entry(cols[segment_idx].to_string()).or_default() += 1;
        *region_counts.entry(cols[region_idx].to_string()).or_default() += 1;
        *category_counts.entry(cols[category_idx].to_string()).or_default() += 1;
    }

    println!("Rust EDA inventory:");
    for (segment, count) in segment_counts {
        println!("segment:{}={}", segment, count);
    }
    for (region, count) in region_counts {
        println!("region:{}={}", region, count);
    }
    for (category, count) in category_counts {
        println!("category:{}={}", category, count);
    }

    Ok(())
}
