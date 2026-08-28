# 阶段一：AI 原理、原生 API 与工程协作

周期：第 1–4 周，共约 28 小时。

目标：建立 LLM 工程直觉，能够脱离高层框架完成模型调用、流式处理、结构化输出和最小 Tool Loop，并形成可靠的 AI 辅助编程习惯。后续仍将完整学习 Spring AI、LangChain、LangGraph 和 Claude Agent SDK；本阶段的原生实现用于理解这些框架隐藏的行为。

## 开始前应会什么

- 能运行一个小程序和单元测试，并保存命令、输入、输出和错误信息。
- 理解 HTTP 请求/响应、JSON、环境变量和函数调用的基本含义。
- 能使用 Git 查看 Diff；不要求任何 AI、数学或模型知识。

## 零基础桥接

开始第 1 周前，用 15–30 分钟完成一个非 AI 小实验：调用公开或本地 Stub HTTP API，打印 JSON 响应、耗时和一次错误响应。后续把模型调用持续映射到这个熟悉的请求链路，再逐步观察 Token、流式事件、结构化输出和工具请求的差异。

## 本阶段不要求什么

- 不要求推导 Transformer、Attention、梯度下降或 Embedding 数学公式。
- 不要求从头训练或微调模型，也不要求搭建 GPU 环境。
- 不要求同时学习 Spring AI、LangChain 或 Agent SDK；本阶段先看清原生协议和失败模式。

## 前测失败处理

如果不能独立运行 HTTP/JSON 小程序或单元测试，先补最小请求、环境变量和测试桥接，并把第 1 天目标缩小为“成功运行并解释输入输出”。不得一边补通用开发基础，一边堆叠多个 AI 术语。

## 第 1 周：LLM 工程基础与可测实验

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | AI、机器学习、深度学习、生成式 AI 与 LLM；训练和推理 | 先画概念包含关系，再用“开发阶段构建产物、运行阶段处理请求”类比训练与推理；注明类比的局限<br>相关资料：[Google 机器学习术语表](https://developers.google.com/machine-learning/glossary) | 一张概念关系图和训练/推理输入输出说明 |
| 周二 | Token、Tokenizer、上下文与逐 Token 生成 | 先观察文本如何变成 Token，再用最小图解释 Transformer/Attention 如何利用上下文预测下一个 Token；不推导公式，不把字符数当 Token 数<br>相关资料：[Hugging Face Tokenizer 概览](https://huggingface.co/docs/transformers/main/tokenizer_summary) | Token 对比脚本、逐 Token 生成图和上下文限制说明 |
| 周三 | Embedding 与语义相似度 | 用 8–10 句自建样本计算相似度，加入一个词相近但语义相反的干扰项<br>相关资料：[Sentence Transformers 语义相似度](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) | 可复现实验和失败解释 |
| 周四 | Temperature、Top-p 与随机性 | 固定 Prompt 分别运行多组参数，每组至少 5 次；区分模型随机性和提示不完整<br>相关资料：[Hugging Face 生成策略](https://huggingface.co/docs/transformers/main/generation_strategies) | 参数—质量—稳定性对比表 |
| 周五 | 上下文污染与幻觉 | 设计有答案、无答案、冲突资料三类问题；要求模型引用输入证据并观察错误模式<br>相关资料：[NIST 生成式 AI 风险框架](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | 三类失败样例和归因 |
| 周六 | 延迟、Token 和成本测量 | 记录首 Token 延迟、总延迟、输入输出 Token；不要用一次结果代表性能<br>相关资料：[OpenAI 延迟优化](https://platform.openai.com/docs/guides/latency-optimization) | 最小基准脚本和原始记录 |
| 周日 | 整理 LLM 工程心智模型 | 用自己的语言解释模型能做什么、不能保证什么；把尚未验证的观点标为假设<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成本周提交 |

### 本周提交

建议 Commit：`docs: add reproducible llm engineering experiments`

必须包含：AI/ML/深度学习/生成式 AI/LLM 概念关系图；训练与推理说明；Token、Embedding、采样和幻觉实验；运行方式；原始结果；至少两个失败案例；`docs/llm-engineering-basics.md`。

最低验收：实验可重复；参数和模型版本有记录；能解释 Token、Embedding、采样与上下文对质量和成本的影响。

## 第 2 周：原生模型 API 与手写 Tool Loop

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 从 HTTP/JSON 映射到模型 API | 先标出 endpoint、headers、请求消息、模型参数、响应和错误，再实现一次非流式请求；保存请求 ID、模型版本和 Usage<br>相关资料：[OpenAI API Quickstart](https://platform.openai.com/docs/quickstart) | 原生调用可运行、字段映射清楚且无密钥入库 |
| 周二 | 从逐 Token 生成映射到流式事件和取消 | 先区分 SSE/事件边界、内容增量、Usage 和结束事件；不要把网络数据块直接当完整消息<br>相关资料：[OpenAI Streaming Events](https://platform.openai.com/docs/api-reference/responses-streaming) | 可按事件类型流式输出并主动取消 |
| 周三 | 结构化输出与 Schema 校验 | 使用 JSON Schema 或类型模型校验；故意诱导缺字段、错误类型和额外字段<br>相关资料：[OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | 成功与校验失败均可复现 |
| 周四 | Tool Calling 协议 | 打印模型提出的工具名、参数和 call ID；明确模型只提出请求，应用负责执行<br>相关资料：[OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | 保存完整工具调用时序 |
| 周五 | 手写最小 Agent Loop | 加入最大步数、未知工具、参数错误和工具异常；不要使用 Agent 框架<br>相关资料：[OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | 两工具循环可正常停止 |
| 周六 | 超时、重试、限流和幂等 | 只重试可安全重试的错误，记录退避；用幂等键避免写工具重复副作用<br>相关资料：[RFC 9110：幂等方法](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods) | 四类故障测试通过 |
| 周日 | 对比框架将要隐藏的能力 | 列出模型客户端、Tool Loop、错误处理和观测接口，作为后续框架对比基线<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: implement native model client and guarded tool loop`

必须包含：非流式与流式调用、结构化输出、两个工具、最大步骤、取消、超时、受控重试、错误分类和测试。

最低验收：不使用 Spring AI、LangChain 或 Agent SDK 也能运行；未知工具和非法参数不会执行；失败不会返回假成功。

## 第 3 周：Prompt 工程与 AI 编程协作

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 从函数契约理解 Prompt 的角色、上下文和约束 | 类比函数的参数、返回类型、前置条件和错误约定，同时记录 Prompt 与确定性函数不一样的地方<br>相关资料：[OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering) | 两版 Prompt 的输入、约束和输出差异有证据 |
| 周二 | Few-shot、反例和拒答 | 示例应覆盖边界而非只给正常路径；加入资料不足时明确拒答的例子<br>相关资料：[OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering) | 固定样例集结果更稳定 |
| 周三 | Prompt 版本与最小 Eval 回归集 | 先固定输入、预期、判定规则和模型配置；每次只改变一个主要变量，不为提分替换困难样例<br>相关资料：[OpenAI Evals 指南](https://platform.openai.com/docs/guides/evals) | 可重复比较两个 Prompt 版本 |
| 周四 | AI 辅助理解代码仓库 | 要求 AI 先搜索证据再下结论，所有结论回到文件和测试；抽查至少三项<br>相关资料：[Google SRE：Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) | 形成可核验调用链说明 |
| 周五 | AI 辅助实现最小变更 | 先写验收测试再让 AI 修改；检查 Diff 中的额外重构和依赖变化<br>相关资料：[Martin Fowler：Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) | 一个小功能测试通过 |
| 周六 | AI 输出审查与安全 | 检查命令、依赖、许可证、敏感信息和越权访问；至少拒绝一条不安全建议<br>相关资料：[OWASP Agentic AI Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 审查清单和拒绝记录 |
| 周日 | 固化可复用协作模板 | 模板包含目标、上下文、非目标、验收、可用工具和停止条件<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成本周提交 |

### 本周提交

建议 Commit：`docs: establish evaluated ai coding workflow`

必须包含：版本化 Prompt、固定回归样例、代码库分析记录、一次测试驱动的小改动和 AI 输出审查清单。

最低验收：结论可追溯；代码修改有测试；Prompt 改进基于同一回归集而非主观感觉。

## 第 4 周：测试、排错、文档与架构表达

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 区分确定性代码与不确定模型并设计 Fake | 先列出可精确断言的 Schema、路由、工具和停止条件，再为模型边界定义 Fake 响应<br>相关资料：[Martin Fowler：Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) | 无密钥也能运行核心测试 |
| 周二 | 基于证据的系统排错 | 按输入、模型、检索、工具、流程、环境分类；一次只验证一个假设<br>相关资料：[Google SRE：Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) | 完成一份排错时间线 |
| 周三 | 错误契约与失败状态 | 区分可重试、不可重试、业务拒绝、人工介入；错误响应不泄露内部信息<br>相关资料：[RFC 9457：Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) | 错误类型和映射测试 |
| 周四 | Trace、架构图和时序图 | 用 traceId 串起请求、模型和工具事件；图中只画已实现边界，并标出信任、数据和控制流<br>相关资料：[OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/) | Trace 能对应到图和代码路径 |
| 周五 | README 与可复现运行 | 从干净环境按文档执行；记录所有隐式前置条件，不写“自行配置”<br>相关资料：[Make a README](https://www.makeareadme.com/) | 新环境可运行核心示例 |
| 周六 | 综合小练习 | 将原生模型调用、Tool Loop、测试、Trace 和错误处理组合；保留失败场景<br>相关资料：[Google SRE：Testing for Reliability](https://sre.google/sre-book/testing-reliability/) | 最小 AI 服务闭环可运行 |
| 周日 | 阶段复盘和框架学习准备 | 列出哪些能力应交给框架、哪些安全和业务规则必须保留在代码中<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成阶段提交 |

### 阶段提交

建议 Commit：`test: complete native ai engineering baseline`

必须包含：原生 AI 服务、Fake Model 测试、错误契约、架构/时序图、排错记录和可复现 README。

最低验收：能解释一次请求的完整生命周期；模型不可用时失败明确；核心逻辑无需真实 API Key 即可测试。

## 阶段出口条件

- 能解释 LLM 推理、Token、Embedding、采样和上下文的工程影响。
- 能手写流式模型调用、结构化输出和受控 Tool Loop。
- 能使用固定数据和指标比较 Prompt 或模型变化。
- 能在 AI 辅助编码中坚持测试、Diff 审查、证据和安全边界。
- 能说明后续 Spring AI、LangChain、LangGraph 和 Claude Agent SDK 分别会替代或增强哪些原生能力。

官方资料：[Hugging Face Tokenizer Summary](https://huggingface.co/docs/transformers/main/tokenizer_summary)、[Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)、[LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)。

下一阶段：[Java LLM、RAG 与 Agent](02-java-llm-rag-agent.md)
