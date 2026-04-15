# Query Brain

Searches across the entire knowledge base and memory to answer Jing's questions.

## When to use

- When Jing asks a question that might be answered by the wiki or memory
- When Jing says "what do I know about...", "search my brain", or "find..."

## Instructions

1. **Check memory first** — Read `memory/memory.md` for relevant context
2. **Search the SQLite index** — Run the search script for fast full-text search:
   ```bash
   python3 scripts/search_brain.py "query terms" --json
   ```
   Filter by source if needed: `--source daily-log`, `--source wiki`, `--source memory`
   Filter by date: `--after 2026-04-01`
3. **Deep read** — For the top results, read the full files for richer context
4. **Search the wiki directly** — If SQLite has no results, read `knowledge/wiki/index.md` and scan articles
5. **Synthesize** — Combine findings from all sources into a direct answer
6. **Cite sources** — Reference which wiki article, memory entry, or daily log the info came from
7. **Flag gaps** — If the question can't be fully answered, say what's missing and suggest sources to add

**Important:** If the search index doesn't exist yet, run `python3 scripts/index_logs.py` first to build it.

## Answer Format

Lead with the answer. Then cite where it came from.

```
[Direct answer]

Sources from your brain:
- wiki/[article].md — [what it said]
- memory.md — [relevant entry]
- daily-logs/[date].md — [relevant conversation]

Gaps: [what's missing, if anything]
```

## Rules

- Never make up information — only answer from what's in the knowledge base
- If the brain doesn't have the answer, say so and offer to research it
- Prefer recent information over old (daily logs > old wiki articles)
- Cross-reference multiple sources when possible
- After searching, run: `python3 scripts/caicai_engine.py xp search_run`
