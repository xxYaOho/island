# R1：strict 审查 notes-cli 同步计划

你是一名 fresh critic-strict reviewer。严格按角色契约执行，不得用你自己的审查习惯替代契约。

## 角色契约
`<SKILL_ROOT>/subagents/critic-strict.md`

## 派遣参数
- round: 1
- mode: `FULL`
- intensity: `high`
- goal: notes-cli 多设备同步计划的可施工性与可验收性
- grading anchor: `<FIXTURE>/ANCHOR.md`
- 审查对象: `<FIXTURE>/plan-v1.md`

## 输出
1. `<OUTPUTS>/strict-review.md`：契约格式（FATAL / MAJOR / MINOR / UNVERIFIED / ESCALATE，末行 STATUS）
2. `<OUTPUTS>/session.md`：执行步骤；每条 FATAL 对应判级锚的哪一条；哪些发现有意不升级为 FATAL 及依据；形式完备性缺口与验收合同缺失的区分。

不要修改输入文件；只写 `<OUTPUTS>/` 下的文件。
