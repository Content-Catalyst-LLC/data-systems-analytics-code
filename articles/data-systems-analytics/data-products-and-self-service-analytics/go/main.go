package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"product_id",
	"domain",
	"product_name",
	"owner",
	"consumer_group",
	"criticality",
	"freshness_sla_hours",
	"semantic_status",
	"quality_score",
	"access_model",
	"lifecycle_status",
}

func main() {
	path := filepath.Join("..", "data", "data_products.csv")
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

	fmt.Println("Go validation passed: data product registry includes all required contract fields.")
}
