# Dispatch Contract

## Eval Host 派遣原则

Eval Host 只发送当前阶段 prompt、列入 manifest 的可见工件路径、对应 repo 路径，以及实际可用的技能路径。不要概括隐藏 Truth Card，也不要把观察断言改写进 prompt。

所有阶段使用 fresh 会话，只有 E-thick Orchestrator 自身跨两个 Milestone 持续。E-thick 内的 Coder Plus 每个 Milestone 都要有独立施工派遣；跨 Milestone 是否 fresh 或 retain 由连续性决策决定，retain 时必须记录理由、保留上下文和新节点边界。被测线程内部是否派遣、续派或自行完成，由当前 yes-subagents 合同决定。

## Step 1 输入

- 当前 case 的 `Decision.md`
- 当前 case 的 `Draft.md`
- 当前 case 的隔离 repo
- go-spec skill 路径
- yes-subagents skill 路径
- 当前 case 的 Step 1 prompt

禁止输入：Truth Card、oracle、断言、另一 case、历史 eval 报告、Step 2 prompt。

## Step 1 保留工件

Eval Host 保留完整 transcript 供评分，但 Step 2 只接收：

- `approved-plan.md`
- `Implement.md`
- 厚计划的 `Milestone-1.md`、`Milestone-2.md`
- `strict-final.md`：最终 verdict 与最小 PASS 凭证
- `open-items.md`：未阻断事项；没有时正文写 `None`

`self-review.md` 与 strict 各轮 transcript 只用于 Step 1 观察，不进入 Step 2 handoff。

若 strict 未 PASS、计划缺少必需工件或出现未解决 blocker，不启动对应 Step 2。

## Step 2 输入

- 当前 case 的隔离 repo
- Step 1 handoff 工件
- yes-subagents skill 路径
- 当前 case 的 Step 2 prompt

禁止输入：Decision/Draft 的单独副本、Step 1 transcript、self-review、strict 修正历史、Truth Card、oracle、断言、另一 case。

批准计划内部仍含冻结 Decision/Draft 属正常真源结构，不要求 Eval Host删节主计划。

## 证据采集

每个阶段完成时立即记录：

- session ID、父 session ID、角色与模型；
- 开始/结束时间、状态与异常；
- 可见输入的实际路径和哈希；
- 输出工件路径和哈希；
- 子代理树、每次派遣的角色、任务边界与结果；
- 每个会话的 input、cache read、output token 与费用；
- direct verification、strict 与 gate verdict。
- Milestone 开工/交付 HEAD、本地 commit 的创建会话、SHA、用途与所属 Milestone、交付时 owned worktree 状态，以及是否存在 push 或受审后历史改写。

token 字段缺失时使用 `null` 并说明来源缺失。不得把缺失记为 0，也不得遗漏嵌套叶子。

## 无效运行

出现以下任一情况，将受影响 case 标记为 INVALID，不判 skill PASS/FAIL：

- 模型或服务商错误导致阶段未完成；
- 超时或被外部中断，且没有完整终态；
- transcript 或派遣树无法取得；
- repo 不是由本包准备的干净副本；
- 隐藏材料被提供给被测线程；
- 阶段收到 manifest 之外的上游 transcript 或另一 case 内容；
- Eval Host 代替被测线程完成了关键计划或施工判断。

业务实现失败、计划错误、错误分派或 gate 缺失本身不是 INVALID，应作为有效失败记录。
