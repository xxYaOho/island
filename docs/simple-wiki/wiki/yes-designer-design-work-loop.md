---
title: yes-designer 设计推进工作流
type: decision
created: 2026-10-18
updated: 2026-11-19
sources: [raw/yes-designer-design-work-loop-v6.md, raw/yes-designer-2026-10-16-design-collaboration-architecture.md, raw/yes-designer-2026-10-17-sketch-copilot-plus-adapter-boundary.md, raw/yes-designer-2026-10-17-design-md-framework-draft.md, raw/yes-designer-2026-10-18-p1-eval-report.md, raw/yes-designer-2026-10-18-p1-closeout-report.md, raw/yes-designer-2026-10-18-p1-validation-plan.md]
topic: yes-designer 设计工作环
tags: [yes-designer, work-loop, baseline, copy-commit, gate, DESIGN.md, P1]
status: current
context: 2

# yes-designer 设计推进工作流

现行方向以 [v6](../raw/yes-designer-design-work-loop-v6.md) 为准：2026-10-18 Human 已批准方向，§15 为 P1 补丁（与正文冲突时以 §15 为准）。v1–v5 及更早讨论已被取代，见[《工作环演进》](yes-designer-work-loop-evolution.md)。

## 问题、原则与流程

事故 B：Human 要求“复制既有页面再修改”，agent 仍从零重写。根因是复用决定只存在于对话中、验收只看视觉、agent 可把任务改判为 `new`。成功标准：从零重写被结构门禁拦住；冷启动只凭工件能判断下一步；agent 不能自行批准 `new` / `independent` / 修改共享组件或 golden；已批准区域退化能被机械发现。不追求设计稿的像素级自动判定。

判断归 agent 与 Human，机械归脚本。只设两处硬门禁：结构门禁与 golden 回归。只持久化 Human 决定过的内容；断言不落盘，VERIFY 从基线即时推导。审批绑定 git blob hash。

切片循环：`READ → BASELINE → BUILD → VERIFY → REVIEW → SETTLE`。`means: copy` 时必须先由脚本做 copy commit，再在 `delta_files` 内修改。越出基线必须停止并提 DEVIATION。结构硬门禁为 S1 文件范围、S2 区域存在、S3 preserve 骨架、S4 样式探针、S5 `rules.yaml`。P1 补丁还要求：`prototype_diff` 未决项阻断 approve；copy 从 `source_page.commit` 取源；delta 取最小区域并用嵌套子区域；S6 暂留作过渡守卫。`new`、`extend` 共享组件、`independent`、基线与 golden 均须 Human 明确批准。

## DESIGN.md 框架（配套草案，未批准）

[草案](../raw/yes-designer-2026-10-17-design-md-framework-draft.md)计划与 v6 联合批准，尚未生效。`DESIGN.md` 是项目设计范式总约束，对所有协作者生效；引用只能单向：范式 ← catalog ← baselines。修改权归 Human；lead 只可更新少数指针并追加 Known Gaps。缺失时直接复制 skill 内置中文模板，不访谈、不推迟。可机械检查的规则进入 `rules.yaml`，由 S5 执行。流程步骤名以 v6 正文为准。

## P1 验证与收尾

依据[计划](../raw/yes-designer-2026-10-18-p1-validation-plan.md)、[验证报告](../raw/yes-designer-2026-10-18-p1-eval-report.md)与[收尾报告](../raw/yes-designer-2026-10-18-p1-closeout-report.md)。P1 于 2026-10-19 由用户确认关闭：**可以有限投入使用，但门禁在真实项目上仍应作为 advisory，而不是自动放行。**

带 skill 的 fresh agent 能走完 ENTRY → BASELINE → COPY → BUILD → VERIFY；未声明的表格标题栏被拦住并转为显式决策。真实 antd 环境 G2 复测中 S1–S6 连续 3 次通过。可以依赖 copy commit、`prototype_diff` 未决阻断、审批绑定 blob，以及归属正确前提下的 S1/S2。不能完全依赖 S3/S4 的零漏报/零误报、真实预览带数据渲染，以及稳定写出嵌套区域 baseline。

主要发现：结构保持主要来自 copy commit 而非提示词；提问覆盖率比答案质量更能区分轮次；写入 `prototype_diff.decision` 比只留在对话里更稳；粗粒度 delta 会使 S3/S4 失效。完整嵌套区域 R2、E1–E6（尤其 E4 自授权）和视觉机械对比仍未验证。golden / V1 属于 P2。
