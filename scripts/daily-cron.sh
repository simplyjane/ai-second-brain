#!/bin/bash
# Daily Brain Maintenance — run via cron once per day
# Indexes new content and promotes insights from daily logs to memory
#
# Suggested cron schedule (runs at 11pm daily):
#   0 23 * * * bash ~/Documents/JingAIJourney/ai-second-brain/scripts/daily-cron.sh >> ~/Documents/JingAIJourney/ai-second-brain/logs/cron.log 2>&1
#
# To install:
#   crontab -e
#   (paste the line above)

BRAIN_DIR="$HOME/Documents/JingAIJourney/ai-second-brain"
SCRIPTS_DIR="$BRAIN_DIR/scripts"
LOG_DIR="$BRAIN_DIR/logs"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# Ensure log directory exists
mkdir -p "$LOG_DIR"

echo "=== Daily Brain Maintenance: $TIMESTAMP ==="

# Step 1: Index new content into SQLite
echo ""
echo "[1/3] Indexing new content..."
python3 "$SCRIPTS_DIR/index_logs.py"

# Step 2: Run memory promotion
echo ""
echo "[2/3] Promoting insights from daily logs..."
python3 "$SCRIPTS_DIR/promote.py" --days 3

# Step 3: Log completion
echo ""
echo "[3/3] Logging maintenance run..."
bash "$SCRIPTS_DIR/log-to-brain.sh" "system" "Daily maintenance complete: indexed content, promoted memory from last 3 days."

echo ""
echo "=== Maintenance complete: $(date +"%H:%M") ==="
