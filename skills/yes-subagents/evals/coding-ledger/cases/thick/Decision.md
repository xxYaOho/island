# Multi-bank Reconciliation And Analysis Plan

> 2026-09-08 · 状态：已对齐

## Problem Statement

本地账本当前只支持 Alpha Bank，且只能粗略跳过已存在的来源 ID。用户同时持有不同银行账户，重复下载或交叉导入账单时，需要可靠地区分新增、重复、冲突和无效记录。缺少统一来源追踪与稳定分类时，用户无法确认账本是否真实反映银行记录。

交易入账后，用户还需要按周和月查看交易对象与分类统计。若分析直接依赖各银行的原始字段，跨银行结果会漂移，退款也无法正确冲减消费。

## Solution

先建立统一的多银行对账层：Alpha 与 Beta CSV 都转换为同一个规范交易模型，再以稳定来源唯一键分类并保留来源证据。随后在规范账本之上增加周度、月度分析，可按 target 或 category 分组，同时输出现金流与消费口径。

## User Stories

1. 作为持有多个银行账户的用户，我希望 Alpha 与 Beta CSV 都能导入同一本地账本，以便集中对账。
2. 作为会重复下载账单的用户，我希望系统稳定区分新增、重复和冲突，以便多次导入不会改变既有正确记录。
3. 作为需要核查异常输入的用户，我希望每条交易保留来源信息并报告 rejected 行，以便追溯原始 CSV。
4. 作为查看消费趋势的用户，我希望按周或月查看 category 统计，以便理解各类支出。
5. 作为核对交易对象的用户，我希望按周或月查看 target 统计，以便识别主要商户和收付款对象。
6. 作为包含退款记录的用户，我希望退款冲减消费但仍保留真实现金流，以便统计不会夸大支出。

## Constraints

- 保持现有账本 JSON 和 `import-alpha` 命令兼容；不要求已有用户迁移数据。
- 来源唯一键为 `bank + account + transaction_id`。
- fixture 仅使用 CNY；金额存储为分单位整数。
- 交易时间保存带时区的 ISO 8601；周期归属使用 `Asia/Shanghai`。
- `target` 保留银行字段语义，只规范空白，不做跨银行实体合并。
- category 固定为 `餐饮`、`日用`、`收入`、`转账`、`未分类`。
- 行级错误进入 rejected，合法行继续处理；文件级错误不得产生部分写入。
- 同键冲突不得覆盖既有交易。

## Implementation Decisions

1. 增加统一命令 `import-csv --bank alpha|beta --account <id> --file <csv>`，同时保留 `import-alpha` 兼容入口。
2. 规范交易至少包含：bank、account、transaction ID、occurred_at、amount_minor、currency、kind、target、category 和 source。
3. source 至少保存原始 CSV 文件名、数据行号和原始字段对象。
4. duplicate 要求相同来源唯一键及相同的时间、金额、币种、kind 与 target。category-only 变化仍按 duplicate 处理，沿用既有分类。
5. conflict 表示相同来源唯一键，但时间、金额、币种、kind 或 target 任一不同。冲突进入结果列表，不写入也不覆盖。
6. import stdout 使用稳定 JSON，至少包含 added、duplicates、conflicts、rejected 计数及每个 conflict/rejected 的来源定位。
7. Alpha 的中文 category 直接映射；Beta 的 `Dining`、`Groceries`、`Income`、`Transfer` 映射为对应中文，空值或未知值为 `未分类`。
8. kind 使用 `expense`、`income`、`refund`；amount_minor 表示现金流，expense 为负，income/refund 为正。
9. 增加 `report --period week|month --anchor <date> --group-by category|target --format table|json`。
10. 每个统计行包含 group、transaction_count、cashflow_minor、spend_minor。spend_minor 中 expense 为正支出、refund 为负支出、income 为 0。
11. week 使用 anchor 所在的周一至周日，month 使用 anchor 所在自然月；JSON 输出包含明确的 period_start、period_end 和 rows。
12. table 是默认格式，JSON 用于稳定的自动化核验。

## Testing Decisions

- 通过 CLI 黑盒测试覆盖 Alpha、Beta 导入，不依赖 adapter 内部实现。
- 覆盖 exact duplicate、同外观不同交易号、同键关键字段冲突、行级 rejected 与文件级失败。
- 重复执行同一导入序列后，账本交易集合必须保持一致。
- 验证每条新交易的来源文件、行号与原始字段可追溯。
- 使用固定 anchor 验证周一/周日、月末/月初边界。
- 分别核对 category 与 target 的 transaction_count、cashflow_minor 和 spend_minor，并包含 refund 冲减。
- 保持既有 list、`import-alpha` 与基线测试全绿。

## Out of Scope

- 不支持真实银行 API、自动下载账单或任意 CSV 自动识别。
- 不支持外汇换算、多币种汇总、账户余额核对或银行间转账配对。
- 不做 target 实体合并、模糊匹配、AI 分类或用户可编辑分类规则。
- 不做数据库迁移、图表、Web UI、预算或预测。
- 不要求并行处理大文件或性能基准。

## Further Notes

稳定对账优先于报表丰富度。分析只能建立在已经验证的规范交易与来源分类之上。
