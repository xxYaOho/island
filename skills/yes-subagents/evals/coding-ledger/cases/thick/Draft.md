## Draft Plan

- 结构总览：银行 adapter 将各自 CSV 行转换为规范交易候选；reconciliation service 统一校验、分类并提交；store 只负责账本读写。report service 从规范交易按周期过滤，再按 target/category 聚合；CLI 提供兼容入口、统一导入和 report 命令。
- 关键契约：adapter 输出规范交易候选或带来源定位的 rejected；reconciliation 输出 added、duplicates、conflicts、rejected，只有 added 进入 store；report 输入 period、anchor、group-by，输出 period 边界与稳定排序的统计 rows。完整字段和分类规则以 Decision 为准。
- 文件结构：保留 `ledger/alpha.py` 并调整为 adapter；新增 `ledger/beta.py`；修改 `ledger/service.py` 承担统一 reconciliation；修改 `ledger/store.py` 保持兼容读写；新增 `ledger/report.py`；修改 `ledger/cli.py`；扩展 `tests/` 中 adapter、reconciliation、CLI 与 report 的外部行为测试。
- 风险与未决：多银行原始字段不能泄漏到 report；同键冲突不能被普通 duplicate 吞掉；行级 rejected 与文件级原子性需要分开；周期必须先转到业务时区再切边界；target 不允许为了报表好看而做未批准实体合并。无产品未决项。
- 里程碑草案：第一阶段建立规范交易、Alpha/Beta adapter、稳定 reconciliation 与来源证据；第二阶段在第一阶段已验证模型上增加周/月 target/category 统计。第二阶段阻塞于第一阶段模型成立。
