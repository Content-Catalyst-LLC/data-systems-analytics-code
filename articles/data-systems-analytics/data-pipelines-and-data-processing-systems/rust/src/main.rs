use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/pipeline_stages.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let pipeline_idx = headers.iter().position(|x| *x == "pipeline_name").unwrap();
    let type_idx = headers.iter().position(|x| *x == "stage_type").unwrap();
    let mode_idx = headers.iter().position(|x| *x == "mode").unwrap();

    let mut pipeline_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut type_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut mode_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *pipeline_counts.entry(cols[pipeline_idx].to_string()).or_default() += 1;
        *type_counts.entry(cols[type_idx].to_string()).or_default() += 1;
        *mode_counts.entry(cols[mode_idx].to_string()).or_default() += 1;
    }

    println!("Rust pipeline stage inventory:");
    for (pipeline, count) in pipeline_counts {
        println!("pipeline:{}={}", pipeline, count);
    }
    for (stage_type, count) in type_counts {
        println!("stage_type:{}={}", stage_type, count);
    }
    for (mode, count) in mode_counts {
        println!("mode:{}={}", mode, count);
    }

    Ok(())
}
