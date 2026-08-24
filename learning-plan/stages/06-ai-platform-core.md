# 阶段六：AI 平台核心

周期：第 17–20 周，共约 28 小时。

目标：把前 16 周的单应用能力演进为可管理的平台控制面，完成平台边界、Agent 注册与版本、模型网关、工具/MCP 和知识库管理。

## 第 17 周：平台需求、领域模型与架构边界

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 定义平台用户和核心用例 | 至少区分平台管理员、Agent 开发者、业务接入方和审计者；每类只写真实任务 | 用户—任务—权限矩阵 |
| 周二 | 划定 MVP 与非目标 | 优先 API、版本和运行闭环；拖拽画布、计费和跨地域先列为非目标 | MVP/非目标清单有理由 |
| 周三 | 设计领域对象 | 建模 Project、Agent、Version、Release、Tool、KnowledgeBase、Workflow、Run；避免直接套数据库表 | 领域关系图和不变量 |
| 周四 | 划分控制面与执行面 | 控制面管理可变配置，执行面只消费发布快照；写清调用和失败边界 | 控制面/执行面时序图 |
| 周五 | 多租户与资源归属 | 第一版可做轻量 Tenant/Project，但所有资源必须带归属且查询默认过滤 | 两项目隔离测试设计 |
| 周六 | 技术选型与 ADR | 对单体/微服务、同步/异步、PGVector/Qdrant 做证据化取舍，不为展示堆组件 | 至少三份 ADR |
| 周日 | 建平台骨架与健康检查 | 先完成模块边界、数据库迁移和健康接口；不提前填充所有功能 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: establish ai platform domain and architecture baseline`

必须包含：用户和用例、MVP/非目标、领域模型、平台架构、信任边界、ADR、服务骨架和数据库迁移。

验收标准：每个核心资源都有归属；控制面与执行面职责清晰；在本地可启动并验证数据库和健康状态。

## 第 18 周：Agent 注册、版本、发布与回滚

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 设计 Agent Definition | 输入输出 Schema、模型策略、Prompt 引用、工具和知识库都使用显式 ID；不要保存不可审计的大对象 | Agent Schema 可校验 |
| 周二 | Draft 与不可变 Version | 编辑 Draft，发布时生成不可变快照；相同内容可用 Hash 识别 | 已发布版本不可原地修改 |
| 周三 | Publish 与 Rollback | 发布前检查依赖版本和 Eval 状态；回滚切换 Release 指针而非覆盖历史 | 发布和回滚测试通过 |
| 周四 | Agent CRUD API 与并发控制 | 使用版本号或 ETag 防止覆盖更新；越权项目不能读取或修改资源 | 并发冲突和隔离测试 |
| 周五 | 配置校验与依赖解析 | 发布时确认模型、工具、知识库存在且可用；错误应定位到具体依赖 | 无效依赖不能发布 |
| 周六 | 最小管理界面或 API 集合 | 先实现列表、详情、编辑、版本、发布和回滚；UI 可简陋但状态必须准确 | 可完成完整管理流程 |
| 周日 | 运行两个 Agent 版本 | 用固定输入比较旧版和新版；确认 Run 记录绑定具体快照 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add versioned agent registry and release lifecycle`

必须包含：Agent 管理 API、版本快照、发布与回滚、项目隔离、并发更新保护、管理入口和自动测试。

验收标准：运行历史可追溯到不可变版本；回滚不删除新版；不同 Project 不可越权访问。

## 第 19 周：模型网关、路由、配额与降级

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | Provider 与 Model Alias | 业务和 Agent 引用平台别名，不直接散落供应商模型名；凭证只存 Secret 引用 | 可切换别名映射 |
| 周二 | 统一请求、响应与错误 | 统一 Usage、FinishReason、ToolCall 和流式事件；保留供应商扩展字段的边界 | 两个 Provider 适配同一接口 |
| 周三 | 本地模型、量化与微调边界 | 运行一个本地开源模型并记录内存/显存、吞吐和量化影响；写清 RAG、Prompt 与 LoRA/PEFT 的选择条件 | 本地推理实验和选型 ADR |
| 周四 | 超时、重试、熔断与 Cache | 重试只覆盖安全错误；Cache Key 包含模型、Prompt、Tool Schema 和参数，敏感内容不跨项目复用 | 故障与 Cache 隔离测试 |
| 周五 | 路由与 Fallback | 按能力、成本、延迟和数据策略路由；Fallback 前确认 Schema、上下文和工具能力兼容 | 主模型失败可受控降级 |
| 周六 | 配额、限流与成本预算 | 同时设置请求、Token、并发和单次预算；超额返回明确业务错误 | 超限请求不会调用模型 |
| 周日 | 基准与路由报告 | 用固定任务比较质量、P95 延迟、Token 和成本，避免只比回答观感 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: implement governed model gateway with routing`

必须包含：统一模型接口、至少两个适配器或一个真实加一个 Stub、模型别名、路由、配额、Fallback、Usage 和基准报告。

验收标准：业务代码不依赖供应商细节；配额和隔离由代码控制；失败、降级和成本可以观测。

## 第 20 周：Tool/MCP 与知识库管理

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | Tool Registry 与版本 | Schema、风险级别、Owner、权限和版本都必填；同名工具不可悄悄换语义 | 工具注册和版本 API |
| 周二 | Tool Credential 与权限 | 凭证使用引用，运行时按 Project、Agent、用户和 Scope 求交集 | 无授权工具无法注入 |
| 周三 | MCP Client/Server 与授权 | 同时做最小 Server 和 Client；HTTP 方式验证资源绑定，stdio 不套用 HTTP OAuth | MCP 往返与拒绝案例 |
| 周四 | 动态工具发现与上下文预算 | 工具多时先搜索再加载；对历史、工具结果和检索内容设置预算、裁剪和摘要策略 | Token 节省和质量对比 |
| 周五 | Knowledge Base 控制面 | 管理数据源、Chunk、Embedding、索引版本和状态；重建索引不覆盖线上版本 | 索引版本可切换 |
| 周六 | 进阶检索、权限与评测 | 比较 BM25+向量混合检索、Rerank、Query Rewrite；加入 ACL，并用 Recall@K/MRR 验证 | 质量提升且越权文档不召回 |
| 周日 | 平台核心端到端验收 | 发布一个同时使用模型、工具和知识库的 Agent，记录每项依赖版本 | 完成阶段提交 |

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

官方资料：[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)、[Hugging Face PEFT/LoRA](https://huggingface.co/docs/peft/main/conceptual_guides/lora)、[MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)、[MCP Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)。

下一阶段：[工作流与平台治理](07-workflow-governance.md)
