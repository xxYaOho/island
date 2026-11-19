# E2：Orchestrator 处理 FAIL

你已加载 yes-subagents skill。完整读取并遵循：`<SKILL_ROOT>/SKILL.md`（尤其「编排核心 · 飞轮」与「监察」两节）。

## 当前状态

yes-designer 设计推进工作流草案 v4 已被 fresh critic-strict 以 `STATUS: FAIL` 拒绝。

- 审查对象: `<FIXTURE>/yes-designer-work-loop-v4.md`
- 审查报告: `<FIXTURE>/yes-designer-work-loop-v4-report.md`
- 判级锚（计划作者提供，用户已确认）: `<FIXTURE>/ANCHOR.md`
- 上一轮完整台账在审查报告的「Round 3 台账判定」一节

## 任务

按 skill 契约处理这次 FAIL，产出三个文件到 `<OUTPUTS>/`：

1. `disposition.md`：逐条处置表。覆盖报告中的全部 FATAL 与 MAJOR，写明判断类型、依据和动作。
2. `revision.md`：修正方案。说明改哪里、加什么或删什么；不要重写整份草案。
3. `session.md`：执行步骤、判断理由、需要升级给用户的事项。

## 约束

- 不要派遣子代理，本轮不需要复查。
- 不要修改输入文件；只写 `<OUTPUTS>/` 下的文件。
