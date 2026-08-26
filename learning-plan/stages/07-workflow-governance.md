# 阶段七：工作流编排与平台治理

周期：第 21–24 周，共约 28 小时。

目标：将 LangGraph 的状态、Checkpoint 和人工审批能力产品化，形成版本化工作流、可靠运行中心、权限审计、评测门禁和基础生产运维能力。

## 开始前应会什么

- 能运行第 11 周 LangGraph 暂停/恢复流程和第 20 周平台 Agent 发布闭环。
- 能解释状态机、Checkpoint、幂等、超时、取消、权限和不可变版本。
- 能根据 traceId 和错误分类定位 Java、Python、模型或 Tool 失败。

## 零基础桥接

先把第 11 周单工作流的一次执行展开成 Run、Step、Event 三层记录，再加入 Project、发布版本和审批主体。用一张“进程在副作用前退出并恢复”的时序图，推导 Checkpoint、幂等键、状态迁移、审计和发布门禁，而不是先设计复杂编排产品。

## 本阶段不要求什么

- 不要求实现 BPMN 全集、通用低代码平台或可视化拖拽运行时。
- 不要求用消息队列掩盖不清晰的状态、幂等和错误契约。
- 不要求把审批、RBAC、预算或安全判断交给模型自由决定。

## 前测失败处理

若状态机和非法转换不清楚，先用普通代码实现三状态任务并写单测；若恢复会重复副作用，先回到单节点 Stub 写操作，验证 Checkpoint 前后边界和幂等键，再扩展工作流。

## 第 21 周：工作流定义与版本化

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 定义 Workflow DSL/Schema | 第一版支持 Agent、Tool、Condition、HumanApproval、End；明确不支持项，不直接做拖拽画布 | Workflow Schema 和示例 |
| 周二 | 节点输入输出与变量引用 | 每个节点声明 Schema，变量引用在保存时校验；避免依赖自由文本约定 | 错误引用不能发布 |
| 周三 | 条件、循环和汇聚 | 确定性条件使用表达式或代码；循环必须有计数和截止条件 | 分支与循环测试通过 |
| 周四 | 工作流版本与发布快照 | 发布时锁定节点配置及其 Agent/Tool 版本；运行中不可被 Draft 影响 | 旧运行不受新版本影响 |
| 周五 | 静态校验 | 检查不可达节点、无结束路径、非法环、缺失权限和 Schema 不匹配 | 无效图返回具体错误 |
| 周六 | 映射到 LangGraph | 平台 DSL 与 LangGraph State/Node/Edge 分层；不要把平台表结构直接当运行 State | 一个工作流可编译运行 |
| 周日 | 管理 API 与最小编辑入口 | 完成创建、校验、版本、发布、回滚和可视化只读图 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add versioned workflow definition and compiler`

必须包含：Workflow Schema、静态校验、版本发布、LangGraph 编译器、管理 API、示例图和测试。

验收标准：无结束路径或非法引用不可发布；运行绑定不可变版本；同一工作流可稳定复现路径。

## 第 22 周：可靠运行时、Checkpoint 与异步执行

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | Run/Step/Event 状态机 | 明确 Pending、Running、Waiting、Succeeded、Failed、Cancelled；非法状态迁移必须拒绝 | 状态迁移单测 |
| 周二 | Checkpoint 和恢复 | 每个有副作用节点前后保存边界；模拟进程退出后从上次成功点恢复 | 重启后不重复已完成步骤 |
| 周三 | 幂等和副作用凭证 | 写工具使用 idempotency key；把请求、结果引用和副作用摘要绑定到 Step | 重复投递不产生重复写入 |
| 周四 | 异步任务、轮询与事件 | 先实现清晰的异步协议和状态查询；消息队列只有在可靠性要求明确时引入 | 提交、查询、事件链路可用 |
| 周五 | Retry、Timeout 与补偿 | 节点级和全局截止时间分开；补偿不是简单重试，先列可逆和不可逆动作 | 故障矩阵与自动测试 |
| 周六 | 取消、暂停和恢复 | 取消需传播到模型和工具；无法取消的外部动作要标为未知并人工核对 | 四种状态行为可复现 |
| 周日 | 故障注入演练 | 注入模型超时、工具 500、进程退出、重复事件和数据库短暂失败 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: implement durable workflow runtime and run center`

必须包含：状态机、Checkpoint、恢复、幂等、取消、受控重试、异步 API、故障注入测试和运行详情。

验收标准：故障不返回假成功；恢复不重复副作用；每个 Run 能查看 Step、Event、错误和最终状态。

## 第 23 周：人工审批、RBAC、审计与 AI 安全

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | RBAC 与资源权限 | 权限至少覆盖查看、编辑、发布、运行、审批和审计；默认拒绝且查询带资源归属 | 角色权限矩阵和测试 |
| 周二 | 审批策略与任务内容 | 审批卡片展示目标、参数、影响、成本和验收；批准、编辑、拒绝都留记录 | 三种决策可恢复工作流 |
| 周三 | 审批超时与职责分离 | 高风险操作不能由发起人自批；超时应转人工或失败，不默认通过 | 自批和超时被阻止 |
| 周四 | 审计日志与证据链 | 记录谁在何时用哪个版本执行什么，敏感参数使用摘要或 Hash | 版本发布到工具调用可追溯 |
| 周五 | Prompt Injection 攻击实验 | 把网页、RAG 文档和工具输出视为不可信数据；测试指令覆盖和数据外泄 | 直接/间接注入阻断记录 |
| 周六 | MCP/Tool 投毒与输出校验 | 测试伪造工具描述、过宽 Scope、恶意输出和 Token 透传；执行前验证结构和权限 | 至少四类攻击测试 |
| 周日 | 威胁模型与残余风险 | 按资产、主体、信任边界、攻击路径、防护和残余风险整理 | 完成本周提交 |

### 本周提交

建议 Commit：`feat: enforce platform approval rbac and audit controls`

必须包含：RBAC、审批策略、职责分离、审计链、Prompt Injection/MCP 攻击用例、自动阻断和威胁模型。

验收标准：越权和自批失败；未审批副作用不发生；审计不泄密；不可信内容不能改变系统权限。

## 第 24 周：Eval、发布门禁、可观测性与运维

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 平台 Eval 对象模型 | Dataset、Case、Evaluator、Run、Score 与 Agent/Workflow Version 关联；数据集发布后不可偷改 | Eval Schema 和 API |
| 周二 | 离线回归和发布门禁 | 设置任务成功、安全、延迟和成本阈值；门禁失败不允许发布但可保留结果 | 劣化版本被阻止 |
| 周三 | Trace 与统一观测字段 | traceId 贯穿 Java、Python、模型和 Tool；默认不记录敏感 Prompt/结果正文 | 跨服务 Trace 可查询 |
| 周四 | 指标、SLO 和告警 | 选择可操作指标：成功率、P95、等待审批时长、Token、成本和越权阻断 | SLO 与告警规则草案 |
| 周五 | 限流、背压和容量测试 | 分别压模型、工作流和工具；记录饱和点和降级行为，不追求虚高 QPS | 压测曲线和容量结论 |
| 周六 | 备份恢复与故障手册 | 备份元数据、Checkpoint、评测和索引定义；实际恢复一次而非只写文档 | 恢复演练证据 |
| 周日 | 平台阶段验收 | 从 Agent Draft 到发布、运行、审批、观测、评测和回滚完整演示 | 完成阶段提交 |

### 阶段提交

建议 Commit：`feat: complete governed and observable workflow platform`

必须包含：Eval 模型、发布门禁、跨服务 Trace、仪表盘或查询、SLO、压测、备份恢复和完整演示脚本。

验收标准：劣化版本不可发布；关键故障有告警和手册；一个工作流可以暂停、恢复、取消、回滚并完整审计。

## 阶段出口条件

- 能把平台 Workflow Schema 编译为可运行、可持久化的 LangGraph 工作流。
- Run/Step/Event 状态清晰，支持恢复、幂等、取消和故障诊断。
- RBAC、审批、审计和工具权限均由平台代码控制。
- Agent/Workflow 发布需要通过固定 Eval 和安全门禁。
- 平台有基础 SLO、告警、压测和恢复证据。

官方资料：[LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[LangChain Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)、[Spring AI Observability](https://docs.spring.io/spring-ai/reference/observability/index.html)、[OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)。

下一阶段：[业务场景与流程设计](08-business-scenario-process.md)
