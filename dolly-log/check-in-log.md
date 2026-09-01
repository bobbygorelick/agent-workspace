# Dolly's Check-In Log

This is an **append-only** log, read and written by code
(`dolly-agent/log_store.py`) and by the `dolly` Claude Code subagent.
Don't hand-edit the structure — only ever append new entries at the
bottom, each as its own `---`-delimited YAML block, exactly like this:

```yaml
---
date: 2026-08-31
time_of_day: morning
habit: marijuana_free
status: true
value: null
streak: 5
notes: ""
---
```

Field reference:
- `date` — ISO date (YYYY-MM-DD), always the real local date the entry
  was logged, never assumed.
- `time_of_day` — `morning` or `evening`.
- `habit` — one of: `marijuana_free`, `bedtime_by_11`, `workout`,
  `meditation`, `yoga`, `outdoor_walk_run`, `dog_park`, `healthy_meal`,
  `sleep`.
- `status` — `true`/`false` for whether the habit was achieved (not used
  for `sleep`, which just records raw values).
- `value` — free-form extra data when needed (e.g. actual bedtime/wake
  time for the `sleep` habit). `null` otherwise.
- `streak` — the current consecutive-day count for that habit *after*
  this entry (0 if `status` is false). Not used for `sleep`.
- `notes` — optional short free text.

The current streak for any habit is always just the `streak` value on
its most recent entry — there's no separate summary section to keep in
sync.

## Entries

<!-- New entries are appended below this line. -->
