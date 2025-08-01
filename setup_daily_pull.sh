#!/bin/bash

# Script to set up a daily cron job that pulls this repository at midday (12:00 PM)

REPO_PATH="/home/tyler/programming/auto-water-purchase"
CRON_COMMAND="0 12 * * * cd $REPO_PATH && git pull origin main"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$REPO_PATH.*git pull"; then
    echo "Cron job for daily git pull already exists."
    echo "Current cron jobs:"
    crontab -l | grep "$REPO_PATH.*git pull"
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -
    echo "Cron job added successfully!"
    echo "The repository will be pulled daily at 12:00 PM (midday)."
    echo "Added cron job: $CRON_COMMAND"
fi

echo ""
echo "To verify the cron job was added, run: crontab -l"
echo "To remove this cron job later, run: crontab -e and delete the line containing '$REPO_PATH'"