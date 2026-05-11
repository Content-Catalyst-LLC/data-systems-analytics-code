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

    let task_idx = headers.iter().position(|x| *x == "task_type").unwrap();
    let family_idx = headers.iter().position(|x| *x == "model_family").unwrap();
    let status_idx = headers.iter().position(|x| *x == "status").unwrap();

    let mut task_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut family_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut status_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *task_counts.entry(cols[task_idx].to_string()).or_default() += 1;
        *family_counts.entry(cols[family_idx].to_string()).or_default() += 1;
        *status_counts.entry(cols[status_idx].to_string()).or_default() += 1;
    }

    println!("Rust predictive task inventory:");
    for (task, count) in task_counts {
        println!("task_type:{}={}", task, count);
    }

    println!("Rust model family inventory:");
    for (family, count) in family_counts {
        println!("model_family:{}={}", family, count);
    }

    println!("Rust model status inventory:");
    for (status, count) in status_counts {
        println!("status:{}={}", status, count);
    }

    Ok(())
}
