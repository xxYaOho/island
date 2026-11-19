---
title: yes-subagents 编排模型：职责、组合、调度与飞轮
type: concept
created: 2026-07-22
updated: 2026-11-19
sources: [raw/yes-subagents-2026-07-22-orchestration-design.md, raw/yes-subagents-2026-07-22-orchestration-plan.md, raw/yes-subagents-2026-09-18-snapshot-workflow-plan.md]
topic: yes-subagents 工作流程与严格回合
tags: [subagent, orchestration, flywheel, swarm, snapshot]
status: current
context: 1

# yes-subagents 编排模型：职责、组合、调度与飞轮

本页整理 2026-07-22 已确认的编排模型（[设计](../raw/yes-subagents-2026-07-22-orchestration-design.md)、[计划](../raw/yes-subagents-2026-07-22-orchestration-plan.md)）。它只覆盖当时一轮优化，不是完整 v3。后续施工路径见[《Coding workflow 重构决策》](coding-workflow-redesign-decisions.md)；审查生命周期见[《Plan-Strict 循环收敛决策》](strict-plan-loop-convergence.md)与[《Strict 飞轮四轮上限》](strict-flywheel-four-round-decision.md)。未批准的研究方向见[《新一代模型下的迭代参考》](frontier-model-iteration-reference.md)。

编排用四个独立维度：代理职责（监察、调查、行动）；组合原则（按任务组合，适用于所有任务，不是可选模式）；调度形态（单体、普通并行或蜂群）；推进机制（飞轮）。组合不要求每项任务都使用多个代理。

调度按独立工作单元计数：1 为单体，2–3 为普通并行，至少 4 才考虑蜂群。重试、返工和分批不增加计数。蜂群不绑定 `swarm`：简单同质单元优先用 `swarm`，需要跨文件推理的单元用 `coder`。共享状态应隔离或分批，有依赖则串行，不得为凑阈值强行并行。

飞轮为：产出 → 验证 → 修正 → 再验证 → 停止。先做直接验证，再按剩余风险决定是否派 `critic-strict` 或 `critic-gate`。该设计中的通用飞轮上限是单次最多修正 10 轮；Strict 审查生命周期的轮次以上游专项决策为准，对象不同。直接验证足够时不为流程完整追加监察。`critic-gate` 在已有批准计划时必须使用该计划当前节点，不得改用更宽松的直接任务基线。

## Snapshot workflow（计划中的现场冻结）

2026-09-18 [计划](../raw/yes-subagents-2026-09-18-snapshot-workflow-plan.md)提出：仅在 Human 显式请求后，用临时 index 做 checkpoint commit，并以 `snapshot/<id>` 分支和持久 worktree 冻结现场，写入 `REPORT.md` 与证据索引。checkpoint 不表示工作完成；当前分支与 index 保持不变；目标路径不得覆盖；无法取得的历史证据标为 `UNAVAILABLE`。本收录未验证该 workflow 已出现在 Island 收拢的 skill 正文中。
