"""Follow a growing log file (like `tail -f`) and yield new lines.

Owner: Person 2 (backend detection/core)
Status: SCAFFOLD, not implemented.

Planned:
- Start at end of file (or beginning, configurable) and poll every
  `settings.poll_interval_seconds`.
- Handle truncation/rotation by reopening when the file shrinks.
- Source path: `settings.log_file_path`.
"""
