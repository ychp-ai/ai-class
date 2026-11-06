# 学习进度识别入口

## Catalog Metadata

```yaml
name: learning-progress-router
version: 3.1.0
status: draft
updated: 2026-11-06
model_target: [Hermes Agent, general tool-using coding agent]
audit_status: pending_model_regression
last_audit: 2026-09-02
owner: repository-maintainer
```

## 模式选择

Hermes 拉取仓库或定时唤醒后，先运行：

```bash
python3 scripts/detect_learning_progress.py \
  --repo <课程仓库> \
  --progress-repo <个人仓库>
```

默认范围为 32 周。学习者明确选择强化后，命令追加 `--include-super-agent`；将该选项传给后续 FAST/REVIEW/FULL，每次重扫均沿用，不按目录数量推断。范围变化必须升级 FULL 并重新解释进度分母。

脚本输出 `progress-scan.v2` 精简 JSON，并显式区分课程规则与个人证据。根据触发场景选择 Prompt：

| 场景 | 使用文件 | 读取范围 |
| --- | --- | --- |
| 日常督促，且 `requires_full_review=false` | `progress-detection-fast.md` | 扫描 JSON、当前周笔记 |
| 周日验收或 `READY_FOR_REVIEW` | `progress-review.md` | 当前周成果、验证、失败和讲师记录 |
| 首次拉取、阶段考试、BLOCKED、INCONSISTENT、规则变化 | `progress-detection-full.md` | 当前阶段和冲突所需语义证据 |

## 路由规则

```text
先运行确定性扫描器；核对 course_scope 与 total_weeks 是否符合已选择范围。
范围变化或 rules_fingerprint 变化：使用 FULL。
COMPLETED 只代表当前选定范围，不能把 core 完成解释为强化通过。

如果 repository_status=INVALID：
  使用 FULL，修复仓库结构识别问题。

如果触发类型是 INITIAL_SCAN 或 STAGE_EXAM：
  使用 FULL。

如果 recognized_status=READY_FOR_REVIEW：
  使用 REVIEW。

如果 recognized_status=BLOCKED 或 INCONSISTENT：
  使用 FULL。

如果 requires_full_review=false：
  使用 FAST。
```

默认不把三个 Prompt 同时放入模型上下文。course_scope 与规则文件指纹均没有变化时，不重复读取完整讲师规范；进度指纹没有变化时，可直接提示“仓库进度无变化”，但仍需正常提醒学习者。

## 验证记录

- 2026-09-02 双仓改造人工复核通过：路由输入已显式区分课程仓库与个人仓库，扫描器回归测试通过。
- 2026-08-24 自动审查通过，无 Critical/High/Medium 风险。
- 自动工具提示缺少否定约束；人工复核确认路由规则已明确禁止同时加载三种模式，实际安全边界由被选中的 Prompt 定义。
- 尚未验证 Hermes 实际定时任务的模式选择稳定性。

## 2026-11-06 范围扩展验证

本版本新增 32/40 周范围传递，状态为草稿；旧版本审查不代表本次已审查。回归使用 `scripts/tests/test_detect_learning_progress.py` 的固定合成状态夹具与范围边界案例，检查扫描器输出；运行结果见脚本验证记录。尚未进行真实 Hermes/LLM 模式选择和评分回归，不能据此发布或自动替换外部已部署 Prompt。
