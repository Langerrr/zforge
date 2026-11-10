import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED_SKILLS = {
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


PHASE_CONTRACT = "skills/feature-execution/references/phase-contract.md"
ACCEPTANCE_CONTRACT = "skills/feature-execution/references/acceptance-contract.md"
PLANNING_CONTRACT = "skills/template-conventions/references/planning-contract.md"

CLAUDE_HOST_FILES = {
    PHASE_CONTRACT: "agents/phase-agent.md",
    ACCEPTANCE_CONTRACT: "agents/acceptance-agent.md",
    PLANNING_CONTRACT: "commands/plan.md",
}
CODEX_HOST_FILES = {
    PHASE_CONTRACT: "codex/skills/phase-agent/SKILL.md",
    ACCEPTANCE_CONTRACT: "codex/skills/acceptance-agent/SKILL.md",
    PLANNING_CONTRACT: "codex/skills/plan/SKILL.md",
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

    def test_acceptance_contract_has_one_home_both_hosts_point_to(self) -> None:
        """The acceptance contract lives in one file; both host files name it.

        Two copies of a contract drift, and a phase accepted under one bar and
        reviewed under the other is the failure this guards. The clauses are in
        the contract file, each host file names that file, and neither host file
        restates them.
        """
        contract = (REPO_ROOT / ACCEPTANCE_CONTRACT).read_text()
        clauses = (
            "## Tier 1 — reconcile every row",
            "## Tier 2 — re-execute what earns it",
            "SHORTFALL-MATERIAL",
            "SHORTFALL-IMMATERIAL",
            "Never accept or reject unilaterally",
            "07_harness_conventions.md",
            "UNVERIFIABLE` is for a command that none of these resolves",
            "The one file you write is `07_harness_conventions.md`",
        )
        for clause in clauses:
            self.assertIn(clause, contract, f"missing from contract: {clause}")
        self.assert_hosts_point_to_contract_only(ACCEPTANCE_CONTRACT, clauses)

    def assert_hosts_point_to_contract_only(
        self, contract: str, clauses: tuple[str, ...]
    ) -> None:
        for host in (CLAUDE_HOST_FILES[contract], CODEX_HOST_FILES[contract]):
            text = (REPO_ROOT / host).read_text()
            self.assertIn(contract, text, f"{host} does not name {contract}")
            for clause in clauses:
                self.assertNotIn(clause, text, f"{host} still contains: {clause}")

    def test_evidence_floor_has_one_home_and_the_planner_points_to_it(self) -> None:
        """The evidence scale states the two unwaivable shortfalls; the planner links it.

        The acceptance contract file names them too, because it has to label a row
        ``FLOOR``. The planner's skill settles shortfalls by reference.
        """
        for relative in (
            "skills/template-conventions/references/evidence-scale.md",
            ACCEPTANCE_CONTRACT,
        ):
            text = (REPO_ROOT / relative).read_text()
            self.assertIn("selected nothing and exited 0", text, relative)
            self.assertIn("user-reachable surface", text, relative)

        planner = (REPO_ROOT / "skills" / "feature-execution" / "SKILL.md").read_text()
        self.assertIn("references/evidence-scale.md", planner)
        self.assertNotIn("selected nothing and exited 0", planner)

    def test_host_specific_run_control_lives_in_the_host_file(self) -> None:
        """Each host's goal mechanics sit in that host's orchestrate surface only."""
        shared = (REPO_ROOT / "skills" / "feature-execution" / "SKILL.md").read_text()
        codex = (
            REPO_ROOT / "codex" / "skills" / "feature-orchestrate" / "SKILL.md"
        ).read_text()
        claude = (REPO_ROOT / "commands" / "feature-orchestrate.md").read_text()
        self.assertNotIn("get_goal", shared)
        self.assertNotIn("/goal", shared)
        self.assertIn("## Goal-budget overlay", codex)
        self.assertIn("/goal", claude)


    def test_artifact_location_stated_wherever_artifacts_are_written_or_read(
        self,
    ) -> None:
        """Every surface that writes or opens an artifact names one location.

        The location went unstated through v4.1.0, and agents improvised it into
        the documentation tree; since v4.3.0 it is outside every repository. A surface that tells an agent to write an artifact
        without saying where re-opens exactly that gap.
        """
        for relative in (
            PHASE_CONTRACT,
            ACCEPTANCE_CONTRACT,
            "commands/review.md",
            "codex/skills/review/SKILL.md",
            PLANNING_CONTRACT,
            "skills/feature-execution/SKILL.md",
            "skills/template-conventions/SKILL.md",
            "skills/template-conventions/references/full-template.md",
            "skills/template-conventions/references/evidence-scale.md",
            "templates/05_progress/05_XX_phase_template.md",
            "skills/retro/references/scoring.md",
        ):
            text = (REPO_ROOT / relative).read_text()
            self.assertIn("/tmp/zforge/artifacts/", text, relative)

    def test_artifact_path_rule_stated_in_both_contracts(self) -> None:
        """The writer and the reader agree on how a row cites an artifact.

        The phase contract tells the agent to write the path and the acceptance
        contract tells the agent to open it. Each says "full path", so a row
        cites a path acceptance can resolve.
        """
        for relative in (PHASE_CONTRACT, ACCEPTANCE_CONTRACT):
            text = (REPO_ROOT / relative).read_text()
            self.assertIn("full path", text, relative)

    def test_phase_contract_has_one_home_both_hosts_point_to(self) -> None:
        """The phase-agent contract lives in one file; both host files name it.

        The agent sets its own reporting state, marks each decision's reach, writes
        harness facts itself, and keeps artifacts to files. The clauses are in the
        contract file, each host file names that file, and neither host file
        restates them, so both hosts' planners read the same phases.
        """
        contract = (REPO_ROOT / PHASE_CONTRACT).read_text()
        clauses = (
            "Never COMPLETED",
            "`Reach` column",
            "append it to the feature's `07_harness_conventions.md`",
            "never a directory",
            "DECISIONS: <count> (<n> outward)",
        )
        for clause in clauses:
            self.assertIn(clause, contract, f"missing from contract: {clause}")
        self.assert_hosts_point_to_contract_only(PHASE_CONTRACT, clauses)

    def test_planning_contract_has_one_home_both_hosts_point_to(self) -> None:
        """The planner's contract lives in one file; both host files name it."""
        contract = (REPO_ROOT / PLANNING_CONTRACT).read_text()
        clauses = (
            "## Pre-flight",
            "## The completeness contract",
            "## Staged materialization",
            "## Completion",
        )
        for clause in clauses:
            self.assertIn(clause, contract, f"missing from contract: {clause}")
        self.assert_hosts_point_to_contract_only(PLANNING_CONTRACT, clauses)

    def test_plugin_root_paths_named_by_claude_surfaces_exist(self) -> None:
        """A ``${CLAUDE_PLUGIN_ROOT}/...`` path that is absent fails at run time."""
        pattern = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w/.-]+)")
        missing: list[str] = []
        files = sorted((REPO_ROOT / "agents").glob("*.md"))
        files.extend(sorted((REPO_ROOT / "commands").glob("*.md")))
        for doc in files:
            for relative in pattern.findall(doc.read_text()):
                relative = relative.rstrip(".")
                if not (REPO_ROOT / relative).exists():
                    missing.append(f"{doc.relative_to(REPO_ROOT)} -> {relative}")
        self.assertEqual(missing, [])

    def test_acceptance_section_shape_stated_wherever_it_is_written(self) -> None:
        """Every surface that writes ## Acceptance names the same two closing lines.

        The section is the acceptance report plus an adjudication line and a
        promoted line. A surface describing it as prose reopens the rewrite this
        shape removed.
        """
        for relative in (
            "skills/feature-execution/SKILL.md",
            "templates/05_progress/05_XX_phase_template.md",
            "skills/template-conventions/references/full-template.md",
        ):
            text = (REPO_ROOT / relative).read_text()
            self.assertIn("ADJUDICATED:", text, relative)
            self.assertIn("PROMOTED:", text, relative)
            self.assertIn("RE-ACCEPTED:", text, relative)

    def test_no_surface_promotes_harness_facts_through_the_planner(self) -> None:
        """Harness facts are written by whoever learns them, not copied at acceptance."""
        for directory in ("agents", "commands", "skills", "templates", "codex"):
            for path in (REPO_ROOT / directory).rglob("*.md"):
                self.assertNotIn(
                    "kind: harness", path.read_text(), str(path.relative_to(REPO_ROOT))
                )

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
