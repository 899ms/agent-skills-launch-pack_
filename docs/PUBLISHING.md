# Publishing Checklist

Use this checklist before creating or updating the GitHub repository.

## Local Checks

```bash
python3 -m unittest discover -s tests -v
python3 tools/validate_skills.py .
./install.sh --list
```

## Recommended GitHub Setup

```bash
git init
git add .
git commit -m "Initial agent skills package"
```

Create an empty GitHub repository, then connect and push:

```bash
git remote add origin git@github.com:YOUR_NAME/account-launch-agent-skills.git
git branch -M main
git push -u origin main
```

## Release Notes Template

```md
## v0.1.0

Initial release with four account-launch skills:

- wechat-account-launch-expert
- xiaohongshu-account-launch-expert
- douyin-account-launch-expert
- x-twitter-cold-start-expert
```

## Before Publishing

- Confirm there are no private notes, local paths, cookies, tokens, or API keys.
- Confirm each `SKILL.md` has `name` and `description` frontmatter.
- Confirm install works against a temporary target directory.
- Confirm platform-specific claims are framed as strategy assumptions unless verified against current official rules.
