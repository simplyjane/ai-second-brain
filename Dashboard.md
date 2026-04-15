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

## Caicai — Your Brain Companion

Click the black cat in the bottom-right corner to pet her!

**Levels** — Caicai grows as you use your brain:

| Level | Name | XP | Look | How to earn |
|---|---|---|---|---|
| 1 | Kitten | 0 | Tiny cat, big head | Just getting started |
| 2 | Cat | 50 | Full cat with tail | Add sources, compile wiki |
| 3 | Smart Cat | 150 | Cat with glasses | Keep promoting memory |
| 4 | Scholar Cat | 400 | Cat with glasses + book | Daily streaks, deep searches |
| 5 | Brain Cat | 1000 | Cat with glasses + brain + sparkles | Master your second brain |

**XP rewards:**
- Add a source: +10 | Compile wiki: +25 | Promote memory: +15
- Session start/end: +3/+5 | Search: +2 | Briefing: +8 | Pet click: +1

**Smart behavior:**
- Mood changes based on how recently you used the brain
- Greetings change by time of day and level
- Reminds you when memory needs promoting or wiki needs compiling
- Celebrates milestones (streaks, source counts, level-ups)

Check status anytime: `python3 scripts/caicai_engine.py status`
Open animation: [[pet/black-cat.html]]

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
