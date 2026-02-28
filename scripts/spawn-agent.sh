#!/bin/bash
# spawn-agent.sh — Spawns a Claude Code agent (fire-and-forget)
# Usage: spawn-agent.sh <working_directory> <prompt_file> [allowed_tools] [pid_file]
#
# Arguments:
#   working_directory  Directory to run the agent in
#   prompt_file        Path to a text file containing the agent prompt
#   allowed_tools      (Optional) Comma-separated tool list
#                      Default: Edit,Write,Read,Glob,Grep,Bash(<script_dir>/safe-run.sh *)
#   pid_file           (Optional) Explicit path to write agent PID file
#
# PID tracking:
#   If pid_file is provided, the agent PID is written there.
#   Otherwise, if the prompt contains "You may ONLY update your assigned phase file: <path>",
#   the agent PID is written to <path>.pid so the monitor can detect orphaned agents.
#
# See also: spawn-codex.sh for OpenAI Codex agent spawning.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

WORK_DIR="${1:?Usage: spawn-agent.sh <working_directory> <prompt_file> [allowed_tools] [pid_file]}"
PROMPT_FILE="${2:?Usage: spawn-agent.sh <working_directory> <prompt_file> [allowed_tools] [pid_file]}"
ALLOWED_TOOLS="${3:-Edit,Write,Read,Glob,Grep,Bash($SCRIPT_DIR/safe-run.sh *)}"
PID_FILE_OVERRIDE="${4:-}"

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

# Clear nested-session guard so agents can spawn from within a Claude Code session
unset CLAUDECODE CLAUDE_CODE_ENTRYPOINT

# Spawn agent in background, fully detached (fire-and-forget)
claude -p "$PROMPT" --allowedTools "$ALLOWED_TOOLS" &>/dev/null &
AGENT_PID=$!
disown "$AGENT_PID"

# Write PID file — explicit path takes priority over regex extraction
if [ -n "$PID_FILE_OVERRIDE" ]; then
    echo "$AGENT_PID" > "$PID_FILE_OVERRIDE"
    echo "Spawned agent PID $AGENT_PID, PID file: $PID_FILE_OVERRIDE"
elif [ -n "$PHASE_FILE" ]; then
    PID_FILE="${PHASE_FILE}.pid"
    echo "$AGENT_PID" > "$PID_FILE"
    echo "Spawned agent PID $AGENT_PID for phase file: $PHASE_FILE"
else
    echo "Spawned agent PID $AGENT_PID (no PID file)"
fi

exit 0
