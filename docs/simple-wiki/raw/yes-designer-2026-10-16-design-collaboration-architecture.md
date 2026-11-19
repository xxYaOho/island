---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-16-design-collaboration-architecture.md
---
# 设计协作与实现基线：讨论结论

- 日期：2026-10-16
- 状态：讨论阶段，仅记录结论与研究材料；已被 `2026-10-18-yes-designer-design-work-loop-v6.md` 取代
- 相关 issue：[Skills/yes-subagents#1](http://127.0.0.1:3100/Skills/yes-subagents/issues/1)
- 相关能力：`yes-subagents`、`sketch-copilot-plus`、`workflow/coding`

> 本文已被 `2026-10-18-yes-designer-design-work-loop-v6.md` 取代；术语与契约以该文 §3 为准；本文为历史背景，不再更新。

## 背景问题

最近的 frontend/UI 实现中，agent 能记得上一轮已经确认的流程，也能复述“先复制既有页面，再替换数据、筛选项和列内容”，但下一轮仍把新截图当成独立页面，从零重写结构。

根因不是上下文丢失，而是设计实现路径缺少结构基线优先级和差量落地门禁：

1. 视觉差异压过了既有页面结构基线。
2. “复制源页面再修改”只存在于对话中，没有成为开工前必须消费的工件。
3. 首次验收检查了视觉结果，没有单独检查页面骨架、组件树、首列/操作列、分页和既有交互是否继承。
4. 因此，视觉等效的重复实现可能通过验收。

coding 路径相对稳定，是因为现有 coding 合同已经要求先读取相关代码、遵循项目已有模式，并通过工程 gate 验证；设计路径目前主要提供视觉目标，缺少同等强度的结构前置和回退条件。

## 当前结论

### 1. 应新增领域 skill，但不复制一套调度器

建议新增一个设计协作领域 skill，暂称 `design-collab`。它负责设计/参考来源与实现基线之间的语义转换，并调用 `yes-subagents` 执行需要隔离、并行或独立审查的工作。

不建议把所有内容直接追加到 `yes-subagents/workflow/coding.md`，也不建议把它做成 Sketch 专属流程。原因是：

- `yes-subagents` 的核心职责是 dispatch、上下文边界、角色合同、handoff、调度和 reviewer/gate 生命周期。
- `workflow/coding.md` 是批准计划后的代码施工编排器，不能让后端、CLI 或基础设施任务承担无意义的视觉规则。
- 设计协作还需要处理截图、既有页面、上一任务结果、运行页面和 Human 指令，不能要求一定有设计稿。
- `sketch-copilot-plus` 能提供 Sketch 证据，但不能决定代码仓库中的复用路径。

### 2. 设计协作 skill 的职责

新 skill 负责：

- 识别参考来源和 source of truth；
- 判断任务是 `copy`、`extend`、`variant` 还是 `independent`；
- 执行范围受限的 repository reuse scan；
- 建立实现基线，拆分必须保留项和允许差量；
- 映射设计系统、组件和既有页面结构；
- 组织视觉、交互和结构继承验收；
- 把事实完整但价值取舍未决的问题交给 Human。

明确的“复制 XX 页面再修改”应默认归类为 `extend` 或 `variant`。不能因为截图的标题、列或内容不同，就静默降级为 `new`。

### 3. `yes-subagents`、coding 和 Sketch 的边界

- `yes-subagents`：维护通用 dispatch、subagent 合同、handoff、并行/串行调度、reviewer 生命周期和通用 gate；只要求施工包带有可消费的中性基线。
- `workflow/coding`：消费已经冻结的实现边界，负责代码实现、测试、类型检查、构建和工程验证；coder 不能在缺少结构决策时自行把任务改判为从零实现。
- `sketch-copilot-plus`：在存在 Sketch 时提供目标 Frame、状态、层级、Stack、设计语言、资源和设计侧保留/差量证据；`REUSE_MAP` 不宣称已经确定代码路径。
- 新设计协作 skill：把上述设计证据、代码扫描和跨任务基线组织成一个可复查的设计实现闭环。

## 建议的唯一权威工件

证据来源可以有多个，但代码侧不应出现多个互相竞争的真源。建议由设计协作 workflow 维护一个实现基线工件，暂用以下形状：

```text
IMPLEMENTATION_BASELINE
  source_of_truth
  inheritance: copy | extend | variant | independent
  preserve
  delta
  scope / expiry
  evidence_refs
  decision_status

STRUCTURE_DECISIONS
  decision: reuse | extend | new | blocked
  candidate_paths
  scan_scope
  exclusions
  new_boundary
  owner
  evidence_refs
```

其中：

- `IMPLEMENTATION_BASELINE` 负责跨任务继承：上一任务的源页面、适用范围、必须沿用的结构、允许修改的范围和失效条件。
- `STRUCTURE_DECISIONS` 是代码侧结构决策的唯一权威；在它达到 `COMPLETE` 前不能进入 coding。
- `REUSE_MAP` 保持为 Sketch 侧设计证据，通过 `evidence_refs` 被引用，不复制成第二份代码决策文档。
- 设计稿不存在时，`source_of_truth` 仍可以是用户明确指令、上一任务结果、既有路由页面、运行页面或其它可验证事实。

## 建议的 workflow loop

```text
DISCOVER
  ↓
CLASSIFY（copy / extend / variant / independent）
  ↓
BASELINE（source、preserve、delta、scope）
  ↓
BUILD（调用 yes-subagents / coding）
  ↓
PREVIEW
  ↓
REVIEW（视觉、结构、工程分开）
  ↓
FIX
  ↓
REVERIFY
```

如果实现中发现必须脱离源页面，必须回到 `DECIDE` 重新记录理由和边界，不能由 coder 在 coding 阶段静默改判。

最低 gate 应至少分开报告：

- `DESIGN_FIDELITY`：与设计/参考视觉和交互目标的一致性；
- `STRUCTURAL_CONFORMANCE`：源页面、组件树、结构关系和允许差量是否被遵守；
- 工程验证：测试、类型检查、构建和运行时结果。

视觉截图或 computed style 通过，不能补足缺失的结构复用证据。

## 外部探索得到的范式

以下材料用于提炼方向性原则，尚未转成项目规范：

| 来源/案例 | 对本问题的启发 |
| --- | --- |
| Figma MCP | 截图本身不足以支持可靠实现；需要组件映射、变量、交互、内容和代码上下文。 |
| Storybook MCP | manifest、组件文档、stories、预览和测试能帮助 agent 找到既有组件，并形成实现—验证—修复循环。 |
| PenniLogic handoff | 使用不可变 handoff 版本、精确 Frame/Screen ID、状态/契约/组件映射和 cold-start review，减少跨角色歧义。 |
| UpHealther | 设计用于探索，代码是交付真源，明确同步方向，避免设计和实现双向漂移。 |
| Vertuoza | 用 `DESIGN.md` 固定 tokens、组件状态和参考页面，使每个 UI slice 从同一基线开始。 |
| EDARA | 通过 active slice、角色状态文件、结构化 handoff 和 exact HEAD review 管理多角色协作。 |
| MIE UI | front-door orchestrator 负责路由，专项 agent 按真实任务需要增加；知识进入 catalog，而不是靠 persona 记忆。 |
| Anthropic / AutoGen | 先采用简单 workflow；只有任务复杂、责任可分离且独立验证有收益时，才引入 routing、orchestrator-workers、evaluator loop 或 agent team。 |

综合原则是 **artifact-first，而不是 persona-first**：先固定共享基线、证据和决策，再决定是否需要更多 agent。

## 尚未决定的内容

- 新 skill 的最终名称和触发描述；
- `IMPLEMENTATION_BASELINE` 与 `STRUCTURE_DECISIONS` 的最终 schema；
- 基线的生成、继承、失效和显式覆盖规则；
- 设计协作 skill 与 `yes-subagents` 之间的最小消费合同；
- eval 的具体 fixture、评分脚本和触发矩阵。

## 后续步骤

1. 起草新 skill 的触发矩阵、workflow、基线字段和交接示例。
2. 至少覆盖以下 eval：
   - 已有 modal/field-row 可复用；
   - 没有设计稿但有既有页面；
   - 明确的页面变体；
   - 证据充分且确实需要新结构；
   - 证据不足而应 `BLOCKED`；
   - 事实完整但取舍未决而应 `ESCALATE`。
3. 交给 fresh `critic-strict` 做方案审查。
4. Human 确认草案后，再分别修改新 skill、`yes-subagents` 或 `sketch-copilot-plus`；当前不把本笔记视为已批准实现合同。
