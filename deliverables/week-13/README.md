# 第 13 周成果：Claude 权限与 Hooks

状态：`未开始`

## 应链接的成果

- [ ] 默认只读、审批写入和拒绝配置。
- [ ] PreToolUse 危险操作拦截器。
- [ ] PostToolUse 脱敏审计日志。
- [ ] 自定义工具或 MCP 示例。
- [ ] Subagent 示例和 `docs/claude-agent-security.md`。

## 验收记录

- 危险操作测试：待填写。
- 审批拒绝后的副作用检查：待填写。
- 最低标准：危险请求被阻断；日志无密钥；子 Agent 不绕过权限。
- 阶段四出口检查：待填写。
- 建议 Commit：`feat: enforce claude agent permissions hooks and audit logs`
