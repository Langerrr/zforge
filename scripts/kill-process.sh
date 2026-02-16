#!/bin/bash
# kill-process.sh — Kill a process by PID or PID file
# Usage: kill-process.sh <pid|pid_file> [signal]
#
# Arguments:
#   pid|pid_file  A numeric PID or path to a file containing a PID
#   signal        (Optional) Signal to send, default: TERM then KILL after 5s

set -euo pipefail

TARGET="${1:?Usage: kill-process.sh <pid|pid_file> [signal]}"
SIGNAL="${2:-}"

PID_FILE=""

if [[ "$TARGET" =~ ^[0-9]+$ ]]; then
    PID="$TARGET"
else
    PID_FILE="$TARGET"
    if [ ! -f "$PID_FILE" ]; then
        echo "PID file not found: $PID_FILE"
        exit 0
    fi
    PID="$(cat "$PID_FILE" 2>/dev/null | tr -d '[:space:]')"
    if [ -z "$PID" ] || ! [[ "$PID" =~ ^[0-9]+$ ]]; then
        echo "Invalid PID in file: $PID_FILE"
        rm -f "$PID_FILE"
        exit 0
    fi
fi

if ! kill -0 "$PID" 2>/dev/null; then
    echo "Process $PID is not running"
    [ -n "$PID_FILE" ] && rm -f "$PID_FILE"
    exit 0
fi

if [ -n "$SIGNAL" ]; then
    kill -"$SIGNAL" "$PID" 2>/dev/null || true
    echo "Sent signal $SIGNAL to PID $PID"
else
    kill -TERM "$PID" 2>/dev/null || true
    echo "Sent SIGTERM to PID $PID, waiting up to 5s..."
    for i in $(seq 1 10); do
        if ! kill -0 "$PID" 2>/dev/null; then
            echo "Process $PID terminated"
            [ -n "$PID_FILE" ] && rm -f "$PID_FILE"
            exit 0
        fi
        sleep 0.5
    done
    kill -KILL "$PID" 2>/dev/null || true
    echo "Sent SIGKILL to PID $PID"
fi

[ -n "$PID_FILE" ] && rm -f "$PID_FILE"
exit 0
