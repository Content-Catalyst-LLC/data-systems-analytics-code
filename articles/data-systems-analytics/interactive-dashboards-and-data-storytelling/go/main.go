package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"dashboard_id",
	"dashboard_title",
	"dashboard_type",
	"audience",
	"primary_use",
	"owner",
	"steward",
	"status",
	"refresh_cadence",
	"view_count",
	"filter_count",
	"created_at_utc",
	"last_reviewed_at_utc",
}

func main() {
	path := filepath.Join("..", "data", "dashboard_inventory.csv")
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

	fmt.Println("Go validation passed: dashboard registry includes all required fields.")
}
