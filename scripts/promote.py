#!/usr/bin/env python3
"""
Automated Memory Promotion — reads daily logs and promotes key insights to memory.md.
Uses Claude Agent SDK to invoke Claude programmatically.

Usage:
    python3 promote.py                  # Promote from last 7 days of logs
    python3 promote.py --days 3         # Promote from last 3 days
    python3 promote.py --dry-run        # Show what would be promoted without writing

Requirements:
    pip install claude-agent-sdk
"""

import subprocess
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

BRAIN_DIR = Path.home() / "Documents" / "JingAIJourney" / "ai-second-brain"
LOGS_DIR = BRAIN_DIR / "daily-logs"
MEMORY_FILE = BRAIN_DIR / "memory" / "memory.md"
USER_FILE = BRAIN_DIR / "memory" / "user.md"


def get_recent_logs(days=7):
    """Read daily logs from the last N days."""
    logs = []
    today = datetime.now()

    for i in range(days):
        date = today - timedelta(days=i)
        log_file = LOGS_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8")
            if content.strip():
                logs.append((date.strftime("%Y-%m-%d"), content))

    return logs


def build_promotion_prompt(logs, current_memory, current_user):
    """Build the prompt for Claude to analyze and promote insights."""
    log_text = ""
    for date, content in logs:
        log_text += f"\n--- {date} ---\n{content}\n"

    return f"""You are the AI Second Brain's memory promotion agent. Your job is to review recent daily logs and extract insights worth promoting to persistent memory.

## Current Memory (memory.md)
{current_memory}

## Current User Profile (user.md)
{current_user}

## Recent Daily Logs (last {len(logs)} days)
{log_text}

## Your Task

1. Read the daily logs carefully.
2. Identify entries worth promoting:
   - Key decisions with reasoning
   - Lessons learned (especially from mistakes)
   - New facts about the user's preferences or workflows
   - Patterns spotted across multiple days
   - New people, projects, or tools mentioned
3. Check for duplicates — skip anything already in memory.md or user.md.
4. Output ONLY the changes to make, in this exact format:

### MEMORY_ADDITIONS
(Lines to append to the appropriate section of memory.md. Include the section header they belong under.)

### USER_ADDITIONS
(Lines to append to the appropriate section of user.md. Include the section header they belong under.)

### NOTHING_TO_PROMOTE
(If there's nothing new worth promoting, say so and explain why.)

Rules:
- Only promote things that are REUSABLE in future sessions
- Include the date promoted: (promoted from YYYY-MM-DD)
- Be specific — include the WHY, not just the what
- Don't promote debugging steps, file paths, or code structure
- Don't duplicate what's already in memory"""


def promote_with_claude_cli(prompt, dry_run=False):
    """Use Claude CLI to run the promotion."""
    if dry_run:
        print("\n--- DRY RUN: Would send this prompt to Claude ---")
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        return None

    try:
        result = subprocess.run(
            ["claude", "-p", "--allowedTools", "Read,Edit,Write", "--model", "sonnet", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(BRAIN_DIR)
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: 'claude' CLI not found. Install Claude Code first.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: Claude CLI timed out after 120 seconds.")
        sys.exit(1)


def promote_with_agent_sdk(prompt, dry_run=False):
    """Use Claude Agent SDK for programmatic promotion."""
    if dry_run:
        print("\n--- DRY RUN: Would send this prompt to Agent SDK ---")
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        return None

    try:
        from claude_agent_sdk import AgentClient
        client = AgentClient()
        response = client.run(
            prompt=prompt,
            working_directory=str(BRAIN_DIR),
            tools=["Read", "Edit", "Write"]
        )
        return response.text
    except ImportError:
        print("Agent SDK not installed. Falling back to Claude CLI...")
        return promote_with_claude_cli(prompt, dry_run)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Promote insights from daily logs to memory")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without writing")
    parser.add_argument("--use-sdk", action="store_true", help="Use Agent SDK instead of CLI")
    args = parser.parse_args()

    print(f"Memory Promotion — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Looking back {args.days} days\n")

    # Gather inputs
    logs = get_recent_logs(args.days)
    if not logs:
        print("No daily logs found. Nothing to promote.")
        return

    print(f"Found {len(logs)} daily logs:")
    for date, content in logs:
        lines = len(content.strip().split("\n"))
        print(f"  {date}: {lines} lines")

    current_memory = MEMORY_FILE.read_text(encoding="utf-8") if MEMORY_FILE.exists() else ""
    current_user = USER_FILE.read_text(encoding="utf-8") if USER_FILE.exists() else ""

    # Build and run promotion
    prompt = build_promotion_prompt(logs, current_memory, current_user)

    print(f"\nRunning promotion{'  (dry run)' if args.dry_run else ''}...")

    if args.use_sdk:
        result = promote_with_agent_sdk(prompt, args.dry_run)
    else:
        result = promote_with_claude_cli(prompt, args.dry_run)

    if result:
        print("\n--- Promotion Results ---")
        print(result)

        # Log the promotion
        log_script = BRAIN_DIR / "scripts" / "log-to-brain.sh"
        subprocess.run(
            ["bash", str(log_script), "system", f"Memory promotion ran. Reviewed {len(logs)} daily logs."],
            capture_output=True
        )

    print("\nDone.")


if __name__ == "__main__":
    main()
