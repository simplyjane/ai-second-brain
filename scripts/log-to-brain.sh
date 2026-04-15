#!/bin/bash
# Log to Brain — appends a message to today's daily log
# Usage: ./log-to-brain.sh "category" "content"
# Example: ./log-to-brain.sh "decision" "Chose PostgreSQL over SQLite for production"

BRAIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$BRAIN_DIR/daily-logs/$TODAY.md"
TIMESTAMP=$(date +%H:%M)
CATEGORY="${1:-note}"
CONTENT="${2}"

if [ -z "$CONTENT" ]; then
    echo "Usage: log-to-brain.sh <category> <content>"
    echo "Categories: decision, lesson, insight, todo, note"
    exit 1
fi

# Create daily log header if file doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    cat > "$LOG_FILE" << EOF
# Daily Log: $TODAY

EOF
fi

# Append the log entry
cat >> "$LOG_FILE" << EOF
- **[$TIMESTAMP] $CATEGORY:** $CONTENT
EOF
