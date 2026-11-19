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
  source_path: docs/simple-wiki/raw/coding-workflow-plan-consumer-implementation-2026-09-08.md
---

# Coding workflow 计划消费实现合同（2026-09-08）

## 定位

`skill/workflow/coding.md` 已重写为计划消费与施工编排器。它不生产计划，也不重复 `SKILL.md` 的组合、飞轮、待机与完成机制；计划生产与结构修正交给 `go-spec`。

## 施工入口

开工前必须取得完整计划、作者 self-review、作者之外 fresh `critic-strict` 的 PASS，以及用户的实施授权。strict 对薄、厚计划一视同仁。施工线程只接收批准计划、PASS 凭证和未阻断事项，不继承计划作者或 strict 的完整 transcript，也不重复计划审查。

## 厚薄与首层派遣

厚薄表示施工结构，不表示代码规模，也不决定是否需要 strict：

- 薄计划由没有里程碑级内部依赖的 Task 组成；Orchestrator 将每个 Task 首层派给 `coder`。
- 厚计划包含 Milestone；Orchestrator 每个 Milestone 只派遣一次 `coder-plus`，不将其内部 Task 扁平直派。
- 风险、迁移、新颖性与验证难度只影响 gate 的核验重点，不改变 Task/Milestone 映射。

每次派遣只交付当前节点。Task 施工包包含目标与实施内容、验收标准、可动文件范围、依赖、约束和下游接口承诺；Milestone 使用 `go-spec` 的 `Milestone-<n>.md` 切片或等价内容。后续节点和历史 transcript 不进入执行者上下文。

## Coder Plus 与 Gate

Coder Plus 默认亲自完成整个 Milestone，只在并行、上下文隔离或专门能力收益明确时分派叶子；Orchestrator 不干预内部 Task 分派，也不为叶子增加独立 gate。

一个批准计划只建立一个 gate reviewer，并跨全部节点、FAIL 修正与补证轮次持续复用：全部节点由子代理实施时由 Orchestrator 兼任；Orchestrator 将亲自实施任一节点时，从计划开始创建一个独立 `critic-gate` 并持续复用。实施者只负责 self-verification，不能作最终 gate。

局部实施问题交回原执行者，并尽量延续原执行会话；同一 gate reviewer 复核。若需要修改目标、范围、验收、设计或 Milestone 边界，则停止施工，回到 `go-spec`，重新取得 fresh strict PASS，并重建 gate 生命周期。

## 收尾与提交

执行者不创建提交。节点 PASS 后是否提交及提交粒度，由 Orchestrator 按用户授权和仓库规则决定。

只有完整计划的全部实施节点 PASS 后，才运行一次 `pruner -> scout`；评估只观察前一至两个 Milestone 时不触发计划级收尾。Pruner 只执行 Scout 判定为 SAFE 的目标，随后直接验证，不再回到 critic-gate。

## 验证

`coding.md` 已检查不存在旧版的计划审查阈值、节点标注、性质轴与 B+ 缓解降级残留；其引用的 Coder、Coder Plus、Critic Gate 与 Pruner 输出字段均与现行子代理合同一致。`git diff --check -- skill/workflow/coding.md` 通过。本轮未运行行为 eval。
