---
title: Plan-Strict 循环收敛决策
type: decision
created: 2026-10-18
updated: 2026-11-19
sources: [raw/strict-plan-loop-convergence-2026-10-18.md, raw/yes-subagents-2026-09-16-strict-review-intensity-design.md, raw/yes-subagents-2026-09-16-strict-review-intensity-plan.md]
topic: yes-subagents 工作流程与严格回合
tags: [review, orchestration, strict, convergence, eval]
status: current
context: 2
---

# Plan-Strict 循环收敛决策

Strict 在 `plan <-> strict` 循环中会把缺陷兑换成新机制，计划持续增厚。四轮上限只截断成本，不改变方向。本决策在不降低攻击性的前提下，用判级锚、分诊、升级条件、修复预算与计划准入五组约束收敛循环。

## 两种膨胀来源

| 来源 | 表现 | 有效干预 |
|---|---|---|
| 形式化协议型 | 工件本身是形式化协议（schema/hash/审批链），审查以完备性为标准，追捕无底 | 判级锚：形式缺口至多 MAJOR；验收合同缺失才可 FATAL |
| 普通计划欠账型 | 计划偏薄、验收合同缺失，判出的 FATAL 多为真缺口，修复只能补机制 | 计划准入 + 修复预算 |

判级锚消除的是形式噪音，不阻止真 FATAL 驱动的增量。逐轮调判级无法解决欠账型膨胀。

## 决策要点

- **判级锚**：派遣 Strict 必须提供第一用途、成功标准、非目标、不可接受失败形态。设计理由与既成取舍仍不提供，以保留攻击角度。
- **两类缺口**：formal-completeness gap（schema、hash、措辞、写序）至多 MAJOR；verification-contract gap（断言无执行层、门禁无基线、回归无触发、状态无转移、复制无证明）可 FATAL。每条 FATAL 必须引用被破坏的成功标准。
- **证据强度**：禁止 never/none/always 等绝对化断言；"合同未保证 X"不等于"X 必然失败"；MAJOR 也必须有具体失败路径，否则降 MINOR。
- **FAIL 后分诊**：真缺陷修工件；前提缺失补背景重审；取舍问题升级用户；流程开销删除产物。修正只处理真缺陷 FATAL 及直接辐射。
- **取舍硬判据**：修复若删/增验收面、机制、门禁，接受风险，或改版本/审批语义，先归取舍并升级用户。
- **升级条件**：出现判断分歧或前提缺失即升级；四轮上限降为兜底。
- **修复预算**：修正方案须列新增机制及其服务标准；单轮新增机制 ≥3 或计划净增 >50%，停止自动修正并交用户。
- **计划准入**：计划须有验收合同（每条成功标准对应可证伪检查 + 明确比较基线，不可机械验证部分声明 Human 验收），否则退回计划生产阶段。
- **减法**：修复对照表/附录不是审查对象；不影响第一用途的 MAJOR 可直接 `ACCEPTED`，不得长期挂 `OPEN` 或以新增机制换关闭。

## 验证结论

- yes-designer（形式化协议型）：校准后 E1 的 4 条 FATAL 全部是验收合同缺失，形式缺口 0 条进 FATAL；E2 把执行层取舍升级用户，修正净增 1.5%、新增机制 0。独立盲评确认 4 条 FATAL 成立，但发现 1 条漏判与 3 条过度 MAJOR，判级有 ±1 档波动。
- plan-loop（普通计划型）：修正 6 个机制、95 → 173 行（+82%）；R2 关闭 R1 全部 FATAL 但新增 5 条 MAJOR。说明真 FATAL 修复本身就会膨胀。
- 规则验证：以新规则处理同一 FAIL，预算触发（4 机制 / +57.9%），未产出 v2 而升级用户；计划准入以 0/4 验收合同拦下 plan-v1，退回补计划。

## 适用边界

- 本决策解决循环的方向与授权边界，不承诺消除全部膨胀；判级精度存在 ±1 档波动。
- 形式化协议类工件的问题（形式化无底）不能推广到普通计划；普通计划上旧契约本来也不把形式缺口当 FATAL。
- Eval 设计注意：baseline 配置不应同时获得判级锚；prompt 不应泄露分诊分类；fixture 应与历史报告隔离；自写断言需独立盲评。

## 关联

- [增量复审契约的 fresh-agent 盲区](delta-review-fresh-agent-blindspot.md) —— 修正轮是否需要 FULL 复核。
- [Strict 飞轮四轮上限与生命周期重启决策](strict-flywheel-four-round-decision.md) —— 本决策的上游生命周期约束。
- [Plan-Strict 循环收敛决策](../raw/strict-plan-loop-convergence-2026-10-18.md) —— 完整决策材料与验证数据。

## 审查强度与严重度判级

设计已在对话中确认（[设计](../raw/yes-subagents-2026-09-16-strict-review-intensity-design.md)，[实施计划](../raw/yes-subagents-2026-09-16-strict-review-intensity-plan.md)）。同一审查代理和同一套严重度定义额外接受 `intensity: low | high | max`。强度只改变主动探索深度，不改变模型身份、effort 或 FATAL 定义。

选择优先级：`Human 显式指定 > Orchestrator 按风险选择 > 默认 high`。`low` 用于局部可逆且可直接验证的单工作单元；`max` 用于不可逆、安全敏感或跨层外部合同；其余用 `high`。

`FATAL` 必须同时满足：会造成实质错误、不安全或不可验证结果；能指出具体失败场景与受影响交付物；当前阶段无法隔离、延后或由后续 Gate 无损补救。证据与结论不匹配不再自动升为 FATAL。仅有 MAJOR/MINOR 时仍返回 `PASS`；MAJOR 必须进入台账，在被下一阶段消费前或最终交付前关闭，终态只能是 `RESOLVED` 或 Human 记录理由的 `ACCEPTED`。修正 MAJOR 默认不触发复审；若改变目标、范围、验收或外部合同，则按 `FULL` 重审。
