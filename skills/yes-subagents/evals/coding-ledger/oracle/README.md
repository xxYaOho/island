# Business Oracle

本目录仅供 Eval Host 与评分者读取。被测线程不可见。

`expected.json` 是人工冻结的业务真值。`verify.py` 只通过公开 CLI 和账本 JSON 验证，不导入被测实现的内部函数。

## 固定调用

薄层：

```bash
python3 -m ledger.cli import-alpha \
  --ledger <temporary-ledger.json> \
  --account alpha-main \
  --file <thin-alpha.csv> \
  --dry-run
```

厚层 M1 按顺序执行：

1. Alpha primary：`import-csv --bank alpha --account alpha-main`
2. Beta primary：`import-csv --bank beta --account beta-card`
3. Alpha primary 重复导入
4. Alpha conflict
5. 兼容入口 `import-alpha` 再读 thin input

厚层 M2 在 M1 数据集上分别请求：

- week / `2026-09-03` / category
- week / `2026-09-03` / target
- month / `2026-09-15` / category
- month / `2026-09-15` / target

所有 report 使用 `--format json`。verifier 忽略 rows 的合法稳定排序差异，但会重复调用并要求两次原始 JSON 结果完全一致。

## 统计口径

- `cashflow_minor`：账本带符号金额之和。
- `spend_minor`：expense 取绝对值，refund 取负绝对值，income 为 0。
- 周区间为 `[2026-08-31, 2026-09-07)`。
- 月区间为 `[2026-09-01, 2026-10-01)`。

expected 中的 report rows 使用以 group 为键的对象，避免把合法排序选择误判为业务错误。
