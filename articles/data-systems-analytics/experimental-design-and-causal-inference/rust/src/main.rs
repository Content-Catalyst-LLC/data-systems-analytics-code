use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/causal_study_registry.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let design_idx = headers.iter().position(|x| *x == "design_type").unwrap();
    let estimand_idx = headers.iter().position(|x| *x == "estimand").unwrap();

    let mut design_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut estimand_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *design_counts.entry(cols[design_idx].to_string()).or_default() += 1;
        *estimand_counts.entry(cols[estimand_idx].to_string()).or_default() += 1;
    }

    println!("Rust causal design inventory:");
    for (design, count) in design_counts {
        println!("design_type:{}={}", design, count);
    }

    println!("Rust estimand inventory:");
    for (estimand, count) in estimand_counts {
        println!("estimand:{}={}", estimand, count);
    }

    Ok(())
}
