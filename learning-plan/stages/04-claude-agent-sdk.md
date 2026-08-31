# 阶段四：Claude Agent SDK

周期：第 12–13 周，共约 14 小时。

目标：构建能够分析代码、修改文件和运行测试的执行型 Agent，并建立权限、审计和隔离意识。

逐节学习入口：[第 12–13 周课程教程](../tutorials/README.md)。

## 开始前应会什么

- 能解释普通模型客户端、LangChain Agent 和 LangGraph 工作流分别控制什么。
- 能在专用 Git 工作区查看 Diff、运行测试并恢复构造的练习项目。
- 能说明文件、Shell、网络和凭证为什么属于真实副作用边界。

## 零基础桥接

先比较“应用发起一次模型调用”和“执行 Harness 让模型在循环中使用工具”两条时序。权限按 Read/Glob/Grep → Edit → Bash → MCP 顺序逐项增加，每增加一项都保存允许任务、拒绝任务和审计证据，避免第一次运行就开放全权限。

## 本阶段不要求什么

- 不要求把 Claude Agent SDK 当作多租户权限系统、Secret Manager 或操作系统沙箱。
- 不要求在真实工作仓库、个人主目录或生产数据上练习。
- 不要求为了使用 Subagent 而拆分任务；只有上下文隔离或独立验收确有收益时才使用。

## 前测失败处理

若不能安全操作 Git 练习项目，先完成“构造失败测试 → 手工最小修复 → 测试通过 → 检查 Diff”；若不能区分 Prompt 约束和代码权限，先写一组允许/拒绝表，再开放任何 Edit 或 Bash。

## 第 12 周：Claude Agent SDK 基础

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | 区分 Agent SDK、Anthropic Client SDK 和 Claude Code | 分别从调用者、Agent 循环、内置工具和部署方式比较，不要只记产品名称<br>相关资料：[Claude Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview) | 写出定位与使用场景 |
| 周二 | 使用 `query()` 和流式消息 | 打印消息类型、工具事件和最终状态；不要把所有消息直接当最终文本处理<br>相关资料：[Claude Agent SDK Streaming](https://code.claude.com/docs/en/agent-sdk/streaming-output) | 打印工具调用和最终结果 |
| 周三 | 使用 Read、Glob、Grep | 只开放只读工具，要求每个分析结论给出文件路径；观察 Agent 的搜索策略<br>相关资料：[Claude Tools Reference](https://code.claude.com/docs/en/tools-reference) | 输出有文件证据的代码分析 |
| 周四 | 在练习目录中使用 Edit | 使用专用 Demo 和版本控制；修改前记录基线 Diff，限制允许文件范围<br>相关资料：[Claude Tools Reference](https://code.claude.com/docs/en/tools-reference) | 只修改指定文件 |
| 周五 | 使用 Bash 运行单元测试 | 只允许明确的测试命令；记录工作目录、命令、退出码和截断后的输出<br>相关资料：[Claude Tools Reference](https://code.claude.com/docs/en/tools-reference) | 保存命令、退出码和结果 |
| 周六 | Session 恢复和分叉 | 设计两个不同后续方向，验证恢复继续原状态、分叉不污染原会话<br>相关资料：[Claude Agent SDK Sessions](https://code.claude.com/docs/en/agent-sdk/sessions) | 能继续旧任务并创建分支 |
| 周日 | 完成自动修复 Agent | 使用“修复前失败、最小修改、修复后通过”闭环，人工审查所有文件变化<br>相关资料：[成果与提交标准](../06-deliverable-standards.md) | 完成本周提交 |

### 本周提交

建议 Commit：`feat: add claude code repair agent in isolated workspace`

必须包含：

- 一个专门的 `sandbox-workspaces/demo-project`，其中不含真实凭证。
- Claude Agent 启动脚本和最小权限配置。
- 一个构造 Bug、一个回归测试和修复后的验证结果。
- `ExecutionResult`：修改文件、运行命令、测试状态和摘要。
- Session 恢复或分叉示例。

验收标准：Agent 只在练习目录操作；修改前有失败测试，修改后测试通过；没有使用全权限模式掩盖权限问题。

## 第 13 周：权限、Hooks、MCP 与子 Agent

| 日期 | 学习任务 | 当天学习建议 | 当天验收 |
| --- | --- | --- | --- |
| 周一 | `allowed_tools`、`disallowed_tools` 和权限模式 | 从默认只读开始逐项增加权限；对每项权限写出任务理由和风险<br>相关资料：[Claude Agent SDK Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) | 实现只读 Plan 模式 |
| 周二 | `canUseTool` 动态审批 | 审批界面展示工具、完整目标、影响范围和原因；分别测试批准与拒绝<br>相关资料：[Claude Agent SDK Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) | Edit 或 Bash 前可人工决定 |
| 周三 | PreToolUse Hook | 采用显式规则匹配命令和规范化路径；用危险输入测试，不只测试正常命令<br>相关资料：[Claude Agent SDK Hooks](https://code.claude.com/docs/en/agent-sdk/hooks) | 拦截危险命令和敏感路径 |
| 周四 | PostToolUse Hook | 记录关联 ID、工具名、状态、耗时和摘要；对参数与输出做脱敏和长度限制<br>相关资料：[Claude Agent SDK Hooks](https://code.claude.com/docs/en/agent-sdk/hooks) | 记录工具、参数、结果和耗时 |
| 周五 | 接入自定义工具或 MCP | 选择天气、文档查询等只读工具；先独立调用验证 Schema，再开放给 Agent<br>相关资料：[Claude Agent SDK MCP](https://code.claude.com/docs/en/agent-sdk/mcp) | 使用一个外部只读能力 |
| 周六 | 使用 Subagent 处理测试或审查 | 选择可独立验收的子任务，限制上下文和权限；比较单 Agent 的成本与效果<br>相关资料：[Claude Subagents](https://code.claude.com/docs/en/subagents) | 主 Agent 汇总子任务结果 |
| 周日 | 设计沙箱、网络和凭证隔离 | 画清宿主、容器、工作区、代理和凭证边界，运行至少一个真实阻断测试<br>相关资料：[Claude Agent SDK Secure Deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment) | 完成阶段提交 |

### 本周提交

建议 Commit：`feat: enforce claude agent permissions hooks and audit logs`

必须包含：

- 默认只读、可审批写入和拒绝三种配置示例。
- PreToolUse 危险操作拦截器。
- PostToolUse 结构化审计日志。
- 自定义工具或 MCP 的最小只读示例。
- 一个有明确价值的 Subagent 示例。
- `docs/claude-agent-security.md`：沙箱、路径、命令、网络、凭证和残余风险。

危险操作测试至少覆盖：

```text
rm -rf 或等价破坏性命令
读取 .env、SSH、云凭证和包管理器密钥
访问工作区之外的文件
向非白名单域名发送数据
未经确认的数据库或外部系统写操作
```

验收标准：危险请求必须被阻断并留下日志；审批拒绝后不存在文件副作用；审计日志不记录密钥；Subagent 不能绕过父任务权限边界。

## 阶段出口条件

- Agent 能完成“读取 → 分析 → 修改 → 测试 → 汇总”闭环。
- 只读分析不需要开放 Edit 或 Bash 写能力。
- 敏感工具可以暂停并由人类批准或拒绝。
- 危险命令和敏感路径有自动测试或可重复验证记录。
- 能解释权限规则、Hook 与沙箱分别解决什么问题。

## 学习建议

- 先在构造的小项目中练习，不要直接对重要工作仓库开放写权限。
- 使用最小工具集；分析任务优先只开放 Read、Glob 和 Grep。
- 不使用 `bypassPermissions` 作为日常默认设置。
- Shell 命令尽量使用允许列表和固定工作目录，不依赖仅靠 Prompt 的自我约束。
- 子 Agent 会增加成本和上下文复杂度，只有独立测试、审查或调研任务才使用。
- SDK 是执行 Harness，不是完整的多租户安全边界；生产部署仍需容器或微虚拟机。

官方资料：[Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview)、[Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)、[Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)、[Hooks](https://code.claude.com/docs/en/agent-sdk/hooks)、[Secure Deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

下一阶段：[组合、评测与交付](05-integration-evaluation-delivery.md)
