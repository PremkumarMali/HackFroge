# frontend

**Owner:** Person 1
**Status:** not started, framework not chosen yet.

## What it needs to show

1. **Live metrics chart**: per-window line count and error rate, with the
   baseline band, streamed from `WS /ws/metrics`.
2. **Alert feed**: newest-first list of alerts from `WS /ws/alerts`, colour-coded
   by severity (`NORMAL`, `LOW`, `MEDIUM`, `HIGH`), each expandable to show the
   explanation and sample log lines.
3. **Connection status**: connected/reconnecting indicator for each socket.

On page load (and after a reconnect), backfill from `GET /metrics` and
`GET /alerts`, then switch to the WebSocket streams.

## Contract

All payloads are defined in [`docs/api-contract.md`](../docs/api-contract.md).
Do not invent fields. If you need one, update the contract in a PR first.

Backend base URL (local): `http://localhost:8000`
WebSocket base URL (local): `ws://localhost:8000`
