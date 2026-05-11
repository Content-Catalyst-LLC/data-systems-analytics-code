#!/usr/bin/env python3
"""
Python Workflow: Streaming Analytics and Event-Time Scorecard

This workflow evaluates event-time lateness, windowed aggregates, watermark
lag, alert triggers, topic governance, and streaming-readiness scores using
only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import statistics
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "in_review": 0.7,
        "watch": 0.55,
        "warn": 0.4,
        "needs_revision": 0.15,
        "fail": 0.0,
    }.get(value, 0.5)

def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.45}.get(value, 0.1)

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def window_start(ts: datetime, size_seconds: int) -> datetime:
    epoch = int(ts.timestamp())
    start = epoch - (epoch % size_seconds)
    return datetime.fromtimestamp(start, tz=timezone.utc)

def main() -> None:
    events_path = ROOT / "data" / "event_stream.csv"
    topics_path = ROOT / "data" / "stream_topic_registry.csv"
    windows_path = ROOT / "data" / "window_definitions.csv"
    watermark_path = ROOT / "data" / "watermark_observations.csv"
    alerts_path = ROOT / "data" / "alert_rules.csv"
    governance_path = ROOT / "data" / "governance_checks.csv"

    events = read_csv(events_path)
    topics = read_csv(topics_path)
    windows = read_csv(windows_path)
    watermarks = read_csv(watermark_path)
    alerts = read_csv(alerts_path)
    governance = read_csv(governance_path)

    enriched = []
    lateness_values = []
    for row in events:
        event_time = parse_ts(row["event_time"])
        processing_time = parse_ts(row["processing_time"])
        lateness = max(0.0, (processing_time - event_time).total_seconds())
        lateness_values.append(lateness)
        enriched.append({
            "event_id": row["event_id"],
            "event_key": row["event_key"],
            "event_type": row["event_type"],
            "event_time": row["event_time"],
            "processing_time": row["processing_time"],
            "lateness_seconds": round(lateness, 3),
            "region": row["region"],
            "source_system": row["source_system"],
            "value": row["value"],
            "quality_score": row["quality_score"],
        })

    # One-minute tumbling event-time window summaries.
    by_window = defaultdict(list)
    for row in events:
        ts = parse_ts(row["event_time"])
        start = window_start(ts, 60)
        by_window[start].append(row)

    window_rows = []
    for start, rows in sorted(by_window.items()):
        values = [float(r["value"]) for r in rows]
        purchases = [float(r["value"]) for r in rows if r["event_type"] == "purchase"]
        sensor_values = [float(r["value"]) for r in rows if r["event_type"] == "sensor_reading"]
        window_rows.append({
            "window_start": start.isoformat().replace("+00:00", "Z"),
            "window_end": datetime.fromtimestamp(start.timestamp() + 60, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
            "event_count": len(rows),
            "purchase_count": sum(1 for r in rows if r["event_type"] == "purchase"),
            "purchase_value_sum": round(sum(purchases), 3),
            "sensor_reading_count": len(sensor_values),
            "sensor_value_mean": round(mean(sensor_values), 3) if sensor_values else "",
            "max_value": round(max(values), 3),
        })

    # Stateful keyed counts and value totals.
    state_by_key = defaultdict(lambda: {"events": 0, "purchase_value": 0.0, "latest_event_time": ""})
    for row in sorted(events, key=lambda r: r["processing_time"]):
        state = state_by_key[row["event_key"]]
        state["events"] += 1
        if row["event_type"] == "purchase":
            state["purchase_value"] += float(row["value"])
        state["latest_event_time"] = row["event_time"]

    state_rows = [
        {
            "event_key": key,
            "event_count": value["events"],
            "purchase_value": round(value["purchase_value"], 3),
            "latest_event_time": value["latest_event_time"],
        }
        for key, value in sorted(state_by_key.items())
    ]

    watermark_rows = []
    for row in watermarks:
        processing_time = parse_ts(row["processing_time"])
        watermark_time = parse_ts(row["watermark_time"])
        observed_max = parse_ts(row["observed_max_event_time"])
        watermark_lag = (processing_time - watermark_time).total_seconds()
        event_progress_lag = (processing_time - observed_max).total_seconds()
        watermark_rows.append({
            "observation_id": row["observation_id"],
            "stream_name": row["stream_name"],
            "processing_time": row["processing_time"],
            "watermark_lag_seconds": round(watermark_lag, 3),
            "event_progress_lag_seconds": round(event_progress_lag, 3),
            "late_event_count": row["late_event_count"],
            "state_size_mb": row["state_size_mb"],
            "backpressure_ms": row["backpressure_ms"],
            "status": row["status"],
        })

    alert_rows = []
    high_sensor_rule = next(a for a in alerts if a["rule_id"] == "al001")
    low_quality_rule = next(a for a in alerts if a["rule_id"] == "al004")
    for row in events:
        value = float(row["value"])
        quality = float(row["quality_score"])
        if row["event_type"] == "sensor_reading" and value > float(high_sensor_rule["threshold"]):
            alert_rows.append({
                "rule_id": high_sensor_rule["rule_id"],
                "event_id": row["event_id"],
                "event_key": row["event_key"],
                "severity": high_sensor_rule["severity"],
                "condition": high_sensor_rule["condition"],
                "observed_value": value,
                "event_time": row["event_time"],
            })
        if quality < float(low_quality_rule["threshold"]):
            alert_rows.append({
                "rule_id": low_quality_rule["rule_id"],
                "event_id": row["event_id"],
                "event_key": row["event_key"],
                "severity": low_quality_rule["severity"],
                "condition": low_quality_rule["condition"],
                "observed_value": quality,
                "event_time": row["event_time"],
            })

    # Governance scoring.
    governance_rows = []
    gov_scores = []
    for check in governance:
        score = max(0.0, status_score(check["status"]) - (severity_penalty(check["severity"]) if check["status"] != "pass" else 0.0))
        gov_scores.append(score)
        governance_rows.append({
            "check_id": check["check_id"],
            "check_type": check["check_type"],
            "status": check["status"],
            "severity": check["severity"],
            "score": round(score, 3),
            "remediation": check["remediation"],
        })

    topic_rows = []
    for topic in topics:
        retention_score = 1.0 if int(topic["retention_hours"]) >= 72 else 0.5
        replication_score = 1.0 if int(topic["replication_factor"]) >= 3 else 0.45
        semantic_score = {
            "exactly_once_effective": 0.85,
            "at_least_once": 0.7,
            "at_most_once": 0.3,
        }.get(topic["delivery_semantics"], 0.5)
        readiness = round(
            0.25 * retention_score
            + 0.25 * replication_score
            + 0.25 * semantic_score
            + 0.25 * status_score(topic["status"]),
            3,
        )
        topic_rows.append({
            "topic_id": topic["topic_id"],
            "topic_name": topic["topic_name"],
            "event_domain": topic["event_domain"],
            "delivery_semantics": topic["delivery_semantics"],
            "status": topic["status"],
            "stream_topic_readiness_score": readiness,
            "readiness_gap": round(1.0 - readiness, 3),
        })

    late_rate = sum(1 for x in lateness_values if x > 30) / len(lateness_values)
    p95_lateness = sorted(lateness_values)[math.floor(0.95 * (len(lateness_values) - 1))]
    readiness = round(
        0.22 * (1.0 - min(late_rate, 1.0))
        + 0.22 * mean(gov_scores)
        + 0.18 * (1.0 if window_rows else 0.0)
        + 0.18 * (1.0 if state_rows else 0.0)
        + 0.10 * (1.0 if alert_rows else 0.5)
        + 0.10 * (1.0 if mean([float(w["backpressure_ms"]) for w in watermarks]) < 60 else 0.5),
        3,
    )

    readiness_rows = [{
        "dataset": "event_stream.csv",
        "event_count": len(events),
        "topic_count": len(topics),
        "window_definition_count": len(windows),
        "alert_count": len(alert_rows),
        "mean_lateness_seconds": round(mean(lateness_values), 3),
        "p95_lateness_seconds": round(p95_lateness, 3),
        "late_event_rate_over_30s": round(late_rate, 4),
        "streaming_readiness_score": readiness,
        "streaming_readiness_gap": round(1.0 - readiness, 3),
    }]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Streaming Data and Real-Time Analytics",
        "workflow": "streaming-analytics-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "event_stream": {"path": str(events_path), "sha256": sha256_file(events_path), "rows": len(events)},
            "stream_topic_registry": {"path": str(topics_path), "sha256": sha256_file(topics_path), "rows": len(topics)},
            "window_definitions": {"path": str(windows_path), "sha256": sha256_file(windows_path), "rows": len(windows)},
            "watermark_observations": {"path": str(watermark_path), "sha256": sha256_file(watermark_path), "rows": len(watermarks)},
            "alert_rules": {"path": str(alerts_path), "sha256": sha256_file(alerts_path), "rows": len(alerts)},
            "governance_checks": {"path": str(governance_path), "sha256": sha256_file(governance_path), "rows": len(governance)},
        },
    }

    write_csv(ROOT / "outputs" / "event_lateness_profile_python.csv", enriched)
    write_csv(ROOT / "outputs" / "event_time_window_summary_python.csv", window_rows)
    write_csv(ROOT / "outputs" / "stateful_key_summary_python.csv", state_rows)
    write_csv(ROOT / "outputs" / "watermark_lag_profile_python.csv", watermark_rows)
    write_csv(ROOT / "outputs" / "alert_records_python.csv", alert_rows)
    write_csv(ROOT / "outputs" / "governance_check_scorecard_python.csv", governance_rows)
    write_csv(ROOT / "outputs" / "stream_topic_readiness_python.csv", topic_rows)
    write_csv(ROOT / "outputs" / "streaming_readiness_python.csv", readiness_rows)
    (ROOT / "outputs" / "streaming_analytics_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Streaming analytics scorecard complete")
    print(json.dumps({"events": len(events), "alerts": len(alert_rows), "readiness": readiness}, indent=2))

if __name__ == "__main__":
    main()
