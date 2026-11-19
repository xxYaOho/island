# INDEX

> [!IMPORTANT]
> Headline 2 为主题聚类, 无主题内容默认放在 Headline 1 中. 同主题条目达到 3 条时, 为它们创建独立主题.
> 每页一行, 先查阅编译后的知识, 按需查阅源材料:
> `- [title](<file>.md) | <context>k | <一句话描述> | tag, tag`

## yes-subagents 工作流程与严格回合

- [编排者轮询导致上下文暴涨](orchestrator-polling-context-bloat.md) | 2k | 后台子代理等待期轮询会烧掉大量 token；应在回合结束时不终止任务，由完成通知触发下一环 | subagent, context-bloat
- [多代理运行的费用核算与价值基准](multi-agent-run-cost-accounting.md) | 2k | 账单按 turns × 平均上下文核算，须含全部嵌套会话，并以 VD、TPVD、CPVD、CPTK 区分效率与价格构成 | subagent, cost, pricing
- [Coding workflow 重构决策](coding-workflow-redesign-decisions.md) | 4k | coding 消费已批准计划并编排施工：Coder Plus 在 Milestone 内整合叶子并做原子提交，以 start/delivery HEAD 和 owned-clean 状态稳定 gate | subagent, coding, workflow
- [Coding 评估 R1 观察与 R2 边界](coding-eval-r1-r2-observation.md) | 1k | R1 证明主要流程合规但暴露质量探针与 oracle 缺口；R2 应先修评估包并暂缓 skill 变更 | subagent, coding, eval
- [增量复审契约的 fresh-agent 盲区](delta-review-fresh-agent-blindspot.md) | 2k | 增量复审只在修复为局部编辑时安全；结构性返工须以骨架字段触发器回落全量重审 | review, contract
- [Strict 飞轮四轮上限与生命周期重启决策](strict-flywheel-four-round-decision.md) | 1k | 一次生命周期为 1 次初审加最多 4 次修正；停滞早停，耗尽后须用户授权且工件有实质变化才用 fresh reviewer 重启 | review, strict, flywheel
- [Plan-Strict 循环收敛决策](strict-plan-loop-convergence.md) | 2k | 判级锚、分诊、修复预算与计划准入，并纳入审查强度分档与 MAJOR 台账闭环 | review, strict, intensity, convergence
- [yes-subagents 编排模型：职责、组合、调度与飞轮](yes-subagents-orchestration-model.md) | 1k | 2026-07 已确认的四维编排模型，并附 Snapshot 现场冻结计划；施工与审查合同以后续专项决策为准 | subagent, orchestration, snapshot
- [新一代模型下的 yes-subagents 迭代参考](frontier-model-iteration-reference.md) | 1k | 研究笔记：强模型上应将 skill 收为薄型治理层；不是已批准规格，也尚未验证增量收益 | subagent, research, governance
- [critic-strict 案例观察（yes-designer 工作环）](critic-strict-yes-designer-case.md) | 1k | 完整五轮 Strict 生命周期样本：修正轮会引入新缺陷，证据—结论匹配是高频失分点，v5 PASS 仍带 carry-forward MAJOR | strict, eval, yes-designer

## go-spec 分层与计划创建

- [计划创建 A/B 评估：go-spec 0.4 vs writing-plans](plan-creation-ab-eval.md) | 2k | 2026-09-07 阶段评估：B 一次过闸，A 被 strict 逼回，价值密度 B 约优 3.4 倍 | eval, go-spec, writing-plans
- [Executor 施工冒烟：M1 段 A/B 对照](executor-smoke-m1-ab.md) | 2k | 计划创建评估的施工段实证：B 零追问、自决假设全留痕，官方峰价分档口径下全管线更便宜 | eval, executor
- [渐进长厚与修复验证 eval（v0.2 → v0.3.0）](layered-growth-eval.md) | 1k | 升层门控过松与来源不可辨析的修复判例；修复验证证据是失义信号重获意义 | eval, 升层纪律, 来源档位
- [分层停点与需求重构](layered-stops-requirement-reframing.md) | 1k | 错误发现层决定返工半径；澄清导向决定需求重构；信息获取时机决定设计完整性 | grill, 停点, 需求重构
- [假设账本来源失实与三档标注](assumption-ledger-source-falsification.md) | 1k | 「未问记成未表态」失败模式；来源档位轻量版已在 0.3.0 验证，全量三档仍候选 | 假设账本, 来源失实
- [执行层详细度定位：高档位只写高维度承诺](execution-layer-detail-level.md) | 1k | 计划者只产出目标、验收、边界与契约，TDD 与微观设计下放执行者 | executor, 承诺立场

## yes-designer 设计工作环

- [yes-designer 设计推进工作流](yes-designer-design-work-loop.md) | 2k | 已批准的 v6 方向：copy commit 与结构门禁；附未批准的 DESIGN.md 草案和 P1 有限可用、门禁仍应 advisory 的结论 | yes-designer, work-loop, P1
- [yes-designer 工作环演进（v1–v6）](yes-designer-work-loop-evolution.md) | 1k | v1–v5 已被 v6 取代；designer 笔记与 1018 快照近乎全文相同，只在状态行上有后注差异 | yes-designer, evolution, superseded

## yes-swiki 契约

- [yes-swiki v0.6 契约重设计](yes-swiki-contract-redesign.md) | 1k | INGEST/READ/MAINTAIN 路由，编译与接线拆分，ingested/integrated 状态机；并收录 librarian/curator 拆分评测的契约前提 | yes-swiki, ingest, schema

## yes-handoff

- [ce-handoff 与 yes-handoff 的定位取舍](ce-vs-yes-handoff-review.md) | 1k | 二者不是替代关系：yes-handoff 管仓库内项目状态，建议吸收 ce-handoff 的安全 resume 边界 | handoff, resume

## go-trail 评估

- [go-trail 评估迭代（原 go-fireside）](go-trail-eval-iterations.md) | 1k | 三轮已验证评估：增量在程序性交接合同，不在对话风格；v0.1.2 验证了安全确认与反事实禁令 | go-trail, eval

## Island 方向

- [将 role 创建独立为可被引用的能力](island-role-creation-space.md) | 1k | 把 role spec 的创建放到独立能力中供其它 skill 引用；Island 中由 skills/recruit/ 承担 | island, recruit, role-spec
