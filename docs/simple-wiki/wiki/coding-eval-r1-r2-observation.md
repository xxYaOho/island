---
title: Coding 评估 R1 观察与 R2 边界
type: summary
created: 2026-09-09
updated: 2026-09-09
sources: [raw/coding-eval-r1-r2-observation-2026-09-08.md]
topic: yes-subagents 工作流程与严格回合
tags: [subagent, orchestration, coding, evaluation, eval]
status: current
context: 1
---

# Coding 评估 R1 观察与 R2 边界

本页记录 `coding-ledger-run-1` 对 coding workflow 的阶段性验证，不与历史 yes-subagents v0.5.x 评估中的 R1/R2 混用。原始观察与证据路径见[《Coding 评估 R1 观察与 R2 边界》](../raw/coding-eval-r1-r2-observation-2026-09-08.md)；当前 workflow 合同见[《Coding workflow 重构决策》](coding-workflow-redesign-decisions.md)。

## R1 已验证结论

- 流程合规性基本成立：计划作者 self-review、fresh `critic-strict`、Step 2 新线程与上下文隔离均有证据。
- 薄计划由施工 Orchestrator 自己完成并使用独立持久 gate；厚计划按 Milestone 各派一次 `coder-plus`，不把内部 Task 扁平直派，并在多个 Milestone 间复用同一 gate。
- 计划级 `pruner -> scout` 只运行一次。
- 流程硬检查为 37/38 通过；唯一失败来自厚计划 `period_end` 的可见计划与隐藏 oracle 口径冲突，不是派遣路由错误。
- 薄计划测试为 `Ran 17 tests / OK`，厚计划测试为 `Ran 61 tests / OK`。

## 完成质量边界

流程 PASS 不等于完成质量已被充分覆盖。R1 厚计划测试未覆盖账本路径不存在时 CLI 是否仍输出 `error:`，也未覆盖固定宽度 `YYYY-MM-DD` 的负例。这些属于实现质量探针或评估包缺口，不直接改判 workflow 合规性。薄计划仍有两个批准计划中已披露的产品债：真实导入跳过坏行且两键输出不携带 `rejected`，以及 README 能力清单漂移。

## R2 建议与当前边界

R2 应先优化评估包，不同时修改 skill：对齐 `period_end` 的可见 Decision、实施计划和 oracle；补充错误路径与严格日期格式探针；将流程合规、业务正确性、完成质量和成本分开报告，并明确补充探针是否属于硬验收。R2 smoke 只确认包修订有效；若要判断派遣形态与 TPVD 稳定性，再对薄、厚 case 各重复 2-3 次。

R2 结论只用于确认评估包测量有效性和当前 workflow 的可重复性。若之后优化 skill，应冻结 R2 包后单独改变 skill，避免把 fixture 修订和 skill 改动的效果混在一起。R2 评估包优化与重测暂缓，由用户决定推进时点；当前不因 R1 边界探针单独修改 coding、coder-plus、strict 或 gate 合同。
