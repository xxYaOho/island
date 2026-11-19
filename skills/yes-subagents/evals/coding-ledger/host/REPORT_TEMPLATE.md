# REPORT：Coding Ledger Evaluation

> Run ID：`<run-id>`
> Package：`coding-ledger-v1`
> Skill version：`<version>`
> Runtime / models：`<runtime-and-model-map>`
> Started：`<timestamp>`
> Finished：`<timestamp>`

## 1. 结论

分别说明薄、厚流水线是否为 VALID，以及 coding workflow 得到了哪些有证据支持的结论。不要把 n=1 写成稳定能力结论。

## 2. 运行有效性

| Pipeline | Status | Evidence |
|---|---|---|
| thin | VALID / INVALID | transcript、输入哈希、异常 |
| thick | VALID / INVALID | transcript、输入哈希、异常 |

INVALID case 只描述基础设施或协议原因，不计入后续 PASS 率。

## 3. Step 1：计划与审查

### P-thin

- 执行层形态：
- self-review 证据：
- fresh strict 证据：
- 修正轮次与最终状态：
- 是否改写冻结 Decision/Draft：
- Step 2 handoff 内容：

### P-thick

- 执行层形态与 Milestone 数：
- Milestone 切分是否按验证主题：
- self-review 证据：
- fresh strict 证据：
- 修正轮次与最终状态：
- Step 2 handoff 内容：

## 4. Step 2：施工与 Gate

### E-thin

- 实施者与派遣树：
- 是否由施工 Orchestrator 自己实施：
- direct verification：
- 独立 gate reviewer 与复用证据：
- 计划级 Pruner/Scout 收尾：
- 业务 verifier：

### E-thick-M1

- 首层 Milestone 派遣：
- Coder Plus 内部执行图：
- 叶子分派及收益，或选择不分派的理由：
- 整合与整体验证：
- Coder Plus 原子提交、起止 HEAD、owned worktree clean 与叶子零提交证据：
- Orchestrator gate：
- 业务 verifier：

### E-thick-M2

- 首层 Milestone 派遣：
- Coder Plus 内部执行图：
- 叶子分派及收益，或选择不分派的理由：
- 整合与整体验证：
- Coder Plus 原子提交、起止 HEAD、owned worktree clean 与叶子零提交证据：
- 与 M1 同一 gate reviewer 的证据：
- 全计划一次 Pruner/Scout 收尾：
- 业务 verifier：

## 5. 机械结果

### 业务正确性

| Check | Status | Evidence |
|---|---|---|
| thin dry-run summary | | |
| thin ledger byte stability | | |
| thick M1 import classifications | | |
| thick M1 canonical transactions and provenance | | |
| thick M1 idempotency and conflict non-overwrite | | |
| thick M2 week/category | | |
| thick M2 week/target | | |
| thick M2 month/category | | |
| thick M2 month/target | | |

### 流程合规性

| Check | Status | Evidence |
|---|---|---|
| Step 1 author 与 strict 分离 | | |
| Step 1 self-review 存在且有效 | | |
| Step 2 为 fresh thread | | |
| Step 2 未继承 Step 1 transcript | | |
| thin 未外派施工 | | |
| thin 最终 gate 独立 | | |
| thick 每 Milestone 一次 Coder Plus | | |
| thick 未扁平直派 Task | | |
| thick 两节点复用同一 Orchestrator gate | | |
| Coder Plus 完成整合与 Milestone 统一验证 | | |
| Coder Plus 提交、起止 HEAD、owned clean、叶子零提交、无 push | | |
| gate 后受审历史冻结，FAIL 修复仅追加 | | |
| 每条完整计划只运行一次 Pruner/Scout 收尾 | | |

## 6. 裁量观察

只描述行为、理由与代价，不判指定角色是否出现：

- Coder Plus 哪些工作自己完成，理由是否成立；
- 哪些叶子被分派，边界、并行性、专长或上下文收益是否明确；
- 是否存在 brief、等待或整合成本高于实际收益的分派；
- 是否出现本可并行却阻塞推进的工作；
- 上下文过滤是否有效。

## 7. Token 与费用

必须包含 Eval Host、计划作者、strict、施工 Orchestrator、gate、Coder Plus 和全部嵌套叶子。缺失值写 `N/A`，不可按零处理。

| Stage / Role | Turns | Input | Cache read | Output | Cost |
|---|---:|---:|---:|---:|---:|
| | | | | | |

- Plan VD：一份执行层计划通过 fresh strict 并形成可消费 handoff，P-thin/P-thick 各最多 1 个。
- Implementation VD：一个实施节点同时通过业务验证与最终 gate，E-thin 最多 1 个，E-thick 最多 2 个。
- TPVD：`全树总 token / VD`，报告为 `kTokens/VD`。
- CPVD：`全树总费用 / VD`。
- CPTK：`全树总费用 / 全树总 token × 1000`。

Plan VD 与 Implementation VD 的验收范围不同，分别计算 TPVD/CPVD，不合并成可比较均值。每个阶段都单独报告；全流程总账只作成本闭合。Eval Host 的主持成本单列，并同时给出“含主持”和“不含主持”的诊断视图。

## 8. 偏差与失败归因

将问题分别归入：业务实现、计划形态、编排机制、角色合同、评估协议、运行基础设施。每条必须引用原始证据，不根据最终输出反推未观测过程。

## 9. 与 Skill 修改的关系

列出候选修改，但不要在 REPORT 中直接修改 skill。区分：

- 有重复证据支持的机制问题；
- 单次观察，需复跑；
- fixture 或 harness 问题；
- 与 skill 无关的问题。

## 10. 原始工件索引

列出阶段 transcript、批准计划、切片、strict/gate verdict、git diff、verifier JSON、observations.json 与 timings.json 的路径和哈希。
