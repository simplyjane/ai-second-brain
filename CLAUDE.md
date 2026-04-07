# AI Second Brain

This is Jing's AI Second Brain — a personal knowledge management system built on Karpathy's 3-phase method (Collect, Compile, Query) with Cole Medin's architecture (memory layer, skills, hooks).

## Structure

```
memory/              — Persistent memory (soul.md, user.md, memory.md)
knowledge/raw/       — Raw sources (drop articles, transcripts, notes here)
knowledge/wiki/      — LLM-compiled structured wiki
daily-logs/          — Raw conversation logs, one file per day
scripts/             — Hook scripts and automation
.claude/skills/      — Claude Code skills for the brain
brain.db             — SQLite FTS5 index for full-text search
logs/                — Cron job logs
```

## Skills

- **compile-wiki** — Build/update wiki from raw sources. Say "compile" or "update wiki".
- **promote-memory** — Promote insights from daily logs to memory. Say "promote" or "update memory".
- **query-brain** — Search across all knowledge and memory. Say "search my brain" or "what do I know about...".
- **find-gaps** — Find what's missing in the knowledge base. Say "find gaps" or "what am I missing".
- **log-session** — Capture important moments to daily log. Say "log this" or use proactively.

## Scripts

- `scripts/index_logs.py` — Index daily logs, wiki, and memory into SQLite FTS5. Run after adding content.
- `scripts/search_brain.py` — Full-text search across the entire brain. Use `--json` for piping to Claude.
- `scripts/promote.py` — Automated memory promotion using Claude CLI. Reads daily logs, promotes to memory.md.
- `scripts/daily-cron.sh` — Daily maintenance: index + promote. Set up as cron job.
- `scripts/log-to-brain.sh` — Append entries to today's daily log. Used by skills and hooks.

## Hooks

- **SessionStart** — Loads soul.md, user.md, memory.md into context
- **Stop** — Saves session marker to daily log
- **PreCompact** — Saves compaction marker to daily log

## Cron Setup

Daily maintenance at 11pm:
```
0 23 * * * bash ~/Documents/JingAIJourney/ai-second-brain/scripts/daily-cron.sh >> ~/Documents/JingAIJourney/ai-second-brain/logs/cron.log 2>&1
```

## Principles

- Memory compounds over time — every session makes the brain smarter
- Zero-trust integrations — start read-only, add write access incrementally
- Build by concept, not by source — wiki articles are organized by topic
- The LLM writes the wiki, Jing curates and queries it
- Daily logs are the raw input; memory.md is the distilled output
