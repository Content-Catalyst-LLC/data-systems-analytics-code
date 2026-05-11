package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"dashboard_id",
	"dashboard_name",
	"domain",
	"primary_user",
	"decision_function",
	"certification_status",
	"refresh_sla_hours",
	"owner",
	"lifecycle_status",
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

	fmt.Println("Go validation passed: BI dashboard inventory includes all required contract fields.")
}
