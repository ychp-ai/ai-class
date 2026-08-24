# Prompt 目录

本目录存放经过验证、可以重复使用的 Prompt，而不是临时聊天内容。

建议按周或场景组织：

- `progress-detection.md`：Hermes 进度识别的低 Token 模式路由入口。
- `progress-detection-fast.md`：每日督促，只读取扫描 JSON 和当前周近期笔记。
- `progress-review.md`：周验收，只读取当前周成果和讲师评分证据。
- `progress-detection-full.md`：首次扫描、阶段考试和状态冲突时的完整语义识别。
- `week-03.md`：Prompt 基础、版本和固定回归练习。
- `coding.md`：需求拆解、实现、测试和代码审查。
- `rag.md`：检索问答、引用和拒答。
- `agent.md`：任务规划、权限和验收要求。

每个 Prompt 应说明用途、所需输入、约束、期望输出、版本、关联 Eval 数据集和至少一个验证记录。仓库级自动化 Prompt 还必须说明指令层级、只读/写入边界、间接 Prompt Injection 防护、错误处理和机器可解析输出。已发布 Agent 引用不可变 Prompt 版本，不能直接覆盖线上内容。不得包含真实 API Key、Cookie、Token 或敏感业务数据。

Hermes 默认只加载路由入口和被选中的一种模式，不要在同一次调用中加载 FAST、REVIEW、FULL 三份 Prompt。
