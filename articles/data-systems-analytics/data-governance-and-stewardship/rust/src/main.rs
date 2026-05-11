use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let path = "../data/policy_register.csv";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let header_line = lines.next().unwrap()?;
    let headers: Vec<&str> = header_line.split(',').collect();

    let domain_idx = headers.iter().position(|x| *x == "policy_domain").unwrap();
    let enforcement_idx = headers.iter().position(|x| *x == "enforcement_status").unwrap();

    let mut domain_counts: BTreeMap<String, u32> = BTreeMap::new();
    let mut enforcement_counts: BTreeMap<String, u32> = BTreeMap::new();

    for line in lines {
        let line = line?;
        let cols: Vec<&str> = line.split(',').collect();
        *domain_counts.entry(cols[domain_idx].to_string()).or_default() += 1;
        *enforcement_counts.entry(cols[enforcement_idx].to_string()).or_default() += 1;
    }

    println!("Rust policy-domain inventory:");
    for (domain, count) in domain_counts {
        println!("policy_domain:{}={}", domain, count);
    }

    println!("Rust enforcement-status inventory:");
    for (status, count) in enforcement_counts {
        println!("enforcement_status:{}={}", status, count);
    }

    Ok(())
}
