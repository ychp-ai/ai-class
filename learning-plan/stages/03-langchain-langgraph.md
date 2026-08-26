# 阶段三：LangChain 与 LangGraph

周期：第 9–11 周，共约 21 小时。

目标：使用 LangChain 构建结构化 Agent，并使用 LangGraph 实现状态、路由、审批和恢复。

## 开始前应会什么

- 能解释手写 Java Agent 的计划、动作、观察、停止和失败状态。
- 能阅读函数、集合、异常和单元测试；不要求已有 Python、Pydantic 或异步经验。
- 能说明确定性路由、权限和副作用控制必须由代码负责。

## 零基础桥接

先用 15–30 分钟完成 `venv → Python 类型标注 → Pydantic 模型校验 → async for` 最小脚本。随后用第 8 周手写 Java Agent 对照 LangChain 的模型、消息、Tool 和 Agent 抽象，再用第 8 周显式状态机对照 LangGraph 的 State、Node、Edge 和 Checkpoint。

## 本阶段不要求什么

- 不要求系统学习全部 Python 语法、LangChain 历史 API 或第三方集成目录。
- 不要求把所有条件判断交给模型，也不要求用 LangGraph 替代业务数据库。
- 不要求在本阶段解决操作系统沙箱、多租户平台和生产级消息队列。

## 前测失败处理

若 Python 脚本、虚拟环境或异常处理不能独立运行，先完成一个类型化纯函数及 pytest 练习；若手写 Agent 状态不清楚，先画出三状态循环并为非法转换写测试，再学习 LangChain/LangGraph。

## 第 9 周：Python 与 LangChain 基础

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 学习虚拟环境、类型标注、异步和环境变量 | 只补本计划需要的 Python；亲手实现一次 `async for`，理解流式 Agent 消息如何消费 | 独立运行异步 Python 脚本 |
| 周二 | LangChain 模型与消息接口 | 先用最简单模型调用，打印消息对象而不只打印文本；确认当前版本 API | 调用 Claude 或 OpenAI 模型 |
| 周三 | Pydantic 结构化输出 | 先定义字段约束和错误样例，再让模型生成；测试枚举、空列表和缺失字段 | 返回可校验的 `TaskPlan` |
| 周四 | 使用 `@tool` 定义工具 | 函数签名和 Docstring 要表达约束；先写纯函数测试，再注册为工具 | 工具可脱离模型单测 |
| 周五 | 使用 `create_agent` | 准备“必须调用、不得调用、工具失败”三类问题，观察 Agent 停止条件 | Agent 自主决定是否调用工具 |
| 周六 | 动态 Context、超时和错误处理 | Context 只传依赖和身份信息，不塞进 Prompt；分别模拟模型与工具超时 | 非法输入不会导致进程崩溃 |
| 周日 | 完成个人任务助手 | 在干净虚拟环境重装并运行，补充一条与手写 Java Agent 的实测差异 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add typed langchain agent and tool tests`

必须包含：

- `python-agent` 的依赖文件和启动说明。
- 至少两个工具及其单元测试。
- Pydantic `TaskPlan` 和结构化输出测试。
- 一个成功任务、一个无需工具任务和一个工具失败示例。
- `notes/week-09.md`：与手写 Java Agent 的对比。

验收标准：全新虚拟环境能安装并运行；输出 Schema 不合法时有重试或明确失败；工具异常不会悄悄变成成功结果。

## 第 10 周：LangChain RAG 与业务 Agent

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 加载和切分文档 | 尽量复用第 6 周资料与切片规则；打印元数据确认两个框架语义一致 | Chunk 元数据完整 |
| 周二 | 复用 Qdrant 或建立实验索引 | 为实验使用独立 Collection 或命名空间，避免覆盖 Spring AI Baseline | 完成语义检索 |
| 周三 | 将 Retriever 暴露为工具 | 工具返回受控长度的片段与来源；准备无需检索的问题检查误调用 | Agent 自主判断是否检索 |
| 周四 | 增加受限文件工具 | 复用第 7 周安全用例，不因换成 Python 就降低路径校验标准 | 保持只读和路径限制 |
| 周五 | 返回结构化引用 | 用 Pydantic 约束答案与引用；程序验证引用是否属于实际召回集合 | 回答关联来源 |
| 周六 | 对比 Spring AI 与 LangChain | 用同一数据、问题、模型和指标；区分开发体验与回答质量 | 完成职责和 API 对比 |
| 周日 | 使用相同问题集验证 | 保存完整成功与失败结果，不根据结果临时替换问题；总结选择建议 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: build langchain rag agent with structured citations`

必须包含：

- LangChain RAG Agent 和 Retriever 工具。
- 与 Spring AI 使用同一批文档和 5 条问题的结果。
- `docs/spring-ai-vs-langchain.md`，对比模型接口、工具、RAG、Agent、测试和适用场景。
- 至少一个“模型不应检索”的问题和一个资料不足的拒答案例。

验收标准：对比基于运行结果而非框架宣传；两种实现的输入数据和评测问题一致；引用能够回到原文件。

## 第 11 周：LangGraph 状态与可控工作流

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | State、Node、Edge | 先用不调用 LLM 的普通函数搭图，理解 State 更新和节点边界后再接模型 | 完成三节点顺序图 |
| 周二 | 条件边与任务分类 | 明确规则能判断的情况用代码路由，只把模糊语义分类交给模型 | 不同任务进入不同分支 |
| 周三 | 循环、最大步骤和失败分支 | 在 State 保存显式计数和错误类型，人为构造循环验证停止逻辑 | 异常不会无限循环 |
| 周四 | Checkpoint 和会话状态 | 使用稳定 thread/session ID；在进程退出后恢复，不能只在同一内存运行中测试 | 中断后可以恢复 |
| 周五 | Human-in-the-loop | 在副作用前中断；审批信息应展示计划、目标文件、命令和风险 | 写操作前暂停等待审批 |
| 周六 | 将 LangChain Agent 作为节点 | Agent 节点只负责开放式判断，鉴权、路由和状态转换仍由普通节点控制 | 确定性步骤与 Agent 共存 |
| 周日 | 完成任务路由工作流 | 运行批准、拒绝、超时、恢复四种情形，并对照状态图检查实际路径 | 完成阶段提交 |

### 本周提交

建议 Commit：`feat: add checkpointed langgraph workflow with approval gate`

必须包含：

- 只读分析、待审批写操作、拒绝三条路径。
- Checkpoint 配置和恢复示例。
- 批准、拒绝、超时、恢复四类测试或运行记录。
- Mermaid 或其他状态图。
- `docs/langgraph-workflow.md`：State Schema、节点职责、路由条件和停止条件。

验收标准：写操作在批准前没有副作用；同一任务恢复后状态一致；路由逻辑可以用普通单元测试验证。

## 阶段出口条件

- 能使用类型标注、Pydantic 和异步 API 编写基础 Python Agent。
- LangChain Agent 能正确处理工具成功、工具失败和无需工具三类任务。
- 能解释 LangChain 与 Spring AI 的选择依据。
- LangGraph 工作流可以暂停、拒绝和恢复。
- 确定性业务规则由代码控制，而不是全部交给模型判断。

## 学习建议

- 不要同时学习 LangChain 的大量历史 API，以当前 `create_agent` 和 LangGraph 文档为主。
- State 只保存后续节点确实需要的数据，避免把完整原始输出无限累积。
- 路由规则可以确定时用普通代码；只有语义分类确实需要模型时才调用 LLM。
- 为每个节点单独测试，再测试完整图。
- LangGraph 解决执行编排问题，不提供操作系统隔离。

官方资料：[LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)、[LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)、[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)

下一阶段：[Claude Agent SDK](04-claude-agent-sdk.md)
