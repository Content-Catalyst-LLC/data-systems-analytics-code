package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"model_id", "series_id", "model_name", "model_family", "frequency",
	"horizon", "uses_exogenous", "validation_design", "status", "owner", "risk_level",
}

func main() {
	path := filepath.Join("..", "data", "forecast_model_registry.csv")
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
	fmt.Println("Go validation passed: forecast model registry includes all required fields.")
}
