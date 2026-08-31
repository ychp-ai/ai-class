# 开发语言路线与切换策略

## 路线结论

本课程采用 **Java 21 为平台主语言、Python 3.11+ 为 AI 执行语言、TypeScript/React 为可选控制台语言** 的组合路线。学习顺序不是同时学习三门语言，而是先用 Python 建立 AI 原理和原生协议直觉，再用 Java 建设业务与平台控制面，随后回到 Python 学习 Agent 运行时，最终通过稳定协议组合两端。

如果只能选择一种语言开始第 1 周，默认选择 Python；如果只能选择一种语言承担最终平台的主要工程职责，默认选择 Java。

## 每种语言负责什么

| 语言 | 课程职责 | 主要目录 | 不负责什么 |
| --- | --- | --- | --- |
| Python 3.11+ | 第 1–4 周可观察实验、原生模型调用；LangChain、LangGraph、Claude Agent SDK 和 Agent Worker | `python-agent/`、`sandbox-workspaces/` | 不承载平台权限、租户、版本和 Secret 管理真相 |
| Java 21 | Spring Boot/Spring AI、平台 API、模型网关、资源版本、权限审批、业务 Connector 和控制面 | `java-service/` | 不替代 LangGraph/Claude Agent SDK 的专用执行运行时 |
| TypeScript/React | Agent、Workflow、Run、审批和 Eval 的最小管理控制台 | `platform-console/` | 不复制服务端权限、状态机和长期凭证 |

PostgreSQL、Docker Compose、Shell 和 YAML 是必要的工程配套，不作为新的主学习语言。SQL 只补当前数据任务所需内容；Shell 只用于可审计的启动、测试和排错命令。

## 32 周语言地图

| 周次 | 默认语言重点 | 学习目的 | 切换验收 |
| --- | --- | --- | --- |
| 1–4 | Python 3.11+ | 用较少样板观察 Token、Embedding、流式事件、结构化输出和手写 Tool Loop | 能运行 pytest；能解释请求、事件、异常和停止条件；记录 Python 与依赖版本 |
| 5–8 | Java 21 | 用 Spring Boot/Spring AI 建立业务 API、RAG、Tool 和手写 Java Agent | 能运行 Maven 测试；能将第 2–4 周原生能力映射到 Java 实现 |
| 9–13 | Python 3.11+ | 学习类型化 Agent、异步消息、LangGraph 状态恢复和 Claude Agent SDK | 能使用类型标注、Pydantic、`async for` 和 pytest；能与 Java Agent 比较状态和失败模式 |
| 14–16 | Java + Python | 用版本化 Schema、traceId、超时、取消和错误码组合控制面与执行面 | 同一契约两端校验一致；任一端失败都不会显示假成功 |
| 17–24 | Java 主导，Python 执行 | Java 建平台控制面，Python 运行工作流和执行型 Agent；TypeScript 只做最小界面 | 权限和版本由 Java 执行路径控制；Python 只消费已授权发布快照 |
| 25–28 | 语言中立，复用现有栈 | 完成业务调研、AS-IS/TO-BE 和接入设计，必要时用现有栈做 Spike | 不为画原型引入新语言；接口、数据、权限和兜底可映射到现有平台 |
| 29–32 | Java + Python，按需 TypeScript | 完成 Connector、E2E、UAT、试点、生产硬化和最终发布 | 从业务入口到 Agent 执行、审批、回写、Trace 和回滚全部可验证 |

## 语言切换桥接

每次切换只安排一个 15–30 分钟桥接任务，不把课程变成通用语言培训：

1. 第 1 周前：建立虚拟环境，运行一个带类型标注、HTTP/JSON 和失败分支的 Python 脚本及测试。
2. 第 5 周前：建立 Java 21/Maven/Spring Boot 健康检查，完成 DTO 校验和一个失败单测。
3. 第 9 周前：完成 `venv → 类型标注 → Pydantic → async for → pytest` 最小闭环。
4. 第 14 周前：让 Java DTO 与 Python Pydantic Model 校验同一份 JSON Schema，并各自拒绝一条非法输入。
5. 第 17 周后：只有管理流程确实需要界面时才补 React/TypeScript；先保证 API 和状态真相正确。

桥接任务失败时，缩小当天 AI 目标并补齐当前所需语法；不得同时补完整语言教程、框架和多个 AI 新概念。已有语言经验可以加快桥接，但不能跳过运行、测试和失败证据。

## 统一实现与对比规则

- 第 1–4 周默认使用 Python，避免不同语言样板影响对 AI 协议的观察；若学习者坚持使用熟悉语言，必须保留相同输入、模型、参数、失败案例和验收口径，并在第 9 周前补齐 Python 桥接。
- 第 5–8 周的 Spring AI 和 Java Agent 成果必须使用 Java，不以 Python 等价实现替代。
- 第 9–13 周的 LangChain、LangGraph 和 Claude Agent SDK 成果必须使用 Python，不以 Java 包装调用替代。
- 第 14 周至少保留一个 Java/Python 契约对照测试，证明语言边界由 Schema 而非自由文本约定连接。
- 确定性权限、预算、幂等和副作用控制由平台普通代码实现；不得因为 Python Agent 更灵活就把控制面责任下放给模型或 Prompt。
- TypeScript 控制台是最小交互层。浏览器隐藏按钮、前端校验和页面状态不能作为权限或运行状态的最终证据。

## 语言能力验收证据

语言本身不单独计为课程成果，但不能成为无法解释的黑盒。每次周成果涉及代码时至少记录：

- 运行时、构建工具和关键依赖版本。
- 一条启动或测试命令，以及实际退出状态。
- 一个正常输入和一个语法之外的工程失败案例，例如 Schema 校验、超时、取消或权限拒绝。
- 当前语言/框架替代了前一阶段哪些样板，又新增了哪些状态和失败模式。
- 学习者能够改变一个输入或约束独立完成小型变体，而不是只复制参考代码。

语言熟练度不足只说明需要桥接，不降低 AI 原理、平台治理和业务交付的阶段出口标准。
