package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"asset_id",
	"asset_name",
	"domain",
	"asset_type",
	"owner",
	"steward",
	"classification",
	"criticality",
	"certification_status",
	"lifecycle_status",
	"created_at_utc",
	"last_reviewed_at_utc",
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

	fmt.Println("Go validation passed: data asset governance registry includes all required fields.")
}
