"""Broadcast metrics/alerts to connected WebSocket clients.

Owner: Person 3 (WebSockets, integration)
Status: SCAFFOLD, not implemented.

Planned:
- Track connected clients per channel (/ws/metrics, /ws/alerts).
- Send {"type": "metrics" | "alert", "data": {...}}; drop dead connections.
"""
