# Java 主服务目录

本目录从第 5 周开始存放 Java 21、Maven、Spring Boot 和 Spring AI 主服务。

后续主要模块包括：

- Chat API 与流式输出。
- 文档扫描、切片、Embedding 和索引构建。
- 检索、RAG、来源引用与拒答。
- `listFiles`、`readFile`、`searchDocs` 等只读工具。
- Java Agent、执行日志、超时和取消。
- 调用 Python Agent Worker 的客户端。
- 平台 Project、RBAC 与资源归属。
- Agent、Model、Tool/MCP、Knowledge Base 和 Workflow 控制面 API。
- 版本、发布、回滚、配额、审计和运行查询。
- 面向业务系统的 Open API、Connector 接口和身份上下文传播。

当前 README 用于预留目录；第 5 周初始化工程后，应补充真实的构建、配置、测试和启动命令。第 17 周起按业务职责拆分平台模块，避免把控制面逻辑全部堆在 Controller 中。真实密钥只能来自环境变量或密钥管理服务。
