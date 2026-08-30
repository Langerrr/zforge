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


if __name__ == "__main__":
    unittest.main()
