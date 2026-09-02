# Prompt 目录

本目录只存放课程仓库自身使用、经过验证且可以重复执行的监督 Prompt，不保存学习者的 Prompt 成果或个人上下文。

建议按周或场景组织：

- `progress-detection.md`：Hermes 进度识别的低 Token 模式路由入口。
- `progress-detection-fast.md`：每日督促，只读取扫描 JSON 和当前周近期笔记。
- `progress-review.md`：周验收，只读取当前周成果和讲师评分证据。
- `progress-detection-full.md`：首次扫描、阶段考试和状态冲突时的完整语义识别。

学习者在课程实践中编写的 Prompt 使用 [`templates/learner-repository/prompts/README.md`](../templates/learner-repository/prompts/README.md) 初始化，并只保存在个人仓库。

每个 Prompt 应说明用途、所需输入、约束、期望输出、版本、关联 Eval 数据集和至少一个验证记录。仓库级自动化 Prompt 还必须说明指令层级、只读/写入边界、间接 Prompt Injection 防护、错误处理和机器可解析输出。已发布 Agent 引用不可变 Prompt 版本，不能直接覆盖线上内容。不得包含真实 API Key、Cookie、Token 或敏感业务数据。

Hermes 默认只加载路由入口和被选中的一种模式，不要在同一次调用中加载 FAST、REVIEW、FULL 三份 Prompt。
