package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"time"
)

type Event struct {
	SystemID string
	Metric  string
	Value   float64
	Time    time.Time
}

func main() {
	events := []Event{
		{"water_grid", "flow_rate", 101.4, time.Now()},
		{"energy_grid", "load", 462.8, time.Now().Add(1 * time.Second)},
		{"food_supply", "delivery_delay", 6.1, time.Now().Add(2 * time.Second)},
		{"health_system", "bed_utilization", 0.84, time.Now().Add(3 * time.Second)},
	}

	if err := os.MkdirAll("outputs", 0755); err != nil {
		panic(err)
	}

	file, err := os.Create("outputs/go-streaming-events.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{"system_id", "metric_name", "metric_value", "event_time"})
	for _, event := range events {
		writer.Write([]string{
			event.SystemID,
			event.Metric,
			strconv.FormatFloat(event.Value, 'f', 4, 64),
			event.Time.Format(time.RFC3339),
		})
		fmt.Printf("streamed event: %+v\n", event)
	}

	fmt.Println("Wrote outputs/go-streaming-events.csv")
}
