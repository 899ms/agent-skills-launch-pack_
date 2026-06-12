from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_skills import validate_repository


class ValidateSkillsTest(unittest.TestCase):
    def test_valid_skill_tree_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "demo-skill"
            (skill_dir / "references").mkdir(parents=True)
            (skill_dir / "agents").mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: demo-skill\n"
                "description: Demo skill for validating a release package.\n"
                "---\n\n"
                "# Demo Skill\n\n"
                "Use `references/demo.md` for details.\n",
                encoding="utf-8",
            )
            (skill_dir / "references" / "demo.md").write_text("Reference.\n", encoding="utf-8")
            (skill_dir / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: \"Demo Skill\"\n"
                "  short_description: \"Demo\"\n"
                "  default_prompt: \"Use $demo-skill.\"\n",
                encoding="utf-8",
            )

            result = validate_repository(root)

            self.assertTrue(result.ok)
            self.assertEqual(result.errors, [])
            self.assertEqual(result.skill_count, 1)

    def test_missing_frontmatter_name_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "bad-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "description: Missing name should fail.\n"
                "---\n\n"
                "# Bad Skill\n",
                encoding="utf-8",
            )

            result = validate_repository(root)

            self.assertFalse(result.ok)
            self.assertIn("bad-skill/SKILL.md is missing frontmatter field: name", result.errors)

    def test_sensitive_patterns_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "leaky-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: leaky-skill\n"
                "description: Contains a local path.\n"
                "---\n\n"
                "Read from /Users/Chen/private-notes before running.\n",
                encoding="utf-8",
            )

            result = validate_repository(root)

            self.assertFalse(result.ok)
            self.assertIn("leaky-skill/SKILL.md contains sensitive pattern: /Users/", result.errors)


if __name__ == "__main__":
    unittest.main()
