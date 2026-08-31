# 进度扫描脚本目录

本目录存放无需调用 LLM 的确定性学习进度扫描工具。

计划入口：

- `detect_learning_progress.py`：读取周状态、验证占位符、讲师结论和阶段计划，向标准输出返回精简 JSON。
- `generate_course_tutorials.py`：从九份阶段四列表格生成 32 份周教程，确保 224 节课都包含学习动机、概念边界、60 分钟步骤、资料章节、参考图/样例代码、验收方法和五步参考答案。
- `tests/`：扫描器的标准库 `unittest` 回归测试。

进度扫描脚本只读，不修改周状态、成果、学习笔记或 Git 历史。课程教程生成器只更新自己的生成目录，不修改上述学习证据。

运行：

```bash
python3 scripts/detect_learning_progress.py --repo .
python3 scripts/detect_learning_progress.py --repo . --pretty
python3 -m unittest scripts.tests.test_detect_learning_progress -v
python3 scripts/generate_course_tutorials.py --check
```

默认输出紧凑的 `progress-scan.v1` JSON；`--pretty` 仅供人工检查。输出包含当前阶段、当前周、周计划、占位符、缺失链接、越序进展、规则/进度指纹和建议路由。

状态判断保持保守：脚本只能在周状态已完成、成果与验证齐全，并存在“讲师结论：通过、Teach-back 已完成、变体任务已完成”时识别为 `PASSED`。语义评审仍由 REVIEW/FULL Prompt 负责。

课程教程生成器只写入 `learning-plan/tutorials/`，不修改阶段计划、周状态、成果或笔记。阶段表格发生变化后先运行生成命令，再用 `--check` 验证生成文件未漂移。
