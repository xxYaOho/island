---
title: Strict 飞轮四轮上限与生命周期重启决策
type: decision
created: 2026-09-09
updated: 2026-09-09
sources: [raw/strict-flywheel-four-round-decision-2026-09-09.md]
topic: yes-subagents 工作流程与严格回合
tags: [review, orchestration, strict, flywheel]
status: current
context: 1
---

# Strict 飞轮四轮上限与生命周期重启决策

一次 Strict 审查生命周期包含 1 次初始审查和最多 4 次修正审查。初始审查使用与作者分离的 fresh reviewer；同一生命周期内的修正轮复用该 reviewer。局部修正使用 `DELTA`，结构性修正使用 `FULL`，但切换模式不会切换生命周期或 reviewer。

同一实质 FATAL 连续两次修正未缩小，或连续两次修正在遗留 FATAL 未清除时引入新的 FATAL，提前停止。达到上限或早停后，Orchestrator 汇报未收敛根因并等待用户决定，不自动换 reviewer。

用户授权且工件发生实质修订、出现新证据或获得用户裁决后，才可开启新生命周期。新生命周期从 fresh reviewer、Round 1、`FULL` 开始，并提供完整当前工件、未解决 FATAL 台账和上一生命周期摘要。原稿不变时禁止更换 reviewer 寻求 PASS。

关联：[增量复审契约的 fresh-agent 盲区](delta-review-fresh-agent-blindspot.md)

## 关联

- [Strict 审查强度与严重度判级](strict-plan-loop-convergence.md) —— 强度分档与 MAJOR 台账。
- [critic-strict 案例观察（yes-designer 工作环）](critic-strict-yes-designer-case.md) —— 四轮修正加 carry-forward 的完整生命周期样本。
