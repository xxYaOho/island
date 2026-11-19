---
title: 新一代模型下的 yes-subagents 迭代参考
type: concept
created: 2026-08-07
updated: 2026-11-19
sources: [raw/2026-08-07-frontier-model-iteration-reference.md]
topic: yes-subagents 工作流程与严格回合
tags: [subagent, research, governance, flywheel]
status: current
context: 1

# 新一代模型下的 yes-subagents 迭代参考

来源为 2026-08-07 研究笔记，针对当时 yes-subagents v0.3.1，[原文](../raw/2026-08-07-frontier-model-iteration-reference.md)明确：**不是已批准规格，不改变当时的 skill contract**。本页只整理其研究方向，不能写成已兑现收益或现行合同。

现行施工与审查合同仍以[《Coding workflow 重构决策》](coding-workflow-redesign-decisions.md)、[《Strict 飞轮四轮上限与生命周期重启决策》](strict-flywheel-four-round-decision.md)为准。更早的概念框架见[《yes-subagents 编排模型》](yes-subagents-orchestration-model.md)。

## 主张

Claude Opus 5 与 GPT-5.6 并未使 yes-subagents 失去价值，但会移动价值中心：不宜再以“补足模型执行能力”为主，而应成为强模型之上的薄型治理层——定义风险路由、权限边界、证据标准、技术问题关闭条件，以及何时必须交给用户判断。对非技术用户的潜在价值尚未在这些模型上验证，不能写成已实现的净收益。

长周期能力不等于无限后台运行。需要区分模型推理、context、agent 循环和宿主环境；宿主仍须处理生命周期、超时、压缩、权限、成本与失败恢复。

## 对协作结构的建议（未批准）

- 保留：简单任务豁免、计划审查判断维度、直接验证优先、事实性缺失与判断性缺失的区分、调查/行动/监察职责与并行文件边界。
- 收窄：`coder` 与蜂群只用于真正独立且并行有收益的工作；`critic` 只补直接验证覆盖不到的隐藏风险或决策性产物；上下文卫生降为次要策略；审查阈值应选择验证方式，而不是“命中即只能派 critic”。
- 重构建议：飞轮改为证据闭环，verdict 绑定 artifact 版本；取消默认每阶段停顿，只把产品价值、范围实质变化、不可逆或高成本操作、证据无法裁决的冲突交给用户。

建议的验证顺序以消融为主：在同一任务和授权边界下比较“强单代理加直接验证 / 仅风险阈值 / 风险阈值加单次 verifier / 完整飞轮”。若单次 verifier 已取得主要收益，就不应继续建设重型飞轮。这些命题均待验证。
