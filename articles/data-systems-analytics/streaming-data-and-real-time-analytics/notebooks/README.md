# Notebook guidance

Use notebooks to inspect streaming evidence, not to hide official event-time logic.

Recommended pattern:

1. Run `python/streaming_analytics_scorecard.py`.
2. Load `outputs/streaming_analytics_manifest_python.json`.
3. Inspect event lateness, event-time windows, keyed state, watermark lag, alerts, topic readiness, and governance checks.
4. Compare event-time and processing-time interpretations.
5. Preserve questions about late data, provisional outputs, replay, and state recovery.
