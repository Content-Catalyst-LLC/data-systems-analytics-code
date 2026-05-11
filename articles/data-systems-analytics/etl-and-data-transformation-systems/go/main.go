package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredCustomerFields = []string{
	"source_system", "source_customer_id", "customer_name", "status_code",
	"country_code", "created_at", "updated_at", "email",
}

func main() {
	path := filepath.Join("..", "data", "raw_customer_extract.csv")
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
	for _, field := range requiredCustomerFields {
		if !present[field] {
			fmt.Printf("missing_required_field=%s\n", field)
			valid = false
		}
	}
	if !valid {
		os.Exit(1)
	}
	fmt.Println("Go validation passed: raw customer extract includes all required fields.")
}
