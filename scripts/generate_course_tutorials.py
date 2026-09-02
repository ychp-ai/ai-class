#!/usr/bin/env python3
"""Generate one tutorial for every daily lesson in the 32-week plan.

Stage documents remain the source of truth for schedule, task, advice and
acceptance. This generator adds a teaching layer without duplicating progress
state or allowing tutorials to drift from the required four-column tables.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STAGES_DIR = REPO_ROOT / "learning-plan" / "stages"
OUTPUT_DIR = REPO_ROOT / "learning-plan" / "tutorials"


@dataclass(frozen=True)
class WeekGuide:
    title: str
    stage_file: str
    why: str
    what: str


@dataclass(frozen=True)
class Lesson:
    day: str
    task: str
    advice: str
    acceptance: str


WEEK_GUIDES: dict[int, WeekGuide] = {
    1: WeekGuide("LLM 工程基础", "01-ai-tools-and-engineering.md", "建立不把模型当数据库、搜索引擎或确定性函数的工程直觉，后续才能正确解释质量、成本和失败。", "LLM 工程基础是把训练、推理、Token、Embedding、采样和幻觉变成可观察实验的心智模型，不要求推导数学公式。"),
    2: WeekGuide("原生模型 API", "01-ai-tools-and-engineering.md", "先看清 HTTP、流式事件、结构化输出和 Tool Loop 的原生协议，之后使用框架时才知道它隐藏了什么。", "原生模型 API 是直接围绕请求、响应、事件和工具调用协议构建最小闭环；Tool Loop 是应用执行工具、回填结果并控制停止的普通代码循环。"),
    3: WeekGuide("Prompt 与 AI 编程协作", "01-ai-tools-and-engineering.md", "把 Prompt 和 AI 生成代码纳入版本、测试与审查，避免一次对话看似成功却无法复现和回归。", "Prompt 是可版本化、可评测的模型输入契约；AI 编程协作是以 Diff、测试和人工审查约束生成式助手，而不是把代码责任交给模型。"),
    4: WeekGuide("测试、排错与架构表达", "01-ai-tools-and-engineering.md", "建立无真实模型也能测试、出错时能分类定位、换人后能复现的工程基线。", "AI 工程测试用 Fake、固定样例和稳定错误契约隔离随机性；架构表达用与实现一致的图、接口和运行说明呈现边界。"),
    5: WeekGuide("Spring AI Chat", "02-java-llm-rag-agent.md", "把原生模型能力接入熟悉的 Java 服务，同时保留流式、配置、错误和观测边界。", "Spring AI Chat 是 Spring 生态中的模型与消息抽象；它减少 Provider 接入样板，但不替代业务权限、失败处理或质量验证。"),
    6: WeekGuide("Spring AI RAG", "02-java-llm-rag-agent.md", "让回答基于可追溯资料，并用检索和拒答证据区分知识问题与生成问题。", "RAG 是先检索外部资料再把受控上下文交给模型生成答案的模式；它不等于训练模型，也不能自动保证事实正确。"),
    7: WeekGuide("Spring AI Tool Calling", "02-java-llm-rag-agent.md", "让模型提出工具请求、让应用掌握校验和执行权，从而安全连接确定性业务能力。", "Tool Calling 是模型按 Schema 生成调用意图，由应用校验权限、执行普通函数并回填结果；模型本身不拥有执行权限。"),
    8: WeekGuide("手写 Java Agent", "02-java-llm-rag-agent.md", "亲手实现规划—工具—观察循环，理解 Agent 的状态、停止条件和副作用边界。", "Agent 是围绕目标反复选择动作、观察结果并决定下一步的受控运行循环；它不是拥有无限权限的自主程序。"),
    9: WeekGuide("LangChain Agent", "03-langchain-langgraph.md", "学习模型、消息、结构化输出和工具抽象，并能与手写 Agent 比较新增状态与失败模式。", "LangChain 提供模型、消息、Retriever、Tool 和 Agent 组合抽象；它提升组合效率，但不会替你完成权限和业务规则。"),
    10: WeekGuide("LangChain RAG", "03-langchain-langgraph.md", "在相同数据和模型条件下建立第二套 RAG 实现，形成基于证据而非宣传的框架选择能力。", "LangChain RAG 把加载、切分、索引、Retriever、工具和结构化引用组合成检索增强 Agent；质量仍取决于数据与评测。"),
    11: WeekGuide("LangGraph 工作流", "03-langchain-langgraph.md", "把开放式 Agent 放入显式状态机，实现可路由、可暂停、可恢复和可审计的长流程。", "LangGraph 用 State、Node、Edge 和 Checkpoint 表达有状态工作流；确定性控制留在图和普通代码，模糊判断才交给模型。"),
    12: WeekGuide("Claude Agent SDK", "04-claude-agent-sdk.md", "掌握隔离环境中的文件、代码和 Shell 执行闭环，同时看清会话和工具事件。", "Claude Agent SDK 提供带 Agent 循环和内置工具的执行型运行时；它不同于普通模型 Client SDK，也不是宿主机全权限执行器。"),
    13: WeekGuide("Claude 安全能力", "04-claude-agent-sdk.md", "把最小权限、动态审批、Hooks、MCP 和沙箱落实到真实阻断测试，而不只写安全说明。", "执行型 Agent 安全由权限集合、审批点、前后置 Hook、凭证与网络隔离共同组成；Prompt 不能充当安全边界。"),
    14: WeekGuide("Java/Python 组合", "05-integration-evaluation-delivery.md", "把控制面与执行面通过稳定协议组合起来，验证超时、取消和部分失败不会形成假成功。", "组合架构用 Java 承担平台 API 与治理，用 Python 承担 Agent 工作流和开放式执行，两端通过版本化 Schema 协作。"),
    15: WeekGuide("Eval 与 Trace", "05-integration-evaluation-delivery.md", "用固定数据、统一指标和跨服务证据判断改动是否真的更好。", "Eval 是对固定样例按明确口径重复评分；Trace 是把一次运行的服务、模型、工具和状态变化关联起来的可观测记录。"),
    16: WeekGuide("首个 AI 应用交付", "05-integration-evaluation-delivery.md", "把分散实验收敛为可安装、可测试、可演示并公开限制的完整应用。", "应用交付包包含代码、配置、启动、测试、架构、安全、演示和已知限制；接口存在不等于交付完成。"),
    17: WeekGuide("平台架构", "06-ai-platform-core.md", "从单应用转向多角色、多资源和多版本平台前，先稳定用例、领域边界和 MVP 范围。", "AI 平台架构把控制面和执行面分开，以 Project、资源 ID、版本和运行记录承载治理；第一版采用 API 优先的模块化单体。"),
    18: WeekGuide("Agent Registry", "06-ai-platform-core.md", "让 Agent 配置可校验、可发布、可追溯和可回滚，避免线上配置被原地覆盖。", "Agent Registry 管理 Definition、Draft、不可变 Version 和 Release 指针，并解析模型、Prompt、Tool 与知识库依赖。"),
    19: WeekGuide("Model Gateway", "06-ai-platform-core.md", "集中处理 Provider 差异、路由、配额、降级和成本，避免策略散落在业务代码。", "Model Gateway 用统一请求响应和模型别名隔离供应商，并在明确兼容条件下执行超时、重试、缓存、路由与 Fallback。"),
    20: WeekGuide("Tool、MCP 与知识库", "06-ai-platform-core.md", "把外部能力和资料变成带 Owner、版本、权限、预算和质量证据的平台资源。", "Tool Registry 管函数能力，MCP 标准化外部上下文和工具协议，Knowledge Base 控制数据源、索引版本、ACL 与检索配置。"),
    21: WeekGuide("Workflow Definition", "07-workflow-governance.md", "让流程在运行前即可静态校验、版本化和编译，减少线上才发现死路或无界循环。", "Workflow Definition 是独立于运行实例的不可变流程描述，包含节点、边、条件、循环上限、输入输出和依赖版本。"),
    22: WeekGuide("Durable Runtime", "07-workflow-governance.md", "让长任务在进程退出、重复请求、取消和依赖故障下仍保持真实一致的状态。", "Durable Runtime 用 Run/Step 状态机、Checkpoint、幂等键和持久事件支持异步执行、恢复、取消与受控重试。"),
    23: WeekGuide("Governance 与 Security", "07-workflow-governance.md", "把谁能做什么、何时审批、发生过什么和攻击如何阻断落实到执行路径。", "平台治理由 RBAC、策略、职责分离、审批、审计和攻击测试构成；前端隐藏按钮和 Prompt 约束都不是授权。"),
    24: WeekGuide("Eval 与 Operations", "07-workflow-governance.md", "把质量、安全、成本、延迟和恢复能力变成发布门禁与日常运行标准。", "平台运维用 Eval Dataset、SLO、Trace、告警、压测、备份恢复和 Runbook 管理发布后的可用性与风险。"),
    25: WeekGuide("场景发现", "08-business-scenario-process.md", "从业务目标和证据选择值得做的场景，避免先有模型再寻找伪需求。", "场景发现通过候选评分、访谈、系统数据盘点和 Baseline 明确 Owner、用户、问题、价值、风险与停止条件。"),
    26: WeekGuide("AS-IS 分析", "08-business-scenario-process.md", "先看清现状的等待、交接、异常、规则和约束，才能优化根因而非自动化低效流程。", "AS-IS 是经流程参与者核对的现状模型，覆盖主流程、异常流程、步骤数据、决策规则和组织合规约束。"),
    27: WeekGuide("TO-BE 与人机边界", "08-business-scenario-process.md", "依据任务适用性和风险重设计流程，明确 AI、代码和人工各自承担什么。", "TO-BE 是目标人机协作流程，包含正常路径、降级路径、责任主体、指标阈值和 ROI/TCO 假设。"),
    28: WeekGuide("接入与试点设计", "08-business-scenario-process.md", "在编码前把业务契约、数据权限、平台配置、测试和回退方案评审清楚。", "接入设计把 TO-BE 映射为 API/事件、字段、身份、Agent/Workflow 版本和试点计划，不向业务泄露内部模型细节。"),
    29: WeekGuide("业务系统集成", "09-pilot-production-capstone.md", "用契约、身份、幂等和端到端测试证明业务系统与平台能够安全协作。", "系统集成通过 Connector/Adapter 隔离业务 DTO 与平台协议，并把身份、Trace、版本和副作用结果贯穿全链路。"),
    30: WeekGuide("UAT 与试点", "09-pilot-production-capstone.md", "让真实用户和受控流量验证流程价值、可用性与失败恢复，而不只验证模型答案。", "UAT 验证用户任务能否完成；试点在限定人群、流量、版本和停止条件下比较 Baseline、收益、风险与成本。"),
    31: WeekGuide("生产硬化", "09-pilot-production-capstone.md", "在发布前通过压测、攻击、恢复和运行交接证明关键故障可发现、可止损、可恢复。", "生产硬化覆盖环境与 Secret、容量、限流、安全回归、备份恢复、告警、Runbook 和发布门禁。"),
    32: WeekGuide("最终发布与复盘", "09-pilot-production-capstone.md", "用统一证据回答平台是否可交付、业务是否值得推广以及能力边界在哪里。", "最终发布把可复现平台包、业务案例、指标、成本、风险、决策和答辩串成完整证据链，允许得出调整或停止结论。"),
}


def language_label(week: int) -> str:
    if 1 <= week <= 4:
        return "Python 3.11+"
    if 5 <= week <= 8:
        return "Java 21"
    if 9 <= week <= 13:
        return "Python 3.11+"
    if 14 <= week <= 16:
        return "Java + Python"
    if 17 <= week <= 24:
        return "Java 主导 + Python 执行"
    if 25 <= week <= 28:
        return "语言中立"
    return "Java + Python，按需 TypeScript"


def language_focus(week: int) -> str:
    if 1 <= week <= 4:
        return "默认使用 Python 3.11+，以较少样板观察 AI 原理和原生协议；记录虚拟环境、依赖版本、pytest 命令和失败结果。"
    if 5 <= week <= 8:
        return "必须使用 Java 21、Maven、Spring Boot/Spring AI，并把前四周的原生能力映射到 Java 实现、测试和错误处理。"
    if 9 <= week <= 13:
        return "必须使用 Python 3.11+、类型标注、Pydantic 和 pytest，重点观察 Agent 抽象、异步事件、状态与恢复。"
    if 14 <= week <= 16:
        return "同时使用 Java 控制/API 层与 Python Agent 执行层；两端通过版本化 Schema、稳定错误、traceId、超时和取消语义连接。"
    if 17 <= week <= 24:
        return "Java 承担平台控制面与治理，Python 承担已授权的 Agent/Workflow 执行；TypeScript 只在管理流程需要时提供最小界面。"
    if 25 <= week <= 28:
        return "本周以业务证据和设计为主，语言中立；技术 Spike 只复用既有 Java/Python/TypeScript 栈，不引入新语言。"
    return "组合 Java 控制面/业务 Connector、Python Agent 执行面和按需 TypeScript 控制台，所有端到端状态与回滚必须可验证。"


WEEK_HEADING_RE = re.compile(r"^## 第 (\d+) 周：(.+)$")
LESSON_ROW_RE = re.compile(r"^\| (周[一二三四五六日]) \| (.+?) \| (.+?) \| (.+?) \|$")


def normalize_inline(text: str) -> str:
    return text.replace("<br>", "\n\n")


def parse_lessons() -> dict[int, list[Lesson]]:
    result: dict[int, list[Lesson]] = {}
    for stage_path in sorted(STAGES_DIR.glob("[0-9][0-9]-*.md")):
        current_week: int | None = None
        for line in stage_path.read_text(encoding="utf-8").splitlines():
            heading = WEEK_HEADING_RE.match(line)
            if heading:
                current_week = int(heading.group(1))
                result[current_week] = []
                continue
            row = LESSON_ROW_RE.match(line)
            if row and current_week is not None:
                result[current_week].append(Lesson(row.group(1), row.group(2), normalize_inline(row.group(3)), row.group(4)))
    return result


def reference_artifact_shape(lesson: Lesson) -> str:
    """Return a concrete answer skeleton suited to the lesson's deliverable."""
    topic = f"{lesson.task} {lesson.acceptance}"
    if any(keyword in topic for keyword in ("配置", "环境变量", "Secret", "API Key", "Starter", "BOM", "依赖")):
        return "运行时与依赖版本；配置键；Secret 引用方式；示例占位值；启动命令；缺失配置的错误；泄露检查"
    if any(keyword in topic for keyword in ("指标", "Baseline", "基线", "ROI", "TCO", "成本", "容量", "基准")):
        return "指标名称；计算公式；数据来源；样本与时间窗；当前值；目标/阈值；限制与未验证项"
    if any(keyword in topic for keyword in ("API", "Schema", "协议", "契约", "DTO", "事件", "错误码")):
        return "版本；请求字段；成功响应；稳定错误码；状态变化；traceId；幂等/并发约束；兼容性说明"
    if any(keyword in topic for keyword in ("图", "流程", "时序", "架构", "关系")):
        return "范围与参与者；输入；主路径；异常/拒绝路径；输出；信任或责任边界；版本与图例"
    if any(keyword in topic for keyword in ("测试", "验证", "检查", "攻击", "故障", "演练", "回归")):
        return "用例 ID；前置条件；输入/故障；预期状态；关键断言；实际结果；日志或 Trace；是否通过"
    if any(keyword in topic for keyword in ("表", "矩阵", "清单", "盘点", "分类", "排序", "映射")):
        return "对象；Owner/角色；输入或来源；规则/约束；风险；证据；状态；下一步"
    if any(keyword in topic for keyword in ("评审", "复盘", "报告", "README", "答辩", "说明", "文档", "ADR", "计划", "Brief", "提纲", "纪要")):
        return "目标；事实与证据；关键决定；备选方案；失败与风险；限制；后续动作；负责人/时间"
    if any(keyword in topic for keyword in ("实现", "调用", "运行", "Agent", "Tool", "工具", "检索", "流式", "脚本", "API", "CLI")):
        return "入口；输入类型；输出类型；依赖版本；校验与权限；超时/错误；日志字段；最小测试命令"
    return "一句话定义；输入；操作；可观察输出；失败/反例；工程意义；证据位置"


def reference_failure_example(lesson: Lesson) -> str:
    topic = f"{lesson.task} {lesson.advice} {lesson.acceptance}"
    if any(keyword in topic for keyword in ("权限", "授权", "RBAC", "审批", "Secret", "安全", "攻击", "凭证", "API Key", "环境变量")):
        return "删除身份、Scope 或审批后再次执行，正确结果应是执行路径明确拒绝且留下脱敏审计；如果仍成功，就是权限边界失效。"
    if any(keyword in topic for keyword in ("访谈", "业务", "场景", "AS-IS", "TO-BE", "试点", "收益", "指标", "Baseline")):
        return "当样本、Owner 或数据来源不足时，把结论标为假设并给出验证计划；不能把模拟结果写成真实业务收益。"
    if any(keyword in topic for keyword in ("模型", "LLM", "Prompt", "RAG", "Embedding", "Agent", "Tool", "LangChain", "LangGraph", "Claude")):
        return "加入无答案、非法 Schema、超时或工具失败输入，正确结果应是拒答或稳定失败状态；如果输出看似正常但证据缺失，应判为失败。"
    return "删掉一个必填输入或让依赖失败，系统应返回可解释的失败结果且不产生假成功；再根据日志、Diff 或流程证据定位原因。"


def resource_details(resource: str) -> tuple[str, str]:
    match = re.search(r"\[([^]]+)\]\(([^)]+)\)", resource)
    return (match.group(1), match.group(2)) if match else ("课程资料", resource)


def chapter_hint(lesson: Lesson, resource_name: str) -> str:
    topic = lesson.task
    rules = (
        (("AI、机器学习", "训练和推理"), "术语条目 → artificial intelligence、machine learning、deep learning、generative AI、large language model、training、inference"),
        (("Token", "Tokenizer"), "Tokenizer summary → Tokenization pipeline、Encoding / Decoding"),
        (("Embedding", "语义相似度"), "Semantic Textual Similarity → Usage / Similarity calculation"),
        (("Temperature", "Top-p"), "Generation strategies → Multinomial sampling / Decoding strategies"),
        (("结构化输出", "Schema"), "Structured Outputs → JSON Schema、Handling mistakes / Validation"),
        (("Tool Calling", "工具选择", "@Tool"), "Function/Tool Calling → Defining tools、Tool execution、Returning tool results"),
        (("Prompt", "Few-shot"), "Prompt engineering → Message roles、Few-shot learning、Provide reference text"),
        (("Trace", "日志", "观测"), "Trace/Log semantic conventions → Span、Attributes、Context propagation"),
        (("ChatClient", "Chat API", "流式响应"), "Chat Client API → Creating ChatClient、call()、stream()"),
        (("初始化 Java",), "Spring Boot Reference → Developing Your First Spring Boot Application；Actuator → Health endpoint"),
        (("Spring AI 模型 Starter",), "Getting Started → Dependency Management、Add repositories and BOM、Model provider starter、API key properties"),
        (("RAG", "解析、切片", "检索和生成"), "Retrieval Augmented Generation → Advisors / ETL Pipeline / Retrieval flow"),
        (("Qdrant", "Embedding"), "Collections / Points → Vectors、Payload、Upsert points、Search"),
        (("路径", "目录白名单"), "Path Traversal → Description、Examples、Mitigation"),
        (("Plan–Act–Observe",), "ReAct paper → Abstract、Method、Figure 1、Experiments"),
        (("async", "异步"), "asyncio → Coroutines and Tasks、Streams、Running an asyncio program"),
        (("Pydantic",), "Models → Basic model usage、Data conversion、Error handling"),
        (("create_agent",), "Agents → Core components、Tools、Invocation、Structured output"),
        (("Retriever", "加载和切分"), "Retrieval → Building a knowledge base、Retrieval pipeline、Retriever as a tool"),
        (("State、Node、Edge", "条件边", "循环"), "Graph API → State、Nodes、Edges、Conditional edges、Reducers"),
        (("Checkpoint", "会话状态", "恢复"), "Persistence → Threads、Checkpoints、Get state history、Replay"),
        (("Human-in-the-loop", "审批", "暂停"), "Interrupts → Pause using interrupt、Resuming interrupts、Approve or reject"),
        (("Agent SDK", "query()", "流式消息"), "Agent SDK → Overview / Streaming output → Message types、Final result"),
        (("Read、Glob、Grep", "Edit", "Bash"), "Tools reference → Read、Glob、Grep、Edit、Bash"),
        (("allowed_tools", "canUseTool", "权限模式"), "Permissions → Permission modes、allowedTools / disallowedTools、canUseTool"),
        (("PreToolUse", "PostToolUse"), "Hooks → Hook events、PreToolUse、PostToolUse、Hook input/output"),
        (("MCP",), "MCP → Architecture / Tools / Authorization / Security best practices"),
        (("OpenAPI", "API 协议", "领域契约"), "OpenAPI Specification → Paths、Operation Object、Schema Object、Responses"),
        (("幂等",), "RFC 9110 → 9.2.2 Idempotent Methods"),
        (("限流", "RateLimit"), "RFC 9333 → RateLimit-Limit、RateLimit-Remaining、RateLimit-Reset"),
        (("BPMN", "AS-IS", "TO-BE", "流程"), "BPMN 2.0 → Flow Objects、Connecting Objects、Pools and Lanes、Events"),
        (("根因", "Five Whys"), "Five Whys → What is Five Whys、When to use、How to use"),
        (("SLO",), "Service Level Objectives → SLI、SLO、Error budgets"),
        (("备份", "恢复"), "Backup and Restore → SQL dump、File-system backup、Continuous archiving"),
        (("UAT", "可用性"), "Moderated usability testing → Prepare、Run sessions、Analyse findings"),
    )
    for keywords, chapter in rules:
        if any(keyword in topic for keyword in keywords):
            return chapter
    return f"该链接指向的“{resource_name}”整篇专题/章节；重点阅读与“{topic}”直接对应的段落，页面更新时使用课程标题中的英文术语或 API 名页内搜索"


def diagram_sample(lesson: Lesson) -> str:
    topic = lesson.task
    if "AI、机器学习" in topic:
        body = "AI[人工智能 AI] --> ML[机器学习 ML]\n    ML --> DL[深度学习 DL]\n    DL --> GenAI[生成式 AI]\n    GenAI --> LLM[大语言模型 LLM]\n    Data[训练数据] --> Train[训练]\n    Train --> Artifact[模型参数/产物]\n    Artifact --> Infer[推理]\n    Request[输入请求] --> Infer\n    Infer --> Output[生成输出]"
    elif "State、Node、Edge" in topic:
        body = "Start([START]) --> Validate[validate_node]\n    Validate --> Work[work_node]\n    Work --> Summarize[summarize_node]\n    Summarize --> End([END])\n    State[(State)] -.读取/更新.-> Validate\n    State -.读取/更新.-> Work\n    State -.读取/更新.-> Summarize"
    elif any(keyword in topic for keyword in ("RAG", "解析、切片", "检索和生成")):
        body = "Document[文档] --> Parse[解析与切片]\n    Parse --> Index[Embedding 与索引]\n    Question[问题] --> Retrieve[TopK 检索]\n    Index --> Retrieve\n    Retrieve --> Generate[带引用生成]\n    Generate --> Answer[回答或拒答]"
    elif any(keyword in topic for keyword in ("Agent", "Plan–Act–Observe", "工具选择")):
        body = "Goal[目标] --> Plan[Plan]\n    Plan --> Act[Act / Tool Call]\n    Act --> Observe[Observe]\n    Observe --> Decide{是否完成}\n    Decide -->|否| Plan\n    Decide -->|是| Result[结果]"
    elif any(keyword in topic for keyword in ("控制面", "执行面", "平台架构")):
        body = "User[用户/业务系统] --> Control[Java Control Plane]\n    Control --> Snapshot[不可变发布快照]\n    Snapshot --> Runtime[Python Execution Plane]\n    Runtime --> Model[Model / Tool / KB]\n    Runtime --> Trace[Run / Trace / Audit]"
    elif any(keyword in topic for keyword in ("AS-IS", "TO-BE", "流程")):
        body = "Request[业务请求] --> Human[人工受理]\n    Human --> Check{资料完整?}\n    Check -->|否| Return[退回补充]\n    Check -->|是| Process[处理/AI 辅助]\n    Process --> Approve{人工审批}\n    Approve -->|拒绝| Fallback[人工兜底]\n    Approve -->|批准| Done[完成并审计]"
    elif "Token" in topic:
        body = "Text[输入文本] --> Tokenizer[Tokenizer]\n    Tokenizer --> Tokens[Token IDs]\n    Tokens --> Context[上下文窗口]\n    Context --> Predict[预测下一个 Token]\n    Predict --> Tokens"
    else:
        body = f'Input[输入] --> Task["{topic}"]\n    Task --> Output["{lesson.acceptance}"]\n    Task -->|边界/失败| Failure[稳定失败或人工处理]'
    return f"```mermaid\ngraph LR\n    {body}\n```"


def code_sample(lesson: Lesson, guide: WeekGuide) -> str:
    topic = lesson.task
    title = guide.title
    if "Spring AI" in title or "Java Agent" in title:
        if "初始化 Java" in topic:
            return """```java
@SpringBootApplication
public class AiPlatformApplication {
    public static void main(String[] args) {
        SpringApplication.run(AiPlatformApplication.class, args);
    }
}

@RestController
final class HealthController {
    @GetMapping("/health")
    Map<String, String> health() { return Map.of("status", "UP"); }
}
```"""
        if "模型 Starter" in topic:
            return """```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.ai</groupId>
      <artifactId>spring-ai-bom</artifactId>
      <version>${spring-ai.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
```

```dotenv
# .env.example：只写变量名，不写真实值
OPENAI_API_KEY=
```"""
        if "@Tool" in topic or "工具" in topic or "Tool" in topic:
            return """```java
record FileRequest(String path) {}

final class SafeFileTools {
    private final Path root = Path.of("sandbox-workspaces/demo").toAbsolutePath();

    @Tool(description = "Read a UTF-8 file inside the demo workspace")
    String readFile(FileRequest request) throws IOException {
        Path target = root.resolve(request.path()).normalize();
        if (!target.startsWith(root)) throw new IllegalArgumentException("PATH_OUTSIDE_ROOT");
        return Files.readString(target);
    }
}
```"""
        if "Agent" in topic or "Plan" in topic:
            return """```java
for (int step = 0; step < MAX_STEPS; step++) {
    Decision decision = planner.next(state);
    if (decision.done()) return RunResult.succeeded(state);
    ToolResult observed = toolExecutor.executeValidated(decision.toolCall());
    state = state.append(decision, observed);
}
return RunResult.failed("MAX_STEPS_EXCEEDED");
```"""
        return """```java
@RestController
final class ChatController {
    private final ChatClient chatClient;

    ChatController(ChatClient.Builder builder) { this.chatClient = builder.build(); }

    @PostMapping("/api/chat")
    ChatResponse chat(@Valid @RequestBody ChatRequest request) {
        String content = chatClient.prompt().user(request.message()).call().content();
        return new ChatResponse(content == null ? "" : content);
    }
}
record ChatRequest(@NotBlank String message) {}
record ChatResponse(String content) {}
```"""
    if "LangGraph" in title or any(keyword in topic for keyword in ("State、Node、Edge", "Checkpoint", "Human-in-the-loop")):
        return """```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    task: str
    attempts: int

def validate(state: State) -> dict:
    if not state["task"].strip():
        raise ValueError("EMPTY_TASK")
    return {"attempts": state["attempts"] + 1}

graph = StateGraph(State)
graph.add_node("validate", validate)
graph.add_edge(START, "validate")
graph.add_edge("validate", END)
app = graph.compile()
print(app.invoke({"task": "demo", "attempts": 0}))
```"""
    if "LangChain" in title:
        return """```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def lookup(query: str) -> str:
    '''Search the fixed lesson dataset; query must be non-empty.'''
    if not query.strip():
        raise ValueError("EMPTY_QUERY")
    return "source=lesson-doc; answer=example"

agent = create_agent(model="provider:model", tools=[lookup])
result = agent.invoke({"messages": [{"role": "user", "content": "查找示例"}]})
print(result)
```"""
    if "Claude" in title:
        return """```python
import asyncio
from claude_agent_sdk import ClaudeAgentOptions, query

async def main() -> None:
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],
        cwd="sandbox-workspaces/demo",
    )
    async for message in query(prompt="分析项目并给出文件证据", options=options):
        print(type(message).__name__, message)

asyncio.run(main())
```"""
    if title in {
        "平台架构", "Agent Registry", "Model Gateway", "Tool、MCP 与知识库",
        "Workflow Definition", "Durable Runtime", "Governance 与 Security",
        "Eval 与 Operations", "业务系统集成", "生产硬化",
    } and not any(keyword in topic for keyword in ("Schema", "DSL", "协议", "契约", "Definition", "状态机")):
        return f"""```java
record LessonCommand(String projectId, String requestId, String payload) {{}}
record LessonResult(String status, String evidence) {{}}

@Service
final class LessonService {{
    LessonResult execute(LessonCommand command) {{
        if (command.projectId() == null || command.projectId().isBlank()) {{
            throw new IllegalArgumentException("PROJECT_REQUIRED");
        }}
        // TODO: 实现“{topic}”，并在执行路径校验权限、版本和幂等约束。
        return new LessonResult("SUCCEEDED", "{lesson.acceptance}");
    }}
}}
```"""
    if any(keyword in topic for keyword in ("Schema", "DSL", "协议", "契约", "Definition", "状态机")):
        return f"""```json
{{
  "schemaVersion": "v1",
  "task": "{topic}",
  "input": {{"requestId": "req-001"}},
  "expected": "{lesson.acceptance}",
  "onError": {{"code": "VALIDATION_FAILED", "retryable": false}}
}}
```"""
    return """```python
def run_case(input_data: dict) -> dict:
    if not input_data:
        return {"status": "FAILED", "error": "EMPTY_INPUT"}
    # Replace this line with the lesson-specific call.
    result = {"observed": input_data, "status": "SUCCEEDED"}
    return result

print(run_case({"case": "normal"}))
print(run_case({}))  # failure case
```"""


def step_three_sample(lesson: Lesson, guide: WeekGuide) -> tuple[str, str]:
    topic = f"{lesson.task} {lesson.acceptance}"
    if any(keyword in topic for keyword in ("图", "流程", "时序", "架构", "关系")):
        return "参考图（按实际角色、字段和状态修改）", diagram_sample(lesson)
    if any(keyword in topic for keyword in ("初始化", "Starter", "配置", "实现", "调用", "运行", "脚本", "API", "CLI", "Tool", "Agent", "检索", "流式", "异步", "Checkpoint", "Hook", "SDK", "State", "Schema", "DSL", "条件边", "路由", "分支")):
        return "样例代码（先核对课程链接中的当前 API，再按本仓库边界修改）", code_sample(lesson, guide)
    shape = reference_artifact_shape(lesson)
    return "参考资料/文档产出", f"- 主题：{lesson.task}\n- 建议字段：{shape}\n- 示例结论：已按统一口径产出“{lesson.acceptance}”；证据不足的部分标记为假设或未验证。"


def render_reference_answer(lesson: Lesson, guide: WeekGuide, action: str, resource: str) -> str:
    artifact_shape = reference_artifact_shape(lesson)
    failure_example = reference_failure_example(lesson)
    resource_name, resource_url = resource_details(resource)
    chapter = chapter_hint(lesson, resource_name)
    sample_label, sample = step_three_sample(lesson, guide)
    return f"""**参考答案（独立尝试至少 20 分钟后再看）**

> 这是一份合格答案骨架，不是唯一实现。看完后必须关闭参考答案，换一个输入或约束独立重做。

#### 步骤 1 参考：先写预测

- 一句话解释：{guide.what}
- 预测：完成“{lesson.task}”后，应能观察到“{lesson.acceptance}”；失败输入不应产生假成功。

#### 步骤 2 参考：阅读资料

- 链接：[{resource_name}]({resource_url})
- 指定章节/条目：{chapter}
- 阅读方法：只摘录一个定义、一个输入输出约束和一个失败边界；记录页面日期、协议版本或依赖版本。

#### 步骤 3 参考：按专项动作完成产出

- 专项动作：{action}
- {sample_label}：

{sample}

#### 步骤 4 参考：制造失败并解释

- 失败注入：{failure_example}
- 参考判断：失败必须映射为明确状态、错误、拒答、人工路径或未验证假设；日志和界面不得显示成功。

#### 步骤 5 参考：整理交付与 Teach-back

- 当天交付：{lesson.acceptance}。
- 完整字段：{artifact_shape}。
- Teach-back 参考：本节输入是什么、经过了什么处理、输出如何验证、哪种失败最危险、为什么当前方案没有越过课程边界。
- 完成后变体：更换一个输入、参数、角色、权限或失败条件，不看上述样例重新完成。
"""


def render_lesson(lesson: Lesson, guide: WeekGuide, number: int) -> str:
    action, separator, resource = lesson.advice.partition("\n\n相关资料：")
    resource_line = f"\n专项资料：{resource}" if separator else ""
    boundary = "只读完资料或只跑通正常路径，都不能证明已经掌握。"
    if "不要" in action:
        caution = action.split("不要", 1)[1].splitlines()[0].rstrip("。；")
        boundary = f"重点边界来自课程原计划：不要{caution}。"
    return f"""### {lesson.day} · 第 {number} 节：{lesson.task}

**为什么学**

本周要{guide.why}本节把“{lesson.task}”推进为可检查成果；如果跳过，后续会缺少“{lesson.acceptance}”这项关键证据。

**这个是什么**

本周核心概念是：{guide.what}今天的“{lesson.task}”是这个核心能力的最小学习单元：你会通过“{action}”观察输入如何转化为“{lesson.acceptance}”。它既包含可观察结果，也包含至少一个失败或不适用边界。{boundary}

**怎么学（约 60 分钟）**

1. `0–5 分钟`：不查资料，写下你对本节主题的一句话解释、预期输入输出和一个疑问。
2. `5–15 分钟`：只阅读下方资料中与当前任务直接相关的部分，记录一个关键约束和版本信息。
3. `15–45 分钟`：执行专项任务：{action}
4. `45–55 分钟`：主动制造一个错误输入、边界条件、依赖失败或反例，保存现象并解释原因。
5. `55–60 分钟`：整理命令、输入、输出、Diff、图表或访谈证据，并用自己的语言完成 Teach-back。
{resource_line}

**怎么验证学会了**

- 必交证据：{lesson.acceptance}。
- Teach-back：不看资料解释“{lesson.task}”解决什么问题、主要输入输出、一个边界，以及它不是什么。
- 失败证据：展示一个非正常场景，指出失败发生在哪一层，不能只贴错误截图。
- 变体任务：改变一个输入、参数、角色、权限或失败条件，在不照抄原步骤的情况下重新完成。
- 通过标准：以上四项均有证据，且能解释关键取舍；只能照步骤运行时最高算 L1，不能判定本节通过。

{render_reference_answer(lesson, guide, action, resource)}
"""


def render_week(week: int, lessons: list[Lesson]) -> str:
    guide = WEEK_GUIDES[week]
    sections = "\n".join(render_lesson(lesson, guide, index) for index, lesson in enumerate(lessons, start=1))
    return f"""<!-- 本文件由 scripts/generate_course_tutorials.py 生成，请修改阶段计划或生成器后重新生成。 -->

# 第 {week:02d} 周教程：{guide.title}

> 计划来源：[{guide.stage_file}](../stages/{guide.stage_file})。阶段文档决定课程任务和验收，[第 {week:02d} 周公共成果要求](../../deliverables/week-{week:02d}/README.md)定义门禁；学习状态只记录在个人学习仓库。

## 本周先理解

### 为什么学

{guide.why}

### 这是什么

{guide.what}

### 本周语言定位

{language_focus(week)}完整职责、切换桥接和替代规则见[开发语言路线](../01-language-roadmap.md)。

### 本周学习策略

- 每天只完成下面一节，控制在约 1 小时，不提前堆叠下一节的新概念。
- 先预测再实验；先保存原始证据，再写结论；失败样例与正常结果同等重要。
- 首次遇到术语时补齐：一句话定义、输入输出、开发类比、类比边界、反例和“不是什么”。
- 使用 H1→H4 提示阶梯；若使用完整参考答案，必须额外完成一个不同输入或约束的变体。

## 逐节教程

{sections}
## 本周收尾

按[成果与提交标准](../06-deliverable-standards.md)整理本周成果，再由讲师按[监督与掌握度规范](../07-instructor-supervision.md)给出“通过、部分通过、未通过”。教程完成不代表学习者已经掌握，必须以独立运行、排错、Teach-back 和变体证据为准。
"""


def render_index() -> str:
    rows = "\n".join(
        f"| {week:02d} | [{guide.title}](week-{week:02d}.md) | {language_label(week)} | [阶段计划](../stages/{guide.stage_file}) |"
        for week, guide in WEEK_GUIDES.items()
    )
    return f"""# 逐节课程教程

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
{rows}

## 输入、输出与边界

- 输入：九份阶段计划中的四列表格、课程资料链接和验收要求。
- 输出：按周组织的逐节学习教程。
- 禁止内容：真实密钥、生产数据、唯一成果副本、自动推进的学习状态和未经验证的业务收益。
- 维护方式：修改阶段日程后运行生成脚本；不要直接改生成的 `week-XX.md`，需要改变教程规则时修改生成器。
"""


def expected_files() -> dict[Path, str]:
    lessons_by_week = parse_lessons()
    missing = sorted(set(WEEK_GUIDES) - set(lessons_by_week))
    invalid = {week: len(lessons) for week, lessons in lessons_by_week.items() if len(lessons) != 7}
    if missing or invalid:
        raise SystemExit(f"invalid course plan: missing_weeks={missing}, lesson_counts={invalid}")
    files = {OUTPUT_DIR / "README.md": render_index()}
    files.update({OUTPUT_DIR / f"week-{week:02d}.md": render_week(week, lessons_by_week[week]) for week in WEEK_GUIDES})
    return files


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when generated tutorials are missing or stale")
    args = parser.parse_args()
    files = expected_files()
    if args.check:
        stale = [path for path, content in files.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
        if stale:
            for path in stale:
                print(path.relative_to(REPO_ROOT))
            return 1
        print(f"course tutorials are current: {len(files) - 1} weeks, 224 lessons")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
    print(f"generated {len(files) - 1} weekly tutorials with 224 lessons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
