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
  source_path: docs/simple-wiki/raw/strict-plan-loop-convergence-2026-10-18.md
---

# Plan-Strict 循环收敛决策

> 2026-10-18 · yes-subagents v0.8.0

## 背景

Strict 审查在 `plan <-> strict` 循环中会不断提升计划复杂性：每一轮修正都把缺陷兑换成新机制，计划持续增厚，直到生命周期耗尽。yes-designer 案例出现完整证据链：v1 742 行经 5 稿变为 874 行（+18%），PASS 时仍挂 6 项 MAJOR，Human 最终不批准。原四轮上限只截断成本，不改变方向。

## 诊断：两种膨胀来源

1. **形式化协议型**：工件本身是形式化协议（如 yes-designer 的 baseline/assertions schema）。审查以完备性为标准，每补一个字段就生成一组新的一致性要求，追捕无底。此时 strict 会把 schema 字段、hash 标注、表头语义、附录索引等判为 FATAL 或必修 MAJOR。
2. **普通计划欠账型**：计划本身偏薄、验收合同缺失。strict 判出的 FATAL 多为真缺口（验收无基线、状态无续接、重试无幂等），修复只能补机制。此时膨胀来自"计划欠账"，不是审查噪音。

两条机制叠加：
- FATAL 判据缺少严重性锚，形式缺口与验收合同缺失被同等对待；
- 修复侧只有加法：FATAL 必须修，MAJOR 一律 carry forward 或由 Human 接受，没有"删除/降级/取舍"的合法出口；
- 修正结构性变化触发 FULL 全量复审，修复本身制造新攻击面；
- 升级条件错位：`lead` 只在轮次耗尽时找用户，而不是在出现判断分歧时。

## 决策（8 项）

1. **判级锚**：派遣 Strict 必须提供第一用途、已声明成功标准、非目标、不可接受失败形态。判级锚不是背景——设计理由、既成取舍、替代方案仍然不提供，以保留攻击角度。缺判级锚时 reviewer 返回 `BLOCKED`，不得自行推断。
2. **两类缺口**：`critic-strict` 区分 formal-completeness gap（schema 字段、hash 标注、措辞、写序叙述，至多 MAJOR）与 verification-contract gap（生成断言无执行层、门禁无比较基线、回归无触发、状态无合法转移、复制路径无证明，可 FATAL）。每条 FATAL 必须引用它破坏的成功标准或第一用途。
3. **证据强度**：禁止绝对化措辞（never/none/always），除非能指出完整缺失或具体无条件路径；"合同未保证 X"不等于"X 必然失败"；MAJOR 也必须给出具体失败路径，否则降 MINOR 或观察。
4. **FAIL 后分诊**：真缺陷修工件；前提缺失补最小背景后原 reviewer 重审，不改工件；取舍问题升级用户；流程开销删除该产物。修正轮只处理真缺陷 FATAL 及其直接辐射，MAJOR 一律 carry forward。
5. **取舍硬判据**：修复若删除或新增验收面、机制、门禁检查，接受某类风险，或改变版本/审批语义，先归取舍并升级用户，不得由 Orchestrator 自裁。
6. **升级条件**：出现判断分歧或前提缺失无法自行补全时立即升级；四轮上限从唯一入口降为兜底保险。
7. **修复预算**：修正方案必须列出新增机制及其服务的成功标准；单轮新增机制达到 3 个，或计划类工件净增超过 50%，停止自动修正并升级用户裁决。
8. **计划准入**：计划进入 strict 前必须具备验收合同——每条成功标准对应至少一个可证伪检查，且检查有明确比较基线；不可机械验证的部分已声明由 Human 验收。缺验收合同时退回计划生产阶段补齐，不在 strict 生命周期内补写。

附带两条减法：修复对照表/附录不构成审查对象（只作为索引，不作为缺陷）；MAJOR 台账中不影响第一用途且消费时点未到来的条目可直接 `ACCEPTED`，不得以"未来条件触发"长期挂 `OPEN`，也不得为关闭台账新增机制。

## 验证

### yes-designer 用例（iteration-11 / 12）

- Round 1：with 新契约 E1 FATAL 1（漏掉 computed/layout 执行层与事故 B 拦截两条真 FATAL）；old 契约 FATAL 3。E2 出现「把验收面取舍包装成真缺陷并补执行层」的加法。
- Round 2（校准后，只测 with）：E1 FATAL 4，全部为验收合同缺失（执行层、design-export 逐 state 期望、事故 B diff 基线、跨切片回归触发）；形式完备性 0 条进 FATAL。E2 四分类 6 真 / 0 前提缺失 / 1 取舍 / 1 流程开销；执行层改判取舍并升级用户；修正净增 ≤15 行（+1.5%）、新增机制 0；附录不再新增。
- 盲评（独立 agent）：4 条 FATAL 全部成立（其中 design-export 的像素归一要求应收窄）；但漏判 1 条应升 FATAL 的阈值审批门禁，且有 3 条 MAJOR 论证过度（一条缺陷不成立、两条证据不足）。判级存在 ±1 档波动。

### plan-loop 用例（iteration-13）

- 与领域无关的 notes-cli 多设备同步计划，plan-v1 95 行、刻意留白。R1：with FATAL 5 / old FATAL 4，两者形式缺口均 0 FATAL。
- 修正：5 条真缺陷修复新增 6 个机制，95 → 173 行（+82%）。R2：FATAL 1（TOCTOU），R1 五条全部关闭，但修正本身新增 5 条 MAJOR。
- 结论：判级锚消除了形式噪音，但没有阻止真 FATAL 驱动的膨胀；普通计划上旧契约本来也不把形式缺口当 FATAL，新契约增量有限。

### 规则验证（iteration-14）

- 修复预算：以新 SKILL.md 处理同一 R1 FAIL，自动修正集 4 个机制（保守合并 3 个）、计划 95 → 150 行（+57.9%）；两条判据独立触发，未产出 plan-v2，改为升级用户裁决。结论对估算误差与分诊口径均不敏感。
- 计划准入：以新 coding.md 检查 plan-v1，4 条成功标准 0/4 有可证伪检查，且实施单元缺 Task/边界/依赖/接口承诺，结论为退回计划生产阶段。

## 边界与教训

- 判级锚解决的是"形式噪音 FATAL"，不解决"真 FATAL 必然带来增量"。膨胀的主因是计划欠账 + 真 FATAL 修复；干预点是准入与预算，不是继续调判级。
- 判级精度仍有 ±1 档波动，无法靠条款完全消除；证据强度规则只能压缩绝对化断言和过度 MAJOR。
- 形式化协议类工件与普通计划的审查行为不同；"形式化无底"不能推广到所有计划。
- Eval 设计陷阱：baseline 配置也被给判级锚会破坏对比；prompt 泄露分诊分类会污染归因；fixture 与历史报告同目录会被误读；自写断言存在循环论证风险，需要独立盲评。

## 关联

- [严格飞轮四轮上限与生命周期重启决策](../wiki/strict-flywheel-four-round-decision.md)
- [增量复审契约的 fresh-agent 盲区](../wiki/delta-review-fresh-agent-blindspot.md)
- eval 产物：`yes-subagents-workspace/iteration-11..14`、`yes-subagents-workspace/blind-review/e1-v2-review.md`
- 契约落点：`skill/subagents/critic-strict.md`、`skill/SKILL.md`、`skill/workflow/coding.md`；提交 `87a2da0`
