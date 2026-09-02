# 业务案例目录

本目录存放一个业务场景从发现到上线复盘的完整证据链。技术架构的正式设计放在 `docs/`，源码放在服务目录，本目录不复制代码和运行日志。

建议每个案例建立独立子目录，例如 `business-cases/case-01/`，并在子目录提供 README。一个完整案例应包含：

```text
01-scene-brief.md          # 业务目标、用户、Owner、范围和停止条件
02-interviews.md           # 访谈对象、事实摘要、分歧和待验证假设
03-systems-and-data.md     # 系统、接口、数据、权限和敏感等级
04-as-is-process.md        # 主流程、异常流程、步骤数据和根因
05-to-be-process.md        # 优化后的人机协作、降级和人工兜底
06-value-and-metrics.md    # Baseline、指标口径、ROI/TCO 和验收阈值
07-integration-design.md   # 接入模式、契约、数据映射和权限传播
08-pilot-plan.md           # UAT、试点范围、灰度、观察和回退
09-pilot-results.md        # 原始数据摘要、反馈、失败分类和指标对比
10-decision-review.md      # 推广、调整或停止的决策与证据
```

必须区分事实、假设和建议。没有真实业务对象时可以做高保真案例，但需要明确模拟角色、数据来源、未验证项，不能把模拟收益标记为真实业务结果。

禁止存放客户身份信息、未脱敏访谈原文、生产数据导出、访问凭证和内部受限资料。
