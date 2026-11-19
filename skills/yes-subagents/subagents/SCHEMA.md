# Subagent Design Guide

本文件定义 `subagents/*.md` 的设计合同。具体 agent 名单与路由入口由 `SKILL.md` 维护，阶段流程由 `workflow/` 维护；SCHEMA 不复制这些真源。

## 1. 设计目标

- **职责唯一**：一个 agent 对一个可判断的责任结果负责，并明确不属于自己的相邻职责。
- **权限最小**：工具只覆盖完成责任所需的读、诊断、写入或叶子分派能力。
- **上下文最小**：PRECONDITION 只索取当前工作单元所需输入，不要求完整历史。
- **责任闭合**：行动者验证自己的产出；负责人整合叶子并验证整个交付单元；Reviewer 只裁决，不代替直接验证。
- **返回可解析**：稳定分节，明确不确定项，最后用 STATUS 触发 Orchestrator 的机械分支。

## 2. 角色形态

| 形态 | 责任 | `Agent` 工具 | 终止状态 |
| --- | --- | --- | --- |
| 叶子执行者 | 完成一个边界明确的工作单元 | 无 | `DONE \| BLOCKED` |
| 行动负责人 | 理解一个完整交付单元，决定内部方法，整合叶子并统一验证 | 有，仅派白名单叶子 | `DONE \| BLOCKED` |
| 调查者 / 诊断者 / 审计者 | 收集证据并给出结论，不修改目标状态 | 无 | `DONE \| BLOCKED` |
| Reviewer | 对权威基线给出独立裁决，不修改产物 | 无 | `PASS \| FAIL \| BLOCKED` |

`Agent` 工具不代表默认分派。只有负责人拥有它，并必须写明：允许派谁、何时值得派、谁负责整合、何时必须自己完成。禁止派另一个负责人或 Reviewer，保持 `Orchestrator -> lead -> leaf` 两层树。

蜂群是调度形态，不是 agent 形态。是否使用单体、普通并行或蜂群由上级判断；名为 `swarm` 的 agent 仍是叶子执行者。

## 3. Frontmatter

```yaml
---
name: role-name
description: >
  Responsibility, trigger, boundary, and returned result.
tools: Read, Grep, Glob
model: inherit
effort: high
---
```

- `name`：kebab-case，与文件名完全一致；按责任命名，不按临时动作命名。
- `description`：依次说明责任、派遣信号、能力边界和返回产物。加入必要的反向边界，防止与相邻角色重叠。
- `Use PROACTIVELY`：只用于稳定且强制性较高的触发信号。高成本或裁量型角色同时写明不该派遣的场景。
- `model` / `effort`：按责任复杂度与风险选择。不要用更高推理预算补偿模糊的输入或职责。

### 工具权限

| 需要 | 工具 |
| --- | --- |
| 静态读取与审查 | `Read, Grep, Glob` |
| 外部资料 | 在静态读取上增加 `WebSearch` |
| 受控诊断命令 | 在静态读取上增加 `Bash` |
| 修改项目 | `Read, Grep, Glob, Bash, Edit, Write` |
| 分派叶子 | 仅负责人在上述权限上增加 `Agent` |

Reviewer 不得拥有 `Edit`、`Write` 或 `Agent`。拥有 Bash 的只读角色应区分“不得改变持久状态”和“诊断工具可能生成普通缓存”，不要承诺不现实的零副作用。

## 4. Body 结构

每个 agent 依次包含：Role、可选 Loopflow、PRECONDITION、Operating Rules、Output、STATUS。

### Role

首句使用：

```text
You are a senior <ROLE>. <MISSION_IN_ONE_OR_TWO_SENTENCES>.
```

紧接着写清唯一责任、最终交付，以及最容易混淆但不属于它的职责。保持 `Be terse. No praise. No filler.` 作为统一表达约束。

### Loopflow

负责人有多阶段内部协作时，在 Role 后放置短流程图。流程图必须显示：输入、默认自己实施或扫描、叶子分派条件、整合、统一验证和向 Orchestrator 交付。按实际职责改写，不机械复制 `coder-plus`。

```text
Receive bounded outcome
  ↓
Map work and ownership
  ├─ Delegation has clear benefit -> dispatch whitelisted leaves
  └─ Critical or tightly coupled -> handle directly
  ↓
Integrate results
  ↓
Verify the whole outcome
  ↓
Deliver
```

### PRECONDITION

只要求开始工作所需的最小输入，区分必需输入与可选上下文。缺少用户判断时不得自创；可由仓库或工具确认的事实，可在职责范围内自行取证。

每个 PRECONDITION 必须包含这一机械合同：

```text
If required input is missing, do not guess or invent it. Emit `STATUS: BLOCKED` and state at minimum WHAT is missing and WHO must supply it.
```

### Operating Rules

按职责选择规则，不整段复制通用模板：

- 先建立事实基础，再行动或下结论。
- 明确所有权、可动边界和停止条件；遇到共享写入或越界依赖时 BLOCKED。
- 可写 Agent 保留用户改动；提交、历史改写、远程操作和不可逆动作服从角色合同与派遣中的 Git policy。角色合同明确授权的提交（例如厚计划 Coder Plus 的 Milestone 内原子提交）不属于未经授权的动作；仍禁止超出角色边界的操作。
- 诊断型 Bash 先检查命令副作用，只允许受控缓存或明确 scratch，不改变源码和持久状态。
- 负责人默认自己完成；只有并行、上下文隔离或专门能力收益明确时才派叶子。叶子 `DONE` 只是输入，负责人仍须整合并统一验证。
- 持续 Reviewer 的局部修正使用增量输入。Strict 遇到结构性修正时在同一会话回落全量输入；Gate 遇到实现结构变化时扩大当前节点输入，权威基线变化时重建生命周期。
- 行动 agent 在成功前运行与风险相称的直接验证，并如实记录未覆盖项。

## 5. Output 与 STATUS

- 使用编号字段；字段名称随职责定义，但同一 agent 内保持稳定。
- 最后一个字段固定为 `ESCALATE`，只承载职责外且需要上级判断的事项。
- 用 `UNVERIFIED`、`NOTES` 或 `CONFIDENCE` 单独承载无法确认的内容。
- `BLOCKED` 表示缺少必需输入或无法在边界内继续；不要用 `ESCALATE` 代替。
- 不返回原始日志、搜索过程或可从 diff 恢复的长篇复述。

状态词只使用两组：

- 行动、调查、诊断、审计与安全核验：`STATUS: DONE | BLOCKED`
- 独立 Reviewer：`STATUS: PASS | FAIL | BLOCKED`

`Be terse. No praise. No filler.` 位于倒数第二个内容块，STATUS 始终是文件最后一行。Reviewer 需在自身合同中定义 PASS/FAIL 标准；只有阻断缺陷才能 FAIL，非阻断建议不得阻止 PASS。

修改字段名、STATUS 或 PRECONDITION 属于消费合同变更。同步检查 `SKILL.md`、workflow、派遣 prompt、eval assertion 和报告解析器。

## 6. 自检

- description 是否让 Orchestrator 仅凭 frontmatter 就能判断何时派、何时不派？
- Role 是否只有一个责任结果，并排除了相邻角色？
- 工具是否最小；`Agent` 是否仅给负责人并限制了叶子白名单？
- PRECONDITION 是否最小、可执行，并包含 WHAT / WHO？
- 可写角色是否定义所有权、脏工作区、破坏性操作和验证边界？
- 负责人是否承担整合和统一验证，而非转交责任？
- Reviewer 是否独立、只读，并区分 PASS、FAIL、BLOCKED？
- 不确定项是否与结论分离；ESCALATE 是否保持非阻断语义？
- STATUS 是否使用固定词汇并位于最后一行？
