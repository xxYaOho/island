# Alpha CSV Dry Run Plan

> 2026-09-08 · 状态：已对齐

## Problem Statement

本地账本已经能导入 Alpha Bank CSV，但命令会立即写入账本。用户在拿到新的银行导出文件时，无法提前确认将新增多少条、多少条已经存在，以及输入是否包含冲突或无效行。直接尝试导入会降低对账信心。

## Solution

为现有 Alpha Bank 导入命令增加 `--dry-run`。预演必须走与真实导入相同的解析、规范化和对账路径，返回确定的分类计数，但不修改账本。用户确认结果后仍可使用原命令完成真实导入。

## User Stories

1. 作为本地账本用户，我希望在导入 Alpha Bank CSV 前预览对账结果，以便确认文件是否符合预期。
2. 作为重复下载银行账单的用户，我希望预演能识别已经存在的交易，以便避免把重复记录误认为新增。
3. 作为谨慎维护本地数据的用户，我希望 dry-run 保证账本逐字节不变，以便安全地反复检查输入。

## Constraints

- 保持现有 Alpha Bank CSV 格式、已有导入命令和账本 JSON 兼容。
- 来源唯一键继续使用 `bank + account + transaction_id`。
- 金额使用 CNY 分单位整数；时间使用带时区的 ISO 8601。
- `target` 只做首尾去空白与连续空白折叠；不做商户实体合并。
- 行级错误不阻断其他行的预演；文件级解析错误直接失败。
- dry-run 期间不得写入账本、临时替换账本或改变账本文件内容。

## Implementation Decisions

1. 命令形态保持现有 `import-alpha`，增加布尔选项 `--dry-run`。
2. dry-run 输出 JSON 对象，固定包含 `would_add`、`duplicates`、`conflicts`、`rejected` 四个整数。
3. duplicate 表示来源唯一键与既有交易相同，且关键业务字段一致。
4. conflict 表示来源唯一键相同，但时间、金额、币种、kind 或 target 至少一项不同；预演不覆盖既有值。
5. rejected 表示当前 CSV 行无法形成有效规范交易；合法行继续参与计数。
6. dry-run 与真实导入共享解析和分类结果，区别只在最终是否写入。
7. 输出顺序和 JSON 字段稳定，便于脚本读取。

## Testing Decisions

- 从 CLI 外部行为验证 dry-run 汇总，不断言内部函数调用。
- 在临时账本副本上执行预演，比较执行前后字节，确认没有任何写入。
- 覆盖新增交易与既有 duplicate 同时出现的输入。
- 保持现有真实导入和 list 行为回归测试全绿。

## Out of Scope

- 不增加 Beta Bank 或其他银行格式。
- 不增加周度、月度或分类统计。
- 不迁移账本 schema，不引入数据库。
- 不增加交互式确认、自动导入或 GUI。
- 不实现 target 实体合并、AI 分类或用户分类规则。

## Further Notes

本需求只有一条连续实施路径：让现有导入管线支持“分类但不提交”。产品行为可以作为一个整体直接验收。
