# 平台管理控制台目录

本目录预留给 AI 平台最小管理控制台。目标是验证管理闭环，不以复杂视觉效果或拖拽画布为优先。

最低页面或交互范围：

- Project 与当前身份上下文。
- Agent 列表、详情、Draft、Version、Publish 和 Rollback。
- Model Alias、Tool/MCP、Knowledge Base 的只读或基础管理入口。
- Workflow 定义、校验、版本、发布和只读流程图。
- Run 列表、Step/Event、Trace、审批、取消和错误详情。
- Eval 结果、版本对比和发布门禁状态。

前端尚未初始化前只保留本说明。初始化后补充实际技术栈、安装、测试、启动和构建命令。不要在浏览器存储模型或业务系统长期凭证，也不要让界面绕过服务端 RBAC。
