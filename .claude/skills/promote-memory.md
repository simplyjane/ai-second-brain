# Promote Memory

Reviews daily logs and promotes key insights to the persistent memory layer.

## When to use

- When Jing says "promote", "update memory", or "what did we learn today"
- At the end of a productive session when important decisions were made
- Can be run as a daily cron job

## Instructions

1. **Read** all daily logs from the past 7 days in `daily-logs/`
2. **Read** current `memory/memory.md` and `memory/user.md`
3. **Extract** from the logs:
   - Key decisions made (with reasoning)
   - Lessons learned (especially from mistakes)
   - New facts about Jing's preferences, tools, or workflows
   - New people, projects, or relationships mentioned
   - Patterns spotted across multiple days
4. **Check for duplicates** — don't promote something already in memory
5. **Update** `memory/memory.md` with new entries under the appropriate section
6. **Update** `memory/user.md` if new preferences or profile info was learned
7. **Report** what was promoted and why

## Promotion Criteria

Only promote things that are:
- **Reusable** — will be relevant in future sessions
- **Non-obvious** — can't be derived by re-reading the code or project
- **Stable** — not a temporary state that'll change tomorrow

Do NOT promote:
- Debugging steps or temporary fixes
- File paths or code structure (read the repo instead)
- Things already documented in project files
- Ephemeral conversation details

## Format for Memory Entries

```markdown
- **[Category]:** [What was learned/decided] — [Why it matters] (promoted from [date])
```
