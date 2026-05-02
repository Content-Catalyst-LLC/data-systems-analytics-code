use std::collections::HashSet;
use std::env;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let path = env::args().nth(1).unwrap_or_else(|| "data/raw/observations.csv".to_string());
    let mut reader = csv::Reader::from_path(&path)?;
    let headers = reader.headers()?.clone();
    let header_set: HashSet<&str> = headers.iter().collect();

    let required = [
        "observation_id",
        "system_id",
        "observed_at",
        "metric_name",
        "metric_value",
        "unit",
        "source_system",
    ];

    let missing: Vec<&str> = required
        .iter()
        .copied()
        .filter(|field| !header_set.contains(field))
        .collect();

    if !missing.is_empty() {
        eprintln!("Missing required fields: {:?}", missing);
        std::process::exit(1);
    }

    let mut count = 0usize;
    for result in reader.records() {
        let _record = result?;
        count += 1;
    }

    println!("{} passed contract check with {} records.", path, count);
    Ok(())
}
