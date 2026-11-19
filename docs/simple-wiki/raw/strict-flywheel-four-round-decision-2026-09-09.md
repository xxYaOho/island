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
  source_path: docs/simple-wiki/raw/strict-flywheel-four-round-decision-2026-09-09.md
---

# Strict 飞轮四轮上限与生命周期重启决策

> 2026-09-09 · yes-subagents v0.5.5

## 决策

Strict 一次审查生命周期包含 1 次初始审查和最多 4 次修正审查。初始产出、蜂群分批和代理重试不计入修正轮次。初始审查必须由与作者分离的 fresh reviewer 完成；同一生命周期内的所有修正轮复用该 reviewer，局部修正用 `DELTA`，结构性修正用 `FULL`。

出现以下任一情况时提前停止：同一实质 FATAL 连续两次修正未缩小；或连续两次修正在遗留 FATAL 未清除时引入新的 FATAL。达到上限或早停后，Orchestrator 必须汇报未收敛根因，不得自行更换 reviewer 或继续审查。

只有用户明确授权，且工件有实质修订、出现新证据或获得用户裁决，才能开启新生命周期。新生命周期使用 fresh reviewer、Round 1、`FULL`，并传入完整当前工件、未解决 FATAL 台账和上一生命周期摘要。原稿不变时禁止更换 reviewer 寻求 PASS。

## 原因

四轮上限控制审查成本，同时保留对常见 3–4 轮收敛路径的覆盖。停滞早停避免重复消耗；受控重启保留 fresh 视角，但防止无变化换 reviewer 导致 reviewer shopping。Reviewer 复用的边界是生命周期，而不是某个 FATAL 是否“看起来相同”。
