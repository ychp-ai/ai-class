# AI 学习计划：程序员从入门到项目落地

这是一份面向程序员的 AI 学习计划，按照 **每天 1 小时、12 周** 设计。路线不是纯算法研究，而是以真实岗位需求为导向，从 AI 工具使用逐步过渡到 LLM API、RAG、工具调用、Agent、评估、可观测性和最终项目落地。

最终目标不是“学过一些概念”，而是完成一个可以放到简历和 GitHub 上展示的项目：

> **AI Dev Knowledge Assistant：面向代码库和技术文档的 AI 知识助手**

它需要支持代码/文档解析、索引、混合检索、RAG 问答、来源引用、工具调用、执行日志、评测集、基础安全治理和项目说明文档。

## 最终完成目标

### 项目名称

AI Dev Knowledge Assistant

### 项目定位

一个面向程序员的 AI 知识助手。它可以读取一个代码仓库或一批技术文档，回答和项目有关的问题，并给出来源引用。

典型问题：

- 这个接口在哪里实现？
- 这个字段从哪里传进来？
- 这个功能的调用链是什么？
- 修改这个模块可能影响哪些地方？
- 这份文档里关于权限校验的规则是什么？
- 当前项目有哪些 TODO、风险点或缺少测试的模块？

### 必须完成的功能

| 模块 | 必须能力 | 验收标准 |
| --- | --- | --- |
| 文档/代码读取 | 支持读取 Markdown、文本、常见代码文件 | 可以扫描一个本地目录并生成文件清单 |
| 文本切片 | 按文件、标题、函数或固定长度切分内容 | 每个 chunk 包含来源路径、位置和内容 |
| 向量索引 | 为 chunk 生成 embedding 并保存 | 可以重复构建索引，支持增量或重建 |
| 检索 | 支持向量检索，最好补充关键词检索 | 输入问题后能返回 topK 相关片段 |
| RAG 问答 | 基于检索片段回答问题 | 回答必须带来源，不知道时拒答 |
| 工具调用 | 至少实现 2 个工具，如列文件、读文件、搜索符号 | 模型能根据问题决定是否调用工具 |
| 评估 | 准备 20 条问答评测集 | 记录正确率、引用命中率、幻觉案例 |
| 可观测性 | 记录问题、检索片段、模型输出、耗时、token | 能复盘一次回答为什么好或不好 |
| 安全治理 | 环境变量管理密钥，限制危险操作 | README 说明权限边界和数据脱敏策略 |
| 展示文档 | 项目 README、架构图、运行方式、复盘 | 其他人能按说明跑起来 |

### 开发语言与框架定稿

本计划统一采用 Java 技术栈，避免在学习过程中被多语言、多框架分散注意力。

最终结论：

- **开发语言**：Java 21
- **主框架**：Spring Boot 3.x
- **AI 集成主线**：Spring AI 2.x
- **AI 框架补充**：LangChain4j，只用于对比学习和扩展视野
- **向量数据库主线**：Qdrant
- **向量数据库备选**：PGVector，如果希望减少组件数量
- **最终交付形态**：Spring Boot Web API + 可选 CLI + 本地 Docker Compose

| 方向 | 推荐 |
| --- | --- |
| 主开发语言 | Java 21 |
| 构建工具 | Maven |
| 后端框架 | Spring Boot 3.x |
| AI 主框架 | Spring AI 2.x |
| AI 备选/对照框架 | LangChain4j |
| Web API | Spring MVC，必要时使用 WebFlux 做流式输出 |
| CLI | Spring Shell 或普通 Spring Boot CommandLineRunner |
| 数据库 | PostgreSQL |
| 向量库 | Qdrant，备选 PGVector |
| ORM / 数据访问 | Spring Data JDBC 或 Spring Data JPA |
| 文档解析 | Java NIO、commonmark-java、Apache Tika 可选 |
| 代码解析 | 先用文件和正则级解析，进阶再引入 JavaParser 或 tree-sitter |
| 日志 | SLF4J + Logback |
| 测试 | JUnit 5、AssertJ、Testcontainers |
| 配置和密钥 | Spring Boot Configuration Properties + 环境变量 |
| 部署 | 本地 Docker Compose，进阶部署到云服务器 |

### 框架选择理由

| 选择 | 理由 |
| --- | --- |
| Java 21 | 当前 Java 主流长期支持版本，适合后端工程和企业项目 |
| Spring Boot 3.x | Java 后端岗位常见基础能力，适合快速做 REST API、配置、测试和部署 |
| Spring AI 2.x | 与 Spring Boot 集成自然，覆盖 Chat、Embedding、Vector Store、Tool Calling、RAG、Observability、Evaluation |
| LangChain4j | Java 生态中常见的 LLM 应用框架，适合作为 Spring AI 之外的对照学习 |
| Qdrant | 独立向量数据库，便于理解向量索引、相似度检索和服务化部署 |
| PGVector | 如果希望减少组件数量，可以把业务数据和向量数据放在 PostgreSQL 中 |

### 最终项目模块划分

建议最终项目采用下面的包结构：

```text
com.example.aidevassistant
├── AiDevAssistantApplication.java
├── config          # 模型、向量库、密钥、应用配置
├── document        # 文件扫描、文档解析、chunk 切片
├── embedding       # embedding 生成和索引写入
├── retrieval       # 向量检索、关键词检索、rerank 预留
├── rag             # RAG Prompt、回答生成、来源引用
├── tool            # listFiles、readFile、searchDocs 等工具
├── agent           # 简单任务规划、执行、状态和日志
├── eval            # 评测集、评测执行、结果统计
├── observability   # 请求日志、token、耗时、trace
├── security        # 只读权限、路径限制、脱敏、人工确认
└── web             # REST API 或简单页面接口
```

### 学习期间依赖选择

| 阶段 | 依赖建议 |
| --- | --- |
| 第 5 周 | Spring Boot Web starter、Spring AI 对应模型 starter，版本以官方 BOM/文档为准 |
| 第 6 周 | Spring AI `DocumentReader`、`TokenTextSplitter`、`VectorStore`，Qdrant 或 PGVector |
| 第 7 周 | Spring AI Tool Calling，使用 `@Tool` 暴露只读工具 |
| 第 8 周 | 先手写轻量 Agent，不急着引入复杂 Agent 框架 |
| 第 10 周 | JUnit 5 + 自定义 Eval Runner，记录 JSON/CSV 结果 |
| 第 11-12 周 | Docker Compose 启动 Qdrant/PostgreSQL，完善 API、日志和 README |

依赖版本原则：

- Spring Boot、Spring AI 使用官方 BOM 管理版本。
- 不在学习计划里硬编码依赖版本，真正建项目时再根据当时官方文档锁定。
- 引入新依赖前执行依赖审计，尤其是 Web、文档解析、向量数据库客户端和 AI SDK。

### 简历描述模板

```text
构建 AI Dev Knowledge Assistant，一个面向代码库和技术文档的 AI 知识助手。项目支持本地仓库扫描、文档切片、embedding 索引、向量/关键词混合检索、RAG 问答、来源引用、工具调用、评测集、日志追踪和基础安全治理。通过 20 条自建评测问题跟踪回答准确率、引用命中率、幻觉问题和响应耗时。
```

## 每日学习节奏

每天 1 小时，固定节奏如下：

| 时间 | 动作 | 说明 |
| --- | --- | --- |
| 15 分钟 | 学概念 | 只学当天要用的概念，不泛读 |
| 35 分钟 | 动手做 | 必须写 Prompt、写代码、跑工具或产出文档 |
| 10 分钟 | 复盘 | 记录今天产出、AI 犯错、明天计划 |

每天复盘模板：

```text
今天学了：
今天做了：
今天产出：
AI 帮我节省了什么：
AI 犯了什么错：
我沉淀的 Prompt：
明天要继续：
```

## 阶段 1：AI 工具与 Prompt 基础，第 1-2 周

阶段目标：从“随便问 AI”升级为“能稳定让 AI 完成明确任务”。

招聘价值：Prompt Engineering、需求表达、AI 辅助开发、沟通能力。

### 第 1 周：基础工具使用

本周目标：熟悉主流 AI 工具，沉淀第一批可复用 Prompt。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 模型体验 | 分别用 ChatGPT、Claude、Gemini 问同一个技术问题 | 记录 3 个模型的优缺点 |
| 周二 | Prompt 结构 | 学会目标、上下文、约束、输出格式、示例 | 写出 3 个结构化 Prompt |
| 周三 | 代码解释 | 选择一个熟悉项目，让 AI 解释目录结构 | 输出一份项目结构说明 |
| 周四 | 报错分析 | 准备一段真实报错日志，让 AI 分析原因 | 输出排查步骤和可能原因 |
| 周五 | 测试生成 | 选择一个函数，让 AI 生成单元测试 | 至少生成 5 个测试场景 |
| 周六 | 小重构 | 让 AI 重构一个小函数，并解释改动 | 对比重构前后差异 |
| 周日 | 模板整理 | 整理本周有效 Prompt | 形成 `prompts/week-01.md` |

本周交付物：

- 5 个常用 Prompt
- 一份 AI 工具对比记录
- 一份项目结构说明

### 第 2 周：个人 AI 工作流

本周目标：形成“给上下文、拆任务、生成、审查、复盘”的个人工作流。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 上下文管理 | 学会给 AI 提供需求、代码、限制、预期输出 | 写一个上下文完整的任务 Prompt |
| 周二 | 方案比较 | 让 AI 对同一需求给出 3 种实现方案 | 输出方案对比表 |
| 周三 | 需求拆解 | 给 AI 一个小需求，让它拆任务 | 得到可执行 checklist |
| 周四 | 验收标准 | 让 AI 为需求补充验收标准和边界条件 | 输出验收清单 |
| 周五 | 代码审查 | 审查 AI 生成的代码 | 记录至少 5 类风险 |
| 周六 | 工作流固化 | 整理从提问到验收的流程 | 输出个人 AI 编程流程 |
| 周日 | 小闭环 | 用 AI 完成一个很小的功能或脚本 | 形成一次完整记录 |

本周交付物：

- AI 代码审查清单
- 个人 AI 编程工作流
- 一次 AI 辅助开发完整记录

## 阶段 2：AI 辅助真实编程，第 3-4 周

阶段目标：让 AI 参与真实代码库任务，但人类负责判断和验收。

招聘价值：AI Coding Agent、代码审查、测试意识、工程质量。

### 第 3 周：AI 与代码库协作

本周目标：使用 Cursor、Copilot、Codex 或 Claude Code 处理真实代码上下文。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 工具安装 | 安装并熟悉一个 AI 编程工具 | 能让工具读取当前项目 |
| 周二 | 多文件理解 | 让 AI 解释一个功能涉及哪些文件 | 输出调用路径或文件关系 |
| 周三 | Bug 定位 | 找一个小 bug 或构造一个 bug | AI 给出定位思路 |
| 周四 | Patch 修改 | 让 AI 修改 bug | 查看 diff 并标注风险 |
| 周五 | 补测试 | 让 AI 为 bug 补测试 | 至少覆盖正常和异常场景 |
| 周六 | 运行验证 | 运行测试或手工验证 | 记录通过/失败原因 |
| 周日 | 复盘 | 复盘 AI 修 bug 流程 | 输出 `notes/ai-debug-record.md` |

本周交付物：

- 一次 AI 修 bug 记录
- 一份 diff 审查记录
- 一组测试用例

### 第 4 周：测试、重构与文档

本周目标：练会 AI 在测试、重构、文档上的高性价比用法。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 测试设计 | 学习正常、异常、边界、回归测试 | 输出测试场景表 |
| 周二 | 边界补充 | 让 AI 找遗漏边界 | 补充至少 5 个边界场景 |
| 周三 | 安全重构 | 选择一个函数做行为保持型重构 | diff 小且可解释 |
| 周四 | 行为验证 | 验证重构前后行为一致 | 测试或手工验证通过 |
| 周五 | 调用链文档 | 让 AI 整理一个功能调用链 | 输出调用链文档 |
| 周六 | 模块 README | 为一个模块生成 README | 包含用途、入口、依赖、风险 |
| 周日 | 规范沉淀 | 整理 AI 编程最佳实践 | 输出 `docs/ai-coding-workflow.md` |

本周交付物：

- 测试场景表
- 模块调用链文档
- AI 编程工作流文档

## 阶段 3：LLM API 与 RAG 基础，第 5-6 周

阶段目标：从“用工具”升级到“能开发 AI 功能”。

招聘价值：LLM API、Streaming、Embedding、Vector Database、RAG。

### 第 5 周：大模型 API

本周目标：用 Java + Spring Boot + Spring AI 完成一个最小可用的 AI 问答工具。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | Spring Boot 初始化 | 用 Spring Initializr 创建 Java 21 + Maven 项目 | 项目能启动，健康检查可访问 |
| 周二 | Spring AI 接入 | 引入 Spring AI 模型 starter，配置 API Key | 不把密钥写进代码 |
| 周三 | Chat API | 写 `ChatController` 或 CLI 问答入口 | 输入问题能得到回答 |
| 周四 | System Prompt | 用 system prompt 固定助手角色和回答规则 | 回答风格稳定 |
| 周五 | 流式输出 | 用 Spring MVC/WebFlux 返回 streaming response | 能边生成边显示 |
| 周六 | 错误处理 | 处理超时、限流、空响应和模型错误 | 有友好错误和日志 |
| 周日 | 成本记录 | 记录模型名、耗时、token 或近似 token | 输出 Java API 调用模板 |

本周交付物：

- Java/Spring Boot AI 问答工具
- Spring AI API 调用模板
- 密钥和错误处理说明

### 第 6 周：RAG 最小闭环

本周目标：用 Spring AI 完成一个本地文档问答 Demo。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | RAG 流程 | 理解解析、切片、索引、检索、生成 | 画出 RAG 流程图 |
| 周二 | 文档准备 | 准备 5-10 个 Markdown 或文本文件 | 放入 `data/docs` |
| 周三 | 文档切片 | 用 Java NIO + Spring AI splitter 生成 chunk | chunk 带文件路径和序号 |
| 周四 | Embedding | 用 Spring AI EmbeddingModel 生成向量 | 写入 Qdrant 或 PGVector |
| 周五 | 检索 | 用 Spring AI VectorStore 召回 topK 片段 | 打印召回片段和分数 |
| 周六 | RAG 回答 | 用 ChatClient 组合检索上下文生成回答 | 回答带来源引用 |
| 周日 | 检索评估 | 准备 5 条问题检查召回效果 | 记录命中/未命中 |

本周交付物：

- 本地文档问答 Demo
- RAG 流程图
- 5 条检索质量记录

## 阶段 4：工具调用、Agent 与安全边界，第 7-8 周

阶段目标：让 AI 从“回答”变成“可控地调用工具执行任务”。

招聘价值：Tool Calling、Agent、权限控制、Human-in-the-loop、安全治理。

### 第 7 周：工具调用

本周目标：用 Spring AI Tool Calling 完成一个带工具调用的 AI 助手。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | Tool Calling 概念 | 理解模型选择工具、传参、接收结果 | 画出工具调用流程 |
| 周二 | 工具定义 | 用 Java 方法和 Spring AI `@Tool` 定义 `listFiles` | 工具描述清晰 |
| 周三 | 工具执行 | 让模型根据问题调用 Java 工具 | 至少成功调用 1 个工具 |
| 周四 | 参数校验 | 使用 DTO、校验和异常处理保护工具参数 | 有错误提示 |
| 周五 | 权限边界 | 限制工具只能访问项目白名单目录 | 无法读取目录外文件 |
| 周六 | 业务工具 | 增加 `readFile`、`searchDocs` 或 `searchSymbol` | 支持自然语言查询 |
| 周日 | 安全复盘 | 记录工具风险和防护策略 | 输出权限设计说明 |

本周交付物：

- 带工具调用的 AI 助手
- 工具 schema 文档
- 权限边界说明

### 第 8 周：简单 Agent

本周目标：用 Java 手写一个能规划、执行、记录日志的小 Agent。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | Agent 流程 | 理解 plan-act-observe | 输出流程图 |
| 周二 | 任务规划 | 用 ChatClient 让模型把任务拆成步骤 | 计划可执行 |
| 周三 | 状态管理 | 设计 `AgentTask`、`AgentStep`、`AgentRunLog` | 有 task state |
| 周四 | 工具编排 | Agent 调用 `listFiles` 和 `readFile` 完成任务 | 能完成小任务 |
| 周五 | 日志记录 | 用 SLF4J 和结构化对象记录每一步 | 可复盘 |
| 周六 | 失败控制 | 加最大步数、超时、重试、人工中断 | 不会无限循环 |
| 周日 | 小项目 | 做一个“自动整理 README 草稿”的 Agent | 输出草稿和执行日志 |

本周交付物：

- 简单 Agent
- 执行日志样例
- 失败重试和人工中断机制

## 阶段 5：评估、可观测性与项目准备，第 9-10 周

阶段目标：让 AI 应用不只“能跑”，还能被评估、调试和改进。

招聘价值：Eval、Observability、Tracing、Prompt 版本管理、质量优化。

### 第 9 周：AI Coding Agent 实战

本周目标：让 AI Coding Agent 完成一个小需求，并由你完成审查。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 任务描述 | 写清目标、范围、限制、验收标准 | 任务描述可复用 |
| 周二 | 先分析 | 要求 Agent 先读代码再给方案 | 有方案而非直接改 |
| 周三 | 执行修改 | 让 Agent 完成一个小功能 | 有可读 diff |
| 周四 | 人工审查 | 检查设计、边界、安全、风格 | 输出 review 记录 |
| 周五 | 测试修复 | 让 Agent 跑测试并修复失败 | 测试通过或说明原因 |
| 周六 | 文档更新 | 让 Agent 更新对应文档 | 文档与代码一致 |
| 周日 | 复盘 | 总结 Agent 擅长和不擅长的部分 | 输出实战报告 |

本周交付物：

- 一次 Coding Agent 实战报告
- 一份 code review 记录
- 一组测试或验证记录

### 第 10 周：Eval 与可观测性

本周目标：为 RAG Demo 建立基础评测体系。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | Eval 概念 | 理解准确率、召回、引用命中、幻觉 | 定义自己的指标 |
| 周二 | 问题集 | 准备 20 条问题 | 覆盖事实、路径、总结、拒答 |
| 周三 | 标准答案 | 为每题写标准答案或判断规则 | 可人工打分 |
| 周四 | 日志字段 | 记录问题、召回片段、回答、耗时、token | 日志结构稳定 |
| 周五 | 第一轮评测 | 跑完整问题集 | 得到 baseline |
| 周六 | 优化实验 | 调整 Prompt、chunk、topK 或 hybrid search | 得到第二轮结果 |
| 周日 | 对比报告 | 对比优化前后指标 | 输出评测报告 |

本周交付物：

- 20 条 Eval 数据
- baseline 结果
- 优化前后对比报告

## 阶段 6：最终项目落地，第 11-12 周

阶段目标：把前面所有能力合成一个完整项目。

招聘价值：端到端 AI 应用、项目交付、工程化、文档表达。

### 第 11 周：AI Dev Knowledge Assistant 基础版

本周目标：完成可运行的最小版本。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 项目初始化 | 建立 Spring Boot 多包结构、README 草稿、配置文件 | 项目可运行 |
| 周二 | 文件扫描 | 实现 `DocumentScanService` 和文件过滤 | 输出文件清单 |
| 周三 | 切片索引 | 实现 `DocumentChunker`、embedding、索引构建命令 | 能构建索引 |
| 周四 | 检索接口 | 实现 `RetrievalService`，支持向量检索和关键词检索 | 返回 topK 来源 |
| 周五 | RAG 问答 | 实现 `RagService` 和 `/api/chat` | 回答带来源引用 |
| 周六 | 拒答机制 | 无来源时拒答或提示资料不足 | 不胡编 |
| 周日 | 基础验收 | 用 10 条问题手工测试 | 记录问题和改进点 |

本周交付物：

- AI Dev Knowledge Assistant 基础版
- 索引构建命令
- 问答命令或简单页面
- 10 条手工测试记录

### 第 12 周：项目完善与可展示化

本周目标：把项目打磨到可以给别人看、可以放简历。

| 日期 | 章节 | 具体任务 | 验收 |
| --- | --- | --- | --- |
| 周一 | 工具调用 | 加入 `listFiles`、`readFile` 或 `searchSymbol` Java 工具 | 模型能调用工具辅助回答 |
| 周二 | 日志追踪 | 记录检索、回答、耗时、token、traceId | 可以复盘一次回答 |
| 周三 | Eval 跑通 | 用 JUnit 或自定义 Eval Runner 跑 20 条问题 | 输出结果表 |
| 周四 | 安全治理 | 补充密钥管理、只读权限、路径白名单、脱敏说明 | README 有安全章节 |
| 周五 | 质量优化 | 优化 Prompt、检索参数、拒答规则 | 指标比 baseline 更好 |
| 周六 | 文档完善 | 写 README、架构图、运行方式、技术取舍 | 新人能跑起来 |
| 周日 | 最终复盘 | 写项目复盘和简历描述 | 项目完成 |

本周交付物：

- 完整项目 README
- 架构图或流程图
- Eval 结果表
- 安全设计说明
- 学习复盘
- 简历项目描述

## 最终项目 README 模板

最终项目建议包含以下章节：

```text
# AI Dev Knowledge Assistant

## 项目背景
解决什么问题，目标用户是谁。

## 核心功能
文件扫描、索引、检索、RAG 问答、来源引用、工具调用、评测、日志。

## 架构设计
用流程图说明：输入问题 -> 检索 -> 工具调用 -> 生成回答 -> 日志 -> 评测。

## 技术栈
Java 21、Spring Boot 3.x、Spring AI 2.x、Maven、Qdrant 或 PGVector、JUnit 5、Docker Compose。

## RAG 流程
文档解析、切片策略、embedding、索引、检索、重排、生成。

## Agent / Tool Calling
有哪些工具，什么时候调用，权限边界是什么。

## Eval 结果
问题数量、准确率、引用命中率、失败案例、优化记录。

## 安全设计
API Key、只读权限、数据脱敏、危险操作确认、提示词注入风险。

## 本地运行
安装、配置环境变量、构建索引、启动服务、提问示例。

## 已知限制
当前做不到什么，下一步怎么优化。
```

## 每周交付物总览

| 周次 | 交付物 |
| --- | --- |
| 第 1 周 | Prompt 模板、模型对比、项目结构说明 |
| 第 2 周 | AI 代码审查清单、个人 AI 工作流、一次小闭环 |
| 第 3 周 | AI 修 bug 记录、diff 审查、测试用例 |
| 第 4 周 | 测试场景表、调用链文档、AI 编程工作流 |
| 第 5 周 | Java/Spring Boot AI 问答工具、Spring AI API 模板、错误处理说明 |
| 第 6 周 | Spring AI RAG Demo、RAG 流程图、检索质量记录 |
| 第 7 周 | Spring AI Tool Calling 助手、工具 schema、权限边界说明 |
| 第 8 周 | Java 简单 Agent、执行日志、失败控制机制 |
| 第 9 周 | Coding Agent 实战报告、code review 记录 |
| 第 10 周 | 20 条 Eval 数据、baseline、优化对比报告 |
| 第 11 周 | 最终项目基础版、10 条手工测试记录 |
| 第 12 周 | 完整项目、README、架构图、Eval、复盘、简历描述 |

## 招聘导向技能地图

根据公开招聘信息、开发者调查和 AI 岗位研究，当前市场更看重“能把 AI 落进业务系统”的工程能力，而不是单纯会使用聊天工具。

| 招聘关键词 | 要证明的能力 | 本计划对应训练 |
| --- | --- | --- |
| LLM API / 多模型接入 | 接入模型，处理流式输出、错误重试、成本控制 | 第 5 周 |
| Prompt Engineering | 把业务需求转成稳定、可复用、可评估的 Prompt | 第 1-2 周、第 10 周 |
| RAG / 企业知识库 | 处理私有文档、检索、引用来源和权限边界 | 第 6 周、第 11-12 周 |
| Vector Database | 理解 embedding、向量库、索引、召回、重排 | 第 6 周、第 10 周 |
| Agent / Tool Calling | 让模型调用 API、文件、搜索等工具并控制执行边界 | 第 7-8 周 |
| AI Coding Agent | 使用 Codex、Claude Code、Cursor、Copilot 提升开发效率 | 第 3-4 周、第 9 周 |
| Eval / Observability | 构造测试集，跟踪准确率、幻觉、延迟、成本和 trace | 第 10 周 |
| Security / Governance | 处理密钥、权限、脱敏、提示词注入和人工确认 | 第 7-8 周、第 12 周 |
| Cloud / Deployment | 把 AI 应用部署成可访问服务，理解日志和监控 | 第 12 周 |
| Business Communication | 能讲清业务价值、技术取舍和落地风险 | 全阶段 |

## 简历展示关键词

- LLM application development
- Java 21
- Spring Boot
- Spring AI
- LangChain4j
- Prompt engineering
- RAG
- Embedding
- Vector database
- Hybrid search
- Reranking
- Function calling / Tool calling
- AI Agent
- AI coding agent
- Eval / LLM evaluation
- Observability / tracing
- Prompt injection defense
- Human-in-the-loop
- Data privacy / permission control
- Streaming response
- Token cost optimization
- API integration
- Cloud deployment
- Technical documentation

## 参考信号

- [Spring AI Reference](https://docs.spring.io/spring-ai/reference/) 显示，Spring AI 已覆盖 Chat、Embedding、Vector Store、Tool Calling、RAG、Observability、Evaluation 和 Spring Boot starters，适合作为 Java AI 应用主线框架。
- [LangChain4j Documentation](https://docs.langchain4j.dev/) 说明它面向 Java 应用，提供 LLM、Vector Store、Tools、Agents、RAG 以及 Spring Boot 集成，适合作为 Java AI 框架补充。
- [Stack Overflow 2025 Developer Survey](https://survey.stackoverflow.co/2025/ai) 显示，84% 的开发者已经使用或计划使用 AI 工具，但对 AI 输出准确性的信任仍然不足，说明“会审查和验证 AI 输出”是关键能力。
- [GitHub Octoverse 2024](https://github.blog/news-insights/octoverse/octoverse-2024/) 显示，生成式 AI 项目数量和贡献量快速增长，Python、Jupyter、AI 项目成为开发者生态的重要增量。
- [Business Insider 关于 Forward Deployed Engineer 的报道](https://www.businessinsider.com/forward-deployed-engineer-jobs-in-demand-2026-5) 和 [Financial Times 相关报道](https://www.ft.com/content/91002071-7874-4cb7-9245-08ca0571c408) 显示，AI 公司和云厂商正在招聘能把 AI 带进客户业务流程的工程角色。
- [Prompt Engineer 岗位研究](https://arxiv.org/abs/2506.00058) 分析了 LinkedIn 上的 AI 岗位，发现单独的 Prompt Engineer 岗位并不多，但 AI 知识、Prompt 设计、沟通和创造性解决问题能力正在扩散到更多软件岗位中。
- [RAG 介绍](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) 和 [AI Agent 介绍](https://en.wikipedia.org/wiki/AI_agent) 可作为概念补充阅读，帮助理解招聘描述中常见的 RAG、Agent、tool use、memory、evaluation 等关键词。

## 学习原则

- 每天都要有一个小产出。
- 不追求一次学完概念，先围绕当天任务够用即可。
- AI 生成内容必须经过人类审查，尤其是代码、安全、权限和数据处理。
- 每周至少沉淀一个可复用文档或工具。
- 最终项目要能回答三个问题：解决什么业务问题、怎么验证效果、如何控制风险。
