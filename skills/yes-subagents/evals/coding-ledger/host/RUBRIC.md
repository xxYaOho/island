# Pre-registered Rubric

> 仅 Eval Host 与评分者可见。运行开始后不得修改。每个判定必须引用 transcript、工件、命令输出或文件哈希；最终答案中的自述不能替代过程证据。

## 判定顺序

1. 先判运行是否 VALID。
2. VALID case 再分别判业务正确性与流程合规性。
3. 裁量行为只作观察，不进入硬性 PASS 数量。
4. token 与费用只对已有完整用量证据的阶段计算；缺失不补零。

## 运行有效性

- `V-1`：阶段取得完整终态与 transcript。
- `V-2`：repo 来自本包 prepare 输出；每个阶段启动前，其应保持不变的输入哈希与 run-manifest 或上游交付记录一致。
- `V-3`：被测线程未获得 Truth Card、oracle、rubric 或另一 case 内容。
- `V-4`：Step 2 未获得 Step 1 transcript、self-review 或 strict 修正历史。
- `V-5`：Eval Host 未代替被测线程作关键计划或施工判断。

任一失败则受影响 pipeline 为 INVALID。业务或编排失败不触发 INVALID。

## Step 1 硬性检查

- `P-1`：P-thin 与 P-thick 使用不同 fresh 计划线程。
- `P-2`：计划作者读取冻结 Decision/Draft 与 repo 后生成执行层，没有改写已批准产品决策。
- `P-3`：P-thin 形成一个整体可验收的薄执行计划，不创造 Milestone 或多节点协调结构。
- `P-4`：P-thick 形成两个 Milestone；M1 是多银行稳定对账，M2 是依赖 M1 的周/月分析。Task 归属于 Milestone。
- `P-5`：计划作者在交给 reviewer 前完成实质 self-review，至少核对需求闭环、层级归属、一致性、占位符与验证边界，并修正发现的问题。只写“已自检”不算证据。
- `P-6`：最终计划由作者之外的 fresh strict 审查；作者 session ID 与 reviewer session ID 不同。
- `P-7`：strict Round 1 获得完整评审基线；若 FAIL，后续轮只消费上一轮 FATAL、对应修复和受影响节，直到 PASS 或技能上限。
- `P-8`：只有最终 `STATUS: PASS` 才建立 Step 2 handoff。handoff 仅含批准计划、执行切片、最终 PASS 凭证与 open-items。

`P-3` 评价结构是否真实为薄计划，不评价代码行数。`P-4` 不要求某种 Task 数量。

## Step 2 通用硬性检查

- `E-1`：E-thin 与 E-thick 各自使用 fresh 施工 Orchestrator，且与对应 Step 1 作者和 strict 不同。
- `E-2`：施工线程消费已有计划，不重新生产计划、不重跑 strict；遇到结构性偏差时按合同回流，而非实施中改写基线。
- `E-3`：执行者先直接验证；最终 gate 使用批准计划当前节点作为唯一基线。
- `E-4`：E-thin 按其 prompt 不创建 commit；E-thick 的每个 Coder Plus 在对应 Milestone 交付 gate 前创建至少一个本地原子提交，并报告开工/交付 HEAD，DONE 时 Milestone-owned 未提交状态为零；叶子不提交，所有被测线程都不 push。commit 不替代 gate。
- `E-5`：完整计划全部节点 PASS 后只运行一次计划级 Pruner；Pruner 取得 touched-file boundary，并自行派 Scout 核验后只执行 SAFE 项。不得逐 Milestone 运行 Pruner。

## E-thin 硬性检查

- `ET-1`：E-thin 施工 Orchestrator 自己完成代码修改与直接验证，没有派 `coder`、`coder-plus`、`swarm` 或其他执行代理代做。
- `ET-2`：Orchestrator 的实现由独立 `critic-gate` 审查；gate session 与 E-thin session 不同。
- `ET-3`：若 gate FAIL 或需要补证，复用同一个 gate reviewer；计划结构变化除外。
- `ET-4`：`verify.py --case thin` PASS。

调查型只读代理若因真实阻碍被使用，记录原因，但不能代替 Orchestrator 实施。是否合理进入裁量观察。

## E-thick 硬性检查

- `EK-1`：E-thick-M1 与 E-thick-M2 属于同一个施工 Orchestrator session，且顺序推进。
- `EK-2`：每个 Milestone 首层恰派一次 Coder Plus 或等价的注入合同执行者；没有把内部 Task 扁平直派，也没有把两个 Milestone 合并为一个施工边界。跨 Milestone 可 fresh 或 retain，但 retain 必须记录连续性理由、保留上下文和当前节点边界。
- `EK-3`：每个 Coder Plus 取得的输入只包含当前 Milestone 的目标、实施内容、验收、可动文件、依赖与下游承诺，不含后续节点或完整历史 transcript。
- `EK-4`：Coder Plus 负责整个 Milestone，整合所有叶子结果并执行统一验证；叶子 DONE 不直接视为 Milestone DONE。
- `EK-5`：Coder Plus 自主承担 Milestone 内原子提交，输出 COMMITS；不承担 plan review、最终 gate、远程发布或计划级 cleanup。
- `EK-6`：E-thick Orchestrator 亲自对 M1、M2 gate，两个节点使用同一个 reviewer session；不为每个 Milestone 新建 `critic-gate`。
- `EK-7`：M1 PASS 后才进入 M2；M2 不读取 M1 的叶子 transcript，只接收已确认接口与事实。
- `EK-8`：`verify.py --case thick-m1` 与 `--case thick-m2` PASS。
- `EK-9`：gate handoff 由开工 HEAD、交付 HEAD、其间提交与干净的 Milestone-owned 状态共同界定；Coder Plus 交付 gate 后受审 HEAD 与历史保持冻结，若 gate FAIL，修复使用追加提交而非改写 reviewer 已见历史。

## 业务检查

以 verifier 的逐项 JSON 为准：

- `B-1`：thin dry-run 分类计数正确，临时账本逐字节不变。
- `B-2`：Alpha/Beta 首次导入、重复导入、同键冲突、行级 rejected 与文件级失败分类正确。
- `B-3`：14 条规范交易、来源字段与 raw evidence 符合 oracle；同外观不同 ID 未被合并。
- `B-4`：既有 `import-alpha` 兼容且不改变已对账账本。
- `B-5`：week/category、week/target、month/category、month/target 全部符合 oracle，重复调用稳定，默认 table 输出存在。

## 裁量观察

以下问题不设指定答案：

- Coder Plus 是否分派叶子；若分派，是否有独立边界、验收与明确的并行、上下文或专长收益。
- 若不分派，是否因为关键路径、强耦合、共享状态或 brief/整合成本不划算。
- 只读调研是否阻碍关键路径；`researcher` 是否被不必要地等待。
- 叶子是否获得过多上下文、重叠写入或继续编排能力。
- Orchestrator、Coder Plus 与 gate 是否出现无信息轮询或重复全文读取。

只有裁量行为直接违反硬性角色边界时，才映射到相应 E 检查失败。

## VD 与效率

- P-thin、P-thick：各自完整计划取得 strict PASS 并形成可消费 handoff，分别计 1 个 Plan VD。
- E-thin：业务 verifier 与 gate 均 PASS，计 1 个 Implementation VD。
- E-thick：M1、M2 分别在业务检查与 gate PASS 后各计 1 个 Implementation VD。
- Pruner、Scout、strict、gate 与失败修正均计入对应 VD 的成本，但不单独增加 VD。
- Plan VD 与 Implementation VD 不混合比较；不同 case 也不宣称工作量相同。TPVD 只用于同一阶段、同一冻结包后续复跑的纵向比较。

总计费 token 按供应商账单字段归一为 cache-miss input、cache-read input 与 output 之和，并覆盖主线程和全部嵌套会话。若供应商的 total 已包含某分项，按其官方口径去重并在 REPORT 声明。
