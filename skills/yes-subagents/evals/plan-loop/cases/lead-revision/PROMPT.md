# Lead：处理 R1 FAIL

你已加载 yes-subagents skill。完整读取并遵循 `<SKILL_ROOT>/SKILL.md`（尤其「编排核心 · 飞轮」与「监察」）。按需读取 `<SKILL_ROOT>/subagents/` 下的角色契约；本轮不派遣子代理。

## 当前状态
notes-cli 多设备同步计划 v1 已被 fresh critic-strict 以 `STATUS: FAIL` 拒绝。

- 计划: `<FIXTURE>/plan-v1.md`
- R1 审查报告: `<R1_OUTPUTS>/strict-review.md`
- 判级锚（计划作者提供、用户已确认）: `<FIXTURE>/ANCHOR.md`

## 任务
按 skill 契约处理这次 FAIL，产出到 `<OUTPUTS>/`：

1. `disposition.md`：逐条处置表，覆盖报告中的全部 FATAL 与 MAJOR，写明判断类型、依据和动作。
2. `revision.md`：修正方案，说明改哪里、加什么或删什么；不要求重写整份计划。
3. `plan-v2.md`：按修正方案产出的完整计划 v2（用于下一轮复审）。
4. `session.md`：执行步骤、判断理由、需要升级给用户的事项。

## 约束
- 不派遣子代理，本轮不需要复查。
- 不修改输入文件；只写 `<OUTPUTS>/` 下的文件。
- 不要读取本用例之外的目录。
