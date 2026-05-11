package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"mapping_id",
	"source_system",
	"target_model",
	"source_field",
	"target_field",
	"transformation_type",
	"semantic_risk",
	"owner",
	"status",
}

func main() {
	path := filepath.Join("..", "data", "schema_mappings.csv")
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

	fmt.Println("Go validation passed: schema mapping registry includes all required contract fields.")
}
