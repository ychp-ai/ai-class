# 逐节课程教程

## 目录定位

本目录为 32 周学习计划提供逐节教程，共 32 份周教程、224 节每日课程。每节都回答四个问题：为什么学、这个是什么、怎么学、怎么验证学会了，并提供一份卡住后再看的参考答案。

参考答案严格对应“怎么学”的五个步骤：先给预测示例，再定位资料链接中的章节/条目，然后提供对应 Mermaid 图、样例代码或文档模板，最后给出失败注入、交付物和 Teach-back 示例。

本目录只负责教学展开，不保存学习进度、运行日志、源码或周验收结论。阶段计划仍以课程仓库的 `learning-plan/stages/` 为准；当周证据与状态以个人学习仓库的 `deliverables/week-XX/README.md` 为唯一入口，学习过程记录在个人仓库的 `notes/week-XX.md`。

## 推荐使用顺序

1. 先看对应[阶段计划](../stages/README.md)，确认本周目标、前置能力和阶段出口。
2. 按[开发语言路线](../01-language-roadmap.md)确认当周默认语言和是否需要桥接，再打开当周教程；每天只做一节，并按 60 分钟节奏留下真实证据，至少独立尝试 20 分钟后再看参考答案。
3. 参考答案只用于解除阻塞。看完后关闭答案，改变一个输入或约束独立重做，并把命令、输入输出、失败解释和 Teach-back 摘要写入周笔记。
4. 周日在个人学习仓库的当周成果 README 中链接证据，完成变体任务，再接受讲师验收。
5. 若教程与阶段四列表格不一致，以阶段表格为准，并运行 `python3 scripts/generate_course_tutorials.py --check` 检查是否需要重新生成。

## 每节课的通过含义

- “做完”：按步骤产出了当天验收物。
- “学会”：还能脱离步骤解释原理、诊断失败并完成变体。
- “通过”：讲师依据证据给出通过结论；只阅读、只复制、只跑通 happy path 都不算通过。

## 32 周教程索引

| 周次 | 教程 | 默认语言 | 对应阶段计划 |
| ---: | --- | --- | --- |
| 01 | [LLM 工程基础](week-01.md) | Python 3.11+ | [阶段计划](../stages/01-ai-tools-and-engineering.md) |
| 02 | [原生模型 API](week-02.md) | Python 3.11+ | [阶段计划](../stages/01-ai-tools-and-engineering.md) |
| 03 | [Prompt 与 AI 编程协作](week-03.md) | Python 3.11+ | [阶段计划](../stages/01-ai-tools-and-engineering.md) |
| 04 | [测试、排错与架构表达](week-04.md) | Python 3.11+ | [阶段计划](../stages/01-ai-tools-and-engineering.md) |
| 05 | [Spring AI Chat](week-05.md) | Java 21 | [阶段计划](../stages/02-java-llm-rag-agent.md) |
| 06 | [Spring AI RAG](week-06.md) | Java 21 | [阶段计划](../stages/02-java-llm-rag-agent.md) |
| 07 | [Spring AI Tool Calling](week-07.md) | Java 21 | [阶段计划](../stages/02-java-llm-rag-agent.md) |
| 08 | [手写 Java Agent](week-08.md) | Java 21 | [阶段计划](../stages/02-java-llm-rag-agent.md) |
| 09 | [LangChain Agent](week-09.md) | Python 3.11+ | [阶段计划](../stages/03-langchain-langgraph.md) |
| 10 | [LangChain RAG](week-10.md) | Python 3.11+ | [阶段计划](../stages/03-langchain-langgraph.md) |
| 11 | [LangGraph 工作流](week-11.md) | Python 3.11+ | [阶段计划](../stages/03-langchain-langgraph.md) |
| 12 | [Claude Agent SDK](week-12.md) | Python 3.11+ | [阶段计划](../stages/04-claude-agent-sdk.md) |
| 13 | [Claude 安全能力](week-13.md) | Python 3.11+ | [阶段计划](../stages/04-claude-agent-sdk.md) |
| 14 | [Java/Python 组合](week-14.md) | Java + Python | [阶段计划](../stages/05-integration-evaluation-delivery.md) |
| 15 | [Eval 与 Trace](week-15.md) | Java + Python | [阶段计划](../stages/05-integration-evaluation-delivery.md) |
| 16 | [首个 AI 应用交付](week-16.md) | Java + Python | [阶段计划](../stages/05-integration-evaluation-delivery.md) |
| 17 | [平台架构](week-17.md) | Java 主导 + Python 执行 | [阶段计划](../stages/06-ai-platform-core.md) |
| 18 | [Agent Registry](week-18.md) | Java 主导 + Python 执行 | [阶段计划](../stages/06-ai-platform-core.md) |
| 19 | [Model Gateway](week-19.md) | Java 主导 + Python 执行 | [阶段计划](../stages/06-ai-platform-core.md) |
| 20 | [Tool、MCP 与知识库](week-20.md) | Java 主导 + Python 执行 | [阶段计划](../stages/06-ai-platform-core.md) |
| 21 | [Workflow Definition](week-21.md) | Java 主导 + Python 执行 | [阶段计划](../stages/07-workflow-governance.md) |
| 22 | [Durable Runtime](week-22.md) | Java 主导 + Python 执行 | [阶段计划](../stages/07-workflow-governance.md) |
| 23 | [Governance 与 Security](week-23.md) | Java 主导 + Python 执行 | [阶段计划](../stages/07-workflow-governance.md) |
| 24 | [Eval 与 Operations](week-24.md) | Java 主导 + Python 执行 | [阶段计划](../stages/07-workflow-governance.md) |
| 25 | [场景发现](week-25.md) | 语言中立 | [阶段计划](../stages/08-business-scenario-process.md) |
| 26 | [AS-IS 分析](week-26.md) | 语言中立 | [阶段计划](../stages/08-business-scenario-process.md) |
| 27 | [TO-BE 与人机边界](week-27.md) | 语言中立 | [阶段计划](../stages/08-business-scenario-process.md) |
| 28 | [接入与试点设计](week-28.md) | 语言中立 | [阶段计划](../stages/08-business-scenario-process.md) |
| 29 | [业务系统集成](week-29.md) | Java + Python，按需 TypeScript | [阶段计划](../stages/09-pilot-production-capstone.md) |
| 30 | [UAT 与试点](week-30.md) | Java + Python，按需 TypeScript | [阶段计划](../stages/09-pilot-production-capstone.md) |
| 31 | [生产硬化](week-31.md) | Java + Python，按需 TypeScript | [阶段计划](../stages/09-pilot-production-capstone.md) |
| 32 | [最终发布与复盘](week-32.md) | Java + Python，按需 TypeScript | [阶段计划](../stages/09-pilot-production-capstone.md) |

## 输入、输出与边界

- 输入：九份阶段计划中的四列表格、课程资料链接和验收要求。
- 输出：按周组织的逐节学习教程。
- 禁止内容：真实密钥、生产数据、唯一成果副本、自动推进的学习状态和未经验证的业务收益。
- 维护方式：修改阶段日程后运行生成脚本；不要直接改生成的 `week-XX.md`，需要改变教程规则时修改生成器。
