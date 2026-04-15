#!/bin/bash
# Session Start Hook — loads memory layer into Claude Code context
# Triggered at the start of every Claude Code session

BRAIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== AI SECOND BRAIN — CONTEXT LOADED ==="
echo ""
echo "--- SOUL ---"
cat "$BRAIN_DIR/memory/soul.md"
echo ""
echo "--- USER PROFILE ---"
cat "$BRAIN_DIR/memory/user.md"
echo ""
echo "--- PERSISTENT MEMORY ---"
cat "$BRAIN_DIR/memory/memory.md"
echo ""

# Show today's morning briefing if it exists
TODAY=$(date +%Y-%m-%d)
if [ -f "$BRAIN_DIR/briefings/$TODAY.md" ]; then
    echo "--- MORNING BRIEFING ---"
    cat "$BRAIN_DIR/briefings/$TODAY.md"
    echo ""
elif [ -f "$BRAIN_DIR/memory/plan.md" ]; then
    echo "--- TODAY'S PLAN ---"
    cat "$BRAIN_DIR/memory/plan.md"
    echo ""
fi

# Load today's log if it exists (resume context from earlier today)
if [ -f "$BRAIN_DIR/daily-logs/$TODAY.md" ]; then
    echo "--- TODAY'S LOG (resuming) ---"
    # Only show the last 50 lines to avoid context bloat
    tail -50 "$BRAIN_DIR/daily-logs/$TODAY.md"
    echo ""
fi

# Get Caicai's level for ASCII art
LEVEL=$(python3 "$BRAIN_DIR/scripts/caicai_engine.py" status 2>/dev/null | head -1 | grep -o 'Level [0-9]' | grep -o '[0-9]')
LEVEL=${LEVEL:-1}

case $LEVEL in
  1)
    cat << 'ART'

    /\_/\
   ( o.o )  ~
    > ^ <
     |_|
ART
    ;;
  2)
    cat << 'ART'

    /\_/\
   ( o.o )
    > ^ <
   /|   |\
  (_|   |_)
ART
    ;;
  3)
    cat << 'ART'

    /\_/\
   ( -.- )  ⌐■-■
    > ^ <
   /|   |\
  (_|   |_)
ART
    ;;
  4)
    cat << 'ART'

    /\_/\  📖
   ( ^.^ )
    > ^ <
   /|   |\
  (_|   |_)
ART
    ;;
  5)
    cat << 'ART'

   ✨/\_/\✨
    ( ◉.◉ )  🧠
     > ^ <
    /|   |\
   (_|   |_)
ART
    ;;
esac

# Smart greeting from Caicai engine
GREETING=$(python3 "$BRAIN_DIR/scripts/caicai_engine.py" greeting 2>/dev/null)
if [ -n "$GREETING" ]; then
    echo "$GREETING"
else
    echo "  Caicai: miao~ Brain online!"
fi
echo ""
echo "=== BRAIN READY — $(date +%H:%M) ==="
