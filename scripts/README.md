# 学习仓库初始化与进度扫描脚本

本目录存放个人仓库初始化工具，以及无需调用 LLM 的双仓确定性进度扫描工具。

计划入口：

- `init_learning_progress.py`：从课程仓库模板初始化一个独立个人仓库，不覆盖已有文件。
- `detect_learning_progress.py`：从课程仓库读取规则和周计划，从个人仓库读取状态与证据，向标准输出返回精简 JSON。
- `generate_course_tutorials.py`：从九份阶段四列表格生成 32 份周教程，确保 224 节课都包含学习动机、概念边界、当周语言定位、60 分钟步骤、资料章节、参考图/样例代码、验收方法和五步参考答案。
- `tests/`：扫描器的标准库 `unittest` 回归测试。

初始化脚本只创建个人仓库中缺失的模板文件，不覆盖已有记录。进度扫描脚本只读，不修改课程或个人仓库；课程教程生成器只更新课程仓库自己的生成目录。

运行：

```bash
python3 scripts/init_learning_progress.py --course-repo . --progress-repo ../ai-class-note
python3 scripts/detect_learning_progress.py --repo . --progress-repo ../ai-class-note
python3 scripts/detect_learning_progress.py --repo . --progress-repo ../ai-class-note --pretty
python3 -m unittest scripts.tests.test_detect_learning_progress -v
python3 scripts/generate_course_tutorials.py --check
```

默认输出紧凑的 `progress-scan.v2` JSON；`--pretty` 仅供人工检查。输出显式区分 `course_root` 和 `progress_root`，并包含当前阶段、当前周、周计划、占位符、缺失链接、越序进展、规则/进度指纹和建议路由。

状态判断保持保守：脚本只能在周状态已完成、成果与验证齐全，并存在“讲师结论：通过、Teach-back 已完成、变体任务已完成”时识别为 `PASSED`。语义评审仍由 REVIEW/FULL Prompt 负责。

课程教程生成器只写入 `learning-plan/tutorials/`，不修改阶段计划、周状态、成果或笔记。当周语言定位由生成器按[开发语言路线](../learning-plan/01-language-roadmap.md)写入每份周教程；阶段表格或语言映射发生变化后先运行生成命令，再用 `--check` 验证生成文件未漂移。
