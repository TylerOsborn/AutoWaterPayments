#!/bin/bash

# Setup script for cron job to run auto water purchase on first of every month at 00:01
# Run this script to add the cron job to your system

# Get the current directory (where the script is located)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Python script path
PYTHON_SCRIPT="$SCRIPT_DIR/auto_water_purchase.py"

# Log file path
LOG_FILE="$SCRIPT_DIR/cron.log"

# Cron job entry - runs at 00:01 on the first day of every month
CRON_ENTRY="1 0 1 * * cd $SCRIPT_DIR && source ./venv/bin/activate &&/usr/bin/python3 $PYTHON_SCRIPT >> $LOG_FILE 2>&1"

echo "Setting up cron job for auto water purchase..."
echo "Script location: $PYTHON_SCRIPT"
echo "Log file: $LOG_FILE"
echo ""

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job added successfully!"
    echo "The script will run automatically at 00:01 on the 1st of every month."
    echo ""
    echo "To view current cron jobs: crontab -l"
    echo "To remove this cron job: crontab -e (then delete the line)"
    echo ""
    echo "Note: Make sure your .env file is properly configured with all required variables."
else
    echo "❌ Failed to add cron job. Please check your crontab configuration."
    exit 1
fi
