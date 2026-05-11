package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

var requiredCandidateFields = []string{
	"candidate_id",
	"left_record_id",
	"right_record_id",
	"entity_type",
	"match_method",
	"name_similarity",
	"address_similarity",
	"identifier_match",
	"relationship_evidence",
	"match_score",
	"recommended_action",
	"review_required",
}

func main() {
	path := filepath.Join("..", "data", "candidate_matches.csv")
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
	for _, field := range requiredCandidateFields {
		if !present[field] {
			fmt.Printf("missing_required_field=%s\n", field)
			valid = false
		}
	}

	if !valid {
		os.Exit(1)
	}

	fmt.Println("Go validation passed: candidate match registry includes all required contract fields.")
}
