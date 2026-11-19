# Coding

适用于已经完成需求讨论、准备按计划实施的编程工作。本 workflow 是**计划消费与施工编排器**：确认计划可施工，判断薄厚层级，组织执行、gate 与收尾。计划生产由 `go-spec` 负责；通用组合、飞轮、待机和完成条件由 `SKILL.md` 负责。

```text
取得已批准计划
  ↓
判断薄计划 / 厚计划
  ├─ 薄计划 → Orchestrator 自己实施
  └─ 厚计划 → Milestone → coder-plus
  ↓
同一 gate reviewer 持续核验
  ↓
全部节点 PASS → pruner → scout
  ↓
完整交付
```

## 1. 进入施工

默认输入是一份由 `go-spec` 或等价方法产出的完整计划。开工前确认：

- 目标、范围和验收标准可判定；
- 计划包含验收合同：每条成功标准对应至少一个可证伪检查，且检查有明确的比较基线；不可机械验证的部分已声明由 Human 验收；
- 实施单元具有明确边界、依赖和下游接口承诺；
- 计划作者已经完成 self-review；
- 计划已经由作者之外的 fresh `critic-strict` 审查并取得 `STATUS: PASS`；
- 用户已经授权进入实施。

缺少验收合同时，退回计划生产阶段补齐，不在 strict 生命周期内补写。

self-review 只检查完整性、一致性和格式，不替代独立 critique。无论计划薄厚，strict 都由 fresh-agent 承担。

Strict `PASS` 后，MAJOR/MINOR 作为非阻断事项进入施工。Orchestrator 必须随批准计划传递 MAJOR 台账，至少包含问题、影响范围、责任方、最迟关闭点和状态。下一节点会直接消费的 MAJOR 必须在消费前变为 `RESOLVED` 或 `ACCEPTED`；未被下一节点消费的 MAJOR 可以继续随施工推进，但最终交付前必须关闭。不影响第一用途且消费时点未到来的 MAJOR 可以直接 `ACCEPTED`；不得以"未来某个条件触发"作为长期 `OPEN` 的理由，也不得为了关闭台账而新增机制。批准基线内消化或披露不触发复审，处置若改变目标、范围、结论、节点、依赖、验收、证据集、交付物或外部契约，则作为结构性新版本重新进入 `FULL`。

缺少计划、计划仍不完整或尚未通过 strict 时，转交 `go-spec` 与用户补齐，不在本 workflow 内临时生产或修补计划。strict 修正轮次遵循 `critic-strict` 的增量输入契约。

施工线程只接收批准计划、strict PASS 凭证和未阻断事项，不继承计划作者或 strict 的完整 transcript，也不重复已经完成的计划审查。

## 2. 判断计划层级

厚薄描述施工结构，不描述改动行数，也不决定是否需要 strict。

**薄计划**：只有一条连贯的实施路径，可作为一个整体直接验收，不需要 Milestone 协调多个内部单元。

**厚计划**：执行层包含 Milestone；每个 Milestone 内含多个 Task、内部依赖，或需要统一验证的交付主题。

按计划已有结构判断：

- 薄计划由 Orchestrator 自己实施，不派 `coder`。
- Milestone 首层映射到 `coder-plus`；一个 Milestone 对应一次派遣。
- 不把 Milestone 扁平拆成多个 Task 后由 Orchestrator 逐项直派。
- `coder-plus` 自己决定 Milestone 内如何实施，并对整体验收负责。
- `coder` 可由 Coder Plus 用作 Milestone 内的叶子，不代表薄计划执行者。
- 风险、迁移、新颖性和验证难度影响 gate 的核验重点，不改变薄/厚施工模式。

若薄计划实际隐藏多个内部单元、依赖链或独立验证阶段，说明计划结构失真。停止施工并返回 `go-spec` 修正；不要在实施期自行发明 Milestone。

## 3. 准备施工上下文

薄计划由 Orchestrator 持有批准计划，按需读取相关代码并直接实施，不创建子代理施工包。

厚计划每次只向 Coder Plus 交付当前 Milestone，不发送完整计划、后续节点或历史讨论。施工包至少包含：

- 当前 Milestone 的目标与实施内容；
- 验收标准；
- 可动文件范围；
- 依赖、约束和下游接口承诺。
- 当前工作区与 Git 策略，包括共享写入、已有脏改动和远程操作限制；未特别声明时按本 workflow 的本地追加提交默认值执行。

派遣前，Orchestrator 记录当前 `HEAD`、staged / unstaged / untracked 状态与已有改动归属，作为 Milestone 的 Git 基线。可动文件内若已有他人改动，施工包必须明确其归属和保留方式；无法证明 Coder Plus 的修改与既有改动可隔离时，不得开工。

施工包使用 `go-spec` 的 `Milestone-<n>.md` 切片或等价内容，并满足 `coder-plus` 的 PRECONDITION。Task 归属于该 Milestone，只由 Coder Plus 消费。

若当前节点依赖上一节点的实际结果，只补充已经确认的接口或事实，不附上上一节点 transcript。

### Milestone 间连续性

Milestone 是独立的施工包、提交边界和 gate 边界，但不自动构成 Coder Plus 的 fresh session 边界。当前 Milestone 通过 gate 后，Orchestrator 必须为下一个 Milestone 做一次连续性决策：

- `fresh`：下一节点可以由已确认的接口、事实和验收摘要交接；创建新的 Coder Plus 会话。
- `retain`：下一节点明显依赖上一节点积累的大量、难以压缩的运行时调查、设计/宿主经验或其他上下文；在同一 Coder Plus 会话中发送新的 Milestone 施工包。

没有明确的上下文收益时选择 `fresh`。无论选择哪条路径，派遣记录都要写明 `continuity`、选择理由、实际保留的上下文和当前节点的重新设定边界。`retain` 不合并 Milestone，也不把上一节点的完整 transcript 作为当前节点输入；当前目标、验收、可动文件、依赖、Git 基线和 gate handoff 仍按本节点重新建立。

## 4. 推进施工

### 薄计划

Orchestrator 直接完成全部实施与直接验证，不为分派而拆分工作。完成后，将批准计划、改动、实现取舍和验证证据交给本计划的独立 `critic-gate`。未取得 `STATUS: PASS`，不进入收尾。

### 厚计划

按计划顺序逐个推进 Milestone：

1. 将当前 Milestone 施工包一次性交给 `coder-plus`。
2. Coder Plus 默认亲自实施；仅在并行、上下文隔离或专门能力收益明确时分派叶子。可写叶子不创建提交，局部结果由 Coder Plus 统一整合。
3. Coder Plus 对完成且已自验证的逻辑单元创建原子提交，自主决定粒度；Task 是自然边界但不强制与 commit 一一对应。
4. 收到 `STATUS: DONE` 后，检查其 DELEGATION、DEVIATIONS、CHANGES、COMMITS、VERIFICATION 与可选的 LEARNINGS，并确认所有 Milestone-owned 改动均已提交、工作区相对开工 Git 基线只保留未变化的既有改动。将 LEARNINGS 作为候选事实或认识暂存；没有 LEARNINGS 不构成缺陷。
5. 以开工 `HEAD`、交付 `HEAD`、两者间提交和干净的 Milestone-owned 状态作为稳定 gate handoff，由当前计划的 gate reviewer 核验整个 Milestone。
6. 只有 `STATUS: PASS` 后，才进入下一 Milestone；进入前完成一次 `fresh` / `retain` 连续性决策，并按决策创建新的 Coder Plus 会话或在当前会话中发送新的 Milestone 施工包。后续 Milestone 若提供新证据，Orchestrator 合并、修正或撤销暂存候选。

Orchestrator 不干预 Coder Plus 的内部 Task 分派，也不为其叶子增加独立 gate。叶子完成只代表局部输入；Milestone 是否完成，以 Coder Plus 的统一验证和计划级 gate 为准。

Coder Plus 若在已有提交后返回 `STATUS: BLOCKED`，必须报告已完成提交、未提交状态和剩余边界；Orchestrator 保留这些恢复点但不得推进下游。事实性输入补齐且当前 Milestone 基线未变时可续用原执行会话；这条续用规则只覆盖当前 Milestone 的修复或补证，不替代进入下一 Milestone 前的 `fresh` / `retain` 决策。若需要改变目标、范围、验收、设计或 Milestone 边界，则按结构性偏差回流 `go-spec`。

## 5. Gate 生命周期

一个批准计划只建立一个 gate reviewer，并在全部节点、FAIL 修正和 Gate 要求的补证轮次中持续复用。

- 薄计划由 Orchestrator 实施：从计划开始创建一个独立 `critic-gate`，并持续复用。
- 厚计划由 Coder Plus 实施：Orchestrator 兼任整个计划的 gate reviewer，审查他人产出不属于 self-critique。
- 实施者负责 self-verification，但不能作最终 gate。
- 同一 reviewer 只读取当前节点基线、实现结果、验证证据和已接受偏差；不重复 strict，也不重读无关计划层。

gate 对照批准计划当前节点判断：验收是否满足、实现是否忠实、下游契约是否保持、是否引入回归。实现方式可以不同，但必须向 reviewer 如实披露；Coder Plus 通过 DEVIATIONS 记录。

commit 是施工持久化检查点，不是 gate 凭证。gate 审查当前 Milestone 的完整最终状态、验证证据和偏差，不以提交数量或拓扑作为 PASS 条件。`STATUS: DONE` 时若仍有 Milestone-owned staged、unstaged 或 untracked 改动，不得进入 gate。Coder Plus 交付 gate 时冻结受审 `HEAD` 与提交历史；之后若 gate `FAIL`，修复以追加提交进入同一审查生命周期，不改写 reviewer 已见的提交。

`STATUS: FAIL` 时，将阻断项交回原执行者修正；条件允许时延续同一执行会话。修正后仍由同一个 gate reviewer 复核。`STATUS: BLOCKED` 按 `SKILL.md` 的缺失项规则处理，补齐必要证据后复用原 reviewer。

`PASS + UNVERIFIED` 只允许包含不影响 Gate 结论的事项，由 Orchestrator 完成直接验证，不自动回传 reviewer。若补证与已审声明矛盾、暴露缺陷或导致实现变化，则恢复原 Gate 生命周期；决定结论所必需的证据未确认时，Gate 应返回 `BLOCKED` 而不是 `PASS`。

gate 发现下列情况时，不继续局部修补：

- 需要修改目标、范围或验收标准；
- 需要改变已批准的设计或 Milestone 边界；
- 当前实现暴露出计划无法成立。

此时停止施工，回到 `go-spec` 记录变更并重新取得 fresh `critic-strict` PASS。受影响计划重新批准后，重新建立 gate 生命周期。

## 6. 提交与计划收尾

提交职责按施工层级划分：

- 薄计划由 Orchestrator 自行实施，并按用户授权与仓库规则创建提交。
- 厚计划由 Coder Plus 创建当前 Milestone 内的原子提交；其叶子不提交。提交只包含该 Milestone 拥有的改动，不得混入用户或其它工作单元的变化。
- 未特别授权时，Coder Plus 只在当前检出分支创建本地追加提交，不 push、不操作远程、不改写既有历史。更宽或更窄的 Git 权限由施工包显式声明。
- gate PASS 只表示当前 Milestone 可以推进，不要求 Orchestrator 再创建包装提交或空提交。Orchestrator 只有在自己产生实际改动时才提交。

若当前执行 Agent 的更高优先级运行时约束禁止创建本地提交，Orchestrator 必须改用具备完整读写、命令与叶子分派能力的独立 Agent，并注入完整 `subagents/coder-plus.md` 合同。内置工具、Rex app 或其他派遣入口不构成职责例外；没有满足能力矩阵的 Agent 时返回 `STATUS: BLOCKED`，不得静默改由主会话代为提交。

全部实施节点 PASS 后，只运行一次 `pruner`，并提供本计划实际触及的文件边界。Pruner 自行派 `scout` 核验清理目标，只执行 `SAFE` 项；完成后直接验证，不再回到 critic-gate。Pruner 不提交；计划级清理产生的实际改动由 Orchestrator 收口提交。

Pruner 不在每个 Task 或 Milestone 后运行。若计划尚未完整执行，例如评估只观察前一至两个 Milestone，则不触发计划级收尾。

计划级清理和最终验证完成后，Orchestrator 必须处理本计划的候选 LEARNINGS：合并重复项，补充实现证据，区分已确认事实、待 Human 判断的项目约定和仅适用于本次工作的局部观察。随后主动向 Human 发起简短复盘；每条先给一句话结论，再给一段说明背景、证据与适用范围。没有候选时也明确说明没有新的可复用认识。Human 确认后，才将具有长期复用价值的内容按 `raw -> wiki` 收录 Simple Wiki；未确认、争议或一次性内容不写入 wiki。

## 7. 交付

完成意味着：

- 所有计划节点均已通过同一 gate reviewer；
- 必要的实现提交与计划级收尾提交已按职责完成；
- 计划级 Pruner/Scout 收尾已完成；
- 最终验证覆盖完整交付，而不只是单个叶子或节点。
- 候选 LEARNINGS 已完成计划级汇总，并已向 Human 发起复盘；Human 确认的可复用内容已收录或明确无需收录。

交付前检查 MAJOR 台账：所有条目必须为 `RESOLVED` 或 `ACCEPTED`。若未关闭条目实际阻断下一步决策或执行，将其升级为 FATAL，停止交付并按 Strict 生命周期处理。向用户汇报最终结果、关键偏差、验证证据、未阻断事项，以及任何未能完成的验证。不要复述子代理过程日志。
