#!/bin/bash
# spawn-agent.sh — Spawns a Claude Code implementation agent (fire-and-forget)
# Usage: spawn-agent.sh <working_directory> <prompt_file> [allowed_tools]
#
# Arguments:
#   working_directory  Directory to run the agent in
#   prompt_file        Path to a text file containing the agent prompt
#   allowed_tools      (Optional) Comma-separated tool list
#                      Default: Edit,Write,Read,Glob,Grep,Bash(<script_dir>/safe-run.sh *)
#
# PID tracking:
#   If the prompt contains "You may ONLY update your assigned phase file: <path>",
#   the agent PID is written to <path>.pid so the monitor can detect orphaned agents.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

WORK_DIR="${1:?Usage: spawn-agent.sh <working_directory> <prompt_file> [allowed_tools]}"
PROMPT_FILE="${2:?Usage: spawn-agent.sh <working_directory> <prompt_file> [allowed_tools]}"
ALLOWED_TOOLS="${3:-Edit,Write,Read,Glob,Grep,Bash($SCRIPT_DIR/safe-run.sh *)}"

if [ ! -d "$WORK_DIR" ]; then
    echo "ERROR: Working directory not found: $WORK_DIR" >&2
    exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
    exit 1
fi

PROMPT="$(cat "$PROMPT_FILE")"

# Extract phase file path from orchestration suffix for PID tracking
PHASE_FILE=""
if [[ "$PROMPT" =~ "You may ONLY update your assigned phase file: "([^$'\n']+) ]]; then
    PHASE_FILE="${BASH_REMATCH[1]}"
fi

cd "$WORK_DIR"

# Spawn agent in background, fully detached (fire-and-forget)
claude -p "$PROMPT" --allowedTools "$ALLOWED_TOOLS" &>/dev/null &
AGENT_PID=$!
disown "$AGENT_PID"

# Write PID file if we identified a phase file
if [ -n "$PHASE_FILE" ]; then
    PID_FILE="${PHASE_FILE}.pid"
    echo "$AGENT_PID" > "$PID_FILE"
    echo "Spawned agent PID $AGENT_PID for phase file: $PHASE_FILE"
else
    echo "Spawned agent PID $AGENT_PID (no phase file detected)"
fi

exit 0
