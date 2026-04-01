#!/bin/bash
# .claude/hooks/context-reminder.sh
# Fires on Notification events
# Reads the notification from stdin and reminds about compaction

INPUT=$(cat)

# Check if the notification mentions context or auto-compact
if echo "$INPUT" | grep -qi "context\|compact\|token"; then
    echo "⚠️  Context reminder: Consider running /compact or committing and starting a fresh session."
fi