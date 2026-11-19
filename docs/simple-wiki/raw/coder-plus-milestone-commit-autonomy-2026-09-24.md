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
  source_path: docs/simple-wiki/raw/coder-plus-milestone-commit-autonomy-2026-09-24.md
---

# Coder Plus Milestone 内提交自治决策（2026-09-24）

## 背景

现行 coding workflow 禁止 Coder Plus 创建提交，要求节点 gate PASS 后再由 Orchestrator 决定是否提交。实际 Milestone 经常包含多个跨层、厚重 Task；全部成果在 gate 前长期停留于工作区，会失去持续恢复点，扩大 diff，并提高故障定位与局部回退成本。

讨论确认：commit 是施工持久化检查点，不是 gate 验收凭证。没有提交时 gate 也能审查 Milestone；存在多个提交时，gate 的审查对象仍是批准基线下整个 Milestone 的最终实现，提交拓扑不改变判定对象。

## 决策

1. Coder Plus 拥有当前 Milestone 内的原子提交自治权。它根据逻辑完整性决定提交粒度，不强制一个 Task 恰好对应一个 commit；较重 Task 可以拆成多个提交。
2. 叶子代理不创建提交。Coder Plus 检查叶子证据与改动，完成整合和相关自验证后统一提交。
3. commit 只表示对应施工单元已经持久化、整合并自验证，不表示 Milestone 已通过 gate。
4. gate 审查整个 Milestone 的最终实现、验证证据、偏差和下游承诺，不以提交数量或拓扑作为 PASS 条件。
5. gate 开始后冻结受审历史。FAIL 时将阻断项交回原 Coder Plus，以追加提交修复并交同一 reviewer 复核；不改写已经审查的提交。
6. gate PASS 后，Orchestrator 推进下一 Milestone 或计划级收尾，不要求再创建一个包装或标记提交。Orchestrator 只有在自己实际产生改动时才提交。
7. Coder Plus 不拥有计划审查、最终 gate、计划级清理或默认远程推送职责。提交只能包含当前 Milestone 拥有的变化，不得混入用户或其它工作单元的改动。
8. Git 的共享工作区、历史整理和远程操作策略属于 workflow 与派遣上下文；运行时内置角色若禁止本合同要求的本地提交能力，应改用可写通用代理注入完整 Coder Plus 合同，不得静默降级。

## 职责分层

- `workflow/coding.md`：定义提交何时允许、gate 前后历史状态、FAIL/PASS 流转和计划级收尾。
- `subagents/coder-plus.md`：定义 Milestone 内实施、叶子整合、自验证和原子提交自治。
- Orchestrator：提供边界与 Git 环境事实，执行 gate 和节点状态转换。
- Gate reviewer：只裁决 Milestone 是否符合批准基线，不接管提交职责。

## 验证要求

- Coder Plus 输出列出其创建的提交及任何剩余未提交变化。
- 评估必须区分叶子提交与 Coder Plus 提交：前者禁止，后者是厚计划施工职责。
- 评估不得再要求 gate PASS 后由 Orchestrator 机械创建 Milestone 提交。
