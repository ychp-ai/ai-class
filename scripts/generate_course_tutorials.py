#!/usr/bin/env python3
"""Generate tutorials for the 32-week core and 8-week reinforcement plan.

Stage documents remain the source of truth for schedule, task, advice and
acceptance. This generator adds a teaching layer without duplicating progress
state or allowing tutorials to drift from the required four-column tables.
"""

from __future__ import annotations

import os
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
    33: WeekGuide("独立设计与单会话基线", "10-super-agent-coordination.md", "把持续协作需求转为可验证的任务边界，先建立公平对照。", "持续协作系统接收事件、管理长期目标并派发执行尝试；Task 是目标，Run 是一次尝试，模型建议由平台校验后才生效。"),
    34: WeekGuide("并发调度与任务隔离", "10-super-agent-coordination.md", "让多个任务共享有限资源时仍能推进并保持隔离。", "调度器依据队列、容量、租约和预算派发已授权任务；并发数增加不会自动带来公平性、文件隔离或执行唯一性。"),
    35: WeekGuide("事件驱动与主动触发", "10-super-agent-coordination.md", "让外部事件触发受控工作，同时抵御重复、积压与通知循环。", "事件说明已经发生的事实，触发规则决定是否行动；接收事件、获得上下文和取得执行权限是三个不同判断。"),
    36: WeekGuide("跨渠道身份与任务上下文", "10-super-agent-coordination.md", "使不同入口的补充信息正确延续同一任务，避免串人、串租户与旧上下文污染。", "跨渠道协作依赖可信身份、显式任务关联和版本校验；语义相似度只提供候选，不能代替身份或权限。"),
    37: WeekGuide("中途纠正、取消与撤权", "11-super-agent-reliability.md", "保证执行期间的控制输入能持久接收，并在明确边界生效。", "命令收件箱记录变更意图，执行器在安全边界应用命令；接收、应用和外部副作用完成具有不同状态。"),
    38: WeekGuide("多任务持久恢复与副作用核对", "11-super-agent-reliability.md", "在进程退出、接管和回执丢失后重建可信状态。", "持久恢复结合数据库、Checkpoint、投递凭证和外部核对；重启不能清除未知事实，也不能重新授予已经撤销的权限。"),
    39: WeekGuide("持续运行、停滞与运行交接", "11-super-agent-reliability.md", "用受控长时间实验识别资源泄漏、无效循环和无法交接的运维问题。", "持续运行需要有效进展观测、有限恢复和可执行 Runbook；心跳只证明存活，短时加速测试不能替代真实墙钟观察。"),
    40: WeekGuide("对照评测与独立交付考试", "11-super-agent-reliability.md", "以公平实验和陌生变体验证架构收益与独立能力。", "专项交付分别判断控制正确性、任务质量、成本、可运维性和学习掌握度；能够实现系统不代表它值得推广。"),
}


# 每节只展开一个原理问题和一个反例；考试条目仅给证据格式。
REINFORCEMENT_PROBES: dict[int, list[tuple[str, str]]] = {
    33: [
        ("怎样把‘持续修复问题’拆成可验收且有停止条件的授权范围？", "需求要求 Agent 自动合并所有修改，是否超出当前交付范围？"),
        ("一次尝试失败后，哪些 ID 应保持不变，哪些需要新建？", "相同问题重试两次却生成三个独立目标，如何从记录发现？"),
        ("为什么模型选择关联某任务后，仍需普通代码决定是否接纳？", "路由建议指向另一个 Project，模型置信度很高时应怎样处理？"),
        ("执行契约为什么同时需要需求版本与发布版本？", "Worker 收到缺少授权引用或过期 revision 的任务。"),
        ("固定案例与留出案例分别防止哪种自我欺骗？", "查看留出失败后改评分规则，却继续把同一结果称为留出评测。"),
        ("基线中的失败、等待和人工操作应该怎样计入分母？", "三个代表任务中一个失败，只报告成功任务的平均耗时。"),
        ("哪些需求用普通函数就足够，什么时候才需要模型参与？", "把一个完全确定的规则交给模型，输出偶尔改变。"),
    ],
    34: [
        ("Worker 数量限制与等待队列容量分别限制什么资源？", "Worker 已满且队列已满，新的任务仍被应答为已派发。"),
        ("如何从有限实验发现饥饿风险，并解释规则的等待上界？", "持续到来的高优先任务让一个旧任务一直无法获得槽位。"),
        ("租约到期与旧 Worker 停止为什么不是同一个事实？", "两个 Worker 同时申请同一个任务，数据库是否接受两个 owner？"),
        ("独立会话为什么不等于文件和工具访问隔离？", "任务 A 尝试用相对路径读取任务 B 的工作目录。"),
        ("为什么需要在执行前预留预算，怎样处理取消后的释放？", "两个任务同时看到剩余额度足够，随后合计超出全局上限。"),
        ("怎样从时间线证明三个任务并行且慢任务没有阻塞其他任务？", "一个任务占用所有执行槽，另一个任务又触发资源耗尽。"),
        ("容量改变后，哪些状态迁移应保持正确？", "容量从三降到二时已有三个任务运行，不能靠删除记录降容量。"),
    ],
    35: [
        ("哪些事件字段来自可信接入层，哪些只是用户正文？", "正文自称管理员且附带别人的 Project ID。"),
        ("去重键为何包含来源，为什么不能只比较时间戳？", "重启后再次收到同一来源同一 eventId 的旧事件。"),
        ("订阅信息或模型兴趣为什么不能自行产生执行授权？", "普通聊天提到一个缺陷，系统没有适用的主动触发规则。"),
        ("任务结束后订阅应该怎样失效，剩余事件如何处理？", "已取消任务仍收到外部更新，旧订阅试图把它唤醒。"),
        ("接收失败和延迟处理应怎样让来源可观察并安全重投？", "事件突发超过容量，系统悄悄丢弃一部分却返回成功。"),
        ("哪些变化值得通知人，怎样防止通知再次触发自身？", "机器人的完成消息被入口适配器重新当作新任务。"),
        ("调换投递顺序后，什么证据决定事件应新建、关联或忽略？", "旧事件晚于任务终态到达且被重复投递五次。"),
    ],
    36: [
        ("渠道账号怎样被验证并绑定到平台主体？", "两个渠道中昵称相同的两个用户访问同一个任务。"),
        ("任务关联需要哪些证据，关联错误如何撤销且保留历史？", "两个候选任务语义相近，其中一个属于别的 Project。"),
        ("为什么时间戳不能代替 expectedRevision 的并发校验？", "两个入口都基于 revision 3 提交不同要求。"),
        ("记忆中的事实、当前需求与权限真相分别由谁维护？", "旧摘要要求扩大范围，但当前需求已缩小且记忆已过期。"),
        ("注入内容在哪里被当成数据，哪里可能变成执行意图？", "检索文档要求读取另一工作区并向外发送结果。"),
        ("跨入口关联正确与执行中修订生效为何需要不同证据？", "补充消息入库成功，但 Worker 仍按旧要求执行。"),
        ("在未见过的入口条件下，你如何独立选择最小关联方案？", "讲师提供一例未练过的错关联；先取证，再定位修复。"),
    ],
    37: [
        ("命令接收成功与命令生效分别可以向用户承诺什么？", "应答成功后进程退出，命令尚未保存。"),
        ("怎样证明长工具等待没有阻塞控制消息接收？", "函数标了 async，却在事件循环中进行同步阻塞调用。"),
        ("需求修订在哪个边界生效，旧结果到达时如何判断有效性？", "新需求已接收，旧 Worker 随后提交旧 revision 的成功结果。"),
        ("取消与完成竞争时依据什么选定终态，已发生动作怎么办？", "先取消、后完成与先完成、后取消产生相互矛盾的状态。"),
        ("恢复前与副作用前为什么都要检查当前授权？", "等待审批期间权限被撤销，旧 Checkpoint 恢复后尝试写入。"),
        ("如何串联命令时间线、版本和副作用次数证明组合行为？", "伪造主体提交取消，之后又有重复命令与迟到工具结果。"),
        ("缩小范围与取消整个任务分别影响哪些未来动作？", "已完成写入被当作取消后不存在的事实。"),
    ],
    38: [
        ("进程消失后哪些数据必须仍存在，怎样证明它们真正持久？", "测试只抛异常但共享内存仍在，误认为验证了重启恢复。"),
        ("状态与投递意图同事务解决什么间隙，还留下什么重复风险？", "提交已成功、派发前退出；重启时又派发了两次。"),
        ("epoch 必须由谁核验，为什么只在 Worker 自查不够？", "旧 Worker 暂停后恢复，新 Worker 此时已取得新租约。"),
        ("外部调用超时后，什么证据能区分未发生、成功与未知？", "外部写成功但回执丢失，外部又不支持查询或幂等。"),
        ("排队、执行中和待审批任务应分别从哪里重建状态？", "重启把所有任务统一置为执行中，连未批准任务也被启动。"),
        ("如何证明退出实验覆盖了真实的跨进程副作用间隙？", "服务与外部 Stub 同时重置，写入计数被清零导致假通过。"),
        ("陌生退出位置下，先检查哪类证据可以缩小故障范围？", "命令已签收未应用时退出，禁止直接改库补出成功结论。"),
    ],
    39: [
        ("什么是可验证进展，正常人工等待为什么不能按无进展重启？", "Worker 不断发心跳却重复同一步骤，没有新的结果。"),
        ("恢复策略何时必须停止自动处理并交人工？", "每次重启都失败，Watchdog 持续重试并发送重复通知。"),
        ("接收延迟、生效延迟和任务完成延迟分别回答什么问题？", "只统计成功请求平均值，隐藏失败与长时间排队。"),
        ("停止派发、保存状态和核对在途操作的顺序有什么依据？", "回滚软件版本时顺手删除了已成功副作用的记录。"),
        ("什么条件使 24 小时后台观察可控并可提前止损？", "观察中预算耗尽或队列失控，却没有可用的终止开关。"),
        ("加速时钟和真实墙钟观察分别能验证哪些问题？", "只运行十分钟却按模拟时间写了连续 24 小时通过。"),
        ("陌生操作者如何仅凭 Runbook 决定重试、终止或人工核对？", "手册只写‘重启即可’，无法处理未知外部写入结果。"),
    ],
    40: [
        ("哪些条件必须相同，才能把差异归因于调度架构？", "新方案使用更强模型或更大总预算，却把提升归因于并发。"),
        ("三轮实验怎样保留失败、样本量和留出结果的独立性？", "第一轮看到留出失败就改实现，再把后三轮都称为盲测。"),
        ("安全断言都通过但性能无收益时，应该如何形成决策？", "只列成功任务成本，省略失败重试、人工操作和通知负担。"),
        ("面对新约束，怎样从需求推导方案而不先套现有实现？", "讲师临场改变条件；考试不预给字段、状态机或标准实现。"),
        ("最小关键路径要验证什么，哪些复用与提示需要如实披露？", "复用完整答案后声称关键实现完全独立。"),
        ("怎样让故障假设被证据证实或推翻，再迁移到第二个约束？", "陌生故障无法安全修复时，需说明安全停止的依据。"),
        ("专项掌握度与系统推广决策为什么要分别记录？", "仅演示正常路径便宣称通过全部可靠性考试或达到生产成熟度。"),
    ],
}


def language_label(week: int) -> str:
    if week >= 33:
        return "Java 控制面 + Python Worker"
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
    if week >= 33:
        return "复用原平台：Java 管任务、授权和持久状态，Python Worker 执行已授权快照，PostgreSQL 保存控制记录；先用持久 Fake/Stub 验证，真实模型与外部系统验证范围单列。"
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
    current_lesson_chapters = {
        "分析失败并形成报告": "实验解释与实现边界 → 失败最小复现（第 15 周）",
        "Checkpoint 和恢复": "Persistence → Checkpointer vs. store；Troubleshooting → MemorySaver does not persist between restarts",
        "幂等和副作用凭证": "实验解释与实现边界 → 恢复边界（第 22 周）",
        "监控业务与 AI 指标": "实验解释与实现边界 → 试点指标（第 30 周）",
        "整理架构、业务案例与岗位证据": "2026-10-22 复核结论 → 本轮样本与可信度、对现有课程的增量调整",
    }
    if lesson.task in current_lesson_chapters:
        return current_lesson_chapters[lesson.task]
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
    experiment_templates = {
        "分析失败并形成报告": """```text
选择：已有失败中的一例；不新增一整套数据
关联：Case ID、Run/Trace、代码/模型/Prompt/Tool/数据及评分版本
夹具：最小脱敏输入、固定 Fake/Stub 输出、初始状态与预期断言
复现：实际命令 → 预期/实际 → 最先出现差异的层 → 下一步验证
边界：Fake 回放验证程序路径；真实模型重跑记录次数与差异，不保证逐字相同
安全：只在隔离副本/Stub 中复现，不把生产 Trace 的写操作再次发送
交付：他人按命令可观察该失败，不能只提交截图或模型自述
```""",
        "Checkpoint 和恢复": """```text
复用：第 11 周工作流和持久 Checkpointer，记录依赖与存储配置
准备：固定任务、发布版本、授权与已完成节点；保存恢复前记录
动作：实际退出执行进程，再用同一任务标识启动恢复
核对：已落盘状态仍在，已记录完成的节点不重复执行
反例：改用内存 Saver 时重启后丢失状态，不能据此宣称持久恢复通过
范围：本日检查已保存状态；外部写成功但未保存回执的窗口在周三验证
```""",
        "幂等和副作用凭证": """```text
准备：单节点写工具；持久外部 Stub 按幂等键保存业务记录和实际写入次数
边界：Stub 独立保留状态，执行进程退出不能清空外部业务记录
注入：外部提交成功 → 丢弃回执 → 本地成功 Checkpoint 前退出执行进程
恢复：原任务/授权/版本/幂等键 → 查询外部凭证或以同键取回已有结果
断言：业务记录 1 条、实际副作用 1 次；Step 绑定外部结果与 Run/Trace
未知：外部不可查询且无幂等保障时停止自动重试，转待核对，不伪造成功
解释：本地准备记录不是成功凭证；Checkpoint 不与外部系统自动构成事务
```""",
        "故障注入演练": """```text
复用：本周超时、工具 500、重复事件、数据库失败和进程退出的既有测试
重点重跑：外部写成功且回执丢失，随后退出并重启执行进程
矩阵：故障点 / 复现命令 / 预期状态 / 实际状态 / 重试与最终去向
证据：Run/Step/Trace、幂等键、持久状态、外部凭证和实际副作用次数
边界：恢复不改变发布版本或扩大授权；无法确定结果进入待核对路径
限制：Stub 只证明控制逻辑，真实下游的查询、幂等和保留期仍需契约验证
```""",
        "监控业务与 AI 指标": """```text
集合：固定入组条件、观察窗口、版本；按唯一任务 ID 去重，标明真实/模拟
状态：自主完成 A、人工接管后完成 H、失败 F、超时 T、拒绝 R、未完成 P
核对：状态互斥，N = A + H + F + T + R + P；人工介入事件另记
指标：自主完成率 A/N，总体完成率 (A+H)/N；N=0 时均为 N/A
成本：所有尝试的模型/工具费用 C，单位完成成本 C/(A+H)，无完成时 N/A
人工：复核与接管时长、单价假设单列；并入总成本时说明范围且避免重复
反例：只算成功调用、漏掉重试费用、把权限拒绝算业务完成或把模拟写成收益
```""",
        "整理架构、业务案例与岗位证据": """```text
来源：两份实际 JD 的链接、核验日期、地点、职级与正文冲突/缺失项
分类：职责 / 必需条件 / 加分项，不根据岗位标题补猜要求
映射：要求 → 已有成果及版本 → 命令/样本/指标 → 独立完成与 AI 辅助 → 差距
边界：课程项目不能替代学历、年限、真实流量、训练或推理基础设施经验
验收：沿用最终报告，不另建项目；数据和业务收益标明真实/模拟
```""",
        "能力答辩与学习复盘": """```text
项目描述：用已有成果写三条，包含问题、个人动作、验证条件、结果和限制
复现：至少一条链接第 15/22 周的失败复现命令，能解释因果与修复取舍
贡献：指出哪些由自己设计/实现/排错，哪些来自 AI 建议及如何人工验证
变体：不看参考答案，现场改变一个预算、权限或检索条件并验证结果
结论：根据独立证据判定掌握，缺少证据的岗位要求记录下一步补强计划
```""",
        "构造有预算的上下文并记录步骤": """```text
输入：必要指令、当前任务、完整工具调用/结果组、可选历史、Token 预算
构造顺序：预留输出空间 → 检查必要内容 → 按相关性加入可选消息组
裁剪单位：完整消息/工具配对；不要截断 JSON 或只保留半个工具调用
必要内容超预算：返回 CONTEXT_BUDGET_EXCEEDED，不继续调用模型
实验：同一任务分别使用原输入/裁剪输入，记录长度、结果和保留的约束
反例：长工具输出挤掉“只读”约束；预算减半后应明确失败或仍保留约束
证据：构造器测试、脱敏消息 ID、实际结果；权限另由执行代码校验
```""",
        "实现最小混合检索对照": """```text
固定：文档/Chunk/模型/问题/TopK；先保存纯向量基线
候选 A：向量检索；候选 B：关键词检索（如 BM25）
混合：按排名融合 A/B（如 RRF），按来源 ID 去重
对照：仅改检索策略，不加重排、不改 Prompt
逐题记录：预期来源、实际候选及顺序、引用、答案、耗时
反例：精确错误码未召回；文档存在但解析为空；无答案题误答
框架对比：Spring AI 与 LangChain 均用原纯向量配置
```""",
        "重排、权限与检索评测": """```text
固定：同一问题集、模型、混合检索候选、TopK、Prompt、评分规则
权限：在候选返回及提交给外部重排服务前过滤 ACL
组 A：混合检索 → TopK；组 B：相同候选 → 重排 → TopK
记录：Recall@K、MRR、引用/答案质量、重排耗时、总延迟
反例：相关片段不在候选中时，重排无法补回；越权片段不得送给模型
结论：提升/持平/退化 + 样本和失败解释；不预设一定提升
```""",
        "跑 Baseline 并人工复核评分": """```text
Case ID / 开发或留出 / 数据版本 / 模型与评分规则版本
预期来源或工具/参数 / 代码断言结果 / 语义分数或无法评分
人工复核：正确、错误、拒答、工具失败、评分存疑各一例
分歧：自动评分、人工判断、证据、处理结论
规则变更：旧版/新版结果按相同新规则重跑，不只重评有利样例
结果：保留全部失败；开发集用于改动选择，留出集用于最终对照
```""",
        "离线回归与 CI 发布门禁": """```text
准备：复用第 15 周 Runner、固定数据集及评分版本
CI 步骤：代码测试 → 固定 Eval → 安全/延迟/成本阈值 → 保存报告
正例：已知基线返回成功退出状态；报告绑定版本和运行环境
反例：故意移除一项权限检查或降低任务质量，CI 失败并阻止发布
外部服务不可用：Fake 只验证执行流程；真实质量门禁记为未验证
验收证据：两次 CI 运行地址或本地等价记录、退出状态、报告
```""",
        "用户反馈转为回归用例": """```text
反馈来源：真实试点/高保真模拟；记录授权与脱敏方式
人工审核：问题归类、预期答案/动作、允许副作用、评分规则
数据流：反馈 ID → 新 Case ID → 新数据集版本 → 固定回归
版本策略：保留原基线集，新增反馈不能覆盖或删除旧失败样例
反例：用户点赞但来源错误；未审核的反馈不得直接作为正确标签
验收：原回归结果、新用例结果、版本、限制及下一步
```""",
        "基准与路由报告": """```text
条件：硬件/运行环境、模型及量化版本、并发、样本数、输入/输出长度上限
指标：首 Token 延迟、P50/P95 总延迟、吞吐、失败率、质量、Token
成本：云端实际 Usage；本地记录运行时间与资源成本假设
对照：先满足相同质量与安全阈值，再比较路由成本和延迟
反例：小样本、缓存命中率不同、输出截断、Stub 结果不当作真实性能
选型：Prompt/RAG/微调各解决哪类问题；未训练则不声明微调经验
```""",
    }
    if lesson.task in experiment_templates:
        return "专项实验骨架（填写实际结果，不预填通过）", experiment_templates[lesson.task]
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


def relocate_stage_links(text: str) -> str:
    """Keep stage-relative sources valid in the sibling tutorials directory."""
    def replace(match: re.Match[str]) -> str:
        label, target = match.groups()
        if target.startswith(("https://", "http://", "#")):
            return match.group(0)
        path, separator, anchor = target.partition("#")
        relative = os.path.relpath(STAGES_DIR / path, OUTPUT_DIR)
        return f"[{label}]({relative}{separator}{anchor})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace, text)


def render_reinforcement_lesson(week: int, lesson: Lesson, number: int) -> str:
    action, separator, resource = lesson.advice.partition("\n\n相关资料：")
    question, failure = REINFORCEMENT_PROBES[week][number - 1]
    resource_line = f"\n专项资料：{relocate_stage_links(resource)}" if separator else ""
    is_exam = (week == 36 and number == 7) or (week == 40 and number >= 4)
    hints = (
        "本节为独立考试或答辩，不预给实现答案。讲师只给需求、约束、故障现象与成功条件；"
        "记录实际提示级别。若已用过完整答案，本题只能计练习，另换陌生变体重考。"
        if is_exam else
        "H1：先找第一个与预测不一致的事件、状态或证据。\n\n"
        "H2：回答上面的原理问题，明确由谁持有状态、授权和副作用凭证。\n\n"
        "H3：只为出错的一步画输入 → 前置校验 → 状态变化 → 可观察结果，"
        "请讲师给局部伪代码或一条断言，再独立补齐。\n\n"
        "H4：仍阻塞时再请求当前小问题的完整参考实现；记录使用范围，"
        "关闭答案后改变一个事件顺序、角色、版本或资源上限重新完成。"
    )
    return f"""### {lesson.day} · 第 {number} 节：{lesson.task}

**为什么学**

本节只推进“{lesson.task}”，为“{lesson.acceptance}”留下可以复核的证据。

**这是什么与今天的边界**

{action}。首次接触术语时，用自己的话补齐定义、输入输出、开发类比及其局限、反例和“不是什么”；复习日不再增加新概念。

**原理问题**

{question}

**怎么学（约 60 分钟）**

1. `0–5 分钟`：检查上次遗留问题和本节依赖，先写正常结果与失败结果的预测。
2. `5–15 分钟`：仅阅读当前任务相关段落，对照既有实现；记录来源版本和差异。考试日这段时间用于独立分析约束。
3. `15–40 分钟`：完成本节最小实现、设计或实验，不扩展到下一天的能力。复用既有平台，所有执行都在隔离练习目录。
4. `40–50 分钟`：验证反例：{failure}
5. `50–60 分钟`：整理证据，用自己的话回答原理问题；改变一个输入或约束先预测再复验。若未完成则记录未通过项，不能凭时间推进。
{resource_line}

**卡住后的提示阶梯**

{hints}

**怎么验证学会了**

- 必交证据：{lesson.acceptance}。
- 记录格式：Case ID、输入/事件顺序、主体与 Project、任务/运行/版本、预期、实际、验证命令、状态/副作用/通知数量、失败解释、提示级别。
- 设计或报告课保留决策依据与反例推演；实现和实验课必须亲自运行。真实模型、持久 Stub、加速时钟和墙钟观察分别标注。
- 不看教程完成复述与一个小变体；只会照抄或运行时最高 L1，不能标记掌握。
- 讲师结论为“通过、部分通过、未通过”；阶段考试只给“通过/未通过”。证据写入个人仓库，公共教程不填个人结果。
"""


def render_week(week: int, lessons: list[Lesson]) -> str:
    guide = WEEK_GUIDES[week]
    sections = "\n".join(
        render_reinforcement_lesson(week, lesson, index)
        if week >= 33 else render_lesson(lesson, guide, index)
        for index, lesson in enumerate(lessons, start=1)
    )
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
    core_rows = "\n".join(
        f"| {week:02d} | [{guide.title}](week-{week:02d}.md) | {language_label(week)} | [阶段计划](../stages/{guide.stage_file}) |"
        for week, guide in WEEK_GUIDES.items() if week <= 32
    )
    reinforcement_rows = "\n".join(
        f"| {week:02d} | [{guide.title}](week-{week:02d}.md) | {language_label(week)} | [阶段计划](../stages/{guide.stage_file}) |"
        for week, guide in WEEK_GUIDES.items() if week >= 33
    )
    return f"""# 逐节课程教程

## 目录定位

本目录为 32 周主线与 8 周 Super-agent 强化提供逐节教程，共 40 份周教程、280 节每日课程。原主线为 224 节，强化为 56 节；原课程毕业与专项通过分别验收。每节回答为什么学、这是什么、怎么学、怎么验证学会了。

参考答案严格对应“怎么学”的五个步骤：先给预测示例，再定位资料链接中的章节/条目，然后提供对应 Mermaid 图、样例代码或文档模板，最后给出失败注入、交付物和 Teach-back 示例。

强化课程使用任务专属的原理问题、失败场景和 H1→H4 提示；不预给阶段考试的实现答案。先独立尝试，再按阻塞程度请求局部示例或完整参考。专项项目、固定评测与进入条件见[强化课程设计](../11-super-agent-reinforcement.md)。

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

## 原 32 周主线教程

| 周次 | 教程 | 默认语言 | 对应阶段计划 |
| ---: | --- | --- | --- |
{core_rows}

## 第 33–40 周 Super-agent 强化教程

| 周次 | 教程 | 默认语言 | 对应阶段计划 |
| ---: | --- | --- | --- |
{reinforcement_rows}

## 输入、输出与边界

- 输入：十一份阶段计划中的四列表格、课程资料链接和验收要求。
- 输出：按周组织的逐节学习教程。
- 禁止内容：真实密钥、生产数据、唯一成果副本、自动推进的学习状态和未经验证的业务收益。
- 维护方式：修改阶段日程后运行生成脚本；不要直接改生成的 `week-XX.md`，需要改变教程规则时修改生成器。
"""


def expected_files() -> dict[Path, str]:
    lessons_by_week = parse_lessons()
    missing = sorted(set(WEEK_GUIDES) - set(lessons_by_week))
    unexpected = sorted(set(lessons_by_week) - set(WEEK_GUIDES))
    invalid = {
        week: [lesson.day for lesson in lessons]
        for week, lessons in lessons_by_week.items()
        if [lesson.day for lesson in lessons] != [f"周{day}" for day in "一二三四五六日"]
    }
    if missing or unexpected or invalid:
        raise SystemExit(f"invalid course plan: missing_weeks={missing}, unexpected_weeks={unexpected}, invalid_days={invalid}")
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
        print(f"course tutorials are current: {len(files) - 1} weeks, {(len(files) - 1) * 7} lessons")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
    print(f"generated {len(files) - 1} weekly tutorials with {(len(files) - 1) * 7} lessons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
