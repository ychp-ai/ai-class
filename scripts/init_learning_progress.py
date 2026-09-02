#!/usr/bin/env python3
"""Initialize a learner-owned progress repository for this course."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WEEK_COUNT = 32
ARTIFACT_READMES = (
    "business-cases/README.md",
    "data/README.md",
    "data/docs/README.md",
    "data/eval/README.md",
    "docs/README.md",
    "infra/README.md",
    "java-service/README.md",
    "platform-console/README.md",
    "python-agent/README.md",
    "sandbox-workspaces/README.md",
    "sandbox-workspaces/runtime/README.md",
)
TOPIC_PATTERN = re.compile(
    r"^\|\s*(?P<week>\d+)\s*\|\s*(?P<topic>[^|]+?)\s*\|", re.MULTILINE
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an independent repository for one learner's progress."
    )
    parser.add_argument(
        "--course-repo",
        default=".",
        help="Course repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--progress-repo",
        required=True,
        help="Target learner repository. It must differ from the course repository.",
    )
    return parser.parse_args()


def read_topics(course_root: Path) -> dict[int, str]:
    index = course_root / "deliverables" / "README.md"
    if not index.exists():
        raise ValueError(f"course deliverable index not found: {index}")
    text = index.read_text(encoding="utf-8")
    topics = {
        int(match.group("week")): match.group("topic").strip()
        for match in TOPIC_PATTERN.finditer(text)
    }
    missing = [week for week in range(1, WEEK_COUNT + 1) if week not in topics]
    if missing:
        raise ValueError(f"course deliverable topics missing weeks: {missing}")
    return topics


def write_new(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_template(path: Path, replacements: dict[str, str] | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in (replacements or {}).items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def initialize(course_root: Path, progress_root: Path) -> None:
    course_root = course_root.resolve()
    progress_root = progress_root.resolve()
    if course_root == progress_root:
        raise ValueError("progress repository must be separate from the course repository")

    topics = read_topics(course_root)
    template_root = course_root / "templates" / "learner-repository"
    required_templates = (
        "README.md",
        "AGENTS.md",
        ".gitignore",
        "deliverables/README.md",
        "deliverables/week-template.md",
        "notes/README.md",
        "notes/week-template.md",
        "prompts/README.md",
    )
    missing_templates = [
        relative
        for relative in required_templates
        if not (template_root / relative).exists()
    ]
    if missing_templates:
        raise ValueError(f"learner templates missing: {missing_templates}")

    write_new(
        progress_root / "README.md",
        render_template(template_root / "README.md"),
    )
    write_new(
        progress_root / "AGENTS.md",
        render_template(template_root / "AGENTS.md"),
    )
    write_new(
        progress_root / ".gitignore",
        render_template(template_root / ".gitignore"),
    )
    write_new(
        progress_root / "deliverables" / "README.md",
        render_template(template_root / "deliverables" / "README.md"),
    )
    write_new(
        progress_root / "notes" / "README.md",
        render_template(template_root / "notes" / "README.md"),
    )
    write_new(
        progress_root / "notes" / "week-template.md",
        render_template(template_root / "notes" / "week-template.md"),
    )
    write_new(
        progress_root / "prompts" / "README.md",
        render_template(template_root / "prompts" / "README.md"),
    )
    week_template = template_root / "deliverables" / "week-template.md"
    for week in range(1, WEEK_COUNT + 1):
        write_new(
            progress_root / "deliverables" / f"week-{week:02d}" / "README.md",
            render_template(
                week_template,
                {
                    "WEEK": f"{week:02d}",
                    "TOPIC": topics[week],
                    "COURSE_REQUIREMENT": f"deliverables/week-{week:02d}/README.md",
                },
            ),
        )
    for relative in ARTIFACT_READMES:
        source = template_root / relative
        if not source.exists():
            raise ValueError(f"artifact README template not found: {source}")
        write_new(progress_root / relative, source.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    try:
        initialize(Path(args.course_repo), Path(args.progress_repo))
    except ValueError as error:
        raise SystemExit(str(error)) from error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
