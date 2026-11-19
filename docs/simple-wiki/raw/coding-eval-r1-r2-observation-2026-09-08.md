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
  source_path: docs/simple-wiki/raw/coding-eval-r1-r2-observation-2026-09-08.md
---

# Coding 评估 R1 观察与 R2 边界（2026-09-08）

## R1 已验证结论

本条目中的 R1 指 `coding-ledger-run-1`，不与历史 yes-subagents v0.5.x 评估中的 R1/R2 混用。

当前报告显示，coding workflow 的流程合规性基本成立：计划作者 self-review、fresh `critic-strict`、Step 2 新线程及上下文隔离均有证据；薄计划由施工 Orchestrator 自己完成并使用独立持久 gate；厚计划按 Milestone 各派一次 `coder-plus`，不把内部 Task 扁平直派，并在多个 Milestone 间复用同一 gate；计划级 `pruner -> scout` 只运行一次。流程硬检查为 37/38 通过，唯一失败由厚计划 `period_end` 的可见计划与隐藏 oracle 口径冲突传导，不是派遣路由错误。

证据：`/Users/teatao/Projects/yes-subagents-eval/coding-ledger-run-1/host/REPORT.md` 的流程检查、业务核验和成本章节；薄计划测试 `Ran 17 tests / OK`，厚计划测试 `Ran 61 tests / OK`。

## 完成质量边界

流程 PASS 不等于完成质量已被充分覆盖。R1 的厚计划测试没有覆盖“账本路径不存在时 CLI 是否仍输出 `error:`”和固定宽度 `YYYY-MM-DD` 的负例；这类观察应区分为实现质量探针或评估包缺口，不直接改判 workflow 合规性。薄计划仍保留两个已在批准计划中披露的产品债：真实导入跳过坏行且两键输出不携带 `rejected`，以及 README 的能力清单发生漂移。

## R2 建议范围

R2 先优化评估包，不同时修改 skill。修订内容包括：对齐 `period_end` 的可见 Decision、实施计划和 oracle；补充错误路径与严格日期格式探针；将流程合规、业务正确性、完成质量和成本分开报告，并明确补充探针是否属于硬验收。R2 smoke 只确认包修订有效；若要判断派遣形态与 TPVD 稳定性，再对薄、厚 case 各重复 2-3 次。

R2 的结论只用于确认评估包测量有效和当前 workflow 的可重复性。若之后要优化 skill，应冻结 R2 包后单独改变 skill，避免把 fixture 修订和 skill 改动的效果混在一起。

## 用户保留决策

R2 评估包优化与重测暂缓，由用户决定推进时点。当前不因 R1 中的边界探针单独修改 coding、coder-plus、strict 或 gate 合同。
