package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"table_id", "table_name", "entity_type", "grain", "primary_key",
	"owner", "normalization_target", "row_count", "certification_status",
}

func main() {
	path := filepath.Join("..", "data", "relational_schema_inventory.csv")
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
	fmt.Println("Go validation passed: relational schema inventory includes all required fields.")
}
