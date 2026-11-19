---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/1018-strict-case/README.md
---
# critic-strict 案例：yes-designer 工作流草案（Round 1–5）

本目录是一次完整 Strict 审查生命周期的文档快照，用于评估与优化 `critic-strict`。

- 案例对象：`yes-designer` 设计推进工作流草案
- 生命周期：Round 1（初始）→ Round 5（PASS），共 4 次修正轮
- 最终结论：v5 `STATUS: PASS`，6 项 MAJOR / 9 项 MINOR 作为 carry-forward
- 说明：目录名按 `docs/strict-case` 创建（需求原文写作 `strici-case`，按 strict 修正；如需保留原拼写可直接改名）

## 目录结构

```text
docs/strict-case/
  README.md
  v1/
    yes-designer-work-loop-v1.md        Round 1 审查对象（742 行）
    yes-designer-work-loop-v1-report.md critic-strict Round 1 反馈（FAIL）
  v2/
    yes-designer-work-loop-v2.md        Round 2 审查对象（538 行）
    yes-designer-work-loop-v2-report.md Round 2 反馈（FAIL）
  v3/
    yes-designer-work-loop-v3.md        Round 3 审查对象（796 行）
    yes-designer-work-loop-v3-report.md Round 3 反馈（FAIL）
  v4/
    yes-designer-work-loop-v4.md        Round 4 审查对象（857 行）
    yes-designer-work-loop-v4-report.md Round 4 反馈（FAIL）
  v5/
    yes-designer-work-loop-v5.md        Round 5 审查对象（874 行）
    yes-designer-work-loop-v5-report.md Round 5 反馈（PASS）
  final/
    critic-strict-major-ledger.md       PASS 后的 carry-forward 台账
```

每份 report 均为该轮 reviewer 原始输出的完整转录，仅追加了元信息头（对象、模式、结论、统计）。行号均指向同目录的 draft。

## 轮次概览

| 轮次 | 对象 | 结论 | FATAL | MAJOR | MINOR | 本轮主要关闭 |
|---|---|---|---|---|---|---|
| Round 1 | v1 | FAIL | 4 | 11 | 7 | 识别状态持久化、冻结门禁、降级自判、无设计稿冲突 |
| Round 2 | v2 | FAIL | 2 | 12 | 6 | F1/F3/F4 CLOSED；F2 转 PARTIAL（断言不可执行） |
| Round 3 | v3 | FAIL | 2 | 8 | 6 | state 维度进入基线；暴露 inherit 预演循环（FATAL-N1） |
| Round 4 | v4 | FAIL | 1 | 7 | 7 | 七层验收、per-state anchor、SSIM 归一 |
| Round 5 | v5 | **PASS** | 0 | 6 | 9 | 无剩余 FATAL；MAJOR/MINOR 转 carry-forward |

每版草案自带附录 A/B，记录上一轮 findings 的修复位置与状态；可与对应 report 对照阅读。

## 可用于优化 strict 的观察点

1. **证据—结论匹配是最高频失分点**：多轮都出现「附录自述已修复，但正文仍是 PARTIAL」（Round 2 附录、Round 4/5 MAJOR-5、Round 3 M11）。strict 将修复对照表当作独立证据源复核的做法有效，可作为固定检查项。
2. **修正轮会引入新缺陷**：Round 3 的 FATAL-N1（inherit 新状态预演循环）由上一轮 state 修复引入。修正轮 FULL 复核是必要机制，不是重复劳动。
3. **判级尺度可校准**：案例中既有「流程合同级」FATAL（state 维度、期望值出处），也有偏向实现/工具细节的 MAJOR（SSIM 参数、hash 算法、approval schema）。可用于评估 strict 在草案阶段应把执行细节压到 MAJOR 还是 FATAL。
4. **收敛速度**：4 次修正轮从 4 FATAL 收敛到 0 FATAL，但 PASS 时仍留 6 项 MAJOR。可用于评估「最大 4 次修正 + carry-forward 台账」的节奏是否合理。
5. **输出格式可复用性**：report 里的章节名 + 行号 + 证据摘录，使修复可以逐条定位。对比不同 strict 版本的输出格式时，这是可量化的基线。

## 使用建议

- 把 `v1`–`v5` 作为回归案例：对同一轮 draft 分别用不同版本 / 不同 intensity 的 strict 跑审查，比较「是否漏掉关键 FATAL」「是否产生无法定位的泛泛结论」。
- 不建议把「v5 必须 PASS」当作唯一成功标准；更有价值的指标是：关键 FATAL 是否在前两轮被捕获、修正后是否被确认关闭、以及 carry-forward 是否被如实标注。
- 注意：v5 的 PASS 是 reviewer 结论，不代表 Human 已批准。草案仍为 `草案 v5`，最终审批与联合批准（配套 DESIGN.md 草案）需 Human 完成。

## 原始文件

快照派生自仓库内的原始笔记（完整版本历史见 `docs/notes/`）：

- v1：`2026-10-17-yes-designer-design-work-loop-draft.md`
- v2：`2026-10-17-yes-designer-design-work-loop-v2.md`
- v3：`2026-10-18-yes-designer-design-work-loop-v3.md`
- v4：`2026-10-18-yes-designer-design-work-loop-v4.md`
- v5：`2026-10-18-yes-designer-design-work-loop-v5.md`
- 台账：`2026-10-18-critic-strict-major-ledger.md`
