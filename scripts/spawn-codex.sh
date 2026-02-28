#!/bin/bash
# spawn-codex.sh — Spawns an OpenAI Codex CLI agent (fire-and-forget)
# Usage: spawn-codex.sh <working_directory> <prompt_file> [pid_file]
#
# Arguments:
#   working_directory  Directory to run the agent in
#   prompt_file        Path to a text file containing the agent prompt
#   pid_file           (Optional) Explicit path to write agent PID file
#
# Codex runs non-interactively via `codex exec` in full-auto mode
# (auto-approve + workspace-write sandbox).
# See also: spawn-agent.sh for Claude Code agent spawning.

set -euo pipefail

WORK_DIR="${1:?Usage: spawn-codex.sh <working_directory> <prompt_file> [pid_file]}"
PROMPT_FILE="${2:?Usage: spawn-codex.sh <working_directory> <prompt_file> [pid_file]}"
PID_FILE_OVERRIDE="${3:-}"

if [ ! -d "$WORK_DIR" ]; then
    echo "ERROR: Working directory not found: $WORK_DIR" >&2
    exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
    exit 1
fi

PROMPT="$(cat "$PROMPT_FILE")"

cd "$WORK_DIR"

# Spawn codex non-interactively in full-auto mode (auto-approve + workspace-write sandbox)
codex exec --full-auto -C "$WORK_DIR" "$PROMPT" &>/dev/null &
AGENT_PID=$!
disown "$AGENT_PID"

# Write PID file
if [ -n "$PID_FILE_OVERRIDE" ]; then
    echo "$AGENT_PID" > "$PID_FILE_OVERRIDE"
    echo "Spawned codex agent PID $AGENT_PID, PID file: $PID_FILE_OVERRIDE"
else
    echo "Spawned codex agent PID $AGENT_PID (no PID file)"
fi

exit 0
