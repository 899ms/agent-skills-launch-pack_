from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = ROOT / "install.sh"


class InstallScriptTest(unittest.TestCase):
    def test_install_all_skills_to_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                ["bash", str(INSTALL_SCRIPT), "--all", "--target", tmp],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((Path(tmp) / "wechat-account-launch-expert" / "SKILL.md").exists())
            self.assertTrue((Path(tmp) / "douyin-account-launch-expert" / "SKILL.md").exists())
            self.assertTrue((Path(tmp) / "xiaohongshu-account-launch-expert" / "SKILL.md").exists())
            self.assertTrue((Path(tmp) / "x-twitter-cold-start-expert" / "SKILL.md").exists())

    def test_install_one_skill_to_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    "bash",
                    str(INSTALL_SCRIPT),
                    "x-twitter-cold-start-expert",
                    "--target",
                    tmp,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((Path(tmp) / "x-twitter-cold-start-expert" / "SKILL.md").exists())
            self.assertFalse((Path(tmp) / "wechat-account-launch-expert").exists())


if __name__ == "__main__":
    unittest.main()
