#!/usr/bin/env python3
"""Read every zforge feature tree under a root and report what the phase files contain.

Counts and sizes only. It reads the ledger and judges nothing: what a number means is
for whoever reads the report.

    python3 tools/corpus_retro.py ~/workspace
    python3 tools/corpus_retro.py ~/workspace --json > corpus.json
"""
import argparse
import datetime
import json
import os
import re
import statistics
import sys

SKIP_DIRS = {"node_modules", ".git", ".worktrees"}
TEMPLATE_SECTIONS = {
    "Agent Prompt", "Required Context", "Evidence Required", "Environment Assumptions",
    "Checklist", "Decisions", "Open Items", "Files Created/Modified", "Session Log",
    "Resume Point", "Acceptance",
}
PHASE_FILE = re.compile(r"05_\d+.*\.md$")
CLASS = re.compile(r"\b([EJ])([0-4])\b")
COMMENT = re.compile(r"<!--.*?-->", re.S)


def phase_files(root):
    for directory, subdirs, names in os.walk(root):
        subdirs[:] = [d for d in subdirs if d not in SKIP_DIRS]
        if os.path.basename(directory) != "05_progress":
            continue
        for name in sorted(names):
            if PHASE_FILE.match(name):
                yield os.path.join(directory, name)


def sections(text):
    """Map each `## ` heading to its body, comments removed."""
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    found = {}
    for heading, body in zip(parts[1::2], parts[2::2]):
        found[heading] = found.get(heading, "") + COMMENT.sub("", body)
    return found


def table_rows(body):
    """Cells of each data row in the first markdown table of a section."""
    lines = [line for line in body.splitlines() if line.lstrip().startswith("|")]
    return [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines[2:]]


def evidence(body):
    rows = []
    for cells in table_rows(body):
        if len(cells) < 4:
            continue
        required, achieved = CLASS.search(cells[1]), CLASS.search(cells[3])
        if not required:
            continue
        rows.append({
            "required": required.group(0),
            "achieved": achieved.group(0) if achieved else None,
            "achieved_chars": len(cells[3]),
        })
    return rows


def gap(row):
    """-1 below, 0 met, 1 above, None when the achieved class is absent or on the other axis."""
    if not row["achieved"] or row["achieved"][0] != row["required"][0]:
        return None
    difference = int(row["achieved"][1]) - int(row["required"][1])
    return (difference > 0) - (difference < 0)


def acceptance(body):
    verdict = re.search(r"^VERDICT:\s*([A-Z-]+)", body, flags=re.M)
    adjudicated = re.search(r"^ADJUDICATED:\s*([A-Z-]+)", body, flags=re.M)
    return {
        "present": bool(body.strip()),
        "chars": len(body.strip()),
        "verdict": verdict.group(1) if verdict else None,
        "adjudicated": adjudicated.group(1) if adjudicated else None,
        "from_artifact": body.count("from-artifact"),
        "re_executed": body.count("re-executed"),
        "re_accepted": len(re.findall(r"^RE-ACCEPTED:", body, flags=re.M)),
    }


def read_phase(path, root):
    text = open(path, errors="replace").read()
    found = sections(text)
    if "Evidence Required" not in found:
        return None
    decisions = table_rows(found.get("Decisions", ""))
    status = re.search(r"^> Status:\s*(\w+)", text, flags=re.M)
    return {
        "path": os.path.relpath(path, root),
        "feature": os.path.relpath(os.path.dirname(os.path.dirname(path)), root),
        "date": datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat(),
        "status": status.group(1) if status else None,
        "bytes": len(text.encode()),
        "section_bytes": {name: len(body.encode()) for name, body in found.items()},
        "extra_sections": sorted(set(found) - TEMPLATE_SECTIONS),
        "evidence": evidence(found["Evidence Required"]),
        "decisions": len(decisions),
        "decisions_outward": sum("outward" in cells[1:2] for cells in decisions),
        "decision_row_chars": [sum(map(len, cells)) for cells in decisions],
        "session_log_rows": len(table_rows(found.get("Session Log", ""))),
        "acceptance": acceptance(found.get("Acceptance", "")),
    }


def median(values):
    values = list(values)
    return int(statistics.median(values)) if values else 0


def summarise(phases):
    rows = [row for phase in phases for row in phase["evidence"]]
    gaps = [gap(row) for row in rows]
    accepted = [phase["acceptance"] for phase in phases if phase["acceptance"]["present"]]
    judged = [a for a in accepted if a["verdict"] and a["adjudicated"]]
    return {
        "phases": len(phases),
        "latest": max(phase["date"] for phase in phases),
        "median_bytes": median(phase["bytes"] for phase in phases),
        "max_bytes": max(phase["bytes"] for phase in phases),
        "evidence_rows": len(rows),
        "below_required": gaps.count(-1),
        "class_unreadable": gaps.count(None),
        "median_achieved_chars": median(row["achieved_chars"] for row in rows),
        "decisions": sum(phase["decisions"] for phase in phases),
        "decisions_outward": sum(phase["decisions_outward"] for phase in phases),
        "median_decision_row_chars": median(n for phase in phases for n in phase["decision_row_chars"]),
        "accepted": len(accepted),
        "adjudication_departed": sum(a["verdict"] != a["adjudicated"] for a in judged),
        "re_accepted": sum(a["re_accepted"] for a in accepted),
        "phases_with_extra_sections": sum(bool(phase["extra_sections"]) for phase in phases),
    }


def group(phases, key):
    groups = {}
    for phase in phases:
        groups.setdefault(key(phase), []).append(phase)
    return {name: summarise(members) for name, members in groups.items()}


COLUMNS = [
    ("phases", "phases"), ("median_bytes", "med B"), ("max_bytes", "max B"),
    ("evidence_rows", "ev"), ("below_required", "below"), ("median_achieved_chars", "ach ch"),
    ("decisions", "dec"), ("decisions_outward", "outw"), ("median_decision_row_chars", "dec ch"),
    ("accepted", "acc"), ("adjudication_departed", "depart"), ("re_accepted", "re-acc"),
    ("phases_with_extra_sections", "extra"),
]


def print_table(title, summaries, first_column):
    print(f"\n{title}")
    print(f"{first_column:<52}" + "".join(f"{label:>8}" for _, label in COLUMNS))
    for name, summary in summaries:
        print(f"{name[-52:]:<52}" + "".join(f"{summary[key]:>8}" for key, _ in COLUMNS))


def report(phases):
    by_feature = sorted(group(phases, lambda p: p["feature"]).items(), key=lambda item: item[1]["latest"])
    by_month = sorted(group(phases, lambda p: p["date"][:7]).items())
    print_table("By feature, oldest first", by_feature, "feature")
    print_table("By month of last change", by_month, "month")
    print_table("All", [("all", summarise(phases))], "")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", help="directory to search for feature trees")
    parser.add_argument("--since", help="only phase files changed on or after YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="print one record per phase file")
    args = parser.parse_args(argv)
    phases = [phase for phase in (read_phase(path, args.root) for path in phase_files(args.root)) if phase]
    if args.since:
        phases = [phase for phase in phases if phase["date"] >= args.since]
    if not phases:
        print("No phase files with an Evidence Required table found.", file=sys.stderr)
        return 1
    if args.json:
        json.dump(phases, sys.stdout, indent=1)
    else:
        report(phases)
    return 0


if __name__ == "__main__":
    sys.exit(main())
