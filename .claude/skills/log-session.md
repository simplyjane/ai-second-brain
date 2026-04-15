# Log Session

Captures important moments from the current conversation into today's daily log.

## When to use

- Automatically before session ends or compaction — summarize what happened
- When Jing says "log this", "save this", or "remember this for later"
- When a key decision is made, a lesson is learned, or an important insight surfaces
- Run this proactively when you notice something worth persisting

## Instructions

Append to today's daily log at `daily-logs/YYYY-MM-DD.md`.

Use the log-to-brain script:
```bash
bash scripts/log-to-brain.sh "<category>" "<content>"
```

Categories:
- **decision** — A choice that was made, with reasoning
- **lesson** — Something learned from a mistake or success
- **insight** — A non-obvious realization or connection
- **todo** — Something to follow up on later
- **note** — General context worth remembering

## Rules

- Be specific. "Decided to use SQLite" is useless. "Decided to use SQLite FTS5 for brain search because no external deps needed and scales fine for personal use" is useful.
- Include the WHY, not just the what.
- One log entry per distinct thing — don't lump multiple decisions into one entry.
- If the conversation was a deep work session, write a 2-3 sentence summary at the end.

## Session Summary Format

When summarizing a session (end of conversation or before compaction):

```bash
bash scripts/log-to-brain.sh "session-summary" "Worked on [topic]. Key outcomes: [1-3 bullet points]. Open questions: [anything unresolved]."
```
