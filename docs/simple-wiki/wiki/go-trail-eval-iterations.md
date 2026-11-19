---
title: go-trail 评估迭代（原 go-fireside）
type: summary
created: 2026-09-22
updated: 2026-11-19
sources: [raw/go-trail-eval-report.md, raw/go-trail-eval-report-iteration-2.md, raw/go-trail-eval-report-iteration-3.md]
topic: go-trail 评估
tags: [go-trail, go-fireside, eval]
status: current
context: 1

# go-trail 评估迭代（原 go-fireside）

三份已验证报告针对当时名为 `go-fireside` 的 skill（现收拢为 `go-trail`）：[iteration-1](../raw/go-trail-eval-report.md)（v0.1.0，2026-09-22）、[iteration-2](../raw/go-trail-eval-report-iteration-2.md)（v0.1.1，2026-09-23）、[iteration-3](../raw/go-trail-eval-report-iteration-3.md)（v0.1.2 定向验证，2026-09-23）。执行模型为 glm-5.3-flash。跨迭代分数不可直接比较，因为合同、断言风格和 harness 隔离同时在变；可比的是结论。

## 稳定结论

1. **程序性合同是真实增量**：会话交接（邀请另开、摘要确认、生成交接 Prompt、交接后停止）在有 skill 时能走完，无合同的对照臂不会自发完成。iteration-2 交接三段合计 13/13 vs 5/13。
2. **风格型场景两臂基本同分**：倾听、拒站队、拒诊断等“不做 X”条款，当时基线模型裸跑即可满足。skill 的增量不在对话形状上。
3. 评测必须把对照臂与合同文本、项目上下文隔离，否则可得性会伪装成能力。iteration-1 曾出现对照臂经项目入口自行读取 SKILL 的污染事故。

## 合同修订的验证链

iteration-1 暴露 with_skill 的引用不实、歧义安全信号确认过晚，以及“抛硬币”类随机装置是否越线的产品问题。v0.1.1 补了引用忠实、随机装置禁令和安全确认优先后，iteration-2 区分度从约 +0.08 升到约 +0.40；引用不实降为轻度缩写，即时风险禁令成为硬区分（6/6 vs 3/6），但歧义信号门禁两臂仍未完全通过。

v0.1.2 针对反事实修辞和更明确的安全确认措辞做定向验证：eval-2 由 4/5 升到 5/5，eval-7 由 2/4 升到 5/5（断言集有拆分，分数不可逐条对齐，但先前失败的门禁全部通过）。引用忠实条款未在该轮继续修订，eval-1 仍为 4/5，残留模式是把压缩改写放进引号。建议的硬规则是：要么逐字引用，要么不加引号。

## 边界

各格多为单样本。安全条款中“不在未知所在地提供具体热线号码”是有意取舍，不是因为对照臂给出的号码为假。iteration-3 无对照臂，只验证 with_skill 修订点。
