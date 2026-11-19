---
class: material
ingested: true
integrated: true
metadata:
  class: material
  ingested: true
  integrated: true
  metadata: ~
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/simple-wiki/raw/coder-plus-gate-handoff-stability-2026-09-24.md
---

# Coder Plus gate handoff 稳定性补充决策（2026-09-24）

## 背景

Coder Plus 获得 Milestone 内提交自治后，单纯冻结“提交历史”仍不足以稳定 gate 对象：若交付时残留 Milestone-owned staged、unstaged 或 untracked 改动，reviewer 实际看到的工作区仍可能漂移。脏工作区中若未记录开工状态和归属，同一路径的用户改动也可能被误纳入提交。

## 决策

1. Orchestrator 派遣 Milestone 前记录开工 `HEAD`、staged / unstaged / untracked 状态及已知归属，并将其作为施工包的 Git 基线。
2. 可动文件内已有他人改动时，只有在归属和 staging 能够可靠隔离的前提下才能继续；无法证明时 Coder Plus 返回 `STATUS: BLOCKED`。
3. Coder Plus 的 `STATUS: DONE` 要求所有 Milestone-owned 改动已经提交，剩余 owned staged / unstaged / untracked 状态为 `None`。
4. 稳定 gate handoff 由开工 `HEAD`、交付 `HEAD`、两者之间的提交、干净的 Milestone-owned 状态以及未变化的既有外部改动共同界定。
5. 交付 gate 后冻结受审 `HEAD` 与历史。gate FAIL 后以追加提交修复，不改写 reviewer 已见提交。
6. Coder Plus 在已有提交后 BLOCKED 时保留这些恢复点，报告已完成提交、未提交状态和剩余边界；Orchestrator 不推进下游。
7. 运行时内置角色无法提交时，替代通用代理必须具备完整读写、命令和叶子分派能力；没有合格代理时 BLOCKED，不继续静默降级。

## 验证边界

本轮更新合同和评估包，但不运行完整多代理行为 eval。运行时 fallback、叶子零提交、无 push、owned-clean handoff 与 gate 后历史冻结仍需独立 eval 证明；不得把静态检查写成运行时已验证。
