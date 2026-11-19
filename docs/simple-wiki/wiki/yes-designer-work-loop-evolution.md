---
title: yes-designer 工作环演进（v1–v6）
type: summary
created: 2026-10-18
updated: 2026-11-19
sources: [raw/yes-designer-design-work-loop-v1.md, raw/yes-designer-design-work-loop-v2.md, raw/yes-designer-design-work-loop-v3.md, raw/yes-designer-design-work-loop-v4.md, raw/yes-designer-design-work-loop-v5.md, raw/yes-designer-design-work-loop-v6.md, raw/yes-subagents-1018-design-work-loop-v1.md, raw/yes-subagents-1018-design-work-loop-v2.md, raw/yes-subagents-1018-design-work-loop-v3.md, raw/yes-subagents-1018-design-work-loop-v4.md, raw/yes-subagents-1018-design-work-loop-v5.md, raw/yes-subagents-1018-readme.md, raw/yes-designer-2026-10-18-critic-strict-major-ledger.md, raw/yes-subagents-1018-critic-strict-major-ledger.md, raw/yes-designer-2026-10-16-design-collaboration-architecture.md, raw/yes-designer-2026-10-17-sketch-copilot-plus-adapter-boundary.md, raw/yes-designer-2026-10-18-v2-critic-round2.md]
topic: yes-designer 设计工作环
tags: [yes-designer, work-loop, superseded, evolution]
status: current
context: 1

# yes-designer 工作环演进（v1–v6）

当前有效合同是 [v6](../raw/yes-designer-design-work-loop-v6.md)，编译见[《yes-designer 设计推进工作流》](yes-designer-design-work-loop.md)。v1 至 v5 已被 v6 明确取代，旧论断保留供溯源，不作为现行合同。Strict 审查过程观察见[《critic-strict 案例观察》](critic-strict-yes-designer-case.md)。

## 材料关系

同一主线同时存在于 skill-designer 笔记和 skill-subagents 的 `1018-strict-case` 快照。正文几乎相同，差异集中在状态行：

- designer 笔记是后注版本：v1–v5 均标明已被 v6 取代；v5 记为 Round 5 PASS，且 MAJOR 台账状态为 `CLOSED`（机制已删除，不再适用）。
- 1018 快照是审查当时的切片：v1–v4 写“已被 v5 取代”；v5 仍写“等待 Round 5”，与同目录 [README](../raw/yes-subagents-1018-readme.md)（v5 已 PASS）以及 designer 后注不一致。这是快照未回写状态行，不是第二套合同。本页以 designer 后注与 README 的审查结论为准，1018 草案正文仅作当时审查对象。

更早的[设计协作讨论](../raw/yes-designer-2026-10-16-design-collaboration-architecture.md)与 [sketch-copilot-plus 适配边界](../raw/yes-designer-2026-10-17-sketch-copilot-plus-adapter-boundary.md)也已被 v6 取代，只作历史背景。

## 演进要点

- v1–v5 的修复方式主要是增加机制（输入 hash、版本目录、多类 oracle、七层验收、waiver、CAS 认领等），文档更自洽，但 v5 仍拦不住“从零重写但视觉等效”的事故 B，因为 `means: copy` 没有派生断言。
- Round 1–5 的审查结论见案例页。v5 PASS 时仍有 6 项 MAJOR 未关闭；这是审查结束状态，不是 Human 对 v5 的批准。
- v6 回到原问题，删除大部分 v5 机制，改用 copy commit、结构门禁（S1–S5，后补 S6 与 `prototype_diff`）和 Human 审批绑定 git blob。v5 台账 M1–M6 依附的机制已删除，不再适用。
- Human 于 2026-10-18 批准 v6 方向，并决定不再对 v6 做 critic-strict 审查。P1 验证与限制见[《yes-designer 设计推进工作流》](yes-designer-design-work-loop.md) 中的 P1 节。
