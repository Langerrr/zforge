import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import corpus_retro  # noqa: E402

PHASE = """# Demo - Phase 1: Schema

> Status: COMPLETED

## Evidence Required

<!-- a comment naming E4 that is not a row -->

| Claim | Required | Command / method | Achieved | Artifact |
|-------|----------|------------------|----------|----------|
| migrations apply | E2 | pytest -k migrate | E2 — 14 passed | /tmp/a.01.xml |
| page loads | E4 | pnpm smoke | E3 — worker only | /tmp/b.01.json |
| vocabulary reads | J2 | walk journey A | | |

## Decisions

| # | Reach | Decision | Why | Alternative rejected | Impact |
|---|-------|----------|-----|---------------------|--------|
| D1 | feature | use asyncpg | pool | psycopg | none |
| D2 | outward | status is tri-state | spec gap | boolean | API |

## Follow-up contract

Scope added after acceptance.

## Acceptance

VERDICT: ACCEPT-WITH-NOTES
| migrations apply | E2 | E2 | from-artifact | /tmp/a.01.xml | — | PASS |
| page loads | E4 | E3 | re-executed | pnpm smoke | 0 | SHORTFALL-IMMATERIAL |
ADJUDICATED: FLAG — 2026-11-01 — the surface is this phase's postcondition
RE-ACCEPTED: 2026-11-02 — row 2 re-verified
"""


class CorpusRetroTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory()
        progress = Path(self.root.name) / "docs" / "demo" / "05_progress"
        progress.mkdir(parents=True)
        (progress / "05_01_schema.md").write_text(PHASE)
        (progress / "review.md").write_text("## Evidence Required\n")
        skipped = Path(self.root.name) / "node_modules" / "x" / "05_progress"
        skipped.mkdir(parents=True)
        (skipped / "05_01_schema.md").write_text(PHASE)

    def tearDown(self) -> None:
        self.root.cleanup()

    def phases(self):
        return [
            corpus_retro.read_phase(path, self.root.name)
            for path in corpus_retro.phase_files(self.root.name)
        ]

    def test_finds_only_phase_files_outside_skipped_directories(self) -> None:
        self.assertEqual([p["path"] for p in self.phases()], ["docs/demo/05_progress/05_01_schema.md"])

    def test_reads_what_the_phase_file_records(self) -> None:
        phase = self.phases()[0]
        self.assertEqual(phase["feature"], "docs/demo")
        self.assertEqual(phase["status"], "COMPLETED")
        self.assertEqual(
            [(row["required"], row["achieved"]) for row in phase["evidence"]],
            [("E2", "E2"), ("E4", "E3"), ("J2", None)],
        )
        self.assertEqual((phase["decisions"], phase["decisions_outward"]), (2, 1))
        self.assertEqual(phase["extra_sections"], ["Follow-up contract"])
        self.assertEqual(phase["acceptance"]["verdict"], "ACCEPT-WITH-NOTES")
        self.assertEqual(phase["acceptance"]["adjudicated"], "FLAG")
        self.assertEqual(phase["acceptance"]["re_accepted"], 1)

    def test_summary_counts_shortfalls_and_departures(self) -> None:
        summary = corpus_retro.summarise(self.phases())
        self.assertEqual(summary["evidence_rows"], 3)
        self.assertEqual(summary["below_required"], 1)
        self.assertEqual(summary["class_unreadable"], 1)
        self.assertEqual(summary["adjudication_departed"], 1)
        self.assertEqual(summary["phases_with_extra_sections"], 1)

    def test_main_reports_and_fails_on_an_empty_root(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(corpus_retro.main([self.root.name, "--since", "2000-01-01"]), 0)
            with tempfile.TemporaryDirectory() as empty:
                self.assertEqual(corpus_retro.main([empty]), 1)
        self.assertIn("docs/demo", out.getvalue())


if __name__ == "__main__":
    unittest.main()
