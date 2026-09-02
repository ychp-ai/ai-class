# AI 平台工程与业务落地学习计划

这是一套面向 **AI 零基础开发者** 的长期 AI 工程实践仓库。学习者只需具备一种编程语言、Git、命令行、HTTP/JSON、数据库、基础测试和排错经验，不要求预先了解机器学习、LLM、RAG、Agent 或任何 AI 框架。

课程目标是在**每天约 1 小时、共 32 周**的节奏下，形成两项可以独立交付的能力：

1. 建设一个技术型 AI 平台，提供模型接入、Agent 管理、工具与知识库管理、工作流编排、运行追踪、评测、安全和基础运维能力。
2. 将 AI 能力接入真实业务系统，完成场景发现、现状调研、流程优化、方案设计、系统集成、试点上线、效果评估与持续迭代。

计划不把“学会框架 API”视为终点。最终需要同时证明：理解核心原理、能实现平台能力、能诊断生产问题、能推动业务闭环。

## 入学基础与教学起点

- 可以阅读和修改小型程序，运行单元测试并根据日志排查基础问题。
- 了解 Web API、JSON、数据库和环境变量的基本使用。
- 不要求掌握 AI 数学、模型训练、Python Agent 开发或 Java AI 框架。
- 第 1 周从 AI、机器学习、生成式 AI 和 LLM 的关系开始；每个新阶段都会先做前测并提供最小桥接。
- 零基础只改变讲解顺序和练习脚手架，不减少 Spring AI、LangChain、LangGraph、Claude Agent SDK、平台治理或业务落地内容。

## 学习计划导航

| 文档 | 内容 |
| --- | --- |
| [完整路线总览](learning-plan/README.md) | 32 周路线、能力模型、架构边界和里程碑 |
| [逐节课程教程](learning-plan/tutorials/README.md) | 32 周、224 节课的学习步骤、资料章节、参考图、样例代码、掌握验证和参考答案 |
| [学习方法与建议](learning-plan/00-learning-method.md) | 每天 1 小时的学习、实践与复盘方式 |
| [开发语言路线](learning-plan/01-language-roadmap.md) | Java 主平台、Python 执行面、TypeScript 控制台的周次分工与切换桥接 |
| [讲师监督与掌握度评估](learning-plan/07-instructor-supervision.md) | 每日监督、提示阶梯、评分、阶段考试和动态调整 |
| [Hermes 进度识别入口](prompts/progress-detection.md) | 确定性扫描器与 FAST、REVIEW、FULL 低 Token 路由 |
| [阶段一：AI 原理、工具与工程协作](learning-plan/stages/01-ai-tools-and-engineering.md) | 第 1–4 周：LLM 原理、原生 API、Prompt 和 AI 编程协作 |
| [阶段二：Java LLM、RAG 与 Agent](learning-plan/stages/02-java-llm-rag-agent.md) | 第 5–8 周：Spring AI、RAG、Tool Calling 和 Agent 循环 |
| [阶段三：LangChain 与 LangGraph](learning-plan/stages/03-langchain-langgraph.md) | 第 9–11 周：结构化 Agent、状态和可恢复工作流 |
| [阶段四：Claude Agent SDK](learning-plan/stages/04-claude-agent-sdk.md) | 第 12–13 周：执行型 Agent、权限、Hooks 和隔离 |
| [阶段五：组合、评测与首个应用](learning-plan/stages/05-integration-evaluation-delivery.md) | 第 14–16 周：端到端 AI 应用、Eval 和可观测性 |
| [阶段六：AI 平台核心](learning-plan/stages/06-ai-platform-core.md) | 第 17–20 周：平台架构、Agent、模型、工具和知识库管理 |
| [阶段七：工作流与平台治理](learning-plan/stages/07-workflow-governance.md) | 第 21–24 周：编排运行时、审批、权限、评测和运维 |
| [阶段八：业务场景与流程设计](learning-plan/stages/08-business-scenario-process.md) | 第 25–28 周：调研、AS-IS/TO-BE、价值评估和接入设计 |
| [阶段九：试点上线与最终交付](learning-plan/stages/09-pilot-production-capstone.md) | 第 29–32 周：系统接入、试点、生产硬化和效果复盘 |
| [成果与提交标准](learning-plan/06-deliverable-standards.md) | 每周提交、阶段出口、平台和业务验收标准 |
| [Agent 协作规范](AGENTS.md) | 仓库目录、讲师监督、工程质量、安全和业务落地约束 |

## 课程仓库与个人仓库

本仓库只保存可共享的课程内容：路线、教程、成果要求、学习者仓库模板、监督 Prompt 和确定性工具。任何人的当前进度、笔记、评分、代码、实验数据和业务成果都必须保存在独立的个人仓库。

新学习者可以直接复用本仓库，并初始化自己的仓库：

```bash
git clone <ai-class-course-repository> ai-class
git clone <your-personal-learning-repository> ai-class-note
python3 ai-class/scripts/init_learning_progress.py \
  --course-repo ai-class \
  --progress-repo ai-class-note
```

每位学习者使用自己的第二个仓库地址即可。`ai-class/` 与 `ai-class-note/` 是两个同级目录和两个独立 Git 仓库，不存在 Git 文件归属冲突。

## 公共模板与工具导航

| 目录 | 存放内容 |
| --- | --- |
| [deliverables](deliverables/README.md) | 第 1–32 周公共成果要求和空白验收模板，不含个人状态 |
| [templates](templates/README.md) | 个人仓库所需的完整目录和文档模板 |
| [prompts](prompts/README.md) | 经评测、带版本的 Prompt 和模板 |
| [scripts](scripts/README.md) | 个人仓库初始化、双仓进度扫描和低 Token 自动化辅助工具 |

## 目标平台边界

最终平台采用“API 优先、轻量控制台、先单体后拆分”的路线，至少支持：

- 项目或轻量租户隔离、用户角色与服务账号。
- 模型供应商配置、模型路由、限额和降级。
- Agent 定义、版本、发布、回滚和运行参数。
- Tool/MCP 注册、权限、凭证引用和调用审计。
- 知识库、索引版本、检索配置和权限过滤。
- 工作流定义、条件分支、循环上限、人工审批、暂停与恢复。
- 同步与异步运行、幂等、取消、重试和失败状态。
- Trace、Token、延迟、成本、评测集和版本回归。
- 一套最小管理控制台：Agent、工作流和运行记录管理。

第一版不强制实现可视化拖拽画布、复杂计费系统、跨地域容灾或大规模 Kubernetes 多集群。只有基线数据证明需要时才增加复杂度。

## 业务落地闭环

```text
业务目标与约束
→ 角色访谈和数据调研
→ AS-IS 现状流程
→ 痛点、风险和价值基线
→ AI 适用性与可行性判断
→ TO-BE 人机协作流程
→ 系统接口和权限设计
→ 试点、验收与灰度上线
→ 效果监测、复盘和持续优化
```

最终业务案例不能只展示模型回答，需要同时提交过程证据、方案取舍、异常流程、人工兜底、业务指标和上线后的改进记录。

## 最终交付

最终成果为 **AI Agent Platform + 一个真实或高保真业务场景**：

- 平台能够管理并发布多个 Agent 和版本化工作流。
- 业务系统通过稳定 API、事件或嵌入式页面接入平台。
- 至少一个场景完整经历调研、流程优化、集成、试点和复盘。
- 具备固定 Eval、安全测试、运行观测、成本统计和故障处理手册。
- 能在干净环境启动，并用成功、失败、审批、恢复和越权阻断场景验收。

## 当前执行方式

1. 使用 `scripts/init_learning_progress.py` 建立独立个人仓库，再阅读[学习方法与建议](learning-plan/00-learning-method.md)。
2. 从[逐节课程教程](learning-plan/tutorials/README.md)打开当周课程，按[开发语言路线](learning-plan/01-language-roadmap.md)确认默认语言；所有进度、笔记和成果写入个人仓库。
3. 每周日整理成果、失败证据和下一周决策。
4. 按[成果与提交标准](learning-plan/06-deliverable-standards.md)自检。
5. 只有通过当前阶段出口条件，才进入下一阶段。

如果一周的核心验收没有通过，优先补齐闭环；平台能力和业务价值必须分别验收，不能互相替代。
