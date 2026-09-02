from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PROJECT_ROOT / "scripts" / "detect_learning_progress.py"
INIT_SCRIPT = PROJECT_ROOT / "scripts" / "init_learning_progress.py"


class LearningProgressInitializerTest(unittest.TestCase):
    def test_initializes_from_templates_without_overwriting_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            progress = Path(tmp) / "progress"
            command = [
                sys.executable,
                str(INIT_SCRIPT),
                "--course-repo",
                str(PROJECT_ROOT),
                "--progress-repo",
                str(progress),
            ]

            first = subprocess.run(command, check=False, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            week_one = progress / "deliverables" / "week-01" / "README.md"
            self.assertTrue(week_one.exists())
            self.assertTrue(
                (progress / "deliverables" / "week-32" / "README.md").exists()
            )
            self.assertIn("状态：未开始", week_one.read_text(encoding="utf-8"))
            self.assertTrue((progress / "notes" / "week-template.md").exists())
            self.assertTrue((progress / "java-service" / "README.md").exists())

            week_one.write_text("# learner-owned state\n", encoding="utf-8")
            second = subprocess.run(command, check=False, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(
                week_one.read_text(encoding="utf-8"), "# learner-owned state\n"
            )


class ProgressScannerTest(unittest.TestCase):
    def run_scan(self, root: Path) -> dict:
        course = root / "course"
        progress = root / "progress"
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo",
                str(course),
                "--progress-repo",
                str(progress),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def create_repo(
        self,
        root: Path,
        *,
        week_overrides: dict[int, str] | None = None,
        omit_week: int | None = None,
    ) -> None:
        week_overrides = week_overrides or {}
        course = root / "course"
        progress = root / "progress"
        (course / "learning-plan" / "stages").mkdir(parents=True)
        (course / "deliverables").mkdir()
        (progress / "deliverables").mkdir(parents=True)
        (progress / "artifacts").mkdir()

        (course / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
        (course / "README.md").write_text("# Course\n", encoding="utf-8")
        (course / "learning-plan" / "README.md").write_text(
            "# 32 周完整学习路线\n", encoding="utf-8"
        )
        (course / "learning-plan" / "00-learning-method.md").write_text(
            "# 学习方法\n", encoding="utf-8"
        )
        (course / "learning-plan" / "06-deliverable-standards.md").write_text(
            "# 成果标准\n", encoding="utf-8"
        )
        (course / "learning-plan" / "07-instructor-supervision.md").write_text(
            "# 讲师监督\n", encoding="utf-8"
        )
        (course / "learning-plan" / "stages" / "README.md").write_text(
            "# 阶段目录\n\n"
            "| 阶段 | 周次 | 文档 |\n"
            "| --- | --- | --- |\n"
            "| AI 基础 | 1–4 | [stage-01.md](stage-01.md) |\n"
            "| Java AI | 5–8 | [stage-02.md](stage-02.md) |\n",
            encoding="utf-8",
        )
        (course / "learning-plan" / "stages" / "stage-01.md").write_text(
            "# 阶段一\n\n"
            "## 第 1 周：基础\n\n"
            "| 日期 | 学习任务 | 当天学习建议 | 当天验收 |\n"
            "| --- | --- | --- | --- |\n"
            "| 周一 | 学习 Token | 做对比实验 | 保存结果 |\n"
            "| 周二 | 学习 Embedding | 使用固定样例 | 保存相似度 |\n"
            "| 周三 | 学习采样 | 单变量对比 | 保存参数 |\n"
            "| 周四 | 学习上下文 | 构造冲突 | 保存失败 |\n"
            "| 周五 | 学习成本 | 记录 Usage | 保存表格 |\n"
            "| 周六 | 综合实验 | 保留原始数据 | 可以复现 |\n"
            "| 周日 | 周验收 | Teach-back | 讲师结论 |\n\n"
            "## 第 2 周：原生 API\n\n"
            "| 日期 | 学习任务 | 当天学习建议 | 当天验收 |\n"
            "| --- | --- | --- | --- |\n"
            "| 周一 | 原生调用 | 先非流式 | 请求成功 |\n"
            "| 周二 | 流式调用 | 解析事件 | 可以取消 |\n"
            "| 周三 | 结构化输出 | 校验 Schema | 失败明确 |\n"
            "| 周四 | Tool Call | 记录时序 | 参数可见 |\n"
            "| 周五 | Agent Loop | 限制步数 | 可以停止 |\n"
            "| 周六 | 故障测试 | 注入超时 | 错误稳定 |\n"
            "| 周日 | 周验收 | 完成变体 | 讲师结论 |\n",
            encoding="utf-8",
        )
        (course / "learning-plan" / "stages" / "stage-02.md").write_text(
            "# 阶段二\n", encoding="utf-8"
        )

        index_lines = [
            "# 每周成果目录",
            "",
            "| 周次 | 主题 | 目录 |",
            "| --- | --- | --- |",
        ]
        for week in range(1, 33):
            index_lines.append(
                f"| {week} | Topic {week} | [week-{week:02d}](week-{week:02d}/README.md) |"
            )
        (course / "deliverables" / "README.md").write_text(
            "\n".join(index_lines) + "\n", encoding="utf-8"
        )
        (progress / "README.md").write_text("# Learner\n", encoding="utf-8")
        (progress / "deliverables" / "README.md").write_text(
            "# Personal progress\n", encoding="utf-8"
        )

        for week in range(1, 33):
            if week == omit_week:
                continue
            week_dir = progress / "deliverables" / f"week-{week:02d}"
            week_dir.mkdir()
            default = (
                f"# Week {week:02d}\n\n"
                "状态：`未开始`\n\n"
                "## 成果链接\n\n"
                "- [ ] 待完成。\n\n"
                "## 验证记录\n\n"
                "- 结果：待填写。\n\n"
                "## 失败、边界或安全案例\n\n"
                "- 待填写。\n"
            )
            (week_dir / "README.md").write_text(
                week_overrides.get(week, default), encoding="utf-8"
            )

    @staticmethod
    def passed_week(root: Path, week: int) -> str:
        artifact = root / "progress" / "artifacts" / f"week-{week:02d}.md"
        artifact.write_text("# Verified artifact\n", encoding="utf-8")
        return (
            f"# Week {week:02d}\n\n"
            "状态：`已完成`\n\n"
            "## 成果链接\n\n"
            f"- [x] [可运行成果](../../artifacts/week-{week:02d}.md)\n\n"
            "## 验证记录\n\n"
            "- 命令：python3 -m unittest\n"
            "- 日期：2026-08-24\n"
            "- 结果：PASS，1 test passed。\n\n"
            "## 失败、边界或安全案例\n\n"
            "- 非法输入被拒绝，退出码为 2。\n\n"
            "## 讲师验收\n\n"
            "- 结论：通过\n"
            "- 当前掌握等级：L2\n"
            "- Teach-back：已完成\n"
            "- 变体任务：已完成\n"
        )

    def test_all_unstarted_selects_week_one_and_start_day(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo)

            result = self.run_scan(repo)

        self.assertEqual(result["repository_status"], "VALID")
        self.assertEqual(result["current_stage"]["id"], 1)
        self.assertEqual(result["current_week"]["number"], 1)
        self.assertEqual(result["current_week"]["recognized_status"], "NOT_STARTED")
        self.assertEqual(result["current_week"]["recommended_day"], "周一")
        self.assertEqual(result["candidate_action"], "START_DAY")
        self.assertFalse(result["requires_full_review"])
        self.assertEqual(result["metrics"]["passed_weeks"], 0)
        self.assertEqual(result["current_week"]["week_plan"][0]["date"], "周一")

    def test_course_repository_cannot_be_used_as_progress_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo)
            course = repo / "course"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo",
                    str(course),
                    "--progress-repo",
                    str(course),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            result = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["repository_status"], "INVALID")
        self.assertIn(
            "progress repository must be separate from course repository",
            result["missing_required_files"],
        )

    def test_completed_with_placeholders_is_inconsistent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(
                repo,
                week_overrides={
                    1: (
                        "# Week 01\n\n"
                        "状态：`已完成`\n\n"
                        "## 成果链接\n\n- [ ] 待完成。\n\n"
                        "## 验证记录\n\n- 结果：待填写。\n\n"
                        "## 失败、边界或安全案例\n\n- 待填写。\n"
                    )
                },
            )

            result = self.run_scan(repo)

        self.assertEqual(result["current_week"]["recognized_status"], "INCONSISTENT")
        self.assertEqual(result["candidate_action"], "REPAIR_EVIDENCE")
        self.assertTrue(result["requires_full_review"])
        self.assertIn("待填写", result["current_week"]["placeholders"])

    def test_teacher_passed_week_advances_to_next_week(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo)
            week_one = self.passed_week(repo, 1)
            (repo / "progress" / "deliverables" / "week-01" / "README.md").write_text(
                week_one, encoding="utf-8"
            )

            result = self.run_scan(repo)

        self.assertEqual(result["metrics"]["passed_weeks"], 1)
        self.assertEqual(result["current_week"]["number"], 2)
        self.assertEqual(result["current_week"]["recognized_status"], "NOT_STARTED")
        self.assertEqual(result["current_week"]["recommended_day"], "周一")

    def test_teacher_gates_are_matched_per_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo)
            content = self.passed_week(repo, 1).replace(
                "Teach-back：已完成", "Teach-back：未完成"
            )
            (repo / "progress" / "deliverables" / "week-01" / "README.md").write_text(
                content, encoding="utf-8"
            )

            result = self.run_scan(repo)

        self.assertEqual(result["current_week"]["number"], 1)
        self.assertEqual(
            result["current_week"]["recognized_status"], "READY_FOR_REVIEW"
        )

    def test_missing_week_readme_makes_repository_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo, omit_week=7)

            result = self.run_scan(repo)

        self.assertEqual(result["repository_status"], "INVALID")
        self.assertIn(
            "progress:deliverables/week-07/README.md",
            result["missing_required_files"],
        )
        self.assertIsNone(result["current_week"])

    def test_later_progress_is_reported_as_out_of_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(
                repo,
                week_overrides={
                    2: (
                        "# Week 02\n\n"
                        "状态：`进行中`\n\n"
                        "## 成果链接\n\n- [x] 已有部分实验。\n"
                    )
                },
            )

            result = self.run_scan(repo)

        self.assertEqual(result["current_week"]["number"], 1)
        self.assertEqual(result["out_of_order_progress"], [2])

    def test_blocked_week_requests_full_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(
                repo,
                week_overrides={
                    1: (
                        "# Week 01\n\n"
                        "状态：`阻塞`\n\n"
                        "## 未完成和风险\n\n"
                        "- 阻塞原因：缺少本地运行环境。\n"
                    )
                },
            )

            result = self.run_scan(repo)

        self.assertEqual(result["current_week"]["recognized_status"], "BLOCKED")
        self.assertEqual(result["candidate_action"], "RESOLVE_BLOCKER")
        self.assertTrue(result["requires_full_review"])

    def test_rules_fingerprint_changes_when_stage_plan_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo)
            before = self.run_scan(repo)["rules_fingerprint"]
            stage = repo / "course" / "learning-plan" / "stages" / "stage-01.md"
            stage.write_text(
                stage.read_text(encoding="utf-8") + "\n新的验收规则。\n",
                encoding="utf-8",
            )

            after = self.run_scan(repo)["rules_fingerprint"]

        self.assertNotEqual(before, after)

    def test_progress_fingerprint_changes_when_current_notes_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.create_repo(repo)
            before = self.run_scan(repo)["progress_fingerprint"]
            (repo / "progress" / "notes").mkdir()
            notes = repo / "progress" / "notes" / "week-01.md"
            notes.write_text("# Week 01\n\n第一次学习记录。\n", encoding="utf-8")

            after = self.run_scan(repo)["progress_fingerprint"]

        self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
