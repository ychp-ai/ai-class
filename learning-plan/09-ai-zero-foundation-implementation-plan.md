# AI 零基础开发者课程改造 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不改变 32 周周期、最终目标、必修知识和成果门禁的前提下，把整套课程调整为适合“具备开发基础、AI 零基础”的学习者。

**Architecture:** 保持现有九阶段和 32 周骨架，以“入口定位 → 学习方法与监督 → 前四周重排 → 后续阶段桥接 → 成果门禁 → 全局验证”的顺序修改。零基础支持通过前置诊断、开发经验类比、最小术语集、可观察实验、失败案例、Teach-back 和变体任务实现，不新增平行进度真相。

**Tech Stack:** Markdown、Python 3 进度扫描器、`rg`、Git 文档检查。

**Spec:** `learning-plan/08-ai-zero-foundation-curriculum-design.md`

## Global Constraints

- 周期固定为 32 周，日均投入约 1 小时。
- 最终交付固定为 `AI Agent Platform + Business Case`。
- Spring AI、LangChain、LangGraph 和 Claude Agent SDK 均保持必修。
- 原生模型 API、流式事件、结构化输出和手写 Tool Loop 必须先于高层框架。
- RAG、Tool/MCP、工作流、Checkpoint、审批、权限、Eval、可观测性、安全、运维和业务闭环不得删除或降级。
- 每日计划表继续使用 `日期`、`学习任务`、`当天学习建议`、`当天验收` 四列。
- 不修改进度扫描器 Schema，不重置或覆盖任何学习成果。
- 未经用户明确授权，不执行 Git Commit 或 Push；每个任务以 Diff 和检查结果作为审核点。

---

### Task 1: 统一课程入口与学习者画像

**Files:**

- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `learning-plan/README.md`

**Interfaces:**

- Consumes: `learning-plan/08-ai-zero-foundation-curriculum-design.md` 中的学习者画像和不变约束。
- Produces: 全仓库统一的入学基础、非前置知识、32 周定位和最终目标表述。

- [ ] **Step 1: 修改根协作规则中的学习者定义**

  将“面向具有后端开发基础的学习者”改为“面向具备基础开发能力、但没有 AI、机器学习、LLM、RAG 和 Agent 知识的开发者”。明确默认只要求一种编程语言、Git、命令行、HTTP、JSON、数据库和基础测试。

- [ ] **Step 2: 增加不可假定的 AI 前置知识**

  在 `AGENTS.md` 讲师规则中明确：首次出现专业术语时必须给出通俗定义、开发类比和反例；不得以学习者是程序员为由假定其理解 Token、Embedding、采样、Prompt、RAG、Tool Calling 或 Agent。

- [ ] **Step 3: 修改根 README 定位**

  首段使用“AI 零基础开发者”，增加简短“入学基础”说明，并保持两项最终交付能力和平台边界原文语义不变。

- [ ] **Step 4: 修改路线总览定位和学习比例**

  在 `learning-plan/README.md` 增加“默认具备/不要求具备”两组说明。学习比例调整为阶段化口径：第 1–4 周 `35% 原理、50% 实践、15% 评测复盘`；第 5–32 周回到 `20% 原理、65% 实践、15% 评测复盘`，总投入仍为约 224 小时。

- [ ] **Step 5: 检查入口表述**

  Run: `rg -n '后端程序员|后端开发经验|AI 零基础|机器学习' AGENTS.md README.md learning-plan/README.md`

  Expected: 入口均出现 AI 零基础定位；旧定位只在必要的历史说明中出现，不再作为入学要求。

### Task 2: 建立零基础学习方法和讲师监督机制

**Files:**

- Modify: `learning-plan/00-learning-method.md`
- Modify: `learning-plan/07-instructor-supervision.md`

**Interfaces:**

- Consumes: 每日零基础学习闭环、三次接触原则和新阶段桥接规则。
- Produces: 学习者每天可执行的方法，以及讲师前测、提示、验收和补救规则。

- [ ] **Step 1: 增加零基础每日闭环**

  在学习方法中加入“开发经验类比 → 一句话定义 → 最小实验 → 反例/失败 → Teach-back → 变体”的固定顺序，规定每天最多一个核心新概念。

- [ ] **Step 2: 增加术语和心智模型管理**

  定义术语记录格式：`术语 / 一句话解释 / 开发类比 / 不是什么 / 可观察证据 / 待验证问题`。禁止复制百科定义作为掌握证据。

- [ ] **Step 3: 增加不同阻塞类型的处理方式**

  区分“首次接触未记住、错误心智模型、语言或框架阻塞、缺少运行证据”，分别使用间隔复习、反例实验、桥接任务和重新运行处理。

- [ ] **Step 4: 增加入学诊断和阶段前测**

  在讲师监督规范中定义首次教学检查 Git、HTTP/JSON、测试和日志基础；每个阶段只检查真实依赖。前测失败时缩小当天范围并布置 15–30 分钟桥接任务。

- [ ] **Step 5: 收紧首次术语教学与判定**

  规定第一次使用 AI 术语时必须解释“是什么、为什么需要、输入输出、一个反例、不是什么”。只会运行示例但无法解释观察结果时最高判定 L1。

- [ ] **Step 6: 检查监督要素**

  Run: `rg -n '一个核心新概念|开发经验类比|一句话定义|入学诊断|阶段前测|15–30 分钟|最高判定.*L1' learning-plan/00-learning-method.md learning-plan/07-instructor-supervision.md`

  Expected: 每个零基础教学和监督要素至少有一个权威定义。

### Task 3: 重排阶段一并同步前四周成果

**Files:**

- Modify: `learning-plan/stages/01-ai-tools-and-engineering.md`
- Modify: `deliverables/week-01/README.md`
- Modify: `deliverables/week-02/README.md`
- Modify: `deliverables/week-03/README.md`
- Modify: `deliverables/week-04/README.md`

**Interfaces:**

- Consumes: 学习者不具备任何 AI 术语和心智模型的假设。
- Produces: 从 AI 基本分类逐步进入原生 API、Prompt/Eval 和 AI 工程闭环的四周课程。

- [ ] **Step 1: 增加阶段前置与非目标**

  增加“开始前应会什么、零基础桥接、本阶段不要求什么、前测失败处理”。非目标明确包括完整数学推导、从头训练模型和同时学习多个框架。

- [ ] **Step 2: 重排第 1 周**

  周一先学习 AI/ML/深度学习/生成式 AI/LLM 的关系以及训练和推理；周二学习 Token 与逐 Token 生成；周三学习 Embedding；周四学习采样；周五学习上下文与幻觉；周六测量延迟、Token 和成本；周日形成心智模型。Transformer/Attention 只作为解释生成机制的最小概念，不要求数学推导。

- [ ] **Step 3: 调整第 2 周桥接**

  将 HTTP/JSON 请求响应映射到模型 API，将逐 Token 生成映射到流式事件；依次进入结构化输出、Tool Calling、手写 Tool Loop 和故障控制，保留原有安全与可靠性要求。

- [ ] **Step 4: 调整第 3–4 周建议**

  第 3 周从函数契约类比 Prompt 契约并引入最小 Eval；第 4 周从确定性代码与不确定模型的边界进入 Fake、排错、错误契约、Trace 和架构表达。

- [ ] **Step 5: 同步前四周成果**

  Week 01 增加 AI 概念关系图和术语/心智模型；Week 02 保留原生客户端和 Tool Loop；Week 03 明确固定回归集；Week 04 明确 Fake、错误分类、Trace 和可复现服务。保留现有讲师验收字段。

- [ ] **Step 6: 验证每日表和成果同步**

  Run: `python3 scripts/detect_learning_progress.py --repo . --pretty`

  Expected: 当前阶段仍为 1、当前周仍为 1，`week_plan` 包含 7 天且周一从 AI 基本分类和训练/推理开始。

### Task 4: 为框架与组合阶段增加及时桥接

**Files:**

- Modify: `learning-plan/stages/02-java-llm-rag-agent.md`
- Modify: `learning-plan/stages/03-langchain-langgraph.md`
- Modify: `learning-plan/stages/04-claude-agent-sdk.md`
- Modify: `learning-plan/stages/05-integration-evaluation-delivery.md`

**Interfaces:**

- Consumes: 阶段一的原生 API、Tool Loop、测试和 Trace 基线。
- Produces: Spring AI、Python/LangChain/LangGraph、Claude Agent SDK 和组合评测的阶段前置与迁移路径。

- [ ] **Step 1: 增加阶段二桥接**

  前测 Java/Maven/Spring Boot 最小能力；用第 2 周原生模型客户端对照 Spring AI ChatClient、结构化输出和 Tool Calling。明确不要求先学完整 Spring 生态或训练模型。

- [ ] **Step 2: 增加阶段三桥接**

  前测 Python 虚拟环境、函数、类型和异常；提供 `venv → Pydantic → async for` 的最小桥接。用手写 Java Agent 对照 LangChain，用显式状态机对照 LangGraph。

- [ ] **Step 3: 增加阶段四桥接**

  从“应用调用模型”与“Agent 获得文件/Shell 工具并自主循环”的差别切入，按 Read → Edit → Bash → MCP 顺序增加权限；明确 SDK 不等于操作系统沙箱。

- [ ] **Step 4: 增加阶段五桥接**

  用一张单请求时序图复习 Java、Python、LangGraph 和 Claude Agent 职责，再组合服务；Eval 首先学习固定输入、预期、指标和 Baseline 四个词，不从复杂评测平台开始。

- [ ] **Step 5: 检查框架映射**

  Run: `rg -n '开始前应会什么|零基础桥接|本阶段不要求什么|前测失败处理' learning-plan/stages/0[2-5]-*.md`

  Expected: 四个阶段各出现完整的四项桥接结构。

### Task 5: 为平台、业务与交付阶段增加问题驱动桥接

**Files:**

- Modify: `learning-plan/stages/06-ai-platform-core.md`
- Modify: `learning-plan/stages/07-workflow-governance.md`
- Modify: `learning-plan/stages/08-business-scenario-process.md`
- Modify: `learning-plan/stages/09-pilot-production-capstone.md`
- Modify: `learning-plan/stages/README.md`

**Interfaces:**

- Consumes: 前 16 周端到端应用及其版本、权限、评测和运行证据。
- Produces: 从单应用痛点到平台抽象，以及从技术能力到业务流程和试点交付的学习路径。

- [ ] **Step 1: 增加阶段六桥接**

  先从“配置无法复用、版本不可追溯、权限散落、运行不可审计”四类单应用痛点推导控制面；明确不先学习微服务、Kubernetes、复杂计费和拖拽画布。

- [ ] **Step 2: 增加阶段七桥接**

  从第 11 周单工作流的暂停恢复映射到多项目 Run/Step/Event、发布门禁和运维；前测状态机、幂等、Checkpoint 和权限边界。

- [ ] **Step 3: 增加阶段八桥接**

  用开发者熟悉的需求、接口和故障流程类比业务角色、泳道、Baseline、AS-IS 和 TO-BE；明确不能用模型能力清单代替业务调研。

- [ ] **Step 4: 增加阶段九桥接**

  用 Stub → 契约测试 → E2E → UAT → 试点 → 生产就绪的顺序连接开发和业务交付；明确模拟数据不能冒充生产收益。

- [ ] **Step 5: 更新阶段索引说明**

  在阶段索引中说明所有阶段统一包含前置、桥接、非目标和前测失败处理，但框架周次和独立成果不变。

- [ ] **Step 6: 检查九阶段结构**

  Run: `rg -l '^## 开始前应会什么$' learning-plan/stages/0[1-9]-*.md | wc -l`

  Expected: `9`。

  Run: `rg -l '^## 零基础桥接$' learning-plan/stages/0[1-9]-*.md | wc -l`

  Expected: `9`。

  Run: `rg -l '^## 本阶段不要求什么$' learning-plan/stages/0[1-9]-*.md | wc -l`

  Expected: `9`。

### Task 6: 更新成果门禁并进行全局一致性验证

**Files:**

- Modify: `learning-plan/06-deliverable-standards.md`
- Modify if checks expose inconsistency: files changed in Tasks 1–5

**Interfaces:**

- Consumes: 重新设计后的学习方法、阶段计划和前四周成果模板。
- Produces: 不降低工程门禁的零基础认知证据要求，以及可验证的一致课程。

- [ ] **Step 1: 增加零基础认知证据门禁**

  在通用成果标准中增加：新概念首次学习需要自己的语言解释、开发类比、反例和可观察证据；第 1–4 周实验统一记录输入、观察、解释、反例和工程意义；复制资料不能代替 Teach-back。

- [ ] **Step 2: 检查必修知识仍存在**

  Run: `rg -n '原生模型 API|Spring AI|LangChain|LangGraph|Claude Agent SDK|RAG|Tool/MCP|Checkpoint|Eval|AS-IS|TO-BE|UAT|试点|回退' learning-plan/README.md learning-plan/stages learning-plan/06-deliverable-standards.md`

  Expected: 所有必修主题仍有路线说明、每日任务或成果门禁。

- [ ] **Step 3: 运行进度识别测试**

  Run: `python3 -m unittest scripts.tests.test_detect_learning_progress -v`

  Expected: 全部测试通过，0 failures。

- [ ] **Step 4: 运行当前仓库扫描**

  Run: `python3 scripts/detect_learning_progress.py --repo . --pretty`

  Expected: `repository_status=VALID`、`current_stage.id=1`、`current_week.number=1`、`recommended_day=周一`，周一任务为 AI 基本分类及训练/推理入门。

- [ ] **Step 5: 检查 Markdown 结构**

  Run: `rg -n '^\| 日期 \| 学习任务 \| 当天学习建议 \| 当天验收 \|$' learning-plan/stages/0[1-9]-*.md | wc -l`

  Expected: `32`。

  Run: `rg -l '^## 讲师验收$' deliverables/week-*/README.md | wc -l`

  Expected: `32`。

- [ ] **Step 6: 执行仓库文档门禁**

  Run: `git diff --check`

  Expected: exit 0，无格式错误。

  Run: `rg --files`

  Expected: 设计、实施计划和所有课程文件均可列出。

  Run: `git status --short`

  Expected: 只出现本次课程改造涉及的文档；不包含意外生成物。

- [ ] **Step 7: 人工核对不变目标**

  对照设计文档的九项验收标准逐条检查，并在最终交付说明中列出修改文件、保留的知识范围、实际验证、未验证项和限制。
