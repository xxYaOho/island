---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-18-critic-strict-major-ledger.md
---
# critic-strict MAJOR 台账：yes-designer 工作流 v5

- 日期：2026-10-18
- 审查生命周期：Round 1 → Round 5（同一 reviewer，FULL），最终 `STATUS: PASS`
- 批准版本：`2026-10-18-yes-designer-design-work-loop-v5.md`（874 行，sha1 `42aa31c…`）
- 规则：下一阶段会直接消费的 MAJOR 必须在消费前关闭；其余 MAJOR 在最终交付前必须变为 `RESOLVED`（已修正并验证）或 `ACCEPTED`（Human 明确接受并记录理由）。
- 状态：`CLOSED`。v5 已被 `2026-10-18-yes-designer-design-work-loop-v6.md` 取代，M1–M6 依附的机制均已删除，不再适用（见 v6 §13）。

## MAJOR（carry-forward）

| ID | 问题 | 影响 | 责任方 | 最迟关闭点 | 状态 |
|---|---|---|---|---|---|
| M1 | 跨地图升版循环与 FREEZE 提交序：§8.4 的串行化是行为约束而非可校验工件；§6.3 检查 1 在检查 2–10 之前就更新 `current.yaml` 并级联，失败时无回滚 | 跨地图共享基线时版本抖动与无谓重冻 | lead（规范修订） | 首个跨地图共享基线切片开工前 | OPEN |
| M2 | screenshot-pixel 的 design-export 期望值不可表达：`source_anchors` kind 只有 `sketch`/`prototype-dom`，截图两者都不是 | 该模式无法通过 FREEZE，或被伪造 anchor | lead（规范修订） | 首次使用截图 pixel 模式前 | OPEN |
| M3 | env 重批不可忠实重放：`golden/approval.yaml` 缺实现 commit / 构建引用；capture_env 承载者列举不一致 | 环境变化后重抓可能把未批准视觉固化进 golden | lead（schema 修订） | 首次 env 重批前 | OPEN |
| M4 | 期望值契约错误缺少 needs-decision 回路：只有 setup/marker/hooks 被归为基线契约错误 | 实现无错但期望值错误时，切片反复 building | lead（状态机修订） | 首次出现期望值错误前 | OPEN |
| M5 | 附录 A/B 状态与正文不符：MAJOR-1/MAJOR-6 标"已修复"但实际 PARTIAL；MINOR/UNVERIFIED 的 hash 与固定方式描述未完全修正 | Human 依赖收口表误判范围 | lead（文档修正） | 批准 v5 前 | OPEN |
| M6 | layout 完整性无 FREEZE 检查，LAYOUT 层可空跑；`fidelity=layout` 的 human-first-review 首轮不执行 LAYOUT | layout 保真模式被静默放行 | lead（门禁修订） | 首个 `fidelity=layout` 切片前 | OPEN |

## MINOR（carry-forward，随交付披露）

1. §10.1 的 hash 标注仍不精确（`git hash-object` 实为 `5c92fdad…`；文件内容 sha1 为 `5b19eb9…`），且 `skills/pro` 未跟踪，提交后需重核。
2. §7.2 "首轮可执行的层"表头语义不清（人类层 7 在 golden 更新/阈值外差异时同样适用）。
3. §8.3 "golden-updated" 行的"从"列不是状态，措辞可能被读成更新方自身被级联。
4. §7.4 "像素层必须与 golden 对比" 与 §4.3 "oracle 为 golden 时不重复生成 regression 条目" 字面冲突。
5. design-export 的导出工具/版本在 oracle schema 中无字段。
6. `rules.yaml` 与 `viewports.yaml` 的 approval schema/记录位置未定义。
7. §7.3 Sketch pixel 的 computed 期望同时写了 `computed_expectations` 与"源页面测量/golden 测量"，优先级未定义。
8. §11 示例的 VERIFY 仍写"结构 → 几何 → 像素"，未更新为七层。
9. §10.3 的"两者版本号在 docs/island/designer/ 的记录中绑定"未定义记录位置与格式。

## UNVERIFIED（技术验证轮）

- 生成器确定性、`must_import` / `diff_scope` 推导、golden measurements 采集/重放、hash/env 校验、FREEZE 升版与跨地图级联、DPR/scale + SSIM 可复现性、handoff 接受度、fixture/harness 可用性、两文件版本绑定记录位置。

## ESCALATE（已移交 Human）

- 配套 `DESIGN.md` 草案仍为未批准草案（版本 0.1），与 v5 联合批准且绑定点尚无落盘位置。
- `sketch-copilot-pro` 工作区 `skills/pro` 未跟踪、有未提交改动；版本固定需在提交后重做。
- yes-subagents 的 go-spec/dispatch 世界观与 v5 的 `.tmp` 派发简报格式未做实现验证。
- 空 `docs/DESIGN.md` 与目标仓库文档布局待 Human 决定。
