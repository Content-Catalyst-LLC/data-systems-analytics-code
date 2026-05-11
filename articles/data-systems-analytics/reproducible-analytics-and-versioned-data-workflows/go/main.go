package main

import (
	"crypto/sha256"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strconv"
)

type Summary struct {
	Records int
	Total   int
}

func sha256File(path string) (string, error) {
	file, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer file.Close()

	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		return "", err
	}
	return fmt.Sprintf("%x", hash.Sum(nil)), nil
}

func main() {
	inputPath := filepath.Join("..", "data", "sample_events.csv")
	outputPath := filepath.Join("..", "outputs", "run_summary_go.csv")

	file, err := os.Open(inputPath)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	header, err := reader.Read()
	if err != nil {
		panic(err)
	}

	systemIdx := -1
	valueIdx := -1
	for i, name := range header {
		if name == "system" {
			systemIdx = i
		}
		if name == "value" {
			valueIdx = i
		}
	}

	summaries := map[string]Summary{}
	for {
		row, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
		value, err := strconv.Atoi(row[valueIdx])
		if err != nil {
			panic(err)
		}
		current := summaries[row[systemIdx]]
		current.Records++
		current.Total += value
		summaries[row[systemIdx]] = current
	}

	if err := os.MkdirAll(filepath.Join("..", "outputs"), 0755); err != nil {
		panic(err)
	}

	out, err := os.Create(outputPath)
	if err != nil {
		panic(err)
	}
	defer out.Close()

	writer := csv.NewWriter(out)
	defer writer.Flush()

	writer.Write([]string{"system", "records", "total_value", "average_value"})

	keys := make([]string, 0, len(summaries))
	for key := range summaries {
		keys = append(keys, key)
	}
	sort.Strings(keys)

	for _, key := range keys {
		s := summaries[key]
		avg := float64(s.Total) / float64(s.Records)
		writer.Write([]string{key, strconv.Itoa(s.Records), strconv.Itoa(s.Total), fmt.Sprintf("%.2f", avg)})
	}

	inputHash, _ := sha256File(inputPath)
	fmt.Printf("Go workflow complete\ninput_sha256=%s\noutput=%s\n", inputHash, outputPath)
}
