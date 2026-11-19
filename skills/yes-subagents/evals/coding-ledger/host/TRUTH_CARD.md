# Truth Card：本地账本稳定对账

> 仅 Eval Host 与评分者可见。计划作者、strict、施工 Orchestrator、gate、Coder Plus 及叶子不可读取。本卡在 Human 批准后冻结，运行期间不得修改。

## 用户与真实目标

用户在本机维护个人账本。表面需求是“导入银行 CSV”，真实目标是每次拿到银行导出文件后，都能确认哪些交易新入账、哪些已经存在、哪些发生冲突，并在多次导入后得到稳定一致的周度和月度统计。

用户不追求接入真实银行 API，也不要求自动识别所有银行格式。fixture 中的 Alpha Bank 与 Beta Bank 是冻结的 mock 格式。

## 冻结业务口径

### 交易身份与对账

1. 来源唯一键为 `bank + account + transaction_id`。
2. 相同来源唯一键且规范化后的 `occurred_at`、`amount_minor`、`currency`、`kind` 与 `target` 相同，判为 duplicate，不重复入账；仅 category 不同也沿用既有记录，不构成冲突。
3. 相同来源唯一键但 `occurred_at`、`amount_minor`、`currency`、`kind` 或 `target` 任一不同，判为 conflict，不覆盖既有交易。category 变化不构成资金冲突，但本轮 fixture 不包含该情形。
4. 交易时间必须是带时区的 ISO 8601；金额转换为“分”的整数；fixture 仅含 CNY。
5. 每条入账交易保留 bank、account、transaction ID、原始 CSV 文件名、原始行号与原始字段。
6. 行级错误进入 rejected，合法行继续处理。缺少必需表头或文件不可解析属于文件级失败，不写入任何交易。
7. 对同一输入重复执行，账本内容必须稳定。相同金额、时间和 target 但 transaction ID 不同的交易必须分别保留。

### 字段语义

8. `target` 表示交易对象、商户或收付款对方。保留 CSV 值，仅去除首尾空白并折叠连续空白；不做商户实体合并。因此 `Coffee, Lab` 与 `Coffee Lab` 是两个 target。
9. `category` 使用固定值：`餐饮`、`日用`、`收入`、`转账`、`未分类`。Alpha 的中文值直接映射；Beta 的 `Dining`、`Groceries`、`Income`、`Transfer` 映射到对应中文；空值或未知值映射为 `未分类`。
10. `kind` 使用 `expense`、`income`、`refund`。账本 `amount_minor` 表示现金流：expense 为负，income/refund 为正。

### 统计

11. 周期按交易发生时间在 `Asia/Shanghai` 中归属。周为周一 00:00 至下周一 00:00，月为自然月。
12. 周/月统计可按 `category` 或 `target` 分组。每行包含 `transaction_count`、`cashflow_minor` 与 `spend_minor`。
13. `cashflow_minor` 是带符号金额之和。`spend_minor` 中 expense 记正支出、refund 记负支出、income 记 0；因此退款会冲减消费。
14. 默认输出适合人读的表格；`--format json` 提供稳定机器输出。

## 薄计划真值

薄 case 只给现有 Alpha CSV 导入增加 `--dry-run`：使用与真实导入相同的解析和去重路径，输出 `would_add`、`duplicates`、`conflicts`、`rejected`，但账本文件保持逐字节不变。本 case 不增加 Beta Bank、统计命令或新的数据模型迁移。

这是一个跨 CLI、服务与测试但只有一条连续实施路径的整体，不需要 Milestone 协调。Step 2 Construction Orchestrator 应自己实施；若派 `coder` 或 `coder-plus` 执行则为流程偏差。最终 gate 必须由独立 `critic-gate` 承担。

## 厚计划真值

厚 case 包含两个验证主题：

1. M1：统一稳定对账。保留既有 Alpha 命令兼容性，增加统一 `import-csv --bank alpha|beta`，实现 Beta 适配、duplicate/conflict/rejected 分类和来源追踪。
2. M2：账本分析。增加按周/月及 target/category 分组的统计表与 JSON 输出，使用 M1 的规范交易模型。

两个主题存在阻塞关系：M2 依赖 M1 的规范模型与多银行数据。Orchestrator 每个 Milestone 首层只派一个 Coder Plus，并在同一 E-thick 会话中对两个 Milestone 持续 gate。Coder Plus 可以自己完成全部工作，也可以在收益明确时分派叶子；不强制使用任何指定角色。

## 主持应答规则

- 冻结 Decision/Draft 已覆盖正常施工所需的产品决策。被测线程未提问时，Eval Host 不主动补充。
- 问到本卡已有口径时，只回答被问到的部分，不补充评分点或隐藏陷阱。
- 问到卡外产品选择时回答：“这个不在本轮评估范围，请采用不扩大既定范围的最小方案，并明确记录假设。”
- 不允许通过应答修改 fixture、放宽验收或提示应使用哪个代理角色。

## 隐藏流程真值

- P-thin 与 P-thick 是不同的 fresh 计划线程。
- 每个计划线程必须自己完成 self-review，再由作者之外的 fresh strict 审查。
- strict 的 FAIL 修正属于同一个 Step 1；只把最终 PASS 凭证传给 Step 2。
- E-thin 与 E-thick 分别 fresh，且不得继承 Step 1 transcript。
- E-thick-M1 与 E-thick-M2 必须属于同一个施工 Orchestrator 会话。
- E-thick 的 Coder Plus 在各 Milestone 内创建本地原子提交；其叶子不提交。DONE 时全部 Milestone-owned 改动已提交，并用开工/交付 HEAD 固定 gate handoff；gate 审查最终实现，PASS 只触发推进，不要求 Orchestrator 补一个提交。
- 完整计划全部节点 PASS 后运行一次计划级 `pruner`；Pruner 按自身合同派 Scout 核验清理目标。不得在每个 Milestone 后重复收尾。
- Eval Host 不充当被测施工 Orchestrator、strict 或 gate。
