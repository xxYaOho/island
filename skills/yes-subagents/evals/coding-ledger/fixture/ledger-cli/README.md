# Local Ledger CLI Fixture

一个只依赖 Python 标准库的本地账本基线。当前支持：

```bash
python3 -m ledger.cli list --ledger data/ledger.json
python3 -m ledger.cli import-alpha \
  --ledger data/ledger.json \
  --account alpha-main \
  --file path/to/alpha.csv
```

基线只实现 Alpha Bank 导入与来源 ID 去重。它尚不支持：

- `--dry-run`
- `import-csv`
- Beta Bank
- 冲突与 rejected 行报告
- 周/月统计

运行基线测试：

```bash
python3 -m unittest discover -s tests -v
```
