# AI Second Brain

## Quick Access

| | |
|---|---|
| [[memory/plan\|Today's Plan]] | [[memory/topics\|Tracked Topics]] |
| [[memory/memory\|Memory]] | [[memory/user\|User Profile]] |
| [[memory/soul\|Soul]] | [[knowledge/wiki/index\|Wiki Index]] |

## Daily Logs

[[daily-logs/]] — raw conversation logs, one per day

## Briefings

[[briefings/]] — morning briefings with news + plan

## Knowledge Base

- **[[knowledge/wiki/index\|Wiki]]** — compiled articles organized by concept
- **Raw sources** — `knowledge/raw/` — drop articles, transcripts, notes here, then say "compile" in Claude Code

## Automation Schedule

| Job | When | What it does |
|---|---|---|
| Morning Briefing | 11:00am daily | Searches web for news on [[memory/topics\|tracked topics]], generates briefing |
| Maintenance | 5:00pm daily | Indexes new content into SQLite, promotes daily log insights to memory |
| Weekly Deep Dive | Saturday 4:30pm | Scans Reddit, X, YouTube, TikTok, Instagram, HN for `[deep]` topics |

> Powered by launchd — runs on wake-up if Mac was asleep. Logs in `logs/`.

## How It Works

```
You add sources → Claude compiles wiki → You query & browse
       ↓                                        ↓
  daily-logs/ ← conversations → memory.md (promoted insights)
       ↓                           ↓
  morning briefing ← topics.md → loaded into next session
```

## Graph View

Open the graph view (Cmd+G) to see how all your knowledge connects. Colors:
- **Red** — Memory (soul, user, memory)
- **Green** — Wiki articles
- **Gray** — Raw sources
- **Blue** — Daily logs
- **Orange** — Briefings
