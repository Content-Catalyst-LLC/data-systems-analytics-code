# Streaming Data and Real-Time Analytics

This companion code models streaming analytics as temporal evidence infrastructure: event logs, event time, processing time, lateness, windows, watermarks, triggers, stateful aggregates, delivery semantics, replay, serving tables, alert records, and governance review.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Streaming analytics interprets a world that is still unfolding.

```text
event sources → durable log → event-time windows + state
        → watermarks + triggers → provisional/refined outputs
        → alerts, serving views, replay, monitoring, governance
```

A mature streaming workflow does not ask only how quickly a metric updates. It asks whether the timestamp semantics are correct, how late events are handled, whether outputs are provisional or final, whether state is recoverable, and whether the system can be replayed and audited.
