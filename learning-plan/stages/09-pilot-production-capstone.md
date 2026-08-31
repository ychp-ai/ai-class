# 阶段九：业务试点、生产硬化与最终交付

周期：第 29–32 周，共约 28 小时。

目标：基于阶段八的方案完成真实或高保真业务系统接入，经历联调、用户验收、灰度试点、故障演练、效果复盘和平台最终发布。

逐节学习入口：[第 29–32 周课程教程](../tutorials/README.md)。

## 本阶段语言定位

第 29–32 周组合 Java 控制面/业务 Connector、Python Agent 执行面与按需 TypeScript 控制台完成交付。最终验收必须覆盖跨语言契约、身份与 traceId 传播、超时取消、幂等副作用、失败映射和版本回滚，不接受三个独立 Demo 代替端到端系统。完整分工见[开发语言路线](../01-language-roadmap.md)。

## 开始前应会什么

- 已完成同一场景的 Scene Brief、AS-IS、TO-BE、接入契约、权限设计、指标和试点计划。
- 能发布并回滚版本化 Agent/Workflow，运行固定 Eval、安全测试和故障恢复。
- 能区分本地 Stub、高保真模拟、测试环境和真实试点证据。

## 零基础桥接

把熟悉的软件交付流程扩展为业务 AI 交付：Stub → 契约测试 → E2E → UAT → 影子/小流量试点 → 生产就绪 → 效果复盘。为每一步写清参与角色、输入数据、通过条件、停止条件和回退动作，确保技术测试与业务验收都能追溯到同一发布版本。

## 本阶段不要求什么

- 不要求未经授权接触生产系统、客户数据或高风险自动执行。
- 不要求用模拟数据证明真实收益，也不要求为了最终展示隐藏失败和 No-Go 结论。
- 不要求达到大型企业平台的规模、跨地域容灾和长期运营成熟度。

## 前测失败处理

若阶段八方案缺少 Owner、Baseline、异常路径或回退，先补齐设计评审，不直接编码；若真实系统不可用，使用明确标记的 Stub/高保真环境完成契约、权限和流程闭环，并把真实验证列为未完成范围。

## 第 29 周：业务系统接入与端到端联调

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 建业务 Connector/Adapter | 将业务 DTO 与平台契约隔离；先实现 Stub 和契约测试，再连接真实测试环境<br>相关资料：[Microsoft Anti-corruption Layer](https://learn.microsoft.com/azure/architecture/patterns/anti-corruption-layer) | Connector 契约测试通过 |
| 周二 | 身份、权限与租户上下文 | 用户、Project、Scope 和审计主体端到端传播；缺失上下文默认拒绝<br>相关资料：[OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700.html) | 越权和缺失身份测试 |
| 周三 | 数据读写与幂等 | 读工具和写工具分离；写入前后保存业务 ID、幂等键和结果状态<br>相关资料：[RFC 9110：幂等方法](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods) | 重试不重复创建业务数据 |
| 周四 | 场景 Agent 与 Workflow 发布 | 从平台发布不可变版本，绑定模型、Prompt、Tool、KB 和 Workflow 版本<br>相关资料：[Semantic Versioning](https://semver.org/) | 发布清单可追溯 |
| 周五 | 正常主流程 E2E | 从业务入口触发到结果回写，全链路传播 traceId；不靠手工改库<br>相关资料：[W3C Trace Context](https://www.w3.org/TR/trace-context/) | 主流程自动化通过 |
| 周六 | 异常、超时和人工路径 E2E | 覆盖资料不足、权限不足、工具失败、审批拒绝和取消<br>相关资料：[Google SRE：Testing for Reliability](https://sre.google/sre-book/testing-reliability/) | 五类异常不假成功 |
| 周日 | 联调问题复盘 | 区分契约、数据、权限、模型、流程和环境问题，记录根因和回归用例<br>相关资料：[Google SRE：Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: integrate business system with agent platform`

必须包含：Connector、契约测试、身份和权限传递、幂等写入、发布清单、正常与异常 E2E、联调问题清单。

验收标准：业务系统不感知内部模型供应商；所有副作用可追踪；异常状态可以被业务方正确处理。

## 第 30 周：用户验收、试点与流程优化验证

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 准备 UAT 数据和脚本 | 从 AS-IS 的真实分布抽取正常、边界和失败案例；脱敏后固定版本<br>相关资料：[GOV.UK Moderated Usability Testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | UAT 数据集和操作脚本 |
| 周二 | 执行内部 UAT | 观察用户操作路径、理解成本和错误恢复，不只问“好不好用”<br>相关资料：[GOV.UK Moderated Usability Testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | 问题按严重度分类 |
| 周三 | 修复 P0/P1 并回归 | 每个修复先增加回归用例；不要在试点前大范围更换模型或架构<br>相关资料：[Google SRE：Testing for Reliability](https://sre.google/sre-book/testing-reliability/) | 关键问题关闭有证据 |
| 周四 | 小流量或影子试点 | 首选建议模式或影子模式验证准确性；高风险动作继续人工审批<br>相关资料：[GOV.UK Beta Phase](https://www.gov.uk/service-manual/agile-delivery/how-the-beta-phase-works) | 试点流量和版本可追踪 |
| 周五 | 监控业务与 AI 指标 | 同时观察处理时间、返工、采纳率、完成率、越权、延迟和成本<br>相关资料：[GOV.UK Measuring Success](https://www.gov.uk/service-manual/measuring-success) | 日报可从数据生成 |
| 周六 | 用户反馈与失败分析 | 将反馈映射到流程、知识、模型、工具、界面或培训，不把所有问题归因于 Prompt<br>相关资料：[GOV.UK Discovery 用户研究](https://www.gov.uk/service-manual/user-research/user-research-in-discovery) | 失败分类和优先级 |
| 周日 | TO-BE 流程验证 | 对比 Baseline，检查流程是否真的减少等待和交接；收益不足则调整或停止<br>相关资料：[GOV.UK Measuring Success](https://www.gov.uk/service-manual/measuring-success) | 完成本周提交 |

### 本周提交

建议 Commit：`test: complete business pilot and workflow validation`

必须包含：UAT 数据、测试记录、修复回归、试点版本、指标日报、用户反馈、失败分析和 AS-IS/TO-BE 对比。

验收标准：试点范围、版本和数据可追溯；没有隐藏失败样例；业务收益和风险都基于统一口径。

## 第 31 周：生产硬化、演练与运行交接

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 配置、Secret 与环境隔离 | 开发、测试、生产配置分离；Secret 只用引用；检查日志、Trace 和错误响应泄露<br>相关资料：[OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | 密钥扫描和配置审查通过 |
| 周二 | 容量、限流与降级演练 | 按试点峰值倍数压测；触发模型限流和外部系统慢响应，验证队列和用户提示<br>相关资料：[Grafana k6 Documentation](https://grafana.com/docs/k6/latest/) | 有容量边界和降级证据 |
| 周三 | 安全攻击回归 | 运行 Prompt Injection、越权、工具投毒、路径和命令攻击集；新版本不得降低阻断率<br>相关资料：[OWASP Agentic AI Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 安全回归报告 |
| 周四 | 备份、恢复和回滚 | 恢复元数据、Checkpoint 与关键配置；演练 Agent/Workflow 回滚和业务开关<br>相关资料：[PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html) | RTO/RPO 或实测恢复时间 |
| 周五 | 告警、Runbook 与值守 | 每条告警关联影响、确认方式、止损、恢复和升级联系人；删除无法行动的告警<br>相关资料：[Google SRE：Practical Alerting](https://sre.google/sre-book/practical-alerting/) | 至少三份 Runbook |
| 周六 | 发布和变更流程 | 建立 Eval、安全、审批、灰度、观察和回滚门禁；Prompt 变更也按版本发布<br>相关资料：[Google SRE：Release Engineering](https://sre.google/sre-book/release-engineering/) | 发布 Checklist 可执行 |
| 周日 | 生产就绪评审 | 逐项审查功能、质量、安全、容量、恢复和业务 Owner；未通过项不得粉饰<br>相关资料：[Google SRE：Reliable Product Launches](https://sre.google/sre-book/reliable-product-launches/) | 完成本周提交 |

### 本周提交

建议 Commit：`chore: harden platform and complete production readiness review`

必须包含：环境与 Secret 设计、压测、安全回归、恢复演练、Runbook、发布门禁和生产就绪评审。

验收标准：关键故障可发现、可止损、可恢复；平台变化均能回滚；已知风险有 Owner 和处理期限。

## 第 32 周：效果复盘、平台发布与能力答辩

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 复核运行和业务数据 | 固定统计区间、样本和口径；区分相关性与因果，不把试点波动都归功于 AI<br>相关资料：[GOV.UK Measuring Success](https://www.gov.uk/service-manual/measuring-success) | 最终指标数据包 |
| 周二 | 计算收益、成本和风险 | 汇总节省时间、返工变化、调用成本、复核成本和事故风险，报告区间而非假精确值<br>相关资料：[AWS Well-Architected Cost Optimization](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html) | ROI/TCO 复盘 |
| 周三 | 决定推广、调整或停止 | 依据预设阈值作决策；推广必须说明适用边界和新增容量/治理需求<br>相关资料：[NIST AI Resource Center](https://airc.nist.gov/) | 决策记录和后续路线 |
| 周四 | 整理平台发布包 | 从干净环境安装、迁移、启动、创建 Agent、发布工作流和运行案例<br>相关资料：[Reproducible Builds](https://reproducible-builds.org/docs/) | 发布包可复现 |
| 周五 | 完成架构和业务案例文档 | 图和字段必须与当前实现一致；分别写平台设计与业务过程，避免只列框架<br>相关资料：[C4 Model](https://c4model.com/) | 文档审查无过期描述 |
| 周六 | 准备最终演示与故障场景 | 依次展示管理、发布、业务触发、审批、恢复、评测、攻击阻断和回滚<br>相关资料：[Google SRE：Testing for Reliability](https://sre.google/sre-book/testing-reliability/) | 20 分钟内稳定演示 |
| 周日 | 能力答辩与学习复盘 | 按原理、实现、取舍、证据、失败、优化和限制回答；列出下一阶段真实流量目标<br>相关资料：[讲师监督与掌握度评估](../07-instructor-supervision.md) | 完成最终提交 |

### 最终提交

建议 Commit：`docs: release ai agent platform and business adoption case`

必须包含：

- 可复现的 AI Agent Platform 发布包和最小管理控制台。
- Agent、模型、Tool/MCP、知识库、Workflow、Run、Eval、RBAC 和审计能力。
- 一个业务案例的调研、AS-IS、TO-BE、接入、UAT、试点、指标和复盘全套材料。
- 自动化测试、固定 Eval、安全攻击集、压测和恢复演练。
- 架构图、部署说明、Runbook、发布/回滚步骤和已知限制。
- 演示脚本：发布 Agent、运行工作流、业务接入、审批、恢复、攻击阻断和版本回滚。

最终验收标准：

1. 干净环境可以按文档启动平台并完成核心流程。
2. 一个业务场景可以从业务系统触发并获得可处理的成功或失败结果。
3. 平台资源和运行均可追溯到具体版本、用户和 Project。
4. 未授权、未审批、超预算和攻击输入被可靠阻断。
5. 业务效果有 Baseline、试点数据、成本和明确结论。
6. 能说明为何采用 Spring AI、LangChain、LangGraph 和 Claude Agent SDK，以及各自没有承担什么职责。

## 阶段出口条件

- 能独立部署、运营和演进一个技术型 AI 平台 MVP。
- 能独立完成业务场景发现、流程分析、方案设计、系统接入、试点和复盘。
- 能基于质量、成本、延迟、安全和业务指标做技术决策。
- 能处理失败、降级、审批、恢复、回滚和安全事件，而不只展示正常回答。
- 能明确平台 MVP 与企业级规模化能力之间尚存的差距。
