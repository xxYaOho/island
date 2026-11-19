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
  source_path: docs/simple-wiki/raw/verified-deliverable-efficiency-metrics.md
---

# 已验证交付单元的 token 与成本指标

## 目的

评估 agent workflow 时，单看总 token 或单价无法回答「完成一个有效结果用了多少资源」。统一以已验证交付单元（Verified Deliverable，VD）作为分母，分别记录 token 效率与货币成本。

## 已验证交付单元（VD）

VD 是具有明确预期结果、独立验收边界，并已有直接验证或 gate PASS 证据的交付单元。VD 不要求等于整个项目：在流式评估中，一份通过独立审查的计划可以是一个 VD；一个通过 gate 的里程碑也可以是一个 VD。不同运行只有在 VD 定义相同时才可比较。

未达到验收边界的运行不计为 VD，也不计算数值型效率指标；应单独标记为未完成，避免用缩小或取消验收范围改善指标。

## 主指标：TPVD

Tokens per Verified Deliverable（TPVD）表示完成一个 VD 消耗的总计费 token：

```text
TPVD = 该评估单元内主会话与全部嵌套子会话的总计费 token / VD 数量
```

默认单位为 `kTokens/VD`，数值越低越好。核算从该单元开始到其通过验证为止，包含规划、审查、失败派遣、返工、gate，以及所有层级子代理会话产生的 token。流式评估按 Step 分别核算；上一步已经完成并交付的成本不重复计入下一步。

TPVD 用于观察上下文管理和编排效率，例如重复全量阅读、无效轮询、过细派遣、重复 gate 或不合理返工造成的 token 增量。比较时应固定 VD 定义，并说明模型、harness 与缓存口径。

## 配套指标：CPVD

Cost per Verified Deliverable（CPVD）表示完成一个 VD 的总模型费用：

```text
CPVD = 该评估单元内主会话与全部嵌套子会话的总模型费用 / VD 数量
```

单位为 `currency/VD`，数值越低越好。CPVD 同时受 token 用量、模型单价、输入输出构成和缓存命中影响；它用于预算判断，不能单独归因编排质量。

## 诊断指标：CPTK

Cost per Thousand Tokens（CPTK）表示混合 token 单价：

```text
CPTK = 总模型费用 / 总计费 token × 1000
```

单位为 `currency/kTokens`。CPTK 只解释模型、缓存与输入输出构成带来的价格差异，不衡量任务是否完成，也不作为 workflow 效率主指标。

## 使用原则

- workflow 优化以 TPVD 为主指标，CPVD 为成本结果，CPTK 为价格构成诊断。
- 质量、正确性和验收范围是 VD 的前置约束，不能与 TPVD 相互抵扣。
- 主会话与全部嵌套子代理必须纳入同一核算口径。
- 流式、多线程评估按各 Step 的 VD 独立核算，再另行记录端到端总量。
