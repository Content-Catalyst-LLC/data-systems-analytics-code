use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/model_registry.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let family_idx = headers.iter().position(|x| *x == "model_family").unwrap();
    let estimand_idx = headers.iter().position(|x| *x == "estimand").unwrap();

    let mut family_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut estimand_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *family_counts.entry(cols[family_idx].to_string()).or_default() += 1;
        *estimand_counts.entry(cols[estimand_idx].to_string()).or_default() += 1;
    }

    println!("Rust statistical model family inventory:");
    for (family, count) in family_counts {
        println!("model_family:{}={}", family, count);
    }

    println!("Rust estimand inventory:");
    for (estimand, count) in estimand_counts {
        println!("estimand:{}={}", estimand, count);
    }

    Ok(())
}
