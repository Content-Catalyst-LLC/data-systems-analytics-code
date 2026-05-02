from pathlib import Path
import csv

def test_observations_required_fields():
    path = Path("data/raw/observations.csv")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
    required = {"observation_id", "system_id", "observed_at", "metric_name", "metric_value", "unit", "source_system"}
    assert required <= fields
