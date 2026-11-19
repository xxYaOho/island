---
title: yes-swiki v0.6 契约重设计
type: decision
created: 2026-09-10
updated: 2026-11-19
sources: [raw/yes-swiki-2026-09-10-contract-redesign.md, raw/yes-swiki-2026-08-31-agent-split-iteration-findings.md]
topic: yes-swiki 契约
tags: [yes-swiki, ingest, doctor, schema, librarian, curator]
status: current
context: 1

# yes-swiki v0.6 契约重设计

主源为 2026-09-10 [契约重设计方案](../raw/yes-swiki-2026-09-10-contract-redesign.md)。Island 当前收拢的 yes-swiki 为 v0.6.0。拆分阶段的评测观察见 2026-08-31 [迭代发现](../raw/yes-swiki-2026-08-31-agent-split-iteration-findings.md)。

## 决策

技能收紧为 `INGEST / READ / MAINTAIN` 路由器：先判断目标再跑 doctor，其它告警不得改写用户目标。doctor 只输出机器可解析事实与绝对路径，不派遣、不修复。

知识编译与共享接线拆分。librarian 只写已协调的 wiki 页面并维护 `ingested`；orchestrator 统一 upsert `INDEX.md`、追加并尽力去重 `LOG.md`，再经 `mark-integrated.sh` 提交 `integrated`。`integrated: true` 只表示本批共享状态已汇总，不表示内容经过复核。

raw 状态机：`false/false` 待编译，`true/false` 待接线，`true/true` 完成；`false/true` 非法。evidence 不单独成页；无引用归宿时保持 `ingested: false` 并上报，不因告警自动翻转。

多 librarian 先并行给出 `PAGE_PLAN`，再按页面重叠分流。协调后的计划是写入白名单；越界需求返回 `PLAN_DEVIATION`，相关 raw 保持 `ingested: false`。

项目 SCHEMA 分为受管核心与本地补充。版本相等才允许写入；`legacy` / `outdated` 先迁移；技能过旧或格式非法禁止写入。迁移只替换受管核心。Compound Interest 只保留维护中发现可复用新知识后的局部闭环。普通文档写作、一次性摘要和与项目知识库无关的检索不触发本技能。

## 拆分评测留下的前提

当时确定 librarian 与 curator 均可使用 haiku，前提是契约不变：不可裁决项上抛 ESCALATE。若放宽门槛，“haiku 足够”不自动延续；样本有限，不宜写成已证伪更强模型。更耐久的产出是契约修正：误报删除须注明反证；LOG 按 outcome 记录。曾观测到正确方向上附加无出处细节、以及把新发现直接写入 ESCALATE 区块（各 1 样本）。一轮冷启动 ingest 测不了 curator。
