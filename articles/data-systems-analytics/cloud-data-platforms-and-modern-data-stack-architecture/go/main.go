package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func readCSV(path string) ([]map[string]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	header, err := reader.Read()
	if err != nil {
		return nil, err
	}

	rows, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	out := make([]map[string]string, 0, len(rows))
	for _, row := range rows {
		m := map[string]string{}
		for i, col := range header {
			m[col] = row[i]
		}
		out = append(out, m)
	}
	return out, nil
}

func main() {
	required := map[string]bool{
		"source": false, "ingestion": false, "storage": false,
		"transformation": false, "orchestration": false, "metadata": false,
		"lineage": false, "semantic": false, "serving": false, "consumption": false,
	}

	components, err := readCSV(filepath.Join("..", "data", "stack_components.csv"))
	if err != nil {
		panic(err)
	}

	for _, row := range components {
		layer := row["layer"]
		if _, ok := required[layer]; ok {
			required[layer] = true
		}
	}

	valid := true
	for layer, present := range required {
		if !present {
			fmt.Printf("missing_required_layer=%s\n", layer)
			valid = false
		}
	}

	if valid {
		fmt.Println("Go validation passed: all required architectural layers are represented.")
	} else {
		os.Exit(1)
	}
}
