import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED_SKILLS = {
    "async-reasoning",
    "feature-execution",
    "retro",
    "template-conventions",
}
CODEX_ONLY_SKILLS = {
    "acceptance-agent",
    "debug",
    "feature-orchestrate",
    "feature-resume",
    "phase-agent",
    "plan",
    "plan-status",
    "review",
    "track",
}


def skill_names(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {
        path.parent.name
        for path in root.glob("*/SKILL.md")
        if path.is_file()
    }


class PluginSurfaceTests(unittest.TestCase):
    def test_runtime_skill_roots_match_host_contract(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / ".codex-plugin" / "plugin.json").read_text()
        )

        self.assertEqual(skill_names(REPO_ROOT / "skills"), SHARED_SKILLS)
        self.assertEqual(
            skill_names(REPO_ROOT / "codex" / "skills"), CODEX_ONLY_SKILLS
        )
        self.assertEqual(
            manifest["skills"], ["./skills/", "./codex/skills/"]
        )

    def test_relative_skill_references_resolve(self) -> None:
        skill_files = list((REPO_ROOT / "skills").glob("*/SKILL.md"))
        skill_files.extend((REPO_ROOT / "codex" / "skills").glob("*/SKILL.md"))

        unresolved: list[str] = []
        for skill_file in skill_files:
            for relative_path in re.findall(
                r"`((?:\.\./)+[^`]+)`", skill_file.read_text()
            ):
                target = skill_file.parent / relative_path
                if not target.exists():
                    unresolved.append(
                        f"{skill_file.relative_to(REPO_ROOT)} -> {relative_path}"
                    )

        self.assertEqual(unresolved, [])


    def test_template_paths_named_by_workflows_resolve(self) -> None:
        """A workflow loading a template by path fails at run time if it is absent.

        Scoped to explicit ``templates/`` paths. Bare ``NN_name.md`` mentions are
        not checked: documents outside the fixed set are named for what they are
        and have no template, so ``03_core_patterns.md`` appears as an example of
        the naming convention rather than as a file to load.
        """
        pattern = re.compile(r"(?:\$\{CLAUDE_PLUGIN_ROOT\}/)?(templates/[\w/.-]+\.md)")
        missing: list[str] = []
        for doc in sorted(REPO_ROOT.rglob("*.md")):
            if {"tmp", "_archive", ".git"} & set(doc.parts):
                continue
            for relative in pattern.findall(doc.read_text()):
                if not (REPO_ROOT / relative).exists():
                    missing.append(f"{doc.relative_to(REPO_ROOT)} -> {relative}")
        self.assertEqual(missing, [])

    def test_harness_conventions_template_exists(self) -> None:
        """Acceptance and both orchestrators read this file; it must be creatable."""
        self.assertTrue(
            (REPO_ROOT / "templates" / "07_harness_conventions.md").is_file()
        )

    def test_acceptance_contract_stated_on_both_hosts(self) -> None:
        """The Claude agent and the Codex skill state one acceptance contract.

        Two copies of a contract drift, and a phase accepted under one bar and
        reviewed under the other is the failure this guards.
        """
        claude = (REPO_ROOT / "agents" / "acceptance-agent.md").read_text()
        codex = (
            REPO_ROOT / "codex" / "skills" / "acceptance-agent" / "SKILL.md"
        ).read_text()

        for clause in (
            "## Tier 1 — reconcile every row",
            "## Tier 2 — re-execute what a trigger selects",
            "SHORTFALL-MATERIAL",
            "SHORTFALL-IMMATERIAL",
            "Never accept or reject unilaterally",
            "07_harness_conventions.md",
        ):
            self.assertIn(clause, claude, f"missing from Claude agent: {clause}")
            self.assertIn(clause, codex, f"missing from Codex skill: {clause}")

    def test_evidence_floor_is_stated_wherever_shortfalls_are_settled(self) -> None:
        """Every surface that settles a shortfall names the two unwaivable ones."""
        for relative in (
            "agents/acceptance-agent.md",
            "codex/skills/acceptance-agent/SKILL.md",
            "skills/feature-execution/SKILL.md",
            "skills/template-conventions/references/evidence-scale.md",
        ):
            text = (REPO_ROOT / relative).read_text()
            self.assertIn("selected nothing and exited 0", text, relative)
            self.assertIn("user-reachable surface", text, relative)


    def test_artifact_location_stated_wherever_artifacts_are_written_or_read(
        self,
    ) -> None:
        """Every surface that writes or opens an artifact names one location.

        The location went unstated through v4.1.0, and agents improvised it into
        the documentation tree. A surface that tells an agent to write an artifact
        without saying where re-opens exactly that gap.
        """
        for relative in (
            "agents/phase-agent.md",
            "codex/skills/phase-agent/SKILL.md",
            "agents/acceptance-agent.md",
            "codex/skills/acceptance-agent/SKILL.md",
            "commands/review.md",
            "codex/skills/review/SKILL.md",
            "commands/plan.md",
            "codex/skills/plan/SKILL.md",
            "skills/feature-execution/SKILL.md",
            "skills/template-conventions/SKILL.md",
            "skills/template-conventions/references/full-template.md",
            "skills/template-conventions/references/evidence-scale.md",
            "templates/05_progress/05_XX_phase_template.md",
            "skills/retro/references/scoring.md",
        ):
            text = (REPO_ROOT / relative).read_text()
            self.assertIn(".zforge/artifacts/", text, relative)

    def test_artifact_path_rule_stated_on_both_hosts(self) -> None:
        """The writer and the reader agree on how a row cites an artifact.

        The phase agent writes the path and the acceptance agent opens it. If the
        two copies of either drift, a row cites a path acceptance cannot resolve.
        """
        pairs = (
            ("agents/phase-agent.md", "codex/skills/phase-agent/SKILL.md"),
            (
                "agents/acceptance-agent.md",
                "codex/skills/acceptance-agent/SKILL.md",
            ),
        )
        for claude_path, codex_path in pairs:
            for relative in (claude_path, codex_path):
                text = (REPO_ROOT / relative).read_text()
                self.assertIn("relative to the workspace root", text, relative)

    def test_no_surface_requires_a_committed_artifact(self) -> None:
        """Artifacts are untracked, so no surface may still demand a commit.

        A single surviving instruction to commit an artifact puts command output
        back in the documentation tree, which is the whole of what this changed.
        Scoped to the surfaces an agent reads as instructions; `docs/` holds design
        records, which name the rules they retired.
        """
        skip = {"tmp", "_archive", ".git", "node_modules"}
        offenders = []
        for directory in ("agents", "commands", "skills", "templates", "codex"):
            for path in (REPO_ROOT / directory).rglob("*.md"):
                if skip & set(path.relative_to(REPO_ROOT).parts):
                    continue
                if "committed artifact" in path.read_text():
                    offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
