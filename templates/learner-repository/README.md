# AI Class 个人学习仓库

本仓库只保存一名学习者的进度、笔记、代码、实验、评测和业务案例。课程计划、教程、公共模板与监督规则来自独立的 `ai-class` 课程仓库。

## 关联课程仓库

- Git 仓库：`git@github.com:ychp/ai-class.git`
- 默认本地目录：`../ai-class`
- 课程规则入口：`../ai-class/AGENTS.md`
- 课程路线入口：`../ai-class/learning-plan/README.md`

个人仓库只保存学习状态与成果；课程目标、周计划、教程、公共成果要求和监督规则均以该课程仓库为准。

## 使用方式

```bash
python3 ../ai-class/scripts/detect_learning_progress.py \
  --repo ../ai-class \
  --progress-repo . \
  --pretty
```

课程仓库可以安全更新或被其他学习者复用；不要把本仓库中的状态、个人笔记或成果复制回课程仓库。课程中的相对成果路径（如 `docs/`、`java-service/`、`python-agent/`）均相对于本仓库根目录。

## 目录边界

- `deliverables/`：每周状态、成果链接、验证证据和讲师验收的唯一入口。
- `notes/`：周复盘、实验过程、错误模型和补救记录。
- `docs/`、`java-service/`、`python-agent/`、`platform-console/`：个人平台成果。
- `business-cases/`、`data/`、`infra/`、`prompts/`、`sandbox-workspaces/`：个人业务、数据、运行、Prompt 和隔离练习成果。

新增目录必须提供 README，说明用途、输入输出、禁止内容和与其他目录的边界。不得提交密钥、Cookie、Token、客户数据、生产导出或未脱敏日志。
