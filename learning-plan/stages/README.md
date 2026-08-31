# 阶段学习计划目录

本目录存放 32 周路线的九个阶段计划。每个阶段都包含逐日任务、当天学习建议、每日验收、周提交和阶段出口条件。

阶段计划回答“何时学什么”；配套的[逐节课程教程](../tutorials/README.md)回答每一节“为什么学、这个是什么、怎么学、怎么验证学会了”，并提供卡住后使用的参考答案。教程不保存学习状态，也不替代本目录的四列表格和阶段出口。

课程面向具备开发基础、AI 零基础的学习者。九个阶段统一提供“开始前应会什么、零基础桥接、本阶段不要求什么、前测失败处理”，用于按需补齐语言、框架、平台或业务方法，但不改变周次、必修框架、独立成果和阶段出口标准。

| 阶段 | 周次 | 文档 |
| --- | --- | --- |
| AI 原理、原生 API 与工程协作 | 1–4 | [01-ai-tools-and-engineering.md](01-ai-tools-and-engineering.md) |
| Java LLM、RAG 与 Agent | 5–8 | [02-java-llm-rag-agent.md](02-java-llm-rag-agent.md) |
| LangChain 与 LangGraph | 9–11 | [03-langchain-langgraph.md](03-langchain-langgraph.md) |
| Claude Agent SDK | 12–13 | [04-claude-agent-sdk.md](04-claude-agent-sdk.md) |
| 组合、评测与首个应用 | 14–16 | [05-integration-evaluation-delivery.md](05-integration-evaluation-delivery.md) |
| AI 平台核心 | 17–20 | [06-ai-platform-core.md](06-ai-platform-core.md) |
| 工作流编排与平台治理 | 21–24 | [07-workflow-governance.md](07-workflow-governance.md) |
| 业务场景与流程设计 | 25–28 | [08-business-scenario-process.md](08-business-scenario-process.md) |
| 试点上线与最终交付 | 29–32 | [09-pilot-production-capstone.md](09-pilot-production-capstone.md) |

阶段文档只存放计划和验收要求。源码、正式设计、业务案例、数据和周验收证据分别放入仓库根目录下的对应成果目录。

框架学习是必修项，不能被平台建设替代：

- Spring AI：第 5–8 周学习，第 17–24 周用于平台控制面、模型网关、工具和观测。
- LangChain：第 9–10 周学习，第 17–24 周用于 Agent 运行时和工具抽象。
- LangGraph：第 11 周学习，第 21–24 周用于工作流编译、Checkpoint、审批和恢复。
- Claude Agent SDK：第 12–13 周学习，第 20–24 周用于受控执行、MCP、权限和审计。
