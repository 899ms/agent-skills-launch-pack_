#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable


REQUIRED_FRONTMATTER_FIELDS = ("name", "description")
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".sh", ".py"}
SENSITIVE_PATTERNS = (
    ("/Users/", re.compile(r"/Users/")),
    ("OpenAI API key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("GitHub token", re.compile(r"(ghp|github_pat)_[A-Za-z0-9_]{20,}")),
    ("Bearer token", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE)),
    ("cookie", re.compile(r"\bcookie\s*[:=]", re.IGNORECASE)),
    ("authorization header", re.compile(r"\bauthorization\s*[:=]", re.IGNORECASE)),
)


@dataclass
class ValidationResult:
    ok: bool
    skill_count: int
    errors: list[str]
    warnings: list[str]


def validate_repository(root: Path | str) -> ValidationResult:
    root_path = Path(root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    skills_path = root_path / "skills"

    if not skills_path.exists():
        return ValidationResult(False, 0, ["skills directory is missing"], warnings)

    skill_dirs = sorted(path for path in skills_path.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("skills directory does not contain any skill folders")

    for skill_dir in skill_dirs:
        validate_skill_dir(skill_dir, skills_path, errors, warnings)

    scan_sensitive_content(skills_path, errors)
    return ValidationResult(not errors, len(skill_dirs), errors, warnings)


def validate_skill_dir(
    skill_dir: Path,
    skills_path: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    skill_file = skill_dir / "SKILL.md"
    relative_skill_file = skill_file.relative_to(skills_path)

    if not skill_file.exists():
        errors.append(f"{skill_dir.name}/SKILL.md is missing")
        return

    content = skill_file.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        errors.append(f"{relative_skill_file} is missing YAML frontmatter")
        return

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if not frontmatter.get(field):
            errors.append(f"{relative_skill_file} is missing frontmatter field: {field}")

    declared_name = frontmatter.get("name")
    if declared_name and declared_name != skill_dir.name:
        warnings.append(
            f"{relative_skill_file} frontmatter name '{declared_name}' does not match folder '{skill_dir.name}'"
        )


def parse_frontmatter(content: str) -> dict[str, str] | None:
    lines = content.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return None

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")

    return None


def scan_sensitive_content(skills_path: Path, errors: list[str]) -> None:
    for path in iter_text_files(skills_path):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for label, pattern in SENSITIVE_PATTERNS:
            if pattern.search(content):
                errors.append(f"{relative_to_skills(path, skills_path)} contains sensitive pattern: {label}")


def iter_text_files(root_path: Path) -> Iterable[Path]:
    ignored_dirs = {".git", "__pycache__", ".pytest_cache"}
    for path in root_path.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def relative_to_skills(path: Path, skills_path: Path) -> str:
    try:
        return str(path.relative_to(skills_path))
    except ValueError:
        return str(path)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    result = validate_repository(root)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    if result.ok:
        print(f"OK: validated {result.skill_count} skill(s)")
        return 0

    print(f"FAILED: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
