# 阶段八：业务场景掌握与流程设计优化

周期：第 25–28 周，共约 28 小时。

目标：掌握从业务问题发现到可实施接入方案的完整方法，避免拿着 Agent 技术寻找场景。四周围绕同一个真实或高保真业务流程持续产出。

## 开始前应会什么

- 能说明平台已经具备哪些 Agent、Workflow、权限、Eval 和运行治理能力及其边界。
- 能进行基础需求分析，阅读接口和数据字典，并区分事实、假设与建议。
- 能接受最终结论可能是规则改造、流程优化或 No-Go，而不是一定使用 AI。

## 零基础桥接

用开发者熟悉的需求、接口调用和故障链路类比业务方法：调用者对应业务角色，时序图扩展为泳道，现有接口与人工步骤组成 AS-IS，优化后的职责和系统交互组成 TO-BE，监控基线扩展为业务 Baseline。先拿一个三步骤非 AI 流程练习，再进入真实或高保真案例。

## 本阶段不要求什么

- 不要求具备产品经理或咨询顾问背景，也不要求使用复杂流程建模工具。
- 不允许用模型能力清单、聊天 Demo 或主观满意度代替业务问题和 Baseline。
- 不要求强行得出 Go 结论；证据不足、风险过高或收益不足时允许 No-Go。

## 前测失败处理

若无法区分事实和假设，先对一份示例需求逐句标注；若不会画泳道，先画“用户提交请求 → 服务处理 → 数据库写入 → 失败返回”的角色/系统流程，并补一个超时异常，再开始场景调研。

## 第 25 周：场景发现、业务调研与价值基线

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 建立候选场景清单 | 从频次、耗时、错误、知识密度、跨系统和可复核性评分；不要以“能聊天”作为价值<br>相关资料：[GOV.UK Discovery Phase](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works) | 至少三个场景评分表 |
| 周二 | 选择场景与明确业务目标 | 与业务负责人确认目标、非目标、用户、Owner 和决策期限；优先选择可小范围试点场景<br>相关资料：[GOV.UK Discovery Phase](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works) | 一页 Scene Brief |
| 周三 | 设计访谈提纲 | 分别询问执行者、审批者、系统 Owner 和风险角色；关注真实例外而非理想 SOP<br>相关资料：[GOV.UK 用户研究计划](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service) | 访谈问题与对象表 |
| 周四 | 执行访谈或高保真模拟 | 记录事实、原话摘要、分歧和待验证项；模拟案例必须注明假设和数据来源<br>相关资料：[GOV.UK Discovery 用户研究](https://www.gov.uk/service-manual/user-research/user-research-in-discovery) | 访谈纪要与问题清单 |
| 周五 | 数据和系统盘点 | 列出系统、接口、数据 Owner、时效、质量、权限、敏感级别和变更窗口<br>相关资料：[NIST Privacy Framework](https://www.nist.gov/privacy-framework) | 数据/系统清单 |
| 周六 | 建立业务基线 | 采集处理时长、等待时长、返工率、错误率、人工成本和满意度中的适用指标<br>相关资料：[GOV.UK Measuring Success](https://www.gov.uk/service-manual/measuring-success) | 有口径的 Baseline |
| 周日 | 场景立项评审 | 说明为什么适合 AI、为什么现在做、最大风险和停止条件；证据不足则不立项<br>相关资料：[NIST AI Resource Center](https://airc.nist.gov/) | 完成本周提交 |

### 本周提交

建议 Commit：`docs: complete business scenario discovery package`

必须包含：候选场景评分、Scene Brief、访谈纪要、系统和数据盘点、业务指标基线、假设清单、风险与停止条件。

验收标准：目标可量化；Owner 明确；每个关键结论标记事实或假设；场景不依赖“模型一定正确”。

## 第 26 周：AS-IS 流程、根因和约束分析

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 绘制 AS-IS 主流程 | 使用泳道表示角色和系统，标出输入、输出、等待和交接；不要只画 happy path<br>相关资料：[OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/) | 主流程图通过角色核对 |
| 周二 | 补异常和人工兜底 | 从历史问题或访谈中提取退回、缺数、超时、重复和紧急处理<br>相关资料：[OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/) | 至少五个异常分支 |
| 周三 | 量化每个步骤 | 区分处理时间与等待时间，记录频次和样本量；无法测量的标记估算<br>相关资料：[GOV.UK Measuring Success](https://www.gov.uk/service-manual/measuring-success) | 流程步骤数据表 |
| 周四 | 根因分析 | 对高耗时/高错误点做 5 Why 或因果分析；不要把“人员能力不足”当默认根因<br>相关资料：[ASQ Five Whys](https://asq.org/quality-resources/five-whys) | 两个痛点根因链 |
| 周五 | 决策与规则盘点 | 将确定性规则、经验判断、知识检索、生成和外部动作分类<br>相关资料：[OMG Decision Model and Notation](https://www.omg.org/spec/DMN/) | 决策表与规则归属 |
| 周六 | 合规、权限和组织约束 | 识别 PII、审批、审计、职责分离、数据驻留和变更窗口<br>相关资料：[NIST Privacy Framework](https://www.nist.gov/privacy-framework) | 约束矩阵 |
| 周日 | AS-IS 评审与机会排序 | 让流程参与者校正；只选最值得优化的 1–2 个环节进入方案<br>相关资料：[GOV.UK 用户全流程映射](https://www.gov.uk/service-manual/design/map-a-users-whole-problem) | 完成本周提交 |

### 本周提交

建议 Commit：`docs: model as-is process and root causes`

必须包含：AS-IS 泳道图、异常流程、步骤数据、根因分析、决策分类、权限合规约束和机会优先级。

验收标准：流程覆盖正常与异常；痛点有数据或访谈证据；AI 机会来自根因而非框架能力清单。

## 第 27 周：AI 适用性、TO-BE 流程与人机边界

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 任务适用性分解 | 按检索、分类、抽取、生成、规划、执行判断 AI 价值；确定性强的规则优先代码化<br>相关资料：[NIST 生成式 AI 风险框架](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | 任务—实现方式矩阵 |
| 周二 | 风险与置信度分层 | 依据影响和可逆性定义自动执行、抽检、事前审批和人工处理，不迷信模型自报置信度<br>相关资料：[NIST 生成式 AI 风险框架](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | 风险—控制策略矩阵 |
| 周三 | 设计 TO-BE 主流程 | 先优化流程再插入 Agent；删除无价值交接，保留必要审计和责任主体<br>相关资料：[GOV.UK 用户全流程映射](https://www.gov.uk/service-manual/design/map-a-users-whole-problem) | TO-BE 泳道图 |
| 周四 | 设计异常和降级流程 | 覆盖无答案、低质量、系统不可用、超时、权限不足和人工拒绝<br>相关资料：[NIST 生成式 AI 风险框架](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | 降级与兜底流程 |
| 周五 | 定义业务和 AI 验收指标 | 同时设置业务指标、模型/Agent 指标、安全指标和工程指标，写清口径与阈值<br>相关资料：[GOV.UK Measuring Success](https://www.gov.uk/service-manual/measuring-success) | 指标树和验收门槛 |
| 周六 | 估算收益、成本与容量 | 计算调用量、Token、人工复核、开发运维和失败成本；给出最好/正常/最差区间<br>相关资料：[AWS Well-Architected Cost Optimization](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html) | ROI/TCO 粗算表 |
| 周日 | 方案评审和 Go/No-Go | 展示 AS-IS/TO-BE 差异、收益、风险、限制和试点范围；允许得出“不该做”<br>相关资料：[NIST AI Resource Center](https://airc.nist.gov/) | 完成本周提交 |

### 本周提交

建议 Commit：`docs: design to-be human ai workflow and value case`

必须包含：AI 适用性矩阵、TO-BE 流程、风险分层、降级方案、指标树、ROI/TCO 和 Go/No-Go 记录。

验收标准：关键责任仍有明确主体；高风险动作有控制；优化收益能够与 AS-IS 基线比较。

## 第 28 周：业务接入与试点设计

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 选择接入模式 | 比较同步 API、异步事件、嵌入页面、批任务和 Copilot；依据用户流程选择，不按技术偏好<br>相关资料：[OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | 接入模式 ADR |
| 周二 | 设计领域契约 | 契约使用业务语义，包含版本、幂等、错误、状态和 Trace；不直接暴露内部 Prompt<br>相关资料：[OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | OpenAPI/事件 Schema 草案 |
| 周三 | 数据映射与权限传递 | 明确字段来源、脱敏、最小化、保留期和授权主体；禁止把用户 Token 直接传给 Tool<br>相关资料：[OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700.html) | 数据映射和权限时序图 |
| 周四 | 配置 Agent 与 Workflow | 将 TO-BE 步骤映射到平台 Agent、Tool、KB、审批和节点，记录每项版本<br>相关资料：[LangGraph Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | 场景配置清单 |
| 周五 | 设计测试金字塔 | 覆盖契约、组件、工作流、Eval、E2E、安全和用户验收；真实外部系统准备 Stub<br>相关资料：[Martin Fowler：Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) | 测试与样例矩阵 |
| 周六 | 制定试点和灰度计划 | 明确人群、流量、时长、观察指标、回退、人工值守和停止条件<br>相关资料：[GOV.UK Beta Phase](https://www.gov.uk/service-manual/agile-delivery/how-the-beta-phase-works) | Pilot Plan |
| 周日 | 接入设计评审 | 业务、平台、安全和运维视角逐项审查，未通过项形成明确闭环<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成阶段提交 |

### 阶段提交

建议 Commit：`docs: finalize business integration and pilot design`

必须包含：接入 ADR、接口契约、数据映射、权限时序、场景配置、测试策略、试点计划、回退和评审记录。

验收标准：业务流程能映射到平台配置；接口和错误语义稳定；安全、运维和业务验收都有负责人和证据要求。

## 阶段出口条件

- 能从业务目标出发选择场景，而不是从模型能力反推伪需求。
- 能绘制并验证 AS-IS、异常流程和 TO-BE 人机协作流程。
- 能区分确定性规则、模型判断、人工决策和系统副作用。
- 能设计业务契约、数据权限、试点、回退和指标体系。
- 能基于证据作出 Go/No-Go 决策。

下一阶段：[试点上线与最终交付](09-pilot-production-capstone.md)
