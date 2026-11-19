---
title: 多代理运行的费用核算与价值基准
type: concept
created: 2026-09-04
updated: 2026-09-08
sources: [raw/multi-agent-run-cost-accounting.md, raw/verified-deliverable-efficiency-metrics.md]
topic: yes-subagents 工作流程与严格回合
tags: [subagent, cost, pricing, token-accounting, context-bloat]
status: current
context: 2
---

# 多代理运行的费用核算与价值基准

> 方法与实证（2026-09-04）：多代理会话的账单结构由「轮次 × 上下文重放」决定，生成量只是零头。核算口径必须覆盖主会话 + 全部嵌套子代理会话；跨服务商比较以 DeepSeek v4-flash 峰价为锚。（[多代理运行的完整费用核算与价值基准 (DeepSeek 峰价)](../raw/multi-agent-run-cost-accounting.md)）

## 计费模型: 轮次 × 上下文重放

- Agent 会话中每个 turn 模型都要重新处理此前全部对话前缀（工具结果/文件读取/派遣指令）才能生成该轮增量。Prompt cache 让重放远便宜于新输入（实测口径：命中 $0.014/M vs 未命中 $0.44/M，约 31 倍价差），但仍按 turn 逐次计费。
- `cache 读账单 ≈ Σ(每个 turn 的上下文体量) ≈ turns × 平均上下文`。自检：81 turns × ~53.5k 平均上下文 ≈ 4.33M，与实测 cache_read 4.34M 吻合。（[多代理运行的完整费用核算与价值基准 (DeepSeek 峰价)](../raw/multi-agent-run-cost-accounting.md)）
- 推论：降本杠杆只有两个——减少 turn 数、压薄常驻上下文。生成量（输出 token）是零头，实证三轮中占 3%-10%。

## 已验证交付单元与效率指标

仅看总 token 或总费用，无法比较不同任务是否完成了同等结果。已验证交付单元（Verified Deliverable，VD）必须有明确预期结果、独立验收边界，并有直接验证或 gate PASS 证据；未达到验收边界的运行不计为 VD，也不计算数值型效率指标。不同运行只有在 VD 定义相同时才可比较。

- **TPVD**（Tokens per Verified Deliverable）= 评估单元内主会话与全部嵌套子会话的总计费 token / VD 数量，单位 `kTokens/VD`，越低越好。核算覆盖规划、审查、失败派遣、返工和 gate；流式评估按 Step 独立核算，已交付成本不在下一 Step 重复计入。
- **CPVD**（Cost per Verified Deliverable）= 同一口径的总模型费用 / VD 数量，单位 `currency/VD`，越低越好。它同时受 token 用量、模型单价、输入输出构成和缓存命中影响，不能单独归因编排质量。
- **CPTK**（Cost per Thousand Tokens）= 总模型费用 / 总计费 token × 1000，单位 `currency/kTokens`。它只诊断模型、缓存及输入输出构成的价格差异，不衡量任务是否完成，也不是 workflow 效率主指标。

workflow 优化以 TPVD 为主指标，CPVD 为成本结果，CPTK 为价格构成诊断；质量、正确性和验收范围是 VD 的前置约束，不能与 TPVD 相互抵扣。（[已验证交付单元的 token 与成本指标](../raw/verified-deliverable-efficiency-metrics.md)）

## 核算口径（硬性）: 主会话 + 全部嵌套子代理会话

stream-json result 行的 usage 只含主会话；子代理是独立计费会话，只按主会话记账会严重低估——E3 实测子代理占总账 23%/42%/35%，漏算最多近半。（[多代理运行的完整费用核算与价值基准 (DeepSeek 峰价)](../raw/multi-agent-run-cost-accounting.md)）

1. 主会话：transcript 的 result 行 usage（timing 脚本既有口径，须全段累计）。
2. 一级子代理：`~/.claude/projects/<主会话cwd-slug>/<session_id>/subagents/agent-*.jsonl`，按每条 assistant 消息的 usage 逐条累加（cache 读按次计费，与计费模型一致）。
3. 二级嵌套探测必做：取各子代理自身的 session_id，再查其 `<slug>/<session_id>/subagents/`（孙代理）。实证三轮均为 0 个，但检查本身是方法的组成部分，不可省略。
4. 失败派遣（如 `Agent type not found`）不产生会话、不计费，但须对账说明（派遣次数 - 失败次数 = 会话数）。

## 价格基准: DeepSeek v4-flash 峰价

2026-08-16 DeepSeek 调价后（多源核实：官方定价页、TechJack、packet.ai 等），v4-flash 按峰谷计费：

| 项 | 峰价 ($/M tokens) | 谷价 |
|---|---|---|
| 输入 (cache miss) | 0.44 | 0.22 |
| 输入 (cache hit) | 0.014 | 0.007 |
| 输出 | 1.32 | 0.66 |

峰时段：01:00-04:00 与 06:00-10:00 UTC，其余为谷时（约半价）。

基准提案：以 v4-flash 峰价作为 yes-subagents 技能运行的价值参考锚——flash 级定价压低了「流程税」的下限，便于跨服务商、跨执行器档位换算比较（换 opus 级执行器约 10-30 倍价差）。（[多代理运行的完整费用核算与价值基准 (DeepSeek 峰价)](../raw/multi-agent-run-cost-accounting.md)）

## E3 三轮实证

三轮同一任务（micro-note JSON→SQLite 迁移），token 分项与折算（峰价）：

| 轮 | turns | 墙钟 | 主会话账 | 子代理账 (会话数) | 合计 | 谷时约 |
|---|---|---|---|---|---|---|
| R1 v0.5.1 | 74 | 34m49s | $0.213 | $0.064 (2) | **$0.277** | $0.14 |
| R2 v0.5.2 | 41 | 46m43s | $0.268 | $0.192 (5) | **$0.460** | $0.23 |
| R3 v0.5.3 | 81 | 75m19s | $0.536 | $0.288 (7) | **$0.824** | $0.41 |

交付物质量百分制（统一尺度的单评估者打分，维度权重：功能完成度 35 / 健壮性边界 25 / 测试可验证性 20 / 工程结构与文档 10 / 决策透明度 10）：

| 轮 | 质量分 | 每分价格 (峰价) |
|---|---|---|
| R1 | 70 | $0.0040 |
| R2 | 78 | $0.0059 |
| R3 | 95 | $0.0087 |

## 解读

1. **每分价格递增不是流程税。** R1 便宜部分源于跳过了派遣与独立 gate（亲自实施，子代理占比仅 23%）。质量分 70→95 的最后 25 分买的是健壮性/边界/诚实披露——都是有息负债的免除（DB 入库的二进制 churn、幂等缺失、失败路径裸奔），属 TCO 利息前置。一次性脚本场景 R1 反而理性；技能目前无从得知任务寿命。
2. **子代理的钱是设计成本而非浪费。** 「把脏活推进子代理」省的是编排者上下文健康，钱由子代理自付，总账不降反升（R2 子代理占 42%）。买的是独立视角与上下文隔离，不是省钱。（[多代理运行的完整费用核算与价值基准 (DeepSeek 峰价)](../raw/multi-agent-run-cost-accounting.md)）
3. **数据边界。** n=1；百分制为单评估者尺度；峰谷价格摆动约 50%；结论用于量级判断，不用于精确预算。

## 关联

- [编排者轮询导致上下文暴涨](orchestrator-polling-context-bloat.md) —— 机制同源：轮询的每次调用就是一次全量上下文重放，换回零信息（完成通知免费推送），是「turns × 平均上下文」公式的极端实例。该页提供行为教训与动机层根因，本页提供定价公式。
