# Strict Convergence Eval

验证 strict 迭代（判级锚 + 分诊 + 减法）在真实草案审查中是否达到预期行为。

用例来源：`docs/1018-strict-case` 的 yes-designer 草案 v4（857 行）。

## 用例

| ID | 名称 | 测试对象 | 输入 | 观察目标 |
|---|---|---|---|---|
| 1 | e1-strict-anchor | fresh critic-strict | v4 + 判级锚 + R3 台账 | FATAL 绑定锚；形式完备性不判 FATAL；验收合同缺失保留 FATAL 资格 |
| 2 | e2-lead-triage | fresh Orchestrator | v4 + R4 report + 判级锚 | 先分诊后修正；只修真缺陷 FATAL；删除/新增验收面归取舍并升级 |

## 轮次

- `iteration-11`（round 1）：with_skill vs old_skill。发现：减法机制生效（附录删除、取舍升级），但判级锚导致召回收缩（with 1 FATAL vs old 3，漏掉执行层与 diff 基线）。E2 的 prompt 差异污染了对比。
- `iteration-12`（round 2）：去掉 old baseline，只测 with_skill；E2 使用中性 prompt；断言改为绝对行为检查，并新增「验收合同缺失保留 FATAL」「删/增验收面归取舍」两条校准断言。old 结果复用 iteration-11，作为历史参照。

## 输入材料

- `fixture/yes-designer-work-loop-v4.md`：857 行草案。
- `fixture/yes-designer-work-loop-v4-report.md`：R4 原始审查报告（1 FATAL / 7 MAJOR）。
- `fixture/yes-designer-work-loop-v3-report.md`：R3 报告，含 R2 台账。
- `fixture/ANCHOR.md`：判级锚（第一用途、4 条成功标准、非目标、不可接受失败形态）。

## 运行约定

- 仅 with_skill：`<SKILL_ROOT>` 指向当前 `skill/`。
- 输出目录：`yes-subagents-workspace/iteration-12/<eval-name>/with_skill/outputs/`。
- 每个 run 另存 `session.md` 供评分与人工复核。
