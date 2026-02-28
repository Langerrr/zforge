#!/bin/bash
# monitor.sh — watches phase files for agent signals and liveness
# Usage: monitor.sh <phase_directory> [poll_interval_seconds] [stale_threshold_seconds]
#
# Signal format (written by impl agents):
#   <!-- AGENT_SIGNAL:DONE T:2026-02-09T19:30:45Z PID:12345 -->
#   <!-- AGENT_SIGNAL:PAUSED T:2026-02-09T19:30:45Z PID:12345 -->
#   <!-- AGENT_SIGNAL:FAILED T:2026-02-09T19:30:45Z PID:12345 -->
#
# The T: timestamp and PID: fields prevent stale/duplicate signal issues:
#   - Monitor ignores signals older than stale_threshold
#   - Monitor matches signal PID against .pid file to verify origin
#   - Only the LAST signal line in the file is considered
#
# Liveness (detected via file modification time):
#   WORKING  — no signal but file was recently modified
#   STALE    — no signal and file hasn't been modified within threshold
#   ORPHANED — PID file exists but agent process is dead, no signal written
#
# On detection: clears agent signals, outputs structured info, exits.

set -euo pipefail

PHASE_DIR="${1:?Usage: monitor.sh <phase_directory> [poll_interval] [stale_threshold]}"
POLL_INTERVAL="${2:-30}"
STALE_THRESHOLD="${3:-300}"  # 5 minutes default

if [ ! -d "$PHASE_DIR" ]; then
    echo "ERROR: Directory not found: $PHASE_DIR"
    exit 1
fi

# --- Cross-platform helpers ---

# Get file modification time as epoch seconds
get_mtime() {
    if stat -c %Y "$1" 2>/dev/null; then
        return
    fi
    # macOS / BSD stat
    stat -f %m "$1" 2>/dev/null || echo 0
}

# Convert ISO 8601 timestamp to epoch seconds
iso_to_epoch() {
    local ts="$1"
    # GNU date
    if date -d "$ts" +%s 2>/dev/null; then
        return
    fi
    # macOS date — strip trailing Z and parse
    local clean="${ts%Z}"
    date -j -f "%Y-%m-%dT%H:%M:%S" "$clean" +%s 2>/dev/null || echo 0
}

# Extract a value from a signal line: extract_field "FIELD:" <line>
# e.g. extract_field "AGENT_SIGNAL:" "<!-- AGENT_SIGNAL:DONE T:... -->"
# Returns the value immediately after the prefix, up to the next space/dash/end
extract_signal() {
    echo "$1" | grep -o 'AGENT_SIGNAL:[A-Za-z_]*' | sed 's/AGENT_SIGNAL://' || true
}

extract_ts() {
    echo "$1" | grep -o 'T:[^ ]*' | sed 's/^T://' || true
}

extract_pid() {
    echo "$1" | grep -o 'PID:[0-9]*' | sed 's/PID://' || true
}

# --- Snapshot modification times at start using a temp directory ---

MTIME_DIR=$(mktemp -d)
trap 'rm -rf "$MTIME_DIR"' EXIT

MONITOR_START=$(date +%s)

for f in "$PHASE_DIR"/05_*.md; do
    [ -f "$f" ] || continue
    key=$(basename "$f")
    get_mtime "$f" > "$MTIME_DIR/$key"
done

ELAPSED=0

while true; do
    sleep "$POLL_INTERVAL"
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
    NOW=$(date +%s)

    for f in "$PHASE_DIR"/05_*.md; do
        [ -f "$f" ] || continue

        # Extract the LAST signal line (agent should only write one, but take last to handle doubles)
        signal_line=$(grep '<!-- AGENT_SIGNAL:' "$f" | tail -1) || true

        if [ -n "$signal_line" ]; then
            # Parse signal components
            signal=$(extract_signal "$signal_line")
            signal_ts=$(extract_ts "$signal_line")
            signal_pid=$(extract_pid "$signal_line")

            [ -z "$signal" ] && continue

            phase=$(basename "$f" .md)

            # Validate signal freshness — ignore signals older than stale threshold
            if [ -n "$signal_ts" ]; then
                signal_epoch=$(iso_to_epoch "$signal_ts")
                signal_age=$((NOW - signal_epoch))

                if [ "$signal_age" -gt "$STALE_THRESHOLD" ]; then
                    # Stale signal from a previous session — clear it silently
                    grep -v '<!-- AGENT_SIGNAL:' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
                    continue
                fi
            fi

            # Validate signal origin — if PID file exists, check it matches
            PID_FILE="${f}.pid"
            if [ -n "$signal_pid" ] && [ -f "$PID_FILE" ]; then
                expected_pid=$(cat "$PID_FILE" 2>/dev/null | tr -d '[:space:]')
                if [ -n "$expected_pid" ] && [ "$signal_pid" != "$expected_pid" ]; then
                    # Signal from a different agent (stale re-spawn) — clear it
                    grep -v '<!-- AGENT_SIGNAL:' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
                    continue
                fi
            fi

            # Valid signal — clear ALL signal lines (handles doubles)
            grep -v '<!-- AGENT_SIGNAL:' "$f" > "$f.tmp" && mv "$f.tmp" "$f"

            echo "SIGNAL:$signal PHASE:$phase FILE:$f PID:${signal_pid:-unknown} TS:${signal_ts:-unknown}"
            exit 0
        fi
    done

    # Check for orphaned agents (PID file exists but process dead, no signal)
    for f in "$PHASE_DIR"/05_*.md; do
        [ -f "$f" ] || continue
        PID_FILE="${f}.pid"
        [ -f "$PID_FILE" ] || continue

        AGENT_PID=$(cat "$PID_FILE" 2>/dev/null) || continue
        if [ -n "$AGENT_PID" ] && ! kill -0 "$AGENT_PID" 2>/dev/null; then
            phase=$(basename "$f" .md)
            echo "SIGNAL:ORPHANED PHASE:$phase FILE:$f PID:$AGENT_PID"
            rm -f "$PID_FILE"
            exit 0
        fi
    done

    # No signal found — check liveness after threshold
    if [ "$ELAPSED" -ge "$STALE_THRESHOLD" ]; then
        for f in "$PHASE_DIR"/05_*.md; do
            [ -f "$f" ] || continue
            CURRENT_MTIME=$(get_mtime "$f")
            key=$(basename "$f")
            INITIAL_MTIME=$(cat "$MTIME_DIR/$key" 2>/dev/null || echo 0)
            AGE=$((NOW - CURRENT_MTIME))

            phase=$(basename "$f" .md)

            if [ "$CURRENT_MTIME" -gt "$INITIAL_MTIME" ] && [ "$AGE" -lt "$STALE_THRESHOLD" ]; then
                echo "SIGNAL:WORKING PHASE:$phase FILE:$f LAST_MODIFIED:${AGE}s_ago"
                exit 0
            elif [ "$CURRENT_MTIME" -eq "$INITIAL_MTIME" ]; then
                echo "SIGNAL:STALE PHASE:$phase FILE:$f UNCHANGED_FOR:${ELAPSED}s"
                exit 0
            fi
        done

        ELAPSED=0
    fi
done
