# 每周课程成果要求与复制模板

本目录保存第 1–32 周主线与第 33–40 周 Super-agent 强化的公共成果要求和空白验收模板，不保存任何学习者的当前状态、成果链接、评分或个人证据。每位学习者应把个人记录放在独立仓库的 `deliverables/week-XX/README.md`。

首次建立个人仓库时运行：

```bash
python3 scripts/init_learning_progress.py \
  --course-repo . \
  --progress-repo ../ai-class-note
```

脚本从 [`templates/learner-repository`](../templates/learner-repository/README.md) 复制通用文档，并从本目录读取 32 周主题。个人源码、设计、业务材料、数据和运行证据都写入个人仓库的对应职责目录，不回写课程仓库。

选择原主线毕业后的强化课程时，初始化和后续扫描均添加 `--include-super-agent`，覆盖 40 周；重复初始化只新增缺失模板，保留已有个人记录。原毕业与专项通过分别评审，不能由目录是否存在推断。

周提交标准见[成果与提交标准](../learning-plan/06-deliverable-standards.md)。

## 课程周要求索引

| 周次 | 主题 | 目录 |
| --- | --- | --- |
| 1 | LLM 工程基础 | [week-01](week-01/README.md) |
| 2 | 原生模型 API 与 Tool Loop | [week-02](week-02/README.md) |
| 3 | Prompt 与 AI 编程协作 | [week-03](week-03/README.md) |
| 4 | 测试、排错与架构表达 | [week-04](week-04/README.md) |
| 5 | Spring AI Chat | [week-05](week-05/README.md) |
| 6 | Spring AI RAG | [week-06](week-06/README.md) |
| 7 | Spring AI Tool Calling | [week-07](week-07/README.md) |
| 8 | 手写 Java Agent | [week-08](week-08/README.md) |
| 9 | LangChain Agent | [week-09](week-09/README.md) |
| 10 | LangChain RAG | [week-10](week-10/README.md) |
| 11 | LangGraph Workflow | [week-11](week-11/README.md) |
| 12 | Claude Agent SDK | [week-12](week-12/README.md) |
| 13 | Claude 权限、Hooks 与 MCP | [week-13](week-13/README.md) |
| 14 | Java/Python 组合 | [week-14](week-14/README.md) |
| 15 | Eval 与 Trace | [week-15](week-15/README.md) |
| 16 | 首个 AI 应用交付 | [week-16](week-16/README.md) |
| 17 | 平台架构 | [week-17](week-17/README.md) |
| 18 | Agent Registry | [week-18](week-18/README.md) |
| 19 | Model Gateway 与本地模型 | [week-19](week-19/README.md) |
| 20 | Tool/MCP/进阶 RAG 管理 | [week-20](week-20/README.md) |
| 21 | Workflow Definition | [week-21](week-21/README.md) |
| 22 | Durable Runtime | [week-22](week-22/README.md) |
| 23 | 权限、审批与安全 | [week-23](week-23/README.md) |
| 24 | Eval、SLO 与运维 | [week-24](week-24/README.md) |
| 25 | 业务场景发现 | [week-25](week-25/README.md) |
| 26 | AS-IS 与根因分析 | [week-26](week-26/README.md) |
| 27 | TO-BE 与价值设计 | [week-27](week-27/README.md) |
| 28 | 接入与试点设计 | [week-28](week-28/README.md) |
| 29 | 业务系统集成 | [week-29](week-29/README.md) |
| 30 | UAT 与业务试点 | [week-30](week-30/README.md) |
| 31 | 生产硬化 | [week-31](week-31/README.md) |
| 32 | 平台和业务最终交付 | [week-32](week-32/README.md) |

## Super-agent 强化成果要求

| 周次 | 主题 | 目录 |
| --- | --- | --- |
| 33 | 需求、独立设计与单会话基线 | [week-33](week-33/README.md) |
| 34 | 多任务调度与隔离 | [week-34](week-34/README.md) |
| 35 | 事件接入与主动触发 | [week-35](week-35/README.md) |
| 36 | 跨渠道身份与上下文 | [week-36](week-36/README.md) |
| 37 | 中途纠正、取消与撤权 | [week-37](week-37/README.md) |
| 38 | 多任务持久恢复与副作用核对 | [week-38](week-38/README.md) |
| 39 | 持续运行与运维 | [week-39](week-39/README.md) |
| 40 | 对照评测与独立交付 | [week-40](week-40/README.md) |
