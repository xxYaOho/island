---
title: critic-strict 案例观察（yes-designer 工作环）
type: summary
created: 2026-10-18
updated: 2026-11-19
sources: [raw/yes-subagents-1018-readme.md, raw/yes-subagents-1018-design-work-loop-v1-report.md, raw/yes-subagents-1018-design-work-loop-v2-report.md, raw/yes-subagents-1018-design-work-loop-v3-report.md, raw/yes-subagents-1018-design-work-loop-v4-report.md, raw/yes-subagents-1018-design-work-loop-v5-report.md, raw/yes-subagents-1018-critic-strict-major-ledger.md, raw/yes-designer-2026-10-18-critic-strict-major-ledger.md, raw/yes-designer-2026-10-18-v2-critic-round2.md]
topic: yes-subagents 工作流程与严格回合
tags: [strict, eval, yes-designer, review]
status: current
context: 1

# critic-strict 案例观察（yes-designer 工作环）

本页整理用 yes-designer 工作流草案做完整 Strict 生命周期评估的观察，主源是 [1018 案例说明](../raw/yes-subagents-1018-readme.md)，审查报告与台账作证据。工作环本身的版本演进见[《yes-designer 工作环演进（v1–v6）》](yes-designer-work-loop-evolution.md)；当前合同见[《yes-designer 设计推进工作流》](yes-designer-design-work-loop.md)。判级模型见[《Plan-Strict 循环收敛决策》](strict-plan-loop-convergence.md)。

## 生命周期结果

对象是 yes-designer 设计推进工作流草案，Round 1 初审后经历 4 次修正，Round 5 得到 `STATUS: PASS`，并留下 6 项 MAJOR 与 9 项 MINOR 作为 carry-forward。v5 的 PASS 是 reviewer 结论，不代表 Human 已批准该草案。

| 轮次 | 对象 | 结论 | FATAL | MAJOR | 要点 |
| --- | --- | --- | --- | --- | --- |
| 1 | v1 | FAIL | 4 | 11 | 状态持久化、冻结门禁、降级自判、无设计稿冲突 |
| 2 | v2 | FAIL | 2 | 12 | 部分 FATAL 关闭；有断言不可执行而转 PARTIAL |
| 3 | v3 | FAIL | 2 | 8 | state 进入基线；暴露 inherit 预演循环（新 FATAL） |
| 4 | v4 | FAIL | 1 | 7 | 七层验收、per-state anchor、SSIM 归一 |
| 5 | v5 | PASS | 0 | 6 | 无剩余 FATAL；MAJOR/MINOR 转 carry-forward |

## 对优化 Strict 仍有用的观察

1. **证据与结论匹配是高频失分点**：多轮出现“附录自述已修复，但正文仍是 PARTIAL”。把修复对照表当作独立证据源复核是有效检查。
2. **修正轮会引入新缺陷**：Round 3 的 inherit 预演循环由上一轮 state 修复引入。修正轮做 FULL 复核是必要机制。
3. **判级尺度可校准**：案例中既有流程合同级 FATAL，也有偏实现/工具细节的 MAJOR（如 SSIM 参数、hash 算法）。可用来评估草案阶段应把执行细节压到 MAJOR 还是 FATAL。
4. **收敛速度**：4 次修正从 4 条 FATAL 收到 0 条，但 PASS 时仍留 6 项 MAJOR。可用于评估“最多 4 次修正 + carry-forward 台账”的节奏。
5. 不宜把“v5 必须 PASS”当作唯一成功标准；更有价值的是关键 FATAL 是否在前两轮被捕获、修正后是否被确认关闭、carry-forward 是否如实标注。

后续 v6 删除了 v5 台账所依附的机制，M1–M6 不再适用。这不影响上述对审查过程本身的观察。
