---
title: 执行层详细度定位：高档位只写高维度承诺
type: decision
created: 2026-09-07
updated: 2026-09-07
sources: [raw/2026-09-07-decision-execution-layer-detail-level.md, raw/2026-09-07-plan-creation-eval.md, raw/2026-09-07-executor-smoke-m1.md]
topic: go-spec 分层与计划创建
tags: [executor, 承诺立场, token 经济, go-spec]
status: current
context: 1
---

# 执行层详细度定位：高档位只写高维度承诺

> 杨桃 2026-09-07 拍板。决策、依据与关联均出自[决策：执行层详细度定位——高档位 token 只花在高维度决策上](../raw/2026-09-07-decision-execution-layer-detail-level.md)；背景数据来自 [Eval 报告：go-spec 0.4 vs writing-plans](../raw/2026-09-07-plan-creation-eval.md)。

## 决策

执行层（go-spec 的 Milestone/Task 层）详细度定位：**计划者（高档位）只产出高维度且详细适中的承诺——目标、验收标准、边界、契约；TDD 节奏等简单、偏实时的代码设计下放执行者（sonnet 级）自行完成，不消耗高档位 token。**

## 背景：executor 经济学

[计划创建 A/B 评估](plan-creation-ab-eval.md) 引出两种成本分布：A（writing-plans 手册式，2047 行 / 69% 内嵌代码）把成本前置——计划贵、施工近零判断力需求；B（go-spec 承诺式，430 行 / 7% 契约代码）后置——计划便宜、施工要付微观设计判断。总账优劣取决于执行者档位：haiku 施工时手册式可能反超，sonnet+ 施工时承诺式更低。

## 依据

1. sonnet 级执行者能力足以自行完成 TDD 与微观代码设计，施工能力不构成瓶颈。
2. B 执行层经 fresh-agent（无对话上下文）审定可施工——有目标、有验收标准即够推进。
3. 手册式预付（A 形态）在「高档位计划 + 中档位执行」的目标场景里是错配支出。

## 关联

- 承接 go-spec 决策 14（承诺立场：自足 = 判据完整 + 边界明确 + 上下文指引，非实现预写）：14 定义「不写什么」，本决策定义「详细度锚在哪、为什么」。
- 承诺式计划的已知代价（执行者需要判断力）见[计划创建 A/B 评估](plan-creation-ab-eval.md)判词；施工冒烟已实证本决策（[Executor 施工冒烟：M1 段 A/B 对照](executor-smoke-m1-ab.md)）：B 零追问、12 条微观自决与「高档位只出高维度承诺」定位精确吻合，官方峰价分档口径下 B 全管线便宜约 38%——计划段的节省发生在最贵的档位上。层级分工与错误截留机制的展开见[分层停点与需求重构](layered-stops-requirement-reframing.md)。
