#!/bin/bash
# Pre-Compact Hook — saves context before memory compaction
# Triggered when Claude Code conversation is about to be compacted (long conversation)

BRAIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$BRAIN_DIR/daily-logs/$TODAY.md"
TIMESTAMP=$(date +%H:%M)

# Create daily log header if file doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    echo "# Daily Log: $TODAY" > "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

# Append compaction marker
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "## Context compacted at $TIMESTAMP" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "> Conversation was compacted. Key context from before this point should be in memory." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
