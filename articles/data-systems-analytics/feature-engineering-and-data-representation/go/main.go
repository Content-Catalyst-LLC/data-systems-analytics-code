package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"feature_id",
	"feature_name",
	"feature_family",
	"source_field",
	"transformation",
	"model_stage",
	"status",
	"owner",
	"leakage_risk",
	"interpretability",
	"cardinality",
}

func main() {
	path := filepath.Join("..", "data", "feature_registry.csv")
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

	fmt.Println("Go validation passed: feature registry includes all required fields.")
}
