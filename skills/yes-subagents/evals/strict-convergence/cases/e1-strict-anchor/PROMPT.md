# E1：strict 判级锚定（单轮审查）

你是一名 fresh critic-strict reviewer。严格按下面的角色契约执行，不要使用你自己的审查习惯替代它。

## 角色契约

完整读取并遵循：`<SKILL_ROOT>/subagents/critic-strict.md`

## 派遣参数

- `round`: 4（修正轮 3）
- `mode`: `FULL`（本轮修正改变了基线与工件结构）
- `intensity`: `high`
- `goal`: yes-designer 设计推进工作流草案的可施工性与可验收性
- `grading anchor`: `<FIXTURE>/ANCHOR.md`
- 审查对象: `<FIXTURE>/yes-designer-work-loop-v4.md`
- 上一轮台账: `<FIXTURE>/yes-designer-work-loop-v3-report.md` 中的「Round 2 台账判定」与 FATAL / MAJOR 部分

## 任务

执行 Round 4 审查，并把结果写入 `<OUTPUTS>/strict-review.md`。

另外写 `<OUTPUTS>/session.md`，记录：

- 你的执行步骤；
- 每条 FATAL 对应判级锚的哪一条成功标准或第一用途；
- 哪些发现你有意不升级为 FATAL，以及依据；
- 你认为工件中有哪些机制不服务任何成功标准（如果有）。

不要修改任何输入文件，不要写 `<OUTPUTS>` 以外的文件。
