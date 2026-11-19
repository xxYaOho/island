## Draft Plan

- 结构总览：CLI 解析 `--dry-run` 后仍调用现有 Alpha parser 与 import service。service 先完成规范化和与账本的分类，再由调用方决定是否保存。真实导入保持原写入路径，dry-run 只序列化分类摘要。
- 关键契约：`import-alpha --ledger <path> --account <id> --file <csv> [--dry-run]`；dry-run stdout 为包含 `would_add`、`duplicates`、`conflicts`、`rejected` 的 JSON。来源身份与冲突规则以 Decision 为准。
- 文件结构：修改 `ledger/cli.py` 负责参数和输出；修改 `ledger/service.py` 负责可复用的分类结果与条件写入；按需要调整 `ledger/alpha.py` 暴露行级 rejected；修改 `tests/test_cli.py` 与 `tests/test_service.py` 覆盖预演及回归。
- 风险与未决：必须避免“先写入再回滚”的伪 dry-run；真实导入与预演若走两套分类逻辑会产生口径漂移。无产品未决项。
- 里程碑草案：略过。该变更只有一个可整体验证的实施主题，不需要多个里程碑协调。
