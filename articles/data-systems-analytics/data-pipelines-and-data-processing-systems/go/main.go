package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"stage_id", "pipeline_name", "stage_name", "stage_type", "mode",
	"upstream_stage", "downstream_stage", "owner", "criticality", "status",
}

func main() {
	path := filepath.Join("..", "data", "pipeline_stages.csv")
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
	fmt.Println("Go validation passed: pipeline stages include all required fields.")
}
