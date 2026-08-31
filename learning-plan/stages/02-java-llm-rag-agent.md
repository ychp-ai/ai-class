# 阶段二：Java LLM、RAG 与 Agent

周期：第 5–8 周，共约 28 小时。

目标：使用 Java 21、Spring Boot 和 Spring AI 完成从模型调用到可控 Agent 的最小闭环。

逐节学习入口：[第 5–8 周课程教程](../tutorials/README.md)。

## 本阶段语言定位

第 5–8 周必须使用 Java 21、Maven、Spring Boot 和 Spring AI。目标不是重做 Python 示例，而是把第 1–4 周观察到的原生协议迁移为可测试的 Java 业务服务，并明确 Spring AI 替代了哪些样板、没有替代哪些权限和失败控制；切换桥接见[开发语言路线](../01-language-roadmap.md)。

## 开始前应会什么

- 能解释第 2 周原生模型请求、流式事件、结构化输出和 Tool Loop 的输入输出。
- 能阅读 Java 方法、DTO 和异常，使用 Maven 运行测试；不要求熟悉完整 Spring 生态。
- 能说明环境变量、HTTP API 和确定性参数校验为什么不能交给模型。

## 零基础桥接

用 15–30 分钟建立一个只含健康检查和单元测试的 Java 21/Spring Boot 项目，再把原生模型客户端的“请求构造、调用、响应解析、错误处理”逐项映射到 Spring AI 的 ChatClient、结构化输出和 Tool Calling。每引入一个 Spring AI 抽象，都要指出它替代了第 2–4 周的哪段代码。

## 本阶段不要求什么

- 不要求先学完整 Spring Cloud、响应式编程体系或所有 Spring AI Provider。
- 不要求训练模型、优化向量数据库规模或构建通用 Agent 平台。
- 不要求记忆 Starter 和 API 历史版本，只使用当前官方接口完成最小闭环。

## 前测失败处理

若 Java/Maven/Spring Boot 基础不足，先完成“健康检查 + DTO 校验 + 一个失败单测”桥接；若无法解释原生 Tool Loop，则回到第 2 周用纸面时序复盘后再引入 `@Tool`。

## 第 5 周：Spring Boot 与大模型 API

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 初始化 Java 21 + Maven + Spring Boot | 只引入 Web 和基础测试依赖，先保证空项目与健康检查稳定，再增加 AI 依赖<br>相关资料：[Spring Boot Reference](https://docs.spring.io/spring-boot/reference/) | 健康检查可访问 |
| 周二 | 引入 Spring AI 模型 Starter | 使用官方 BOM 和当前文档；先配置 `.env.example`，再设置本地环境变量<br>相关资料：[Spring AI Getting Started](https://docs.spring.io/spring-ai/reference/getting-started.html) | API Key 仅来自环境变量 |
| 周三 | 实现 Chat API 或 CLI | 保持 Controller/CLI 薄，模型调用放在 Service；记录一次原始请求和响应结构<br>相关资料：[Spring AI ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html) | 完成一次真实模型调用 |
| 周四 | System Prompt 与结构化输出 | 先定义 Java DTO 和校验规则，再写 Prompt；主动测试字段缺失和类型错误<br>相关资料：[Spring AI Structured Output](https://docs.spring.io/spring-ai/reference/api/structured-output.html) | 返回值能被 Java 对象解析 |
| 周五 | 实现流式响应 | 用命令行客户端观察分块，关注断连、首 Token 延迟和流结束信号<br>相关资料：[Spring AI ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html) | 客户端逐步接收内容 |
| 周六 | 处理超时、限流、空响应和模型错误 | 使用 Stub 或错误配置稳定复现失败，不要等待真实服务偶然报错<br>相关资料：[Resilience4j Guide](https://resilience4j.readme.io/docs/getting-started) | 有统一异常和日志 |
| 周日 | 记录耗时、模型和 Token | 把运行、测试、配置和一次失败结果补进周成果，提交前检查密钥<br>相关资料：[Spring AI Observability](https://docs.spring.io/spring-ai/reference/observability/index.html) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add spring ai chat api with streaming and error handling`

必须包含：

- 可启动的 `java-service` 模块。
- 普通和流式问答入口。
- `.env.example` 或配置说明，不提交真实密钥。
- 至少一个结构化输出测试和一个错误处理测试。
- `notes/week-05.md`，记录模型、耗时和一次失败调用。

验收标准：新环境按 README 能启动；错误不会以未处理堆栈直接返回给用户；密钥扫描无泄漏。

## 第 6 周：RAG 最小闭环

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 理解解析、切片、索引、检索和生成 | 为每一步写清输入输出和可能失败点，区分检索质量与生成质量<br>相关资料：[Spring AI RAG](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html) | 绘制 RAG 流程图 |
| 周二 | 准备 5–10 个文档或代码文件 | 选自己能判断答案的资料，提前写 5 个问题和预期来源，避免事后挑题<br>相关资料：[RAG 资料目录](../../data/docs/README.md) | 放入 `data/docs` |
| 周三 | 文档解析与切片 | 先打印 Chunk 人工检查，不要只看数量；保留标题、路径和位置元数据<br>相关资料：[Spring AI ETL Pipeline](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html) | Chunk 带路径、位置和序号 |
| 周四 | 生成 Embedding 并写入 Qdrant | 使用稳定文档 ID，先考虑重建策略；重复执行前后比较记录数<br>相关资料：[Qdrant Points](https://qdrant.tech/documentation/concepts/points/) | 能重复构建索引 |
| 周五 | 实现 TopK 检索 | 暂时不生成答案，只观察召回片段和分数，记录漏召回与干扰项<br>相关资料：[Spring AI Vector Databases](https://docs.spring.io/spring-ai/reference/api/vectordbs.html) | 输出片段、来源和分数 |
| 周六 | 生成带引用回答并加入拒答 | Prompt 明确只能使用上下文；引用由程序关联元数据，不让模型随意编文件名<br>相关资料：[Spring AI RAG](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html) | 资料不足时不编造 |
| 周日 | 使用 5 条问题检查召回 | 固定问题、TopK 和模型配置后再测试，失败项完整保存<br>相关资料：[Stanford IR Book：检索评测](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: implement spring ai rag pipeline with citations`

必须包含：

- 文档扫描、切片、索引构建和检索代码。
- 索引重建命令或 API。
- 5 条固定问题及预期来源。
- 每次回答返回引用；无可靠来源时拒答。
- `docs/rag-design.md`：切片策略、TopK、局限和失败案例。

验收标准：5 条问题至少 4 条召回正确来源；重复建索引不会产生无法解释的数据膨胀；引用能定位到原文件。

## 第 7 周：Tool Calling 与权限边界

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 理解工具选择、参数生成和结果回传 | 画出模型与应用的责任边界，明确模型只能请求工具，真正执行由代码负责<br>相关资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) | 绘制 Tool Calling 流程 |
| 周二 | 使用 `@Tool` 定义 `listFiles` | 描述工具何时使用和不适用；直接调用 Java 方法完成单元测试后再接模型<br>相关资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) | 工具描述和 Schema 清晰 |
| 周三 | 增加 `readFile` 与 `searchDocs` | 设计问题分别触发三个工具，也准备一个完全不应调用工具的问题<br>相关资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) | 模型能选择正确工具 |
| 周四 | DTO、参数校验和错误处理 | 在工具入口校验，不依赖模型自觉；错误信息要可操作但不暴露内部路径<br>相关资料：[Spring AI Schema Validation](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html) | 非法输入得到稳定错误 |
| 周五 | 路径规范化和目录白名单 | 测试 `../`、绝对路径、符号链接和编码变体，比较规范化前后路径<br>相关资料：[OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal) | 无法越界读取 |
| 周六 | 完成一次多工具任务 | 限制最大工具调用次数，保存每次参数、结果状态和耗时<br>相关资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) | 工具顺序和结果可追踪 |
| 周日 | 威胁建模和安全复盘 | 从资产、入口、攻击方式和防护四方面整理，不把 Prompt 当安全边界<br>相关资料：[OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add read-only ai tools with path allowlist`

必须包含：

- `listFiles`、`readFile`、`searchDocs` 三个只读工具。
- 正常、非法参数、路径穿越和越界访问测试。
- 工具调用日志，包含工具名、结果状态和耗时。
- `docs/tool-security.md`：权限边界和威胁清单。

验收标准：`../`、绝对路径和符号链接等越界方式被处理；错误结果不会暴露敏感路径或凭证。

## 第 8 周：手写 Java Agent

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 学习 Plan–Act–Observe | 用纸面模拟两轮循环，明确完成、失败和继续三个判断，不急着写代码<br>相关资料：[ReAct 论文](https://arxiv.org/abs/2210.03629) | 画出 Agent 循环 |
| 周二 | 生成结构化任务计划 | 步骤必须包含动作和验收条件；限制步骤数量并测试无法解析的计划<br>相关资料：[Spring AI Structured Output](https://docs.spring.io/spring-ai/reference/api/structured-output.html) | 计划可被 Java 对象解析 |
| 周三 | 设计任务、步骤和运行日志对象 | 先定义状态机，避免用多个布尔值组合出矛盾状态；为状态转换写测试<br>相关资料：[W3C SCXML 状态机规范](https://www.w3.org/TR/scxml/) | 状态转换明确 |
| 周四 | 调用文件与检索工具完成任务 | 只做只读任务，把 Agent 与工具本身的错误分开记录<br>相关资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) | 完成只读分析任务 |
| 周五 | 记录模型、工具、观察和结果 | 日志保存必要摘要和关联 ID，不记录密钥或无限增长的完整上下文<br>相关资料：[OpenTelemetry Logs](https://opentelemetry.io/docs/specs/otel/logs/) | 可复盘每一步 |
| 周六 | 最大步数、超时、重试和人工中断 | 人为制造循环与工具失败，验证限制真正生效；重试只针对可恢复错误<br>相关资料：[Resilience4j Guide](https://resilience4j.readme.io/docs/getting-started) | Agent 不会无限循环 |
| 周日 | 完成 README 整理 Agent | 演示一次成功、一次失败和一次超限，按阶段出口条件自检<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成阶段提交 |

### 本周提交

建议 Commit：`feat: implement bounded java agent loop with run logs`

必须包含：

- `AgentTask`、`AgentStep`、`AgentRunLog` 等状态对象。
- 最大步骤、整体超时、有限重试和取消机制。
- 至少一个成功任务、一个工具失败和一个超限测试。
- 一份完整执行日志，能还原每个 Action 和 Observation。

验收标准：Agent 达到停止条件后不会继续调用模型；失败状态明确；日志中不记录密钥和完整敏感内容。

## 阶段出口条件

- Spring AI Chat API 支持普通与流式输出。
- RAG 回答有来源，资料不足时拒答。
- 三个只读工具有参数与路径安全测试。
- 手写 Agent 有边界、日志、超时和停止条件。
- 能解释 Tool Calling 与 Agent 的区别。

## 学习建议

- Spring Boot 和 Spring AI 依赖通过官方 BOM 管理，不在计划中固定易过期版本。
- 第一次 RAG 使用少量干净文档，先验证闭环再扩大数据量。
- 先记录原始检索结果，再讨论回答质量，避免把召回问题误判成模型问题。
- 工具函数应当可以脱离 LLM 独立测试。
- 手写 Agent 的目的不是生产使用，而是理解高级框架替你做了什么。

官方资料：[Spring AI Reference](https://docs.spring.io/spring-ai/reference/)、[Qdrant Documentation](https://qdrant.tech/documentation/)

下一阶段：[LangChain 与 LangGraph](03-langchain-langgraph.md)
