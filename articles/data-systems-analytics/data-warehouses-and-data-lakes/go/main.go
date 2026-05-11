package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"asset_id", "asset_name", "architecture_zone", "storage_form", "schema_strategy",
	"file_or_table_format", "owner", "governance_status", "row_count", "size_gb",
	"freshness_hours", "pii_classification", "query_frequency_per_day", "ml_ready",
}

func main() {
	path := filepath.Join("..", "data", "data_assets.csv")
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	header, err := reader.Read()
	if err != nil {
		panic(err)
	}

	present := map[string]bool{}
	for _, field := range header {
		present[field] = true
	}

	valid := true
	for _, field := range requiredFields {
		if !present[field] {
			fmt.Printf("missing_required_field=%s\n", field)
			valid = false
		}
	}
	if !valid {
		os.Exit(1)
	}
	fmt.Println("Go validation passed: data assets include all required fields.")
}
