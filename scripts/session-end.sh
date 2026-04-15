#!/bin/bash
# Session End Hook — saves conversation summary to daily log
# Triggered when Claude Code session ends or conversation is stopped

BRAIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$BRAIN_DIR/daily-logs/$TODAY.md"
TIMESTAMP=$(date +%H:%M)

# Create daily log header if file doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    echo "# Daily Log: $TODAY" > "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

# Append session end marker
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "## Session ended at $TIMESTAMP" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "> Session context was saved. Review and promote key insights to memory.md." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Award Caicai XP
python3 "$BRAIN_DIR/scripts/caicai_engine.py" xp session_end 2>/dev/null
