# Python Agent Worker 目录

本目录从第 9 周开始存放 Python 3.11+ Agent 服务。

计划结构：

```text
python-agent/
├── src/
│   ├── chain/           # LangChain 模型、工具和结构化 Agent
│   ├── graph/           # LangGraph 状态、路由、审批和恢复
│   ├── claude_worker/   # Claude Agent SDK 执行层
│   ├── runtime/         # 已发布 Agent/Workflow 的运行、Checkpoint 和事件
│   └── api/             # 与 Java 服务通信的接口
└── tests/               # pytest 测试
```

当前 README 用于预留目录；第 9 周建立虚拟环境和依赖文件后，应补充安装、运行、测试、环境变量和 API 协议说明。执行面只运行控制面发布的不可变快照，不自行修改权限、模型、工具或业务策略。不要提交 `.venv`、缓存、会话凭证或 Agent 生成的未脱敏日志。
