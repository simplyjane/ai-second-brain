#!/usr/bin/env python3
"""
Morning Briefing Generator — creates a daily briefing with news + plan.

Reads tracked topics, searches for news, pulls open todos from yesterday,
and generates a briefing file that session-start displays.

Usage:
    python3 morning_briefing.py                # Generate today's briefing
    python3 morning_briefing.py --dry-run      # Preview without writing
    python3 morning_briefing.py --no-news      # Skip news, just update plan

Requires: claude CLI (for news synthesis)
"""

import subprocess
import sys
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

BRAIN_DIR = Path.home() / "Documents" / "JingAIJourney" / "ai-second-brain"
TOPICS_FILE = BRAIN_DIR / "memory" / "topics.md"
PLAN_FILE = BRAIN_DIR / "memory" / "plan.md"
MEMORY_FILE = BRAIN_DIR / "memory" / "memory.md"
LOGS_DIR = BRAIN_DIR / "daily-logs"
BRIEFINGS_DIR = BRAIN_DIR / "briefings"
SCRIPTS_DIR = BRAIN_DIR / "scripts"

TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def ensure_dirs():
    BRIEFINGS_DIR.mkdir(exist_ok=True)


def parse_topics():
    """Extract search queries from topics.md."""
    if not TOPICS_FILE.exists():
        return []

    content = TOPICS_FILE.read_text(encoding="utf-8")
    queries = []

    # Extract items from bullet lists (- item)
    in_custom = False
    for line in content.split("\n"):
        line = line.strip()

        if "## Custom Searches" in line:
            in_custom = True
            continue

        if in_custom and line.startswith("- "):
            # Custom search queries — use verbatim
            query = line[2:].strip().strip('"')
            if query:
                queries.append(query)
        elif line.startswith("- ") and not line.startswith("- ("):
            # Regular topic — convert to search query
            # Strip markdown links and formatting
            topic = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line[2:])
            topic = re.sub(r'[*_]', '', topic)
            # Take just the main topic before any dash explanation
            topic = topic.split("—")[0].split("–")[0].strip()
            if topic and len(topic) > 2:
                queries.append(topic)

    return queries


def get_yesterday_open_items():
    """Extract unfinished todos from yesterday's daily log."""
    log_file = LOGS_DIR / f"{YESTERDAY}.md"
    if not log_file.exists():
        return []

    content = log_file.read_text(encoding="utf-8")
    open_items = []

    for line in content.split("\n"):
        stripped = line.strip()
        # Find unchecked todos
        if stripped.startswith("- [ ]"):
            open_items.append(stripped)
        # Find todo-category log entries
        if "**todo:**" in stripped.lower():
            # Extract the todo content
            match = re.search(r'\*\*.*?todo.*?\*\*:?\s*(.*)', stripped, re.IGNORECASE)
            if match:
                item = match.group(1).strip()
                if item:
                    open_items.append(f"- [ ] {item}")

    return open_items


def get_yesterday_summary():
    """Get a brief summary of yesterday's log for context."""
    log_file = LOGS_DIR / f"{YESTERDAY}.md"
    if not log_file.exists():
        return None

    content = log_file.read_text(encoding="utf-8")
    # Look for session summaries
    summaries = []
    for line in content.split("\n"):
        if "session-summary" in line.lower() or "decision" in line.lower():
            summaries.append(line.strip())

    return summaries if summaries else None


def search_news(queries, max_per_query=3):
    """Use Claude CLI to search and summarize news for each topic."""
    if not queries:
        return "No topics configured. Edit memory/topics.md to add topics.\n"

    # Build a single prompt with all queries for efficiency
    query_list = "\n".join(f"  {i+1}. {q}" for i, q in enumerate(queries[:8]))  # Cap at 8 to avoid timeout

    prompt = f"""You are a news briefing agent. Search the web for the latest updates on these topics and create a concise briefing.

Topics to search:
{query_list}

For each topic:
1. Find the most important development from the last 24-48 hours
2. Write 1-2 sentences summarizing what happened
3. Note why it matters

Format your output as:

### [Topic Name]
[1-2 sentence summary of the latest news/development]
**Why it matters:** [one sentence]

If there's nothing new on a topic in the last 48 hours, skip it entirely — don't say "no news found."

Keep the entire briefing under 500 words. Be direct, no fluff."""

    try:
        result = subprocess.run(
            ["claude", "-p", "--allowedTools", "WebSearch", "--model", "sonnet", prompt],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(BRAIN_DIR)
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return "News search unavailable — Claude CLI returned no results.\n"
    except FileNotFoundError:
        return "News search unavailable — Claude CLI not found.\n"
    except subprocess.TimeoutExpired:
        return "News search timed out.\n"


def generate_plan(open_items, yesterday_summary):
    """Generate today's plan section."""
    lines = []
    lines.append(f"## Today: {TODAY}")
    lines.append("")

    lines.append("### Priorities")
    if open_items:
        lines.append("> Carried forward from yesterday:")
        for item in open_items:
            lines.append(item)
    else:
        lines.append("- [ ] (add your priorities for today)")
    lines.append("")

    if yesterday_summary:
        lines.append("### Yesterday's Key Moments")
        for item in yesterday_summary[:5]:
            lines.append(f"  {item}")
        lines.append("")

    lines.append("### Notes")
    lines.append("> Add quick thoughts or context here.")
    lines.append("")

    return "\n".join(lines)


def generate_briefing(news_content, plan_content):
    """Assemble the full morning briefing."""
    lines = []
    lines.append(f"# Morning Briefing: {TODAY}")
    lines.append(f"> Generated at {datetime.now().strftime('%H:%M')} by your AI Second Brain")
    lines.append("")

    lines.append("---")
    lines.append("## Daily Plan")
    lines.append("")
    lines.append(plan_content)

    lines.append("---")
    lines.append("## News & Updates")
    lines.append("")
    lines.append(news_content)
    lines.append("")

    lines.append("---")
    lines.append(f"*Edit memory/topics.md to change tracked topics. Edit memory/plan.md to adjust priorities.*")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate morning briefing")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--no-news", action="store_true", help="Skip news search, just update plan")
    args = parser.parse_args()

    print(f"Morning Briefing Generator — {TODAY}")
    ensure_dirs()

    # 1. Get open items from yesterday
    print("Checking yesterday's open items...")
    open_items = get_yesterday_open_items()
    yesterday_summary = get_yesterday_summary()
    print(f"  Found {len(open_items)} open items")

    # 2. Generate plan
    print("Generating today's plan...")
    plan_content = generate_plan(open_items, yesterday_summary)

    # 3. Search news (unless --no-news)
    if args.no_news:
        news_content = "*News skipped (--no-news flag)*"
    else:
        print("Searching for news on tracked topics...")
        queries = parse_topics()
        print(f"  {len(queries)} search queries from topics.md")
        news_content = search_news(queries)

    # 4. Assemble briefing
    briefing = generate_briefing(news_content, plan_content)

    if args.dry_run:
        print("\n--- DRY RUN ---")
        print(briefing)
        return

    # 5. Write briefing file
    briefing_file = BRIEFINGS_DIR / f"{TODAY}.md"
    briefing_file.write_text(briefing, encoding="utf-8")
    print(f"Briefing saved: {briefing_file}")

    # 6. Update plan.md with today's plan
    plan_header = "# Daily Plan\n\n> Your priorities for today. Updated each morning by the heartbeat.\n> Unfinished items carry forward automatically. Edit freely.\n\n"
    PLAN_FILE.write_text(plan_header + plan_content, encoding="utf-8")
    print(f"Plan updated: {PLAN_FILE}")

    # 7. Log it + Caicai XP
    subprocess.run(
        ["bash", str(SCRIPTS_DIR / "log-to-brain.sh"), "system",
         f"Morning briefing generated. {len(open_items)} items carried forward."],
        capture_output=True
    )
    subprocess.run(
        ["python3", str(SCRIPTS_DIR / "caicai_engine.py"), "xp", "briefing_generated"],
        capture_output=True
    )

    print("Done.")


if __name__ == "__main__":
    main()
