# 基础设施与运行目录

本目录存放本地环境、部署、可观测性和运行维护资料，不存放业务源码、真实 Secret 或生产数据。

计划内容：

- `compose/`：本地 PostgreSQL、Vector Store、观测组件和服务编排。
- `observability/`：Trace、Metric、Log 的本地配置、查询和仪表盘。
- `load-test/`：模型网关、工作流和业务入口的压测脚本及说明。
- `runbooks/`：告警确认、止损、恢复、回滚和升级路径。
- `backup-restore/`：元数据、Checkpoint、评测和索引定义的备份恢复步骤。
- `security/`：密钥扫描、依赖检查和攻击回归入口。

新增子目录时必须提供 README，说明用途、运行命令、输入输出、禁止内容和清理方式。部署配置必须区分开发、测试和生产环境，并使用 Secret 引用而非明文值。
