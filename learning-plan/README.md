# 32 周完整学习路线

## 计划定位

本计划面向具备基础开发能力、但没有 AI、机器学习、LLM、RAG 和 Agent 知识，希望独立建设 AI 平台并推动业务落地的开发者。每天投入约 1 小时，32 周总计约 224 小时。

224 小时可以完成一个可运行、可演示、具备基础生产约束的平台 MVP 和一个业务试点闭环，但不等同于大型企业平台的全部能力。完成后仍需要通过真实流量、多个业务场景和持续运维提升熟练度。

阶段文档给出 32 周排期和四列表格；[逐节课程教程](tutorials/README.md)进一步把 224 节课逐节展开为“为什么学、这个是什么、怎么学、怎么验证学会了”，并提供独立尝试后使用的参考答案。学习者应从当周教程进入每日实践，进度和通过状态仍以 `deliverables/week-XX/README.md` 为准。

| 项目 | 安排 |
| --- | --- |
| 周期 | 32 周 |
| 日均投入 | 约 1 小时 |
| 总投入 | 约 224 小时 |
| 第 1–4 周学习比例 | 35% 原理和心智模型、50% 实践、15% 评测与复盘 |
| 第 5–32 周学习比例 | 20% 原理和资料、65% 实践、15% 评测与复盘 |
| 主技术栈 | Java 21、Spring Boot、Spring AI、PostgreSQL |
| Agent 运行时 | Python 3.11+、LangChain、LangGraph、Claude Agent SDK |
| 数据与检索 | PostgreSQL/PGVector 或 Qdrant、对象/文件存储 |
| 管理端 | API 优先；React/TypeScript 最小控制台可按现有前端基础实现 |
| 运行与观测 | Docker Compose、OpenTelemetry/Micrometer、结构化日志 |

## 开发语言路线

课程不是让学习者在第一天同时学习 Java、Python 和 TypeScript，而是按职责分阶段切换：

```text
第 1–4 周：Python 建立 AI 原理和原生协议直觉
→ 第 5–8 周：Java/Spring AI 建业务与平台基础
→ 第 9–13 周：Python 学 Agent 运行时
→ 第 14–32 周：Java 控制面 + Python 执行面，按需增加 TypeScript 控制台
```

Java 21 是最终平台的主工程语言，Python 3.11+ 是 AI 实验与 Agent 执行语言，TypeScript/React 只承担最小控制台。每次语言切换使用 15–30 分钟桥接任务，并通过运行、测试和失败案例验收；不要求先完成整门语言教程。完整周次、职责边界和替代规则见[开发语言路线与切换策略](01-language-roadmap.md)。

## 学习者起点

默认已经具备：

- 至少一种主流编程语言的开发和单元测试能力。
- Git、命令行、IDE、HTTP、JSON、数据库和环境变量基础。
- 阅读错误日志、缩小问题范围和按 README 运行项目的经验。

不要求预先具备：

- AI、机器学习、深度学习、概率统计或线性代数知识。
- Token、Embedding、Prompt、RAG、Tool Calling、Agent 或 Eval 心智模型。
- Spring AI、LangChain、LangGraph、Claude Agent SDK 或 MCP 使用经验。
- Java 21、Spring Boot 或 Python 异步编程的完整熟练度。

课程对 Java、Spring Boot 和 Python 采用“完成当周任务所需的最小桥接”，不会把通用语言教程塞入 AI 主线。如果 Git、HTTP、测试或基础编程也不熟练，需要在课程外补齐，并相应增加实际投入时间。

## 最终能力模型

每个主题按四级掌握，阶段出口至少达到 L3，最终核心模块达到 L4。

| 等级 | 能力定义 | 证明方式 |
| --- | --- | --- |
| L1 使用 | 能按文档完成调用 | 可运行示例 |
| L2 解释 | 能说明原理、边界和取舍 | 设计说明与对比实验 |
| L3 实现 | 能脱离高层封装实现关键路径 | 原生 API、核心代码与测试 |
| L4 交付 | 能诊断、评测、安全化并生产运行 | Trace、Eval、压测、告警和业务指标 |

## 两条主线

### 平台工程线

```text
LLM 与原生 API
→ RAG、Tool Calling 与 Agent Runtime
→ Agent/模型/工具/知识库控制面
→ 工作流运行时
→ 权限、审批、评测、观测和运维
→ 可部署 AI Agent Platform
```

### 业务落地线

```text
目标与指标
→ 场景调研
→ AS-IS 流程
→ AI 适用性分析
→ TO-BE 人机流程
→ 接口、数据和权限设计
→ 试点上线
→ 效果复盘与推广决策
```

## 阶段地图

| 阶段 | 周次 | 核心目标 | 阶段交付 |
| --- | --- | --- | --- |
| [一：AI 原理、工具与工程协作](stages/01-ai-tools-and-engineering.md) | 1–4 | 理解 LLM 工程原理并可靠使用原生 API 和 AI 编程工具 | 原生调用、Tool Loop、对比实验、测试闭环 |
| [二：Java LLM、RAG 与 Agent](stages/02-java-llm-rag-agent.md) | 5–8 | 构建可控的 Java AI 应用能力 | Chat、RAG、Tool、手写 Agent |
| [三：LangChain 与 LangGraph](stages/03-langchain-langgraph.md) | 9–11 | 构建结构化、有状态、可恢复的 Agent | RAG Agent、持久化工作流、审批 |
| [四：Claude Agent SDK](stages/04-claude-agent-sdk.md) | 12–13 | 构建安全的开放式执行 Agent | 代码执行、权限、Hooks、MCP |
| [五：组合、评测与首个应用](stages/05-integration-evaluation-delivery.md) | 14–16 | 打通端到端 AI 应用并建立 Baseline | Java/Python 应用、Eval、Trace、安全说明 |
| [六：AI 平台核心](stages/06-ai-platform-core.md) | 17–20 | 从单应用演进为可管理的平台控制面 | 平台 ADR、Agent 注册表、模型网关、Tool/KB 管理 |
| [七：工作流与平台治理](stages/07-workflow-governance.md) | 21–24 | 建设可恢复运行时和治理能力 | 工作流版本、运行中心、RBAC、审计、SLO |
| [八：业务场景与流程设计](stages/08-business-scenario-process.md) | 25–28 | 掌握从业务问题到可实施方案的全过程 | 调研包、AS-IS/TO-BE、价值和接入设计 |
| [九：试点上线与最终交付](stages/09-pilot-production-capstone.md) | 29–32 | 完成系统接入、试点、上线和复盘 | 业务试点、平台发布包、运营报告、答辩材料 |

## 平台参考架构

```text
业务系统 / 管理控制台 / Open API
                 ↓
Java Control Plane
├── Tenant / Project / RBAC
├── Agent Registry / Version / Release
├── Model Gateway / Policy / Quota
├── Tool & MCP Registry / Credential Reference
├── Knowledge Base / Index Version
├── Workflow Definition / Run Management
└── Audit / Eval / Observability API
                 ↓
Python Agent Runtime
├── LangChain：模型、工具与结构化 Agent
├── LangGraph：状态、路由、Checkpoint 与 HITL
└── Claude Agent SDK：隔离的开放式执行任务
                 ↓
PostgreSQL / Vector Store / Object Storage / Sandbox
```

控制面负责配置、权限、版本和审计；执行面只接收经过授权且已发布的不可变快照。业务权限必须由平台代码执行，不能交给 Prompt 或模型判断。

## 平台最小功能集

| 能力域 | 最低要求 |
| --- | --- |
| 身份与隔离 | Project 或轻量 Tenant、RBAC、服务账号、资源归属 |
| 模型管理 | Provider 配置、模型别名、路由、超时、配额、Fallback |
| Agent 管理 | Draft、Version、Publish、Rollback、输入输出 Schema |
| 工具管理 | Tool/MCP 注册、版本、权限、凭证引用、调用审计 |
| 知识库 | 数据源、索引版本、权限过滤、检索参数和评测 |
| 工作流 | 条件、循环上限、并行或汇聚、审批、暂停、恢复、取消 |
| 运行中心 | Run/Step 状态、幂等、重试、错误分类、事件和日志 |
| 质量治理 | Eval Dataset、Baseline、版本对比、发布门禁 |
| 可观测性 | Trace、Token、成本、延迟、错误率和工具调用 |
| 安全运维 | Secret 引用、审计、限流、备份恢复和应急手册 |

## 业务场景选择标准

第 25 周必须选择一个真实或高保真案例。合格场景应同时满足：

- 有明确业务负责人、用户和可量化目标。
- 现状至少包含三个步骤或两个系统之间的协作。
- AI 能解决非确定性任务，但关键规则仍可由代码约束。
- 数据来源、权限和人工兜底可以说清楚。
- 四周内能够做小范围试点，不依赖大规模组织改造。

不选择“做一个万能聊天机器人”作为场景。优先考虑知识密集、重复判断、跨系统协作、结果可复核的流程。

## 里程碑

- 第 4 周：能解释并手写模型调用、流式处理和 Tool Loop。
- 第 8 周：能用 Java 构建安全的 RAG 与 Agent 基础能力。
- 第 13 周：能构建持久化工作流和隔离的执行型 Agent。
- 第 16 周：有一个可评测、可观测的端到端 AI 应用。
- 第 20 周：完成平台核心控制面和资源版本管理。
- 第 24 周：平台工作流、运行治理和发布门禁可用。
- 第 28 周：完成一个业务场景的调研、流程优化和接入设计。
- 第 32 周：完成业务试点、生产硬化、效果复盘和平台交付。

## 资料使用原则

每个每日课程的“当天学习建议”末尾都附有“相关资料”链接。每天约 20 分钟的资料学习只阅读与当天任务直接相关的章节，并把版本、关键结论和仍待验证的问题记入周笔记；链接是实践入口，不替代亲自运行、失败实验和 Teach-back。

框架和 API 优先链接当前官方入口，协议则固定到明确的稳定版本，避免课程内容随网页默认版本静默变化。平台工作流设计应利用持久化、人工审批和故障恢复能力；LangGraph 的 Checkpoint 用于 HITL、恢复和调试，Spring AI 的模型、工具与向量调用可以接入统一观测，MCP HTTP 接入必须按协议实现授权和资源绑定。MCP 课程当前以 `2025-11-25` 稳定版为基线，`2026-07-28` Release Candidate 暂不作为实现验收依据。

相关官方资料：[LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Spring AI Observability](https://docs.spring.io/spring-ai/reference/observability/index.html)、[MCP Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)、[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)。

每天先从[逐节课程教程](tutorials/README.md)进入当周课程，通用执行方式见[学习方法与建议](00-learning-method.md)，当周语言和切换桥接见[开发语言路线](01-language-roadmap.md)，讲师监督和掌握度判定见[讲师监督与掌握度评估](07-instructor-supervision.md)，每周提交前检查[成果与提交标准](06-deliverable-standards.md)。本次学习者起点调整的边界和迁移依据见[AI 零基础开发者课程改造设计](08-ai-zero-foundation-curriculum-design.md)。
