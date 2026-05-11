use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/replica_status.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let shard_idx = headers.iter().position(|x| *x == "shard_id").unwrap();
    let state_idx = headers.iter().position(|x| *x == "replica_state").unwrap();
    let leader_idx = headers.iter().position(|x| *x == "is_leader").unwrap();

    let mut shard_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut state_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut leader_count = 0u32;

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *shard_counts.entry(cols[shard_idx].to_string()).or_default() += 1;
        *state_counts.entry(cols[state_idx].to_string()).or_default() += 1;
        if cols[leader_idx] == "1" {
            leader_count += 1;
        }
    }

    println!("Rust distributed replica inventory:");
    for (shard, count) in shard_counts {
        println!("shard:{}={}", shard, count);
    }
    for (state, count) in state_counts {
        println!("replica_state:{}={}", state, count);
    }
    println!("leader_replicas={}", leader_count);

    Ok(())
}
