---
class: material
ingested: true
integrated: true
metadata:
  class: material
  ingested: true
  metadata:
    version: 0.1.1
    type: decision-note
  source_repo: "https://github.com/xxYaOho/skiil-go-spec"
  source_commit: 05f560f
  source_path: docs/simple-wiki/raw/2026-09-07-decision-execution-layer-detail-level.md
---

# 决策：执行层详细度定位——高档位 token 只花在高维度决策上

> 杨桃拍板于 2026-09-07。背景：plan-creation eval 0.1 的 executor 可施工性评估与 A/B 实施计划对比讨论。

## 背景

eval 0.1 中 A（writing-plans 手册式，2047 行 / 69% 内嵌代码）与 B（go-spec 承诺式，430 行 / 7% 契约代码）的对比引出 executor 经济学：A 把成本前置（计划贵、施工近零判断力需求），B 后置（计划便宜、施工要付微观设计判断）；总账优劣取决于执行者档位——haiku 施工时手册式可能反超，sonnet+ 施工时承诺式更低。

## 决策

执行层（go-spec 的 Milestone/Task 层）详细度定位：**计划者（高档位）只产出高维度且详细适中的承诺——目标、验收标准、边界、契约；TDD 节奏等简单、偏实时的代码设计下放执行者（sonnet 级）自行完成，不消耗高档位 token。**

## 依据

1. sonnet 级执行者能力足以自行完成 TDD 与微观代码设计，施工能力不构成瓶颈。
2. eval 0.1 中 B 执行层被 fresh-agent（无对话上下文）审定可施工：有目标、有验收标准即够推进。
3. 手册式预付（A 形态）在「高档位计划 + 中档位执行」的目标场景里是错配支出。

## 关联

- 承接 go-spec 决策 14（承诺立场：自足 = 判据完整 + 边界明确 + 上下文指引，非实现预写）：14 定义「不写什么」，本决策定义「详细度锚在哪、为什么」。
- 来源评估：`.tmp/eval/plan-creation-ab/`（route-a / route-b 对照产物）。
