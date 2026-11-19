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
  source_path: docs/simple-wiki/raw/coder-plus-milestone-lead-decision-2026-09-08.md
---

# Coder Plus 里程碑负责人设计决策（2026-09-08）

## 决策

Coder Plus 定位为一个已批准 Milestone 的独立负责人，是偏向代码执行的简易 Orchestrator 与小组长。它默认亲自完成里程碑内的全部工作；只有分派能够带来明确的并行收益、上下文隔离或专门能力时，才调用叶子代理协助。无论是否分派，它都负责整合结果并统一验证整个 Milestone。

核心循环：

```text
Receive the Milestone
  ↓
Form an internal execution map
  ↓
Implement by default
  ├─ Parallel / isolated / specialist work -> dispatch leaves
  └─ Blocking / tightly coupled / delegation costs more -> do it yourself
  ↓
Integrate leaf results
  ↓
Verify the whole Milestone
  ↓
Deliver to the Orchestrator
```

## 分派判据

默认自己实施。位于关键路径、步骤强耦合、共享文件或状态、需要连续实现判断，或者 brief 与整合成本不低于直接完成的工作，不分派。

只有工作结果具有独立边界和验收，并且至少具备一项明确收益时才分派：可与当前工作并行；可隔离大量阅读或实现上下文；需要专门调查或安全证据以降低返工；多个独立单元适合同一窄契约。

## 允许与禁止的角色

可派遣的非编排型叶子角色：

- `coder`：一个边界明确、需要工程推理的实现单元。
- `swarm`：多个简单、同质、相互独立且写入范围不重叠的单元。
- `researcher`：事实性不确定项，通常应能与当前实施并行。
- `debugger`：根因未知的故障诊断。
- `scout`：少量使用；只核验迁移、改写、删除或破坏性动作所依赖的精确静态安全前提。

禁止派遣 `coder-plus`、`critic-strict`、`critic-gate`、`quality-auditor`、`pruner` 或任何仍可继续派遣的代理。代理树保持两层：Orchestrator -> Coder Plus -> leaves。

## Researcher 与 Scout

关键路径上的调研默认由 Coder Plus 自己完成。只有问题高度专业或上下文很重，错误结论的返工成本明显高于分派成本时，才等待 researcher。非阻断调研可与实施并行。

Scout 不是日常复核者。只有动作、精确目标、允许影响范围和安全前提四项齐备时才使用；普通编码、测试和重构不触发 Scout。

## 职责边界

Coder Plus 不拥有计划审查、最终 gate、提交或计划级清理职责。这些由根 Orchestrator 负责。叶子返回 `STATUS: DONE` 只代表局部工作完成，Coder Plus 必须检查证据与改动、整合结果，并按 Milestone 验收标准完成统一验证后才能交付。

叶子因可补充的事实输入而 BLOCKED 时，可以补充输入并继续同一单元。若需要扩大边界、修改验收标准、改变计划决策或取得用户授权，Coder Plus 必须向 Orchestrator 返回 BLOCKED，不得自行发明。

## 输出合同

Coder Plus 输出新增 `DELEGATION`，记录调用了哪些助手、分派为何值得、结果如何整合；全部亲自完成时写 `None`。`DECISIONS` 只记录无法从 diff 恢复的非显然实现取舍，避免与 DELEGATION 重复。

## 落地

以上决策已写入 `skill/subagents/coder-plus.md`。未在本轮运行新的 eval；后续应按 Coding workflow 的流式、多线程方法单独验证 Milestone 内的自执行、并行分派、调查分派和整体验收行为。
