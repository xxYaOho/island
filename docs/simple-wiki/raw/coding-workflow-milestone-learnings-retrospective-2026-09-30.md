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
  source_path: docs/simple-wiki/raw/coding-workflow-milestone-learnings-retrospective-2026-09-30.md
---

# Coding workflow Milestone 学习反馈与计划复盘决策（2026-09-30）

## 背景

当具体开发由 Coder Plus 承接时，Orchestrator 只拥有施工包和交付摘要，不一定知道实施过程中形成的局部事实、验证认识或项目约定候选。若只依赖 diff、验证结果和固定输出节，这些信息可能在 Milestone 交接时丢失。

## 决策

1. Coder Plus 输出增加可选 `LEARNINGS` 节。只有存在可能影响后续判断、值得复用或可能形成项目约定的观察时才填写；没有时写 `None`，不得为满足格式制造洞见。
2. 每条 `LEARNINGS` 先给一句话结论，再给简短背景、证据和适用范围。它是候选输入，不自动改变计划、验收标准或项目规则。
3. Orchestrator 在 Milestone 交接时暂存候选，在后续 Milestone 有新证据时合并、修正或撤销；`LEARNINGS` 不影响 `STATUS: DONE` 或 gate 判定。
4. 全部节点通过、计划级清理和最终验证完成后，Orchestrator 主动与 Human 做简短复盘：先展示一句话结论，再补一段说明。没有候选时也明确说明没有新的可复用认识。
5. 只有 Human 确认且具有长期复用价值的内容才按 `raw -> wiki` 收录；未确认、争议或仅适用于本次工作的观察不写入 wiki。

## 适用边界

该机制记录的是从实施中产生、且可能影响未来工作的认识，不替代 `DEVIATIONS`、`DECISIONS`、`VERIFICATION` 或 `ESCALATE`。结构性变更仍按原 workflow 回流 `go-spec` 和 strict；一次性施工日志仍不进入 Simple Wiki。
