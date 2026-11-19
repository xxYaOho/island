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
  source_path: docs/simple-wiki/raw/coding-workflow-thin-plan-execution-correction-2026-09-08.md
---

# Coding workflow 薄计划执行纠正（2026-09-08）

## 纠正

本决定覆盖 2026-09-08 早先材料中的“薄计划 Task -> coder”映射。

- 薄计划只有一条连贯的实施路径，可作为一个整体直接验收，不需要 Milestone 协调内部单元。
- 薄计划由 Orchestrator 自己实施，不派 `coder`，也不为分派而人为拆成 Task。
- Orchestrator 完成实施与直接验证后，将整个薄计划交给独立 `critic-gate`；同一 reviewer 持续处理 FAIL 修正与补证。
- 厚计划仍按 Milestone 首层派遣 `coder-plus`；`coder` 只作为 Coder Plus 的可选叶子，或用于其他 workflow 的单工作单元。

`researcher` 不是 coding workflow 的必经角色，也不应成为评估通过条件。Coder Plus 仅在非阻断调研可与实施并行，或专门调查的收益明确高于分派与整合成本时，选择性使用 researcher；关键路径调研默认自行完成。

以上决定已经写入 `skill/workflow/coding.md`。旧 raw 正文保留，用本纠正文档表达取代关系。
