package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredFields = []string{
	"node_id", "region", "zone", "role", "status",
	"storage_gb", "cpu_utilization", "network_rtt_ms", "last_heartbeat",
}

func main() {
	path := filepath.Join("..", "data", "cluster_nodes.csv")
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
	fmt.Println("Go validation passed: cluster nodes include all required fields.")
}
