package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"visual_id",
	"visual_title",
	"visualization_context",
	"audience",
	"primary_task",
	"owner",
	"steward",
	"status",
	"version",
	"publication_surface",
	"created_at_utc",
	"last_reviewed_at_utc",
}

func main() {
	path := filepath.Join("..", "data", "visualization_inventory.csv")
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

	fmt.Println("Go validation passed: visualization registry includes all required fields.")
}
