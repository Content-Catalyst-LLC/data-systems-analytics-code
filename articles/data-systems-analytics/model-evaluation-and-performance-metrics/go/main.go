package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"model_id",
	"model_name",
	"task_type",
	"prediction_target",
	"owner",
	"steward",
	"status",
	"version",
	"training_window",
	"validation_window",
	"intended_use",
	"risk_level",
}

func main() {
	path := filepath.Join("..", "data", "model_registry.csv")
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

	fmt.Println("Go validation passed: model evaluation registry includes all required fields.")
}
