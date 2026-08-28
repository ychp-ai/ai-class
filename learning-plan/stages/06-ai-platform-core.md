# 阶段六：AI 平台核心

周期：第 17–20 周，共约 28 小时。

目标：把前 16 周的单应用能力演进为可管理的平台控制面，完成平台边界、Agent 注册与版本、模型网关、工具/MCP 和知识库管理。

## 开始前应会什么

- 能运行第 16 周端到端应用，并指出模型、Prompt、Tool、KB、Workflow 和运行记录的位置。
- 能说明版本、资源归属、权限、Trace 和 Eval 为什么影响发布与排错。
- 能使用 Spring Boot、数据库迁移和 API 测试建立模块化单体骨架。

## 零基础桥接

先从单应用的四个真实痛点建立平台需求：配置无法复用、版本不可追溯、权限散落、运行不可审计。为每个痛点写出一个用户、一次失败和一个期望的平台能力，再推导控制面、执行面和资源模型，不从技术组件清单反推架构。

## 本阶段不要求什么

- 不要求微服务、Kubernetes、复杂消息系统、跨地域容灾或完整计费。
- 不要求先做拖拽画布；第一版坚持 API 优先和轻量管理入口。
- 不要求把业务权限、租户隔离或 Secret 管理交给 Agent 框架。

## 前测失败处理

若第 16 周应用不能复现，先修复启动、测试、Eval 和 Trace 基线；若无法解释四类单应用痛点，先为一个 Agent 配置变更做手工版本、发布、运行和回滚演练，再开始平台建模。

## 第 17 周：平台需求、领域模型与架构边界

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 定义平台用户和核心用例 | 至少区分平台管理员、Agent 开发者、业务接入方和审计者；每类只写真实任务<br>相关资料：[GOV.UK Discovery Phase](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works) | 用户—任务—权限矩阵 |
| 周二 | 划定 MVP 与非目标 | 优先 API、版本和运行闭环；拖拽画布、计费和跨地域先列为非目标<br>相关资料：[GOV.UK Discovery Phase](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works) | MVP/非目标清单有理由 |
| 周三 | 设计领域对象 | 建模 Project、Agent、Version、Release、Tool、KnowledgeBase、Workflow、Run；避免直接套数据库表<br>相关资料：[Microsoft：Domain-Driven Design](https://learn.microsoft.com/azure/architecture/microservices/model/domain-analysis) | 领域关系图和不变量 |
| 周四 | 划分控制面与执行面 | 控制面管理可变配置，执行面只消费发布快照；写清调用和失败边界<br>相关资料：[AWS：Control Plane and Data Plane](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/control-planes-and-data-planes.html) | 控制面/执行面时序图 |
| 周五 | 多租户与资源归属 | 第一版可做轻量 Tenant/Project，但所有资源必须带归属且查询默认过滤<br>相关资料：[OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | 两项目隔离测试设计 |
| 周六 | 技术选型与 ADR | 对单体/微服务、同步/异步、PGVector/Qdrant 做证据化取舍，不为展示堆组件<br>相关资料：[Architecture Decision Records](https://adr.github.io/) | 至少三份 ADR |
| 周日 | 建平台骨架与健康检查 | 先完成模块边界、数据库迁移和健康接口；不提前填充所有功能<br>相关资料：[Spring Modulith](https://docs.spring.io/spring-modulith/reference/) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: establish ai platform domain and architecture baseline`

必须包含：用户和用例、MVP/非目标、领域模型、平台架构、信任边界、ADR、服务骨架和数据库迁移。

验收标准：每个核心资源都有归属；控制面与执行面职责清晰；在本地可启动并验证数据库和健康状态。

## 第 18 周：Agent 注册、版本、发布与回滚

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 设计 Agent Definition | 输入输出 Schema、模型策略、Prompt 引用、工具和知识库都使用显式 ID；不要保存不可审计的大对象<br>相关资料：[JSON Schema 入门](https://json-schema.org/learn/getting-started-step-by-step) | Agent Schema 可校验 |
| 周二 | Draft 与不可变 Version | 编辑 Draft，发布时生成不可变快照；相同内容可用 Hash 识别<br>相关资料：[Semantic Versioning](https://semver.org/) | 已发布版本不可原地修改 |
| 周三 | Publish 与 Rollback | 发布前检查依赖版本和 Eval 状态；回滚切换 Release 指针而非覆盖历史<br>相关资料：[Google SRE：Release Engineering](https://sre.google/sre-book/release-engineering/) | 发布和回滚测试通过 |
| 周四 | Agent CRUD API 与并发控制 | 使用版本号或 ETag 防止覆盖更新；越权项目不能读取或修改资源<br>相关资料：[RFC 9110：条件请求](https://www.rfc-editor.org/rfc/rfc9110.html#name-preconditions) | 并发冲突和隔离测试 |
| 周五 | 配置校验与依赖解析 | 发布时确认模型、工具、知识库存在且可用；错误应定位到具体依赖<br>相关资料：[JSON Schema 入门](https://json-schema.org/learn/getting-started-step-by-step) | 无效依赖不能发布 |
| 周六 | 最小管理界面或 API 集合 | 先实现列表、详情、编辑、版本、发布和回滚；UI 可简陋但状态必须准确<br>相关资料：[OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | 可完成完整管理流程 |
| 周日 | 运行两个 Agent 版本 | 用固定输入比较旧版和新版；确认 Run 记录绑定具体快照<br>相关资料：[OpenAI Evals 指南](https://platform.openai.com/docs/guides/evals) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add versioned agent registry and release lifecycle`

必须包含：Agent 管理 API、版本快照、发布与回滚、项目隔离、并发更新保护、管理入口和自动测试。

验收标准：运行历史可追溯到不可变版本；回滚不删除新版；不同 Project 不可越权访问。

## 第 19 周：模型网关、路由、配额与降级

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | Provider 与 Model Alias | 业务和 Agent 引用平台别名，不直接散落供应商模型名；凭证只存 Secret 引用<br>相关资料：[Spring AI ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html) | 可切换别名映射 |
| 周二 | 统一请求、响应与错误 | 统一 Usage、FinishReason、ToolCall 和流式事件；保留供应商扩展字段的边界<br>相关资料：[OpenAI API Quickstart](https://platform.openai.com/docs/quickstart) | 两个 Provider 适配同一接口 |
| 周三 | 本地模型、量化与微调边界 | 运行一个本地开源模型并记录内存/显存、吞吐和量化影响；写清 RAG、Prompt 与 LoRA/PEFT 的选择条件<br>相关资料：[Hugging Face Quantization](https://huggingface.co/docs/transformers/main/en/quantization/overview) | 本地推理实验和选型 ADR |
| 周四 | 超时、重试、熔断与 Cache | 重试只覆盖安全错误；Cache Key 包含模型、Prompt、Tool Schema 和参数，敏感内容不跨项目复用<br>相关资料：[Resilience4j Guide](https://resilience4j.readme.io/docs/getting-started) | 故障与 Cache 隔离测试 |
| 周五 | 路由与 Fallback | 按能力、成本、延迟和数据策略路由；Fallback 前确认 Schema、上下文和工具能力兼容<br>相关资料：[Google SRE：Handling Overload](https://sre.google/sre-book/handling-overload/) | 主模型失败可受控降级 |
| 周六 | 配额、限流与成本预算 | 同时设置请求、Token、并发和单次预算；超额返回明确业务错误<br>相关资料：[RFC 9333：RateLimit 字段](https://www.rfc-editor.org/rfc/rfc9333.html) | 超限请求不会调用模型 |
| 周日 | 基准与路由报告 | 用固定任务比较质量、P95 延迟、Token 和成本，避免只比回答观感<br>相关资料：[OpenAI Eval 最佳实践](https://platform.openai.com/docs/guides/evaluation-best-practices) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: implement governed model gateway with routing`

必须包含：统一模型接口、至少两个适配器或一个真实加一个 Stub、模型别名、路由、配额、Fallback、Usage 和基准报告。

验收标准：业务代码不依赖供应商细节；配额和隔离由代码控制；失败、降级和成本可以观测。

## 第 20 周：Tool/MCP 与知识库管理

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | Tool Registry 与版本 | Schema、风险级别、Owner、权限和版本都必填；同名工具不可悄悄换语义<br>相关资料：[MCP Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | 工具注册和版本 API |
| 周二 | Tool Credential 与权限 | 凭证使用引用，运行时按 Project、Agent、用户和 Scope 求交集<br>相关资料：[MCP Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | 无授权工具无法注入 |
| 周三 | MCP Client/Server 与授权 | 同时做最小 Server 和 Client；HTTP 方式验证资源绑定，stdio 不套用 HTTP OAuth<br>相关资料：[MCP 2025-11-25 Specification](https://modelcontextprotocol.io/specification/2025-11-25) | MCP 往返与拒绝案例 |
| 周四 | 动态工具发现与上下文预算 | 工具多时先搜索再加载；对历史、工具结果和检索内容设置预算、裁剪和摘要策略<br>相关资料：[LangChain Context Engineering](https://docs.langchain.com/oss/python/langchain/context-engineering) | Token 节省和质量对比 |
| 周五 | Knowledge Base 控制面 | 管理数据源、Chunk、Embedding、索引版本和状态；重建索引不覆盖线上版本<br>相关资料：[Spring AI ETL Pipeline](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html) | 索引版本可切换 |
| 周六 | 进阶检索、权限与评测 | 比较 BM25+向量混合检索、Rerank、Query Rewrite；加入 ACL，并用 Recall@K/MRR 验证<br>相关资料：[Qdrant Hybrid Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) | 质量提升且越权文档不召回 |
| 周日 | 平台核心端到端验收 | 发布一个同时使用模型、工具和知识库的 Agent，记录每项依赖版本<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成阶段提交 |

### 阶段提交

建议 Commit：`feat: complete platform tool mcp and knowledge registries`

必须包含：Tool/MCP Registry、凭证引用、Scope、MCP 示例、上下文预算、Knowledge Base 与索引版本、混合检索/Rerank、ACL、检索评测、Agent 依赖快照和端到端记录。

验收标准：已发布 Agent 的所有依赖可追溯；未授权工具和文档不可见；索引升级可以灰度或回滚。

## 阶段出口条件

- 平台控制面能够管理 Agent、模型、工具/MCP 和知识库。
- 所有可运行配置都有不可变版本和发布记录。
- 至少支持 Project 级资源隔离和基础 RBAC。
- 模型调用具备路由、配额、降级、成本和错误治理。
- Agent 运行可以追溯到模型、Prompt、工具和索引的具体版本。

官方资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)、[Hugging Face PEFT/LoRA](https://huggingface.co/docs/peft/main/conceptual_guides/lora)、[MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)、[MCP Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)。本课程以 `2025-11-25` 稳定版为实现和验收基线；[2026-07-28 RC](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) 仅用于了解下一版变化。

下一阶段：[工作流与平台治理](07-workflow-governance.md)
