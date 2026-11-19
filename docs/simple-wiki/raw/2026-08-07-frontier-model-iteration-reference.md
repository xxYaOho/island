---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/note/2026-08-07-frontier-model-iteration-reference.md
---
# 新一代模型下的 yes-subagents 迭代参考

- 记录时间：2026-08-07T16:04:24+0800
- 适用版本：yes-subagents v0.3.1
- 状态：研究笔记，非已批准规格，不改变当前 skill contract

## 结论

Claude Opus 5 与 GPT-5.6 没有使 yes-subagents 失去价值，但改变了它的价值中心。

过去的主要叙事是把低价值、耗上下文的工作交给子代理。新模型已经能在更长的任务链中保持目标，完成多文件、重构和端到端工作。yes-subagents 后续不应继续以“补足模型执行能力”为主要价值，而应成为强模型之上的薄型治理层：定义风险路由、权限边界、证据标准、技术问题关闭条件，以及何时必须交给用户判断。

对非技术用户，这一方向具有中等到较高的潜在价值，但当前版本在 Opus 5 与 GPT-5.6 上的实际增量收益尚未验证。后续不能把潜在价值表述为已经兑现的净收益。

## 如何理解 Opus 5 的长周期能力

Anthropic 官方将 Opus 5 的主要提升描述为：

- 在延长的工具调用循环中保持任务目标；
- 完成多文件功能、大型重构和端到端任务，不留下占位实现；
- 在 Claude API 中提供 1M token context、最高 128k 输出、默认 thinking，以及 `low` 到 `max` 的 effort；
- 更主动地验证、自我纠错和派遣子代理；
- 更好地协调 writer-verifier 模式。

“长周期”不等于无限后台运行。需要区分四层能力：

| 层次 | 模型或平台提供的能力 | 不代表 |
| --- | --- | --- |
| 模型推理 | 在较长任务链中保持目标和推进工作 | 判断必然正确 |
| Context | 容纳更多代码、历史和工具结果 | 永久记忆 |
| Agent 循环 | 持续调用工具并完成更多步骤 | 不受超时和预算限制 |
| 宿主环境 | 管理工具、状态、恢复和权限 | 模型自动获得操作授权 |

因此，新模型可以让主代理长期持有完整任务，减少顺序工作中的交接和上下文损失。宿主仍需处理进程生命周期、超时、上下文压缩、权限、成本和失败恢复；真实测试与运行时证据也不能省略。

GPT-5.6 的方向相同：增强意图理解、持续执行和 token 效率。Responses API 另有 persisted reasoning、Multi-agent beta 和 Programmatic Tool Calling。这些属于具体 API 或宿主能力，不能假定所有 Codex 或其他运行环境都已提供。

## 对当前协作结构的判断

### 保留

1. 简单任务豁免。它能避免强模型被低价值编排拖慢。
2. 计划审查阈值。可逆性、阶段依赖、验证透明度和既有基线偏离仍是有效判断维度。
3. 直接验证优先。测试、真实渲染、运行时结果和契约检查比角色数量更接近事实。
4. 事实性缺失与判断性缺失的区分。技术事实由 agent 补全，产品价值判断由用户决定。
5. 调查、行动、监察的职责边界，以及并行写入时互不重叠的文件边界。

### 收窄

1. `coder` 和 `swarm` 只用于真正独立、可隔离、并行有收益的工作。单一依赖链优先交给主代理持续执行。
2. `critic` 只补充直接验证无法覆盖的隐藏风险、高代价错误或决策性产物，不机械重复模型已有的自我验证。
3. 上下文卫生保留为次要策略，不再作为主要价值主张。
4. 计划审查阈值保留判断维度，但不必继续维持“命中任一条件就只能派 critic”的二元路由。阈值应决定验证方式，包括直接验证、提高 effort、定向 reviewer、异质证据或用户判断门。

### 重构

#### 飞轮与 PASS

飞轮应从状态循环改为证据闭环：

```text
权威基线
  -> 产出
  -> 直接验证
  -> 剩余风险审查
  -> finding 处置
  -> 重新运行直接验证
  -> 对变更部分复核
  -> 技术闭环或用户判断门
```

每个 verdict 必须绑定具体 artifact 版本。任何实质修改都会使旧 verdict 失效。

每项 finding 必须进入以下终态之一：

- 已修复并通过新证据验证；
- 被新证据否定；
- 经有权做出该决定的人接受残余风险；
- 明确移出当前范围；
- 因无法取得关键证据而阻断。

`PASS` 不应仅表示没有 FATAL。面向非技术用户时，它至少应表示：影响当前验收的技术问题已经处置，重要风险有对应证据，material UNVERIFIED 已阻断或升级。

#### 用户判断门

取消默认的每阶段停顿。只有以下情况交给用户：

- 产品体验、目标和价值优先级；
- 范围发生实质变化；
- 不可逆、外部或高成本操作；
- 技术证据无法裁决的冲突。

技术修正和技术 finding 应由 agent 在内部关闭，不要求非技术用户批准无法核查的中间态。

#### 调度

`1 / 2-3 / >=4` 可以保留为提示，不再作为主要路由依据。调度应同时考虑：

- 工作是否真正独立；
- 是否共享文件或运行时状态；
- 是否位于关键路径；
- 并行是否缩短总时间；
- context 复制和协调成本；
- 模型 effort 与宿主原生 multi-agent 能力；
- 单一长周期主代理是否已经足够。

同模型子代理提供的是角色与上下文隔离，不是认知独立。高风险审查应优先取得新的外部证据；必要时再考虑异构模型、工具或运行环境。

## 面向非技术用户的目标形态

用户负责：

- 目标和验收体验；
- 产品价值与优先级；
- 不可逆操作和残余风险的授权。

Agent 负责：

- 技术方案和实现细节；
- 风险到证据的对应；
- 测试、运行时验证和 finding 关闭；
- 将无法取得证据的部分明确标为未知或阻断。

最终汇报应回答三个问题：验证了什么、仍不知道什么、哪些事项确实需要用户决定。子代理数量和审查轮次不应作为可信度信号。

## 建议迭代顺序

### P0：最小可信语义

- 重定义 `PASS / NEEDS_JUDGMENT / BLOCKED_EVIDENCE`；
- 增加 artifact 版本绑定；
- 增加风险到证据的对应关系；
- 增加 finding disposition；
- 定义 material UNVERIFIED 的阻断规则；
- 用无进展、重复 finding、意见振荡和预算代替固定十轮上限。

### P1：立即做消融验证

在同一任务、同一终态质量标准和同一授权边界下比较：

1. 强单代理加直接验证；
2. 仅风险阈值；
3. 风险阈值加单次 verifier；
4. 当前完整飞轮。

比较真实任务成功、遗漏缺陷、误报、用户介入次数、时间和成本。如果单次 verifier 已取得主要收益，不继续建设重型飞轮。

### P2：判断门

将默认阶段确认改为只处理用户拥有的判断和授权。

### P3：长周期与能力感知调度

- 主代理承担顺序、跨文件、需要持续理解的工作；
- 子代理承担独立并行、证据隔离或定向审查；
- 根据宿主能力选择原生 multi-agent、不同 effort 或其他验证手段；
- skill 只定义策略，不重复宿主已经提供的编排机制。

### P4：价值主张

将“分担累活、保护主上下文”改为：

> 让强模型自主运行，但不能自行降低证据标准。

## 待验证命题

1. 在 Opus 5 或 GPT-5.6 上，风险阈值加单次 verifier 是否已经覆盖完整飞轮的大部分收益。
2. 长周期主代理是否优于多个 coder 串联处理同一依赖链。
3. 同模型 critic 能增加多少真实缺陷发现，多少只是重复或误报。
4. 用户判断门能否减少非技术用户的技术确认负担，同时保留必要控制权。
5. capability-aware dispatch 是否优于更简单的“仅高风险时单次 critic”。

## 官方资料

- [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
- [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model.md)
- [Multi-agent beta](https://developers.openai.com/api/docs/guides/responses-multi-agent.md)

## 关联文件

- `skill/SKILL.md`
- `skill/subagents/critic-strict.md`
- `skill/subagents/critic-gate.md`
- `docs/superpowers/specs/2026-07-22-yes-subagents-orchestration-design.md`
- `docs/superpowers/plans/2026-07-22-yes-subagents-orchestration.md`
