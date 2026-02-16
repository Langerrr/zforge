#!/bin/bash
# safe-run.sh — mutex wrapper for any command
# Prevents concurrent execution of commands sharing the same lock name.
# Usage: safe-run.sh <lock_name> <command...>
#   e.g., safe-run.sh npm npm install
#         safe-run.sh pip pip install -r requirements.txt
#         safe-run.sh cargo cargo build

set -euo pipefail

LOCK_NAME="${1:?Usage: safe-run.sh <lock_name> <command...>}"
shift

if [ $# -eq 0 ]; then
    echo "ERROR: No command provided" >&2
    echo "Usage: safe-run.sh <lock_name> <command...>" >&2
    exit 1
fi

LOCK_DIR="/tmp/safe-run-${LOCK_NAME}-lock"
WAIT_INTERVAL=5
MAX_WAIT=300  # 5 minutes

elapsed=0
while ! mkdir "$LOCK_DIR" 2>/dev/null; do
    echo "${LOCK_NAME} locked by another agent, waiting... (${elapsed}s)" >&2
    sleep "$WAIT_INTERVAL"
    elapsed=$((elapsed + WAIT_INTERVAL))
    if [ "$elapsed" -ge "$MAX_WAIT" ]; then
        echo "ERROR: ${LOCK_NAME} lock timeout after ${MAX_WAIT}s" >&2
        exit 1
    fi
done

# Auto-release lock on exit (success or failure)
trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT

"$@"
