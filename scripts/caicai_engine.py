#!/usr/bin/env python3
"""
Caicai Engine — manages pet state, XP, levels, mood, and smart responses.

Usage:
    python3 caicai_engine.py xp <action>       # Award XP for an action
    python3 caicai_engine.py pet                # Record a pet/click
    python3 caicai_engine.py status             # Show current state
    python3 caicai_engine.py greeting           # Get a smart greeting for terminal
    python3 caicai_engine.py check              # Check brain health and return reminders

Actions that award XP:
    source_added, wiki_compiled, memory_promoted, session_start,
    session_end, search_run, briefing_generated, gap_found
"""

import json
import sys
import os
import glob
from datetime import datetime, timedelta
from pathlib import Path

BRAIN_DIR = Path.home() / "Documents" / "JingAIJourney" / "ai-second-brain"
STATE_FILE = BRAIN_DIR / "pet" / "caicai-state.json"

# ─── LEVEL SYSTEM ─────────────────────────────────────────────
LEVELS = [
    {"level": 1, "name": "Kitten",      "xp": 0,    "emoji": "🐱"},
    {"level": 2, "name": "Cat",          "xp": 50,   "emoji": "🐈"},
    {"level": 3, "name": "Smart Cat",    "xp": 150,  "emoji": "🐈‍⬛"},
    {"level": 4, "name": "Scholar Cat",  "xp": 400,  "emoji": "📚🐈‍⬛"},
    {"level": 5, "name": "Brain Cat",    "xp": 1000, "emoji": "🧠🐈‍⬛"},
]

# XP rewards per action
XP_TABLE = {
    "source_added":      10,
    "wiki_compiled":     25,
    "memory_promoted":   15,
    "session_start":     3,
    "session_end":       5,
    "search_run":        2,
    "briefing_generated": 8,
    "gap_found":         5,
    "pet":               1,
}

# ─── MILESTONES ───────────────────────────────────────────────
MILESTONES = [
    {"id": "first_source",    "check": lambda s: s["stats"]["sources_added"] >= 1,      "msg": "First source added! Caicai is learning~"},
    {"id": "first_compile",   "check": lambda s: s["stats"]["wikis_compiled"] >= 1,      "msg": "First wiki compiled! Knowledge is growing!"},
    {"id": "first_promote",   "check": lambda s: s["stats"]["memories_promoted"] >= 1,   "msg": "First memory promoted! Caicai remembers now~"},
    {"id": "10_sources",      "check": lambda s: s["stats"]["sources_added"] >= 10,      "msg": "10 sources! The knowledge base is getting serious!"},
    {"id": "5_compiles",      "check": lambda s: s["stats"]["wikis_compiled"] >= 5,      "msg": "5 compiles! The wiki is evolving~"},
    {"id": "7_day_streak",    "check": lambda s: s["streak_days"] >= 7,                  "msg": "7-day streak! Caicai is so proud of you!"},
    {"id": "30_day_streak",   "check": lambda s: s["streak_days"] >= 30,                 "msg": "30-day streak! You and Caicai are unstoppable!"},
    {"id": "100_pets",        "check": lambda s: s["total_pets"] >= 100,                 "msg": "100 pets! Caicai is the happiest cat~"},
    {"id": "50_sessions",     "check": lambda s: s["stats"]["sessions_completed"] >= 50, "msg": "50 sessions! Brain Cat status incoming!"},
    {"id": "level_2",         "check": lambda s: s["level"] >= 2,                        "msg": "Level 2 — Cat! Caicai grew up!"},
    {"id": "level_3",         "check": lambda s: s["level"] >= 3,                        "msg": "Level 3 — Smart Cat! Caicai wears glasses now~"},
    {"id": "level_4",         "check": lambda s: s["level"] >= 4,                        "msg": "Level 4 — Scholar Cat! Caicai reads books!"},
    {"id": "level_5",         "check": lambda s: s["level"] >= 5,                        "msg": "MAX LEVEL — Brain Cat! Caicai has ascended!"},
]

# ─── MOOD SYSTEM ──────────────────────────────────────────────
def calculate_mood(state):
    """Determine Caicai's mood based on brain activity."""
    now = datetime.now()
    last = state.get("last_session")

    if last:
        last_dt = datetime.fromisoformat(last)
        hours_since = (now - last_dt).total_seconds() / 3600

        if hours_since < 2:
            return "excited"      # just used
        elif hours_since < 8:
            return "happy"        # recent activity
        elif hours_since < 24:
            return "relaxed"      # today
        elif hours_since < 72:
            return "sleepy"       # been a while
        else:
            return "lonely"       # miss you
    return "curious"              # brand new


# ─── SMART GREETINGS ─────────────────────────────────────────
def get_greeting(state):
    """Generate a context-aware greeting."""
    import random
    now = datetime.now()
    hour = now.hour
    mood = state["mood"]
    level = state["level"]
    level_name = state["level_name"]
    streak = state["streak_days"]
    xp = state["xp"]

    # Time-based
    if hour < 12:
        time_greet = "Good morning"
    elif hour < 17:
        time_greet = "Good afternoon"
    else:
        time_greet = "Good evening"

    # Level-based flavor
    level_flavor = {
        1: "*tiny miao*",
        2: "miao~",
        3: "*adjusts glasses* miao!",
        4: "*looks up from book* miao~",
        5: "*radiates wisdom* ...miao.",
    }.get(level, "miao~")

    # Mood-based lines
    mood_lines = {
        "excited":  [f"{time_greet}! {level_flavor} Let's keep going!",
                     f"{level_flavor} I was just thinking about our wiki~",
                     f"Back so soon! {level_flavor} I love it!"],
        "happy":    [f"{time_greet}! {level_flavor} Ready when you are.",
                     f"{level_flavor} What are we learning today?",
                     f"{time_greet}~ Your brain is in good shape!"],
        "relaxed":  [f"{time_greet}. {level_flavor} Nice to see you.",
                     f"{level_flavor} *stretches* ...ready.",
                     f"Welcome back~ {level_flavor}"],
        "sleepy":   [f"*yawns* Oh, you're here! {level_flavor}",
                     f"Caicai was napping... {level_flavor} Let's go!",
                     f"*blinks awake* {time_greet}! Missed you~"],
        "lonely":   [f"Jing!! You're back! {level_flavor} I missed you!",
                     f"*runs to you* {level_flavor} It's been so long!",
                     f"Finally! {level_flavor} The brain was getting dusty~"],
        "curious":  [f"{time_greet}! {level_flavor} I'm Caicai, your new companion!",
                     f"Hi! {level_flavor} Let's build something amazing~"],
    }

    lines = mood_lines.get(mood, mood_lines["happy"])
    greeting = random.choice(lines)

    # Add streak mention
    if streak >= 7:
        greeting += f" ({streak}-day streak!)"

    # Next level hint
    next_level = None
    for lv in LEVELS:
        if lv["xp"] > xp:
            next_level = lv
            break
    if next_level:
        remaining = next_level["xp"] - xp
        greeting += f"\n  [{level_name} — {xp} XP, {remaining} to {next_level['name']}]"
    else:
        greeting += f"\n  [Brain Cat — MAX LEVEL — {xp} XP]"

    return greeting


# ─── HEALTH CHECK ─────────────────────────────────────────────
def check_brain_health(state):
    """Check brain state and return reminders."""
    reminders = []
    now = datetime.now()

    # Check last promotion
    logs_dir = BRAIN_DIR / "daily-logs"
    log_files = sorted(glob.glob(str(logs_dir / "*.md")))
    if log_files:
        latest_log = Path(log_files[-1]).stem
        try:
            log_date = datetime.strptime(latest_log, "%Y-%m-%d")
            days_since_log = (now - log_date).days
            if days_since_log > 3:
                reminders.append(f"No daily logs in {days_since_log} days — Caicai misses your conversations!")
        except ValueError:
            pass

    # Check wiki size
    wiki_dir = BRAIN_DIR / "knowledge" / "wiki"
    wiki_files = list(wiki_dir.glob("*.md")) if wiki_dir.exists() else []
    wiki_count = len([f for f in wiki_files if f.name != "index.md"])

    raw_dir = BRAIN_DIR / "knowledge" / "raw"
    raw_files = list(raw_dir.glob("*")) if raw_dir.exists() else []
    raw_count = len(raw_files)

    if raw_count > 0 and wiki_count == 0:
        reminders.append(f"You have {raw_count} raw sources but no wiki! Say 'compile' to build it~")
    elif raw_count > wiki_count * 3:
        reminders.append(f"{raw_count} raw sources, only {wiki_count} wiki articles — time to recompile?")

    # Check memory staleness
    memory_file = BRAIN_DIR / "memory" / "memory.md"
    if memory_file.exists():
        mtime = datetime.fromtimestamp(os.path.getmtime(memory_file))
        days_since_promote = (now - mtime).days
        if days_since_promote > 3:
            reminders.append(f"Memory hasn't been promoted in {days_since_promote} days — say 'promote'!")

    # Positive reinforcement
    if not reminders:
        if state["streak_days"] >= 7:
            reminders.append(f"Everything looks great! {state['streak_days']}-day streak going strong~")
        else:
            reminders.append("Brain is healthy! Keep it up~")

    return reminders


# ─── STATE MANAGEMENT ─────────────────────────────────────────
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {
        "xp": 0, "level": 1, "level_name": "Kitten",
        "total_pets": 0, "streak_days": 0,
        "last_session": None, "last_pet": None,
        "mood": "curious", "milestones": [],
        "stats": {
            "sources_added": 0, "wikis_compiled": 0,
            "memories_promoted": 0, "sessions_completed": 0,
            "searches_run": 0, "briefings_generated": 0
        },
        "created": datetime.now().strftime("%Y-%m-%d")
    }


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def update_level(state):
    """Recalculate level based on XP."""
    for lv in reversed(LEVELS):
        if state["xp"] >= lv["xp"]:
            state["level"] = lv["level"]
            state["level_name"] = lv["name"]
            return


def update_streak(state):
    """Update consecutive day streak."""
    today = datetime.now().strftime("%Y-%m-%d")
    last = state.get("last_session")

    if last:
        last_date = last[:10]  # YYYY-MM-DD
        if last_date == today:
            return  # already counted today
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if last_date == yesterday:
            state["streak_days"] += 1
        else:
            state["streak_days"] = 1
    else:
        state["streak_days"] = 1


def check_milestones(state):
    """Check for new milestones and return any new ones."""
    new_milestones = []
    for m in MILESTONES:
        if m["id"] not in state["milestones"] and m["check"](state):
            state["milestones"].append(m["id"])
            new_milestones.append(m["msg"])
    return new_milestones


def award_xp(state, action):
    """Award XP for an action and update state."""
    xp = XP_TABLE.get(action, 0)
    if xp == 0:
        return []

    state["xp"] += xp

    # Update stats
    stat_map = {
        "source_added": "sources_added",
        "wiki_compiled": "wikis_compiled",
        "memory_promoted": "memories_promoted",
        "session_start": "sessions_completed",
        "session_end": "sessions_completed",
        "search_run": "searches_run",
        "briefing_generated": "briefings_generated",
    }
    stat_key = stat_map.get(action)
    if stat_key and action != "session_start":  # don't double count sessions
        state["stats"][stat_key] = state["stats"].get(stat_key, 0) + 1

    old_level = state["level"]
    update_level(state)

    # Check milestones
    new_milestones = check_milestones(state)

    if state["level"] > old_level:
        new_milestones.insert(0, f"LEVEL UP! Caicai is now a {state['level_name']}!")

    return new_milestones


# ─── CLI ──────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: caicai_engine.py <command> [args]")
        print("Commands: xp <action>, pet, status, greeting, check")
        sys.exit(1)

    cmd = sys.argv[1]
    state = load_state()

    if cmd == "xp" and len(sys.argv) >= 3:
        action = sys.argv[2]
        update_streak(state)
        state["last_session"] = datetime.now().isoformat()
        state["mood"] = calculate_mood(state)
        milestones = award_xp(state, action)
        save_state(state)

        if milestones:
            for m in milestones:
                print(f"  ★ {m}")
        print(f"  +{XP_TABLE.get(action, 0)} XP ({state['xp']} total)")

    elif cmd == "pet":
        state["total_pets"] = state.get("total_pets", 0) + 1
        state["last_pet"] = datetime.now().isoformat()
        state["xp"] += 1
        update_level(state)
        milestones = check_milestones(state)
        save_state(state)

        if milestones:
            for m in milestones:
                print(m)

    elif cmd == "status":
        state["mood"] = calculate_mood(state)
        lv = LEVELS[state["level"] - 1]
        print(f"  {lv['emoji']} Caicai — {state['level_name']} (Level {state['level']})")
        print(f"  XP: {state['xp']} | Pets: {state['total_pets']} | Streak: {state['streak_days']} days")
        print(f"  Mood: {state['mood']}")
        print(f"  Sources: {state['stats']['sources_added']} | Compiles: {state['stats']['wikis_compiled']} | Promotes: {state['stats']['memories_promoted']}")
        print(f"  Sessions: {state['stats']['sessions_completed']} | Searches: {state['stats']['searches_run']}")
        next_lv = None
        for l in LEVELS:
            if l["xp"] > state["xp"]:
                next_lv = l
                break
        if next_lv:
            print(f"  Next: {next_lv['name']} at {next_lv['xp']} XP ({next_lv['xp'] - state['xp']} to go)")
        else:
            print(f"  MAX LEVEL!")
        save_state(state)

    elif cmd == "greeting":
        update_streak(state)
        state["last_session"] = datetime.now().isoformat()
        state["mood"] = calculate_mood(state)
        milestones = award_xp(state, "session_start")
        save_state(state)

        greeting = get_greeting(state)
        print(greeting)

        if milestones:
            for m in milestones:
                print(f"  ★ {m}")

        # Health reminders
        reminders = check_brain_health(state)
        for r in reminders:
            print(f"  → {r}")

    elif cmd == "check":
        state["mood"] = calculate_mood(state)
        reminders = check_brain_health(state)
        for r in reminders:
            print(f"  → {r}")
        save_state(state)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
