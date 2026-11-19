---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/1018-strict-case/v1/yes-designer-work-loop-v1.md
---
# yes-designer 设计推进工作流草案

- 日期：2026-10-17
- 状态：草案 v1（Round 1 FAIL）；已被 `2026-10-18-yes-designer-design-work-loop-v5.md` 取代，不视为合同
- 关联：`skill_yes-designer`、`sketch-copilot-plus`、`yes-subagents`
- 背景材料：
  - `2026-10-16-design-collaboration-architecture.md`
  - `2026-10-17-sketch-copilot-plus-adapter-boundary.md`

## 目标

`yes-designer` 负责管理和推进设计落地，而不仅是指导一次 UI 实现。

它的核心职责是：

- 将不同来源的设计输入转换为统一的 `Design Reading`；
- 建立并维护持久的实现基线；
- 将大型设计工作拆成可独立推进、可独立验收的设计切片；
- 组织从基线、实现、结构验收、视觉验收到快照沉淀的完整闭环；
- 把机械性错误转化为自动检查，把设计判断交给 Human。

## 非目标

`yes-designer` 不负责：

- 取代 Human 做视觉品味和设计取舍；
- 取代 `sketch-copilot-plus` 解读 Sketch 原始事实；
- 取代 `yes-subagents` 做通用派发、上下文隔离和工程执行；
- 把原型 HTML 的临时 DOM 结构直接照搬进项目；
- 依赖 agent 记忆来维持跨轮次一致性。

## 关键原则

1. **Artifact-first，不是 persona-first**
   先固定共享工件：Design Map、Design Reading、Baseline、Structure Decisions、Snapshots，再决定是否需要 subagent。

2. **每轮先 Resume，不靠记忆**
   所有 UI 相关任务开工前，必须读取当前项目里的地图、基线、组件目录和快照状态。

3. **默认继承，独立必须有证据**
   新截图、设计稿或原型不能因为内容不同就默认视为独立页面。若无法确认来源，状态为 `unknown`，进入扫描和判断。

4. **基线冻结前不能写 UI 代码**
   未明确 `preserve / delta / means / assertions` 前，不进入实现。

5. **视觉通过不能抵消结构不通过**
   结构、几何、像素、Human review 分层执行；前一层不通过，不进入下一层。

6. **golden 只能由 Human 批准更新**
   agent 可以生成候选快照和差异报告，但不能自行更新验收基准。

## 核心工件

```text
Design Map
  └─ Slice
      ├─ Design Reading
      ├─ Implementation Baseline
      ├─ Structure Decisions
      ├─ Assertions
      └─ Snapshots / Golden
```

### Design Map

Design Map 管理一项设计工作的整体推进。它是索引，不是事实存储。决策细节保存在切片或基线文件中，地图只记录一句概述和链接。

Design Map 在以下任一条件成立时创建：

- 任务跨会话；
- 任务包含两个或更多切片。

agent 可以提议创建，Destination 由 Human 确认。单次小改动不必创建 Design Map，但仍需创建或更新 Baseline 和 Snapshot。

建议结构：

```markdown
## Destination

<这项设计工作完成时的目标状态。>

## Notes

<设计来源、当前生效基线、组件目录位置、固定偏好、约束。>

## Decisions so far

- [<决策或基线名称>](link)：<一句话概述>

## Not yet specified

<已经看到但尚不能精确定义的问题。>

## Out of scope

- <明确不做的内容>：<理由>
```

### Design Reading

Design Reading 是所有设计输入的统一中间格式。

```yaml
source:
  kind: sketch | prototype-html | screenshot | existing-page | human-description
  refs: []
  fidelity: pixel | visual | layout

screens:
  - id: string
    states: []

regions:
  - id: string
    screen: string
    state: string
    role: preserve | delta | unknown
    source_anchor: {}
    dom_anchor: string | null

components:
  - name: string
    evidence_refs: []
    catalog_match: string | null

language:
  tokens: []
  spacing: []
  typography: []
  state_semantics: []
  generation: string | unknown

interactions:
  - from: string
    event: string
    to: string

unknowns:
  - question: string
    blocks: []
```

不同来源只影响 Design Reading 的生成方式，不影响后续 workflow。

### Implementation Baseline

Implementation Baseline 记录跨轮次的实现继承关系。

```yaml
id: string
version: string
scope:
  routes: []
  features: []
  expires_when: []
source_of_truth:
  kind: sketch | prototype | existing-page | human-instruction | previous-golden
  refs: []
relation: inherit | independent | unknown
preserve: []
delta: []
regions: []
evidence_refs: []
decision_status: draft | complete | blocked | escalated
```

### Structure Decisions

Structure Decisions 是本切片代码侧结构决策的唯一权威。

```yaml
slice: string
status: draft | complete | blocked | escalated
scan_scope: []
candidate_paths: []
exclusions:
  - path: string
    reason: string
means:
  - region: string
    decision: copy | reuse | extend | new | blocked | escalated
    target: string | null
    reason: string
evidence_refs: []
```

`Researcher` 或其它扫描者只能输出候选、排除项和证据，不直接判定可复用性。

## 来源适配

### Sketch packet

`sketch-copilot-plus` 提供 Sketch 事实：document、page、frame、layer、stack、symbol、style、asset、截图和 evidence refs。

`yes-designer` 在此基础上：

- 将多个 Frame 归并成 `screen × state`；
- 将 layer tree 归纳为语义区域；
- 将 Symbol 与项目组件目录对齐；
- 拆分 `preserve / delta / unknown`；
- 生成区域锚点、断言和验收基准；
- 推进实现和验收。

Sketch packet 不决定代码路径，不写入 `candidate_paths`、`scan_scope` 或代码侧复用结论。

### 原型 HTML

原型 HTML 表达视觉意图和交互意图，但不默认表达项目内的实现结构。

适配步骤：

1. 用浏览器打开原型；
2. 截取全图和初步区域图；
3. 读取 DOM、accessibility tree 和 computed style；
4. 触发交互并记录状态切换；
5. 提取区域、布局、token、状态和未知项；
6. 由 Human 确认 fidelity：
   - `pixel`：原型为视觉定稿；
   - `visual`：原型表达视觉方向；
   - `layout`：原型只表达结构和流程，视觉以项目设计语言为准。

原型 DOM 不得直接作为项目 DOM 结构的权威。

### 既有页面或上一轮结果

既有页面是结构事实的重要来源。读取方式包括：

- 运行页面截图；
- 读取组件树和源码；
- 对照组件目录；
- 对照已批准 golden。

当 Human 明确要求“复制某页面再修改”时，默认关系为 `inherit`，除非有明确证据证明该页面不适用。

## 两层循环

### 外层：Design Map Loop

```text
CHART
  ↓
FRONTIER
  ↓
WORK SLICE
  ↓
SETTLE
  ↓
RETRO
  ↓
UPDATE MAP
```

外层负责：

- 定义 Destination；
- 识别 Frontier；
- 管理 Not yet specified 和 Out of scope；
- 记录 Decisions so far；
- 保证每个会话只推进一个清晰切片。

### 内层：Slice Loop

```text
ENTRY
  ↓
READ
  ↓
RELATE
  ↓
SCAN
  ↓
DECIDE
  ↓
FREEZE
  ↓
BUILD
  ↓
VERIFY
  ↓
REVIEW
  ↓
SETTLE
```

#### ENTRY

每轮开工前读取：

- Design Maps；
- Baselines；
- Component Catalog；
- Golden Snapshots；
- 当前输入来源。

输出：

- 命中的 map 或 baseline；
- 建议路由：quick、chart、work、retro；
- 未知项；
- 是否需要 Human 确认。

#### READ

将当前输入转换为 Design Reading。

#### RELATE

判断当前设计与既有实现关系：

- `inherit`：明确继承已有页面、组件或上一轮 golden；
- `independent`：有证据表明不继承；
- `unknown`：证据不足，进入扫描。

#### SCAN

按限定范围扫描复用候选：

1. 组件目录；
2. 同 feature 或同路由下的相邻页面；
3. grep / code search；
4. 运行页面对比。

必须记录：

- 查了哪里；
- 找到什么；
- 排除什么；
- 排除理由。

#### DECIDE

对每个 region 决定实现手段：

- `copy`：复制既有骨架后只改 delta；
- `reuse`：直接复用已有组件；
- `extend`：扩展已有组件或模式；
- `new`：新建结构；
- `blocked`：证据不足；
- `escalated`：需要 Human 判断。

设计代际、共享组件扩展、视觉取舍和产品语义均属于 Human 可介入的决策。

#### FREEZE

冻结 Baseline 和 Structure Decisions，并生成：

- region 清单；
- DOM anchors；
- structural assertions；
- geometry expectations；
- pixel oracle；
- snapshot plan。

未冻结不得进入 BUILD。

#### BUILD

两种模式：

```text
Direct mode: lead 自己实现
Delegated mode: yes-subagents Coder / Coder Plus 实现
```

实施者不能自行将 `inherit` 改判为 `new`。若发现必须偏离基线，记录 `DEVIATION` 并回到 DECIDE。

#### VERIFY

验收顺序固定：

```text
STRUCTURAL_CONFORMANCE
  ↓
GEOMETRY_CONFORMANCE
  ↓
REGION_PIXEL_DIFF
  ↓
INTERPRET_FAILED_REGIONS
  ↓
HUMAN_REVIEW
```

前一层失败，不进入下一层。

#### REVIEW

Human 审查：

- 首轮没有设计稿的 delta 区域；
- 需要更新 golden 的区域；
- 设计取舍；
- agent 无法可靠判断的视觉问题。

#### SETTLE

收尾动作：

- 保存或更新 golden；
- 更新 baseline version；
- 写入 Design Map 的 Decisions so far；
- 更新组件目录；
- 清理本轮临时快照；
- 若出现流程失效，进入 RETRO。

## 切片原则

设计切片是可独立推进、可独立验收的纵向单元。

切片规则：

1. **纵向切片**
   一个切片必须包含结构、样式、状态和验收，不做“先统一写 CSS，再统一写 DOM”的横向切分。

2. **一个切片对应一个清晰决策边界**
   每个切片只挂一份主基线，`preserve / delta` 边界清楚。

3. **每个切片有自己的区域和快照**
   验收结果必须能定位到区域，而不是只看整图。

4. **大小适合一个新会话完成**
   切片结束后，上下文可丢弃，状态保存在工件里。

5. **共享组件先做**
   会被多个切片依赖的共享组件，应先成为独立切片。

6. **静态先于交互**
   先完成每个状态的静态界面，再实现状态之间的转换。

7. **阻塞关系显式记录**
   每个切片标注 blocking edges，只有未阻塞切片进入 Frontier。

## 切片状态机

```text
needs-triage
  ├─► needs-info
  ├─► needs-decision
  └─► ready-to-build
        ▼
      building
        ├─► needs-decision   (DEVIATION)
        └─► verifying
              ▼
            needs-review
              ▼
            settled
```

状态含义：

- `needs-triage`：尚未判断是否可推进；
- `needs-info`：缺少来源或证据；
- `needs-decision`：需要 Human 做设计判断；
- `ready-to-build`：基线冻结，断言和快照计划已生成；
- `building`：正在实现；
- `verifying`：正在分层验收；
- `needs-review`：等待 Human 验收；
- `settled`：已沉淀快照和基线。

## 视觉验收设计

### 分层验收

```text
1. STRUCTURAL_CONFORMANCE
2. GEOMETRY_CONFORMANCE
3. REGION_PIXEL_DIFF
4. INTERPRET_FAILED_REGIONS
5. HUMAN_REVIEW
```

#### STRUCTURAL_CONFORMANCE

机械检查：

- 必须 import 的组件；
- 禁止出现的新容器或字面量；
- 是否沿用源页面骨架；
- diff 是否只发生在 delta 范围；
- 关键交互结构是否存在。

#### GEOMETRY_CONFORMANCE

按 region 检查 bbox：

- x；
- y；
- width；
- height；
- gap；
- alignment。

该层用于提前发现布局位移，避免整图像素差异被级联位移污染。

#### REGION_PIXEL_DIFF

按 region 裁图对比，不以整图作为主要验收依据。

对比类型：

- 回归对比：actual region vs golden region；
- 还原对比：actual region vs design export region。

回归对比可使用更严格阈值。还原对比需考虑 Sketch 与浏览器渲染差异。

#### INTERPRET_FAILED_REGIONS

agent 只解读未通过区域的三联图：expected、actual、diff。

agent 输出：

- 差异位置；
- 可能原因；
- 是否越界到 preserve 区域；
- 建议修复方向。

agent 不用整图主观判断“像不像”。

#### HUMAN_REVIEW

Human 审查：

- 首轮无设计稿区域；
- 需要批准 golden 更新的区域；
- 阈值外但可能可接受的差异；
- 设计品味和产品语义。

### 存储布局

目标项目中按生命周期分两处存放：

```text
docs/island/designer/                 持久，进仓库
  catalog/                            组件目录（含设计语言标记）
  baselines/<baseline-id>.yaml        基线（含 regions 与断言数据）
  golden/<baseline-id>/               按基线归属，不按切片
    regions/*.png
    approval.yaml
  maps/<effort>/map.md                Design Map（完成后归档保留）
  maps/<effort>/slices/NN-<slug>.md   切片决策记录：问题、结论、证据
  thresholds.yaml                     验收阈值（预设 + 校准记录）

.tmp/island/designer/                 一次性，不进仓库
  readings/                           Design Reading（可由来源再生）
  scans/                              复用扫描日志
  exports/                            设计稿导出图缓存
  rounds/<slice>/rNN/                 每轮快照
    full.png
    regions/*.png
    diff/*.png
    report.yaml
    meta.yaml
```

判定依据：下一轮或下一位协作者需要读取的进 `docs/`；可以从来源再生、或只服务当前切片的进 `.tmp/`。bootstrap 需确认 `.tmp/` 已被目标项目忽略。

### golden 生命周期

golden 与基线同寿命，不按时间永久保留：

- 基线生效期间保留，作为 `preserve` 回归和无设计稿 `delta` 的对比基准；
- 基线升版时，由 Human 批准替换；工作区只保留当前版本，旧版本依靠 git 历史追溯；
- 基线失效或页面下线时，随基线一并删除；
- 渲染环境变化（浏览器版本、字体、DPR）时，需批量重新批准，不得由 agent 自动刷新。

### 阈值预设

预设值用于首轮，之后根据首个切片的实测噪声校准，再经 eval 调整。校准结果写入 `thresholds.yaml` 并记录来源。

| 对比类型 | 指标 | 预设 |
|---|---|---|
| 回归：actual vs golden | 几何 bbox | 0 px |
| 回归：actual vs golden | pixelmatch，per-pixel threshold 0.1，忽略抗锯齿 | 差异像素占比 ≤ 0.1% |
| 还原：actual vs 设计稿导出 | 几何 bbox | 位置与尺寸 ±1 px；文本块高度 ±2 px |
| 还原：actual vs 设计稿导出 | SSIM，非文字主导区域 | ≥ 0.95 |
| 还原：actual vs 设计稿导出 | SSIM，文字主导区域 | ≥ 0.90 |

校准方法：

- 回归噪声：同一提交、同一环境连续截图 5 次，取区域差异最大值；
- 还原噪声：取首个切片中已由 Human 判定为正确的区域，计算与设计稿导出图的 SSIM 分布；
- 阈值取实测噪声 p95 加安全余量，不低于噪声本身。

色值、字号、间距等可直接读取的属性，优先用 computed style 断言，不依赖像素指标。

`meta.yaml` 至少记录：

- commit SHA；
- viewport；
- DPR；
- browser version；
- data fixture hash；
- screenshot timestamp；
- source refs。

## 无设计稿时的验收

无设计稿不等于无验收。

流程：

1. 使用原型 HTML、既有页面或 Human 描述生成 Design Reading；
2. 首轮实现后，Human 审查 delta 区域；
3. Human 批准后生成 golden；
4. 后续轮次与 golden 做回归对比；
5. preserve 区域始终与既有 golden 或源页面快照对比。

## Retro

当 Human 指出问题，或切片 settle 后，可运行 design-retro。

Retro 只修改环境，不修改业务代码：

| 问题类型 | 处理方式 |
|---|---|
| 机械性结构偏离 | 新增 structural assertion |
| 几何反复偏移 | 新增 region bbox 断言 |
| 视觉判断失误 | 补充组件目录设计语言标记 |
| 流程被绕过 | 更新项目 `AGENTS.md` 的 ENTRY 规则 |
| 复用扫描遗漏 | 更新 reuse scan 规则或组件目录 |
| Human 反复介入同类判断 | 抽象为明确设计规则或 catalog 条目 |

## 与其它能力的边界

### sketch-copilot-plus

`sketch-copilot-plus` 是 Sketch 事实适配器。

它提供：

- document / page / frame / layer 锚点；
- layer tree；
- stack / layout / style / asset 事实；
- SymbolInstance 和 override 事实；
- 截图和 evidence refs。

它不负责：

- 代码仓库扫描；
- 结构复用决策；
- 实现路线规划；
- 设计工作推进。

### yes-subagents

`yes-subagents` 是可选执行层。

`yes-designer` 可调用：

- Researcher：执行 bounded reuse scan，只输出候选和证据；
- Coder / Coder Plus：在基线冻结后实现；
- Critic Gate：对照权威基线审查结构与工程结果。

当前不需要在 `yes-subagents` 中新增 design role。

## 示例：完整 Sketch 静态交互界面

输入：Sketch packet 包含列表页、弹窗、详情抽屉和 prototype 连线。

### Chart

1. 读取 packet；
2. 归并 Frame 为 screen × state：
   - list：default、filter-open、empty、loading；
   - create-modal：blank、invalid；
   - detail-drawer：default；
3. 识别共享 Symbol 和重复模式；
4. 对每个 screen 做 RELATE；
5. 生成候选切片；
6. Human 确认 Destination 和切片边界。

### 可能切片

```text
S1  共享组件：StatusTag / FieldRow 与组件目录比对
S2  列表页 default：继承既有列表页骨架
S3  列表页其它状态：filter-open / empty / loading
S4  新建弹窗：blank / invalid
S5  详情抽屉：default
S6  交互连线：按 prototype 验证状态切换
```

### Work S2

```text
Resume
  读取 map、S1 决策和生效基线

RELATE
  inherit 既有列表页基线

SCAN
  核对源页面、RecordsTable、FilterPanel

DECIDE
  页面骨架 copy
  表格组件 reuse
  列定义 delta

FREEZE
  生成 regions、assertions、design exports、snapshot plan

BUILD
  实现 delta

VERIFY
  structural → geometry → region pixel

REVIEW
  Human 批准 delta 区域

SETTLE
  golden、baseline version、map decisions 更新
```

## 待定事项

已决定：

- 持久内容进 `docs/island/designer/`，一次性内容进 `.tmp/island/designer/`；
- region anchor 统一使用 `data-region`；
- golden 进 `docs/island/designer/golden/`，生命周期与基线绑定；
- 阈值采用预设，按首个切片实测噪声校准，经 eval 调整；
- L3 断言采用方式 A：断言数据进项目 `docs/island/designer/`，执行器留在 skill，由 VERIFY 阶段调用；不改项目依赖与 scripts，不接入 CI。eval 后再评估是否升级为方式 B（静态检查进项目、本地命令）或方式 C（接入 CI）。断言修改与基线版本绑定，由 Human 批准。

仍待定：

- eval fixture 的具体仓库和数据来源。

## 初始 eval fixture

至少覆盖：

1. 已有 modal / field-row 可复用；
2. 没有设计稿但有既有页面；
3. 明确的页面变体；
4. 有 Sketch packet 的完整多状态界面；
5. 原型 HTML 作为视觉来源；
6. 证据充分且确实需要新结构；
7. 证据不足，应 `needs-info / blocked`；
8. 事实完整但取舍未决，应 `needs-decision / escalated`；
9. preserve 区域被无意改动，应被结构或视觉回归验收拦下。
