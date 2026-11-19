---
title: Coding workflow 重构决策
type: decision
created: 2026-09-08
updated: 2026-09-30
sources: [raw/coding-workflow-redesign-discussion-2026-09-08.md, raw/coder-plus-milestone-lead-decision-2026-09-08.md, raw/coding-workflow-plan-consumer-implementation-2026-09-08.md, raw/coding-workflow-thin-plan-execution-correction-2026-09-08.md, raw/coder-plus-milestone-commit-autonomy-2026-09-24.md, raw/coder-plus-gate-handoff-stability-2026-09-24.md, raw/coding-workflow-milestone-learnings-retrospective-2026-09-30.md]
topic: yes-subagents 工作流程与严格回合
tags: [subagent, orchestration, coding, workflow, evaluation]
status: current
context: 4
---

# Coding workflow 重构决策

本页记录 2026-09-08 起逐步落地的 coding workflow 合同。`workflow/coding.md` 是计划消费与施工编排器：它消费已批准计划，选择施工协作形态，推进计划级 gate 与收尾；计划生产和结构修正由 `go-spec` 负责。完整背景见[《Coding workflow 重构讨论纪要》](../raw/coding-workflow-redesign-discussion-2026-09-08.md)，Coder Plus 合同见[《Coder Plus 里程碑负责人设计决策》](../raw/coder-plus-milestone-lead-decision-2026-09-08.md)，施工消费合同见[《Coding workflow 计划消费实现合同》](../raw/coding-workflow-plan-consumer-implementation-2026-09-08.md)，提交职责的后续修订见[《Coder Plus Milestone 内提交自治决策》](../raw/coder-plus-milestone-commit-autonomy-2026-09-24.md)，gate 交接边界见[《Coder Plus gate handoff 稳定性补充决策》](../raw/coder-plus-gate-handoff-stability-2026-09-24.md)。

## 职责边界

- `SKILL.md` 保留角色、组合、飞轮、待机、监察与完成条件等编排原语和全局原则。
- `go-spec` 生产并维护决策层、Draft、Implement Plan、Milestone 及派生切片；发现结构性偏差时接收回流并重新定稿。
- `workflow/coding.md` 消费已批准计划，判断薄厚实施层，选择施工协作形态，推进 gate、偏差分流和计划级收尾。
- `subagents/*.md` 定义各角色收到任务后的内部执行契约。

coding 不重复通用飞轮、最大轮次、等待机制、计划生产过程或子代理完整契约。

## 流式多线程评估

Step 是评估阶段，不等于线程。计划作者 self-review、fresh strict、施工 Orchestrator、执行者和 gate reviewer 分属不同上下文，评估重点是职责分离和工件传递。薄、厚计划分别进入以下流水线：

```text
P-thin  -> 通过审查的薄计划  -> E-thin
P-thick -> 通过审查的厚计划  -> E-thick-M1 -> E-thick-M2（可选）
```

self-review 只检查完整性、一致性和格式，不替代独立 critique；strict 对两种计划都交给 fresh-agent。Step 1 只向 Step 2 交付批准计划、PASS 凭证和未阻断事项，不传完整 transcript；Step 2 不重复 strict，只观察实施、自执行、分派和 gate。厚实施默认只跑一个 Milestone，只有需要观察跨节点流转时才增加第二个。稳定回归使用冻结的已批准计划，动态接力只承担集成观察。

## 计划消费与施工入口

开工必须取得完整计划、作者 self-review、作者之外 fresh `critic-strict` 的 PASS，以及用户的实施授权。施工线程只接收批准计划、PASS 凭证和未阻断事项，不继承计划作者或 strict 的完整 transcript，也不重复计划审查。

计划结构决定实施方式：薄计划只有一条连贯的实施路径，可作为整体直接验收，由 Orchestrator 自行实施，不人为拆成 Task 或派遣 `coder`；厚计划包含 Milestone，Orchestrator 每个 Milestone 只派遣一次 `coder-plus`，不把其内部 Task 扁平直派。Milestone 边界不自动等于 Coder Plus 的 fresh session 边界；当前节点 PASS 后，Orchestrator 依据上下文收益在 `fresh` 与 `retain` 之间做一次明确决策。`retain` 只适用于下一节点明显依赖难以压缩的大量运行时、设计或宿主上下文，并须记录理由、保留范围和新的节点边界；无明显收益时使用 `fresh`。无论选择哪条路径，Milestone 仍保持独立施工包、提交和 gate 边界。风险、迁移、新颖性和验证难度只改变 gate 的核验重点，不替代薄厚计划的结构判断。该薄计划规则取代早先材料中的 Task→coder 映射（[Coding workflow 薄计划执行纠正](../raw/coding-workflow-thin-plan-execution-correction-2026-09-08.md)）。

每次派遣只交付当前节点。Task 的最小施工包包含目标与实施内容、验收标准、可动文件范围、依赖、约束和下游接口承诺；Milestone 使用 `go-spec` 的 `Milestone-<n>.md` 切片或等价内容。后续节点和历史 transcript 不进入执行者上下文。

Orchestrator 在派遣 Milestone 前记录开工 `HEAD`、staged / unstaged / untracked 状态及已知归属，作为施工包的 Git 基线。可动文件已有他人改动时，只有在归属和 staging 能可靠隔离的前提下才能继续；同一文件的变化无法隔离或归属无法证明时，Coder Plus 返回 `STATUS: BLOCKED`。

## Coder Plus 里程碑负责人

`coder-plus` 是已批准 Milestone 的独立负责人，偏向代码执行的简易 Orchestrator。它默认亲自完成里程碑内全部工作；只有分派能带来明确的并行收益、上下文隔离或专门能力时，才调用叶子代理。无论是否分派，它都负责整合结果并统一验证整个 Milestone。

允许的非编排型叶子角色包括：边界明确的 `coder`；多个简单、同质且不重叠单元的 `swarm`；事实性不确定项的 `researcher`；根因未知故障的 `debugger`；仅用于核验迁移、改写、删除或破坏性动作静态安全前提的 `scout`。禁止派遣 `coder-plus`、`critic-strict`、`critic-gate`、`quality-auditor`、`pruner` 或任何仍可继续派遣的代理，代理树保持两层：Orchestrator -> Coder Plus -> leaves。

关键路径、强耦合、共享文件或状态、需要连续判断，或简报与整合成本不低于直接完成的工作，默认不分派。叶子返回 `STATUS: DONE` 只代表局部完成；Coder Plus 必须核对证据与改动，完成 Milestone 验收后再交付。可补充事实输入的 BLOCKED 可在同一单元补充后继续；若需扩大边界、修改验收标准、改变计划决策或取得用户授权，必须向 Orchestrator 返回 BLOCKED。

Coder Plus 输出必须包含 `DELEGATION`：记录助手、分派收益和整合结果；全部亲自完成时写 `None`。`DECISIONS` 只记录无法从 diff 恢复的非显然取舍。它不负责计划审查、最终 gate 或计划级清理，但拥有当前 Milestone 内的原子提交自治权；提交粒度按逻辑完整性决定，不强制一个 Task 恰好对应一个 commit。较重 Task 可以拆成多个提交，每个提交只能包含当前 Milestone 拥有、已经整合并完成相关自验证的变化。

Coder Plus 可在交付中增加 `LEARNINGS`，反馈可能影响后续判断、值得复用或可能形成项目约定的观察；没有时写 `None`，不得为满足格式制造洞见。每条先给一句话结论，再给背景、证据和适用范围。Orchestrator 在 Milestone 交接时暂存候选，后续有新证据时合并、修正或撤销；候选不影响 `STATUS: DONE` 或 gate 判定。

叶子代理不创建提交。Coder Plus 检查叶子证据与改动、完成整合和相关自验证后统一提交，并在输出中列出其创建的提交和任何剩余未提交变化。`STATUS: DONE` 要求所有 Milestone-owned 改动均已提交，剩余 owned staged / unstaged / untracked 状态为 `None`；已有提交后转为 BLOCKED 时保留这些恢复点，并报告已完成提交、未提交状态和剩余边界。commit 是施工持久化与恢复点，不是 gate 的验收凭证，也不授予默认远程推送职责。此前“Coder Plus 不提交”的合同已由[提交自治决策](../raw/coder-plus-milestone-commit-autonomy-2026-09-24.md)明确取代。

## 计划级 Gate 与偏差

一个批准计划只建立一个持久 gate reviewer，跨全部节点、FAIL 修正和补证轮次复用同一 reviewer。子代理实施时由 Orchestrator 兼任；Orchestrator 自行实施任一节点时，从计划开始创建独立 `critic-gate` 并持续复用。实施者可 self-verify，但不能作最终 gate。

gate 审查的是批准基线下整个 Milestone 的最终实现、验证证据、偏差和下游承诺；提交数量与拓扑不改变审查对象，也不构成 PASS 条件。稳定的 gate handoff 由开工 `HEAD`、交付 `HEAD`、两者之间的提交、干净的 Milestone-owned 状态以及未变化的既有外部改动共同界定。Milestone 进入 gate 后冻结受审 `HEAD` 与历史。局部实施问题交回原执行者并尽量延续原会话，由 Coder Plus 追加修复提交，再交同一 gate reviewer 复核，不改写已经审查的提交。若出现结构性偏差，或需要修改目标、范围、验收、设计或 Milestone 边界，则停止施工并回到 `go-spec`，重新取得 fresh strict PASS，同时重建 gate 生命周期。计划结构性变更、reviewer 不可用或上下文失真时也重建 gate。

## 计划级收尾与提交

完整计划的全部实施节点 gate PASS 后，才运行一次 `pruner -> scout`；评估只观察前一至两个 Milestone 时不触发计划级收尾。Pruner 只处理 Scout 判定为 SAFE 的目标，随后直接验证并完成收束，不在每个 Milestone 后重复运行。

旧合同曾规定执行者不创建提交、节点 PASS 后由 Orchestrator 决定是否提交；该规则已被[《Coder Plus Milestone 内提交自治决策》](../raw/coder-plus-milestone-commit-autonomy-2026-09-24.md)取代。Coder Plus 在 gate 前为 Milestone 内施工创建原子提交；gate PASS 后，Orchestrator 推进下一 Milestone 或计划级收尾，不要求再创建包装或标记提交。Orchestrator 只在自己实际产生改动时提交。

共享工作区、历史整理和远程操作策略由 workflow 与派遣上下文明确。Coder Plus 不得把用户或其他工作单元的变化混入提交；运行时内置角色若禁止本合同要求的本地提交能力，应使用可写通用代理注入完整 Coder Plus 合同，不得静默降级。

全部节点通过、计划级清理和最终验证完成后，Orchestrator 主动与 Human 做简短复盘：每条先展示一句话结论，再补一段背景、证据和适用范围。只有 Human 确认且具有长期复用价值的内容才按 `raw -> wiki` 收录；未确认、争议或一次性观察不写入 wiki。

## 当前验证边界

2026-09-24 本轮结论只覆盖合同与评估包的静态验证，没有运行完整多代理行为 eval。运行时 fallback、叶子零提交、无 push、Milestone-owned clean handoff 与 gate 后历史冻结仍需独立行为评估证明，不得把静态检查写成运行时已验证。

## 关联

- [多代理运行的费用核算与价值基准](multi-agent-run-cost-accounting.md) —— 计划级流水线和嵌套派遣的效率评估，应按 TPVD、CPVD、CPTK 的全会话核算口径观察。
- [yes-subagents 编排模型](yes-subagents-orchestration-model.md) —— 更早的职责、组合、调度与飞轮框架。
