# 起号专家 Agent Skills / Account Launch Agent Skills

一组面向中文内容运营场景的 agent skills，覆盖微信公众号、小红书、抖音和 X/Twitter 的合规起号、定位、选题、内容计划和复盘。

A bilingual agent skills pack for Chinese content operators, covering compliant account launch planning, positioning, topic systems, content calendars, and review loops for WeChat Official Accounts, Xiaohongshu, Douyin, and X/Twitter.

## 语言 / Language

- [中文说明](#中文说明)
- [English README](#english-readme)

---

## 中文说明

### Skills

| Skill | 用途 |
| --- | --- |
| `wechat-account-launch-expert` | 微信公众号起号、定位、选题库、文章简报、发布节奏和周复盘 |
| `xiaohongshu-account-launch-expert` | 小红书账号定位、笔记简报、内容日历、转化路径和复盘 |
| `douyin-account-launch-expert` | 抖音新号冷启动、观看理由、9 条视频实验、互动和复盘 |
| `x-twitter-cold-start-expert` | 中文 X/Twitter 冷启动、定位、回复区曝光、主贴转化和 7 天计划 |

### 安装

默认安装到 Codex skills 目录：

```bash
./install.sh --all
```

安装指定 skill：

```bash
./install.sh wechat-account-launch-expert
```

安装到自定义 agent skills 目录：

```bash
./install.sh --all --target ~/.codex/skills
```

也可以使用环境变量：

```bash
AGENT_SKILLS_DIR=~/.claude/skills ./install.sh --all
```

查看可安装的 skill：

```bash
./install.sh --list
```

### 仓库结构

```text
.
├── skills/
│   ├── wechat-account-launch-expert/
│   ├── xiaohongshu-account-launch-expert/
│   ├── douyin-account-launch-expert/
│   └── x-twitter-cold-start-expert/
├── tools/
│   └── validate_skills.py
├── tests/
├── manifest.json
└── install.sh
```

每个 skill 文件夹都包含 `SKILL.md`，并可附带：

- `references/`: 方法论、流程和检查清单。
- `agents/`: 面向不同 agent UI 的展示信息。

### 验证

运行单元测试：

```bash
python3 -m unittest discover -s tests -v
```

运行发布包校验：

```bash
python3 tools/validate_skills.py .
```

校验器会检查：

- `skills/` 是否存在。
- 每个 skill 是否有 `SKILL.md`。
- `SKILL.md` 是否包含 `name` 和 `description` frontmatter。
- skill 内容里是否出现常见本机路径、API key、token、cookie 或授权头。

### 兼容性

这个仓库使用通用的 `skills/<skill-name>/SKILL.md` 结构。默认安装路径面向 Codex，也可以通过 `--target` 或 `AGENT_SKILLS_DIR` 安装到其他支持 skills 的 agent 环境。

### 安全说明

这些 skills 只提供内容运营规划、诊断和复盘框架，不承诺涨粉、收益、播放量或爆款结果。涉及平台规则、广告能力、处罚边界、导流方式和收益门槛时，应以平台当前官方规则为准。

### 许可证

MIT License. See `LICENSE`.

---

## English README

### Skills

| Skill | Purpose |
| --- | --- |
| `wechat-account-launch-expert` | WeChat Official Account launch planning, positioning, topic library, article briefs, publishing cadence, and weekly review |
| `xiaohongshu-account-launch-expert` | Xiaohongshu account positioning, note briefs, content calendar, conversion path, and review loop |
| `douyin-account-launch-expert` | Douyin cold start planning, viewing reasons, 9-video experiments, interaction design, and performance review |
| `x-twitter-cold-start-expert` | Chinese X/Twitter cold start planning, positioning, reply-based discovery, post/thread conversion, and a 7-day execution plan |

### Install

Install all skills into the default Codex skills directory:

```bash
./install.sh --all
```

Install one skill:

```bash
./install.sh wechat-account-launch-expert
```

Install into a custom agent skills directory:

```bash
./install.sh --all --target ~/.codex/skills
```

You can also use an environment variable:

```bash
AGENT_SKILLS_DIR=~/.claude/skills ./install.sh --all
```

List available skills:

```bash
./install.sh --list
```

### Repository Structure

```text
.
├── skills/
│   ├── wechat-account-launch-expert/
│   ├── xiaohongshu-account-launch-expert/
│   ├── douyin-account-launch-expert/
│   └── x-twitter-cold-start-expert/
├── tools/
│   └── validate_skills.py
├── tests/
├── manifest.json
└── install.sh
```

Each skill folder contains `SKILL.md` and may also include:

- `references/`: playbooks, workflows, and checklists.
- `agents/`: display metadata for different agent UIs.

### Validate

Run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Run the package validator:

```bash
python3 tools/validate_skills.py .
```

The validator checks that:

- `skills/` exists.
- Each skill has a `SKILL.md`.
- Each `SKILL.md` includes `name` and `description` frontmatter.
- Skill content does not contain common local paths, API keys, tokens, cookies, or authorization headers.

### Compatibility

This repository uses the generic `skills/<skill-name>/SKILL.md` layout. The default install target is Codex, but `--target` and `AGENT_SKILLS_DIR` let you install the skills into other agent environments that support skill folders.

### Safety Notes

These skills provide planning, diagnosis, and review frameworks for content operations. They do not promise followers, revenue, views, or viral outcomes. For platform rules, ad features, enforcement boundaries, external-link behavior, and monetization thresholds, use the current official platform rules as the source of truth.

### License

MIT License. See `LICENSE`.
