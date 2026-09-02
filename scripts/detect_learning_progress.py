#!/usr/bin/env python3
"""Scan a learner repository against this course without calling an LLM."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WEEK_COUNT = 32
COURSE_FILES = (
    "AGENTS.md",
    "README.md",
    "learning-plan/README.md",
    "learning-plan/00-learning-method.md",
    "learning-plan/06-deliverable-standards.md",
    "learning-plan/07-instructor-supervision.md",
    "learning-plan/stages/README.md",
    "deliverables/README.md",
)
PROGRESS_FILES = (
    "README.md",
    "deliverables/README.md",
)
PLACEHOLDER_TERMS = ("待填写", "待完成", "待补充")
STATUS_PATTERN = re.compile(r"^(?:-\s*)?状态：\s*`?([^`\n]+)`?\s*$", re.MULTILINE)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
STAGE_PATTERN = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<start>\d+)\s*[–-]\s*"
    r"(?P<end>\d+)\s*\|\s*\[[^\]]+\]\((?P<path>[^)]+)\)\s*\|$",
    re.MULTILINE,
)
TOPIC_PATTERN = re.compile(
    r"^\|\s*(?P<week>\d+)\s*\|\s*(?P<topic>[^|]+?)\s*\|", re.MULTILINE
)
DAY_PATTERN = re.compile(
    r"^\|\s*(周[一二三四五六日])\s*\|\s*([^|]+?)\s*\|\s*"
    r"([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Stage:
    id: int
    name: str
    start: int
    end: int
    path: str


@dataclass(frozen=True)
class WeekScan:
    number: int
    topic: str
    declared_status: str | None
    recognized_status: str
    placeholders: list[str]
    missing_links: list[str]
    unchecked_items: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read course rules plus learner artifacts and emit progress-scan.v2 JSON."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository directory or a child directory. Defaults to current directory.",
    )
    parser.add_argument(
        "--progress-repo",
        required=True,
        help="Independent learner repository containing deliverables/ and notes/.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON. Compact JSON is the default for low-token agent use.",
    )
    return parser.parse_args()


def locate_course_repo(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if all((candidate / path).exists() for path in COURSE_FILES[:4]):
            return candidate
    return None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_files(root: Path, paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        path = root / relative
        digest.update(relative.encode("utf-8"))
        if path.exists():
            digest.update(path.read_bytes())
        else:
            digest.update(b"<missing>")
    return f"sha256:{digest.hexdigest()}"


def parse_declared_status(text: str) -> str | None:
    match = STATUS_PATTERN.search(text)
    return match.group(1).strip() if match else None


def extract_section(text: str, title: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(title)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def find_placeholders(text: str) -> list[str]:
    return [term for term in PLACEHOLDER_TERMS if term in text]


def find_missing_links(readme: Path, text: str) -> list[str]:
    missing: list[str] = []
    for target in LINK_PATTERN.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "#")):
            continue
        if not (readme.parent / target).resolve().exists():
            missing.append(target)
    return sorted(set(missing))


def has_checked_item(text: str) -> bool:
    return bool(re.search(r"^-\s*\[[xX]\]\s+", text, re.MULTILINE))


def count_unchecked_items(text: str) -> int:
    return len(re.findall(r"^-\s*\[\s\]\s+", text, re.MULTILINE))


def section_has_evidence(section: str) -> bool:
    if not section or any(term in section for term in PLACEHOLDER_TERMS):
        return False
    meaningful = [
        line.strip()
        for line in section.splitlines()
        if line.strip() and line.strip() not in {"-", "无", "暂无"}
    ]
    return bool(meaningful)


def field_has_value(section: str, field: str, value: str) -> bool:
    pattern = rf"^(?:-\s*)?{re.escape(field)}：\s*`?{re.escape(value)}`?\s*$"
    return bool(re.search(pattern, section, re.MULTILINE))


def classify_week(readme: Path, topic: str) -> WeekScan:
    text = read_text(readme)
    declared = parse_declared_status(text)
    placeholders = find_placeholders(text)
    missing_links = find_missing_links(readme, text)
    unchecked = count_unchecked_items(text)
    verification = extract_section(text, "验证记录")
    failure = extract_section(text, "失败、边界或安全案例")
    teacher = extract_section(text, "讲师验收")
    teacher_passed = field_has_value(teacher, "结论", "通过")
    teach_back = field_has_value(teacher, "Teach-back", "已完成")
    variation = field_has_value(teacher, "变体任务", "已完成")

    if declared == "阻塞":
        recognized = "BLOCKED"
    elif declared == "进行中":
        recognized = "IN_PROGRESS"
    elif declared == "已完成":
        missing_gate = (
            bool(placeholders)
            or bool(missing_links)
            or unchecked > 0
            or not section_has_evidence(verification)
            or not section_has_evidence(failure)
        )
        if missing_gate:
            recognized = "INCONSISTENT"
        elif teacher_passed and teach_back and variation:
            recognized = "PASSED"
        else:
            recognized = "READY_FOR_REVIEW"
    elif declared == "未开始":
        recognized = "INCONSISTENT" if has_checked_item(text) else "NOT_STARTED"
    else:
        recognized = "INCONSISTENT"

    return WeekScan(
        number=int(readme.parent.name.split("-")[-1]),
        topic=topic,
        declared_status=declared,
        recognized_status=recognized,
        placeholders=placeholders,
        missing_links=missing_links,
        unchecked_items=unchecked,
    )


def parse_stages(root: Path) -> list[Stage]:
    text = read_text(root / "learning-plan/stages/README.md")
    stages: list[Stage] = []
    for index, match in enumerate(STAGE_PATTERN.finditer(text), start=1):
        stages.append(
            Stage(
                id=index,
                name=match.group("name").strip(),
                start=int(match.group("start")),
                end=int(match.group("end")),
                path=f"learning-plan/stages/{match.group('path').strip()}",
            )
        )
    return stages


def parse_topics(root: Path) -> dict[int, str]:
    text = read_text(root / "deliverables/README.md")
    return {
        int(match.group("week")): match.group("topic").strip()
        for match in TOPIC_PATTERN.finditer(text)
        if 1 <= int(match.group("week")) <= WEEK_COUNT
    }


def stage_for_week(stages: list[Stage], week: int) -> Stage | None:
    return next((stage for stage in stages if stage.start <= week <= stage.end), None)


def extract_week_plan(root: Path, stage: Stage | None, week: int) -> list[dict[str, str]]:
    if stage is None:
        return []
    path = root / stage.path
    if not path.exists():
        return []
    text = read_text(path)
    section_match = re.search(
        rf"^##\s+第\s*{week}\s*周[^\n]*\n(?P<body>.*?)(?=^##\s+第\s*\d+\s*周|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not section_match:
        return []
    return [
        {
            "date": match.group(1).strip(),
            "task": match.group(2).strip(),
            "advice": match.group(3).strip(),
            "acceptance": match.group(4).strip(),
        }
        for match in DAY_PATTERN.finditer(section_match.group("body"))
    ]


def invalid_result(
    course_root: Path | None,
    progress_root: Path | None,
    missing: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "progress-scan.v2",
        "repository_status": "INVALID",
        "course_root": str(course_root) if course_root else None,
        "progress_root": str(progress_root) if progress_root else None,
        "missing_required_files": missing,
        "current_stage": None,
        "current_week": None,
        "metrics": {
            "passed_weeks": 0,
            "schedule_progress_percent": 0.0,
        },
        "out_of_order_progress": [],
        "candidate_action": "REPAIR_EVIDENCE",
        "requires_full_review": True,
    }


def scan(course_root: Path, progress_root: Path) -> dict[str, Any]:
    if course_root.resolve() == progress_root.resolve():
        return invalid_result(
            course_root,
            progress_root,
            ["progress repository must be separate from course repository"],
        )
    course_required = list(COURSE_FILES)
    progress_required = list(PROGRESS_FILES) + [
        f"deliverables/week-{week:02d}/README.md" for week in range(1, WEEK_COUNT + 1)
    ]
    missing = [
        f"course:{relative}"
        for relative in course_required
        if not (course_root / relative).exists()
    ] + [
        f"progress:{relative}"
        for relative in progress_required
        if not (progress_root / relative).exists()
    ]
    if missing:
        return invalid_result(course_root, progress_root, missing)

    stages = parse_stages(course_root)
    topics = parse_topics(course_root)
    if not stages:
        return invalid_result(
            course_root,
            progress_root,
            ["course:learning-plan/stages/README.md:stage mappings"],
        )

    weeks = [
        classify_week(
            progress_root / f"deliverables/week-{week:02d}/README.md",
            topics.get(week, f"Week {week:02d}"),
        )
        for week in range(1, WEEK_COUNT + 1)
    ]
    passed = [week for week in weeks if week.recognized_status == "PASSED"]
    current = next(
        (week for week in weeks if week.recognized_status != "PASSED"),
        None,
    )

    rules_paths = [*COURSE_FILES, *[stage.path for stage in stages]]
    progress_paths = [
        "deliverables/README.md",
        *[
            f"deliverables/week-{week:02d}/README.md"
            for week in range(1, WEEK_COUNT + 1)
        ],
    ]
    current_notes = f"notes/week-{current.number:02d}.md" if current else None
    if current_notes and (progress_root / current_notes).exists():
        progress_paths.append(current_notes)

    if current is None:
        return {
            "schema_version": "progress-scan.v2",
            "repository_status": "VALID",
            "course_root": str(course_root),
            "progress_root": str(progress_root),
            "rules_fingerprint": sha256_files(course_root, rules_paths),
            "progress_fingerprint": sha256_files(progress_root, progress_paths),
            "overall_status": "COMPLETED",
            "current_stage": None,
            "current_week": None,
            "metrics": {
                "passed_weeks": WEEK_COUNT,
                "schedule_progress_percent": 100.0,
            },
            "out_of_order_progress": [],
            "candidate_action": "MAINTENANCE",
            "requires_full_review": True,
        }

    current_stage = stage_for_week(stages, current.number)
    week_plan = extract_week_plan(course_root, current_stage, current.number)
    recommended_day = None
    if current.recognized_status == "NOT_STARTED" and week_plan:
        recommended_day = week_plan[0]["date"]
    elif current.recognized_status == "READY_FOR_REVIEW":
        recommended_day = "周日"

    action_by_status = {
        "NOT_STARTED": "START_DAY",
        "IN_PROGRESS": "CONTINUE_DAY",
        "READY_FOR_REVIEW": "WEEKLY_REVIEW",
        "BLOCKED": "RESOLVE_BLOCKER",
        "INCONSISTENT": "REPAIR_EVIDENCE",
    }
    later_progress = [
        week.number
        for week in weeks
        if week.number > current.number
        and week.recognized_status not in {"NOT_STARTED"}
    ]
    stage_passed = (
        len(
            [
                week
                for week in passed
                if current_stage and current_stage.start <= week.number <= current_stage.end
            ]
        )
        if current_stage
        else 0
    )
    stage_total = (
        current_stage.end - current_stage.start + 1 if current_stage else 0
    )

    return {
        "schema_version": "progress-scan.v2",
        "repository_status": "VALID",
        "course_root": str(course_root),
        "progress_root": str(progress_root),
        "rules_fingerprint": sha256_files(course_root, rules_paths),
        "progress_fingerprint": sha256_files(progress_root, progress_paths),
        "overall_status": (
            "BLOCKED"
            if current.recognized_status == "BLOCKED"
            else "INCONSISTENT"
            if current.recognized_status == "INCONSISTENT"
            else "IN_PROGRESS"
            if passed or current.recognized_status != "NOT_STARTED"
            else "NOT_STARTED"
        ),
        "current_stage": (
            {
                "id": current_stage.id,
                "name": current_stage.name,
                "path": current_stage.path,
                "progress": f"{stage_passed}/{stage_total}",
            }
            if current_stage
            else None
        ),
        "current_week": {
            "number": current.number,
            "topic": current.topic,
            "declared_status": current.declared_status,
            "recognized_status": current.recognized_status,
            "recommended_day": recommended_day,
            "week_plan": week_plan,
            "readme_path": f"deliverables/week-{current.number:02d}/README.md",
            "notes_path": (
                f"notes/week-{current.number:02d}.md"
                if (progress_root / f"notes/week-{current.number:02d}.md").exists()
                else None
            ),
            "placeholders": current.placeholders,
            "missing_links": current.missing_links,
            "unchecked_items": current.unchecked_items,
        },
        "metrics": {
            "passed_weeks": len(passed),
            "schedule_progress_percent": round(len(passed) / WEEK_COUNT * 100, 1),
        },
        "out_of_order_progress": later_progress,
        "candidate_action": action_by_status[current.recognized_status],
        "requires_full_review": current.recognized_status
        in {"READY_FOR_REVIEW", "BLOCKED", "INCONSISTENT"},
    }


def main() -> int:
    args = parse_args()
    course_root = locate_course_repo(Path(args.repo))
    progress_root = Path(args.progress_repo).resolve()
    if course_root is None:
        result = invalid_result(None, progress_root, list(COURSE_FILES[:4]))
    else:
        result = scan(course_root, progress_root)
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
