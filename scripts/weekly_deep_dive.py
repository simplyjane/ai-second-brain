#!/usr/bin/env python3
"""
Weekly Deep Dive — runs last30days on top topics marked [deep] for social media research.
Searches Reddit, X, YouTube, TikTok, Instagram, HN, Polymarket.

Usage:
    python3 weekly_deep_dive.py              # Run deep dive on all [deep] topics
    python3 weekly_deep_dive.py --dry-run    # Preview which topics would be researched
    python3 weekly_deep_dive.py --days 7     # Look back 7 days instead of default

Runs weekly via launchd (Sunday 9pm).
"""

import subprocess
import sys
import re
import os
from datetime import datetime
from pathlib import Path

BRAIN_DIR = Path.home() / "Documents" / "JingAIJourney" / "ai-second-brain"
TOPICS_FILE = BRAIN_DIR / "memory" / "topics.md"
BRIEFINGS_DIR = BRAIN_DIR / "briefings"
SCRIPTS_DIR = BRAIN_DIR / "scripts"

# Find last30days script
LAST30DAYS_CANDIDATES = [
    Path.home() / ".claude" / "plugins" / "marketplaces" / "last30days-skill" / "scripts" / "last30days.py",
    Path.home() / ".claude" / "skills" / "last30days" / "scripts" / "last30days.py",
]

TODAY = datetime.now().strftime("%Y-%m-%d")


def find_last30days():
    """Locate the last30days.py script."""
    for path in LAST30DAYS_CANDIDATES:
        if path.exists():
            return path
    return None


def parse_deep_topics():
    """Extract topics marked with [deep] from topics.md."""
    if not TOPICS_FILE.exists():
        return []

    content = TOPICS_FILE.read_text(encoding="utf-8")
    topics = []

    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("- ") and "[deep]" in line.lower():
            # Extract topic name, strip [deep] tag and markdown
            topic = line[2:]
            topic = re.sub(r'`?\[deep\]`?', '', topic, flags=re.IGNORECASE).strip()
            topic = re.sub(r'\*\*([^*]+)\*\*', r'\1', topic)  # strip bold
            # Take main topic before explanation dash
            topic = topic.split("—")[0].split("–")[0].strip()
            topic = topic.rstrip(" -")
            if topic and len(topic) > 2:
                topics.append(topic)

    return topics


def run_last30days(topic, script_path, days=7):
    """Run last30days.py for a single topic and return the output."""
    cmd = [
        "python3", str(script_path),
        topic,
        "--emit=compact",
        "--no-native-web",
        f"--save-dir={BRIEFINGS_DIR / 'weekly'}",
        f"--days={days}"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(BRAIN_DIR)
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"Timeout researching: {topic}\n"
    except Exception as e:
        return f"Error researching {topic}: {e}\n"


def synthesize_results(topic_results):
    """Use Claude CLI to synthesize all research into a weekly digest."""
    combined = ""
    for topic, raw_output in topic_results:
        combined += f"\n\n=== RESEARCH: {topic} ===\n{raw_output[:3000]}"

    prompt = f"""You are a weekly digest agent for an AI Second Brain. You've just researched these topics across Reddit, X/Twitter, YouTube, TikTok, Instagram, HN, and Polymarket.

{combined}

Create a weekly digest with these sections:

## Top Stories This Week
(3-5 biggest developments across all topics, with source attribution like "per @handle" or "per r/subreddit")

## Topic Summaries
(For each topic: 2-3 sentence summary of what's new, with citations)

## Trending Voices
(Notable people/accounts driving conversation this week)

## Worth Watching
(1-2 emerging trends or predictions that aren't mainstream yet)

Be direct, cite sources, no fluff. Under 800 words total."""

    try:
        result = subprocess.run(
            ["claude", "-p", "--allowedTools", "WebSearch", "--model", "sonnet", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(BRAIN_DIR)
        )
        return result.stdout if result.returncode == 0 else "Synthesis unavailable.\n"
    except Exception:
        return "Synthesis unavailable.\n"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Weekly social media deep dive")
    parser.add_argument("--dry-run", action="store_true", help="Preview topics without researching")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    args = parser.parse_args()

    print(f"Weekly Deep Dive — {TODAY}")

    # Find last30days
    script_path = find_last30days()
    if not script_path and not args.dry_run:
        print("Error: last30days.py not found. Is the skill installed?")
        sys.exit(1)

    # Parse topics
    topics = parse_deep_topics()
    if not topics:
        print("No topics marked [deep] in topics.md. Add `[deep]` to topics you want researched weekly.")
        return

    print(f"Found {len(topics)} deep-dive topics:")
    for t in topics:
        print(f"  - {t}")

    if args.dry_run:
        print("\nDry run — no research performed.")
        return

    # Create weekly briefing dir
    weekly_dir = BRIEFINGS_DIR / "weekly"
    weekly_dir.mkdir(parents=True, exist_ok=True)

    # Research each topic
    topic_results = []
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] Researching: {topic} (last {args.days} days)...")
        output = run_last30days(topic, script_path, args.days)
        topic_results.append((topic, output))
        print(f"  Done.")

    # Synthesize into digest
    print("\nSynthesizing weekly digest...")
    digest = synthesize_results(topic_results)

    # Write the weekly briefing
    briefing_file = BRIEFINGS_DIR / f"weekly-{TODAY}.md"
    header = f"""# Weekly Deep Dive: {TODAY}
> Social media research across Reddit, X, YouTube, TikTok, Instagram, HN, Polymarket
> Topics: {', '.join(topics)}

---

"""
    briefing_file.write_text(header + digest, encoding="utf-8")
    print(f"\nWeekly briefing saved: {briefing_file}")

    # Log it
    subprocess.run(
        ["bash", str(SCRIPTS_DIR / "log-to-brain.sh"), "system",
         f"Weekly deep dive complete. Researched {len(topics)} topics: {', '.join(topics)}"],
        capture_output=True
    )

    print("Done.")


if __name__ == "__main__":
    main()
