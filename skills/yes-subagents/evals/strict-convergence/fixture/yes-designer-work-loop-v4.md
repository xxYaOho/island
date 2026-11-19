# yes-designer 设计推进工作流草案 v4

- 日期：2026-10-18
- 状态：草案 v4（Round 4 FAIL）；已被 `2026-10-18-yes-designer-design-work-loop-v5.md` 取代，不视为合同
- 前一版：
  - `2026-10-18-yes-designer-design-work-loop-v3.md`（796 行，Round 3 FAIL）
  - `2026-10-17-yes-designer-design-work-loop-v2.md`（538 行，Round 2 FAIL）
  - `2026-10-17-yes-designer-design-work-loop-draft.md`（742 行，Round 1 FAIL）
- 背景材料（历史；术语以本文 §2 为准）：
  - `2026-10-16-design-collaboration-architecture.md`
  - `2026-10-17-sketch-copilot-plus-adapter-boundary.md`
- 配套草案（与本文联合批准）：`2026-10-17-design-md-framework-draft.md`
- 本版修复对照见附录 A。

## 1. 目标与非目标

### 1.1 目标

`yes-designer` 管理并推进设计落地：把任意来源的设计输入转换为统一的 Design Reading，建立并维护持久的实现基线，将设计工作拆成可独立验收的切片，并组织从基线、实现、分层验收到快照沉淀的闭环。

核心特征：

- **artifact-first**：跨轮状态、结构决策、验收基准与审批全部落盘，不依赖 agent 记忆；
- **状态为一等维度**：每个 `screen × state × region` 都有独立的 oracle 与验收记录；
- **门禁可机械执行**：断言由生成器产出且可校验出处，冻结前不可手改；
- **结构与视觉分层验收**：视觉通过不能抵消结构失败。

### 1.2 非目标

- 代替 Human 做视觉品味、设计代际和产品语义的判断；
- 解读 Sketch 原始事实（由 `sketch-copilot-pro`（原 `sketch-copilot-plus`）提供）；
- 通用派发、上下文隔离和工程执行（可选调用 `yes-subagents`）；
- 将原型 HTML 的 DOM 结构直接作为项目结构；
- 提供项目级测试框架或 CI 集成（断言执行器留在 skill 内，见 §12.4）。

## 2. 术语表

本文术语为唯一权威。背景笔记与 Sketch packet 中的旧术语按下表映射。

| 术语 | 定义 | 旧术语映射 |
|---|---|---|
| `relation` | 当前设计与既有实现的关系：`inherit` / `independent` / `unknown` | v1 的 `inheritance`；Sketch `design_relation: variant` 仅作为 `inherit` 的候选证据 |
| `means` | 区域级代码实现手段：`copy` / `reuse` / `extend` / `new` / `blocked` | v1 的 `decision` |
| `delta` | 允许改动的白名单：region + state + 文件范围 + 改动类型 | 语义相同，现为白名单 |
| `preserve` | 不再有顶层列表；`inherit` 下凡不在 `delta` 中的即为保留。region 级仍用 `role: preserve` | v1 的顶层 preserve 列表 |
| `region` | 语义区域，身份 = DOM 上 `data-region` 的值，在一个基线内唯一 | — |
| `screen` | 页面或界面的标识，对应 `data-screen` 值 | Design Reading 的 `screens` |
| `state` | 界面状态（默认、筛选展开、空态、校验失败等），对应 `data-state` 值 | Design Reading 的 `states` |
| `state marker` | 状态可观测断言：`[data-screen="x"][data-state="y"]` 存在 | — |
| `state origin` | `source`：源页面已有该状态；`introduced`：本切片新增，FREEZE 不预演 | — |
| `hooks` | setup 与 marker 依赖的稳定选择器，是实现的接口契约 | — |
| `capture env` | oracle 抓取或测量的环境：浏览器主版本、字体哈希、DPR、viewport | — |
| `setup` | 到达某状态的有序步骤配方（ui-action / fixture / wait），属于基线内容 | — |
| `oracle` | 某个 `region × state` 的对比基准，类型见 §7.2 | v1 的 `pixel oracle` |
| `oracle evidence` | oracle 所依赖的图像或测量数据，持久化在基线版本目录 | — |
| `golden` | Human 批准的 region × state 快照，作为回归基准或 `human-first-review` 区域的转换 oracle；golden 更新不改变基线内容 | — |
| `assertions` | 生成器从基线、源页面、规则与阈值机械生成的验收断言集 | — |
| `content hash` | 基线内容的规范化 hash，审批绑定该值 | — |
| `generation` | 设计代际标签，由组件目录维护（如 `gen1`、`gen2`）；无法识别时为 `unknown` | v1 的 `language.generation` |
| Map Loop | 外层：CHART → FRONTIER → WORK → ADVANCE | v1 的外层，`SETTLE` 改名 `ADVANCE` |
| Slice Loop | 内层：ENTRY → READ → RELATE → SCAN → DECIDE → FREEZE → BUILD → VERIFY → REVIEW → SETTLE | — |
| Resume | ENTRY 命中一个已存在、未结束切片时的路由：读取切片 frontmatter、决策与审批后继续 | v1 未定义 |
| BLOCKED | 验收或冻结被阻断的结论：工件不一致、断言过期、环境失配、oracle 不可用；落到切片为 `needs-triage` + `blocked_reason` | v1 仅作为返回值出现 |
| waiver | Human 批准的、限区域限版本的阈值外差异豁免，随基线版本失效 | — |
| viewport ref | `viewports.yaml` 中的断点 ID；一个基线只绑定一个断点 | — |
| lead | 运行 `yes-designer` 的主会话 agent | — |

## 3. 不变量

1. 每轮 UI 任务先执行 ENTRY，读取工件，不依赖对话记忆。
2. 默认 `inherit`；`independent` 必须有证据并经 Human 批准；证据不足为 `unknown`。
3. 切片状态未达 `ready-to-build` 不写 UI 代码。
4. `inherit` 下改动只允许落在 `delta` 白名单内；漏写 `delta` 只会使检查更严。
5. 断言由生成器从基线、源页面、`rules.yaml` 与阈值机械生成；lead 与实施者均不手写断言；FREEZE 重新生成并校验 `output_hash`，不一致即阻断。
6. 状态是验收的一等维度：每个 `region × state` 必须有独立 oracle；实现必须提供 `data-region`、`data-screen`、`data-state` 与稳定选择器，否则结构层不通过。
7. 验收分层执行，前一层失败不进入下一层；视觉通过不能抵消结构失败。
8. 基线内容、golden、阈值、断言与 waiver 的创建、变更、放宽只能由 Human 批准，且审批绑定 content hash 或对应哈希。
9. 基线内容（新增 screen/state/region/delta、oracle 类型、scope、origin/hooks）的任何变更都升版；golden 快照更新不升版但需 Human 批准；`human-first-review` 转 `golden` 属内容变更。版本目录永久保留，旧版本状态为 `superseded`。
10. `docs/island/designer/` 只由 lead 写入；subagent 只产出提案；同一地图同一时刻最多一个未过期 claim。
11. 所有 oracle 证据、golden、`waivers.yaml`、`thresholds.yaml`、`viewports.yaml` 都记录 hash 与抓取/审批环境；FREEZE 与 VERIFY 校验，缺失或失配即 `BLOCKED`。

### 3.1 决策权

| 决策 | 决定者 | 记录位置 |
|---|---|---|
| `means: copy / reuse`，附证据 | lead | 切片 Structure Decisions |
| `means: new`（任何情况） | Human | 切片 Structure Decisions + Approvals |
| `means: extend` 共享组件 | Human | 同上 + Approvals |
| `relation` 由 `inherit` 或 `unknown` 改为 `independent` | Human | 切片 Relation + Approvals |
| 接受 `DEVIATION` | Human；任何人可提出，实施者不能自批 | 切片 Deviations + Approvals |
| 基线的创建、内容变更、升版、失效 | Human | `baseline.yaml` approvals |
| screen / state 集合、state origin、setup 配方、state marker、hooks、region 的 role 与 content | Human（作为基线内容） | `baseline.yaml` |
| golden 快照的创建与更新（同一版本内） | Human | `golden/approval.yaml`（记录旧/新 hash） |
| `human-first-review` 转 `golden`（升版） | Human | `baseline.yaml` approvals |
| 阈值变更、waiver | Human | 对应文件 approvals |
| 设计代际是否一致、能否合并 | Human | 组件目录条目 + 切片 Approvals |
| reopen 已 `settled` 切片 | Human | 切片 Approvals |
| 释放过期 claim | Human | 切片 Approvals |
| `DESIGN.md` 指针级更新、追加 Known Gaps | lead | `design-md.log.md` |
| `DESIGN.md` 规范内容的修正与补充 | Human（直接编辑或指示 lead） | `design-md.log.md` |

## 4. 工件与存储

### 4.1 存储布局

```text
DESIGN.md                                  项目根目录，设计范式总约束（配套草案）

docs/island/designer/                      持久，进仓库，仅 lead 写入
  design-md.log.md                         DESIGN.md 的来源、审批与待审队列
  rules.yaml                               可机械检查的规则，按编号指回 DESIGN.md
  thresholds.yaml                          阈值预设、校准记录与 approvals
  viewports.yaml                           断点预设与 approvals
  project.yaml                             项目接入配置（fixture 提供者、harness 形态、bootstrap 记录）
  catalog/<component>.yaml                 组件目录条目
  baselines/<baseline-id>/
    current.yaml                           当前版本指针：{version, status, approved_at}
    v<N>/
      baseline.yaml                        基线（Human 批准）
      assertions.yaml                      生成的断言（随基线版本）
      oracles/<region>.<state>.png         source-snapshot / design-export 证据（含 sha256、capture env）
      golden/<region>/<state>.png          经 Human 批准的区域快照
      golden/approval.yaml                 golden 审批、测量值与抓取环境
      waivers.yaml                         Human 批准的阈值外豁免
  maps/<effort>/map.md                     Design Map
  maps/<effort>/slices/NN-<slug>.md        地图内切片
  slices/<YYMMDD>-<slug>.md                无地图的独立切片

.tmp/island/designer/                      一次性，被忽略
  readings/<slice>.yaml                    Design Reading
  scans/<slice>.md                         扫描原始日志
  exports/                                 导出与源页面截图的临时缓存（正式证据进基线版本目录）
  rounds/<slice>/rNN/                      每轮快照、diff、report、meta
  proposals/                               subagent 提案
  dispatch/                                每轮派发简报（可再生产物）
```

判定依据：后续轮次或协作者需要读取、或包含 Human 确认的内容进 `docs/`；可再生或只服务当前轮次的内容进 `.tmp/`。oracle evidence 属于验收基准的一部分，必须进基线版本目录，不能只留在 `.tmp/`。

所有切片都有切片文件，包括单会话的小改动；Design Map 只在任务跨会话或包含两个及以上切片时创建。

### 4.2 baseline.yaml

```yaml
schema: 3
id: person-verification-records
version: 3
status: active                  # active | superseded | expired
scope:
  routes: ["/person-verification/*"]
  maps: []
  expires_when: ["Human 指定新的来源页面"]
viewport_ref: desktop-1440      # viewports.yaml 中的 ID；一个基线只绑定一个断点
source:
  kind: existing-page           # sketch | prototype-html | screenshot | existing-page | human-description
  refs: []                      # 版本固定证据：Sketch document id+version、原型文件 hash、截图 hash
  fidelity: visual              # pixel | visual | layout
  fidelity_confirmed_by: human
  confirmed_at: <ISO>
source_page:                    # inherit 且来源页面可运行时存在，否则 null
  route: /person-verification/records
  files: [src/views/PersonVerificationRecordsPage.vue]
  commit: <sha>
  # 工作区路径属于本地环境，不写入基线、不参与 content hash
relation: inherit               # inherit | independent；unknown 不进基线
screens:
  - id: records
    route: /person-verification/records
    states:
      - id: default
        origin: source          # source | introduced
        setup: []               # 空 = 初始加载后即为该状态
        marker: '[data-screen="records"][data-state="default"]'
        hooks: []
      - id: filter-open
        origin: introduced      # 源页面没有该状态，本轮新增
        setup:
          - {kind: ui-action, action: click, target: '[data-region="filter-toggle"]'}
          - {kind: wait, condition: 'selector:[data-state="filter-open"]'}
        marker: '[data-screen="records"][data-state="filter-open"]'
        hooks: ['[data-region="filter-toggle"]']
interactions:                   # 可选：prototype 连线或 Human 确认的状态切换
  - id: open-filter
    screen: records
    from: default
    action: {kind: click, target: '[data-region="filter-toggle"]'}
    to: filter-open
delta:
  - id: columns
    kind: replace               # replace | add | remove
    regions: [table-body]
    states: [default, filter-open]   # 缺省 = 该 region 的全部状态
    files: ["src/views/<new-page>/columns.ts"]
regions:
  - id: filter-panel
    screen: records
    role: preserve              # preserve | delta
    content: graphic            # graphic | text
    states: [default, filter-open]
    layout: null                # fidelity=layout 时必填：{order: [...], align: [...]}
    source_anchor: null         # design-export 几何期望来源：{kind: sketch|prototype-dom, ref, frame}
oracles:
  - region: filter-panel
    state: default
    kind: source-snapshot       # source-snapshot | design-export | golden | human-first-review
    evidence: oracles/filter-panel.default.png
    evidence_sha256: <sha256>
    export: null                # design-export 必填：{scale, origin}
    capture_env: {browser: chromium, browser_version: "<major.minor>", fonts_hash: <sha256>, dpr: 1}
    threshold_ref: regression.default
    mask: []
  - region: filter-panel
    state: filter-open
    kind: human-first-review
    evidence: null
    evidence_sha256: null
    export: null
    capture_env: null
    threshold_ref: null         # human-first-review 允许为 null
    mask: []
computed_expectations:          # 首轮无源页面/golden 时，Human 批准的期望属性
  - region: filter-panel
    state: filter-open
    source: human               # human | design-tokens
    props: {padding: 8px 12px, color: var(--color-text)}
approvals:                      # 不参与 content hash
  - action: create              # create | content-change | bump | expire
    version: 3
    content_hash: <sha256>
    by: human
    at: <ISO>
    note: ""
```

约束：

- 每个 `region × state`（state 取自该 region 的 `states`）必须有且仅有一条 oracle；
- `human-first-review` 的 `evidence`、`evidence_sha256`、`capture_env` 与 `threshold_ref` 允许为 null，其余 kind 必须有证据 hash 与阈值；`golden` 的证据在 `golden/<region>/<state>.png`；
- 使用 `source-snapshot` 时 `source_page` 必填，且 oracle 记录 `capture_env`；`design-export` 必须记录 `source.refs` 的来源版本与 `export {scale, origin}`；
- `design-export` 的几何期望由 `region.source_anchor`（Sketch frame 或 prototype DOM）按 `export` 映射得到；`computed` 期望来自源页面测量、golden 测量或 `computed_expectations`；
- `layout` 与 `interactions` 是 Human 批准的内容，生成器只复制，不自行推断；
- 区域改名、增删、`states` 变化、state origin/hooks 变化、oracle 变化、`computed_expectations` 变化、`delta` 变化、screen/setup 变化均属内容变更，必须升版；
- 一个基线可被多个切片引用；引用旧版本的未结束切片在升版时级联（§6.5）。

### 4.3 assertions.yaml

由 skill 内的生成器从 `baseline.yaml`、`source_page.commit`、`rules.yaml`、`thresholds.yaml` 机械生成，不手写。

```yaml
schema: 3
baseline: person-verification-records@3
generated:
  generator_version: 1
  inputs:
    content_hash: <sha256>
    rules_hash: <sha256>
    design_md_hash: <sha256 | null>
    thresholds_hash: <sha256>
    waivers_hash: <sha256 | null>
    viewports_hash: <sha256>
    golden_hash: <sha256 | null>
    source_commit: <sha | null>
  output_hash: <sha256>        # 对除本字段外的整个文件内容做规范化 hash
structural:
  diff_scope:
    files: ["src/views/<new-page>/columns.ts"]       # = 所有 delta.files
    regions: ["table-body"]                           # = 所有 delta.regions（展开 state）
  must_import: [RecordsTable, FilterPanel]
  forbid: []                                          # rules.yaml 合并结果
  states:
    - screen: records
      state: default
      marker: '[data-screen="records"][data-state="default"]'
      regions_present: [filter-panel, table-header, table-body]
      regions_hidden: []
  interactions:
    - id: open-filter
      screen: records
      from: default
      action: {kind: click, target: '[data-region="filter-toggle"]'}
      to: filter-open
geometry:
  - region: filter-panel
    screen: records
    state: default
    expected_source: source-snapshot       # source-snapshot | design-export | golden | human
    expected_bbox: {x: 240, y: 96, width: 640, height: 48}   # CSS px，四值
    tolerance_ref: geometry.regression
computed:
  - region: table-header
    screen: records
    state: default
    expected_source: golden                # source-snapshot | golden | human
    tolerance_ref: computed.default
    props:
      font-size: 14px
      color: var(--color-text-secondary)
      padding: 8px 12px
layout:
  - region: filter-panel
    screen: records
    state: filter-open
    order: [filter-toggle, filter-fields, filter-actions]
    align: [{axis: horizontal, mode: start}]
    tolerance_ref: layout.default
pixel:
  - region: filter-panel
    screen: records
    state: default
    oracle: source-snapshot
    threshold_ref: regression.default
    mask: []
regression:
  - region: filter-panel
    screen: records
    state: default
    golden: golden/filter-panel/default.png
    sha256: <golden hash>
    threshold_ref: regression.default
```

约束：

- 每个 `region × state` 的 oracle 决定断言内容：`source-snapshot` / `design-export` / `golden` 生成 geometry、computed 与 pixel；`human-first-review` 在该版本不生成 geometry/computed/pixel，仅在结构层检查 `regions_present`；
- 断言中的每个期望值必须有持久出处：`source-snapshot`（源页面测量）、`design-export`（`source_anchor` + `export` 映射）、`golden`（golden measurements）、`human`（`computed_expectations`）；生成器发现缺失时直接失败，不得省略或自填；
- `layout` 与 `interactions` 断言由生成器从基线同名字段复制，不独立推断；
- `content_hash`、`rules_hash`、`design_md_hash`、`thresholds_hash`、`waivers_hash`、`viewports_hash`、`golden_hash` 变化时断言过期；`thresholds`、`rules`、`waivers`、`viewports` 变化与 golden 更新（需先获 Human 批准）可自动重生成，基线内容变化必须升版并重新批准；
- 存在 golden 的 `region × state` 生成 `regression` 条目，记录 golden 路径与 sha256；
- FREEZE 与 VERIFY 都重新运行生成器并比较 `output_hash`；不一致时按 §6.3 阻断。

### 4.4 切片文件

```markdown
---
id: S2
title: 列表页 default + filter-open
map: person-verification
kind: page                 # page | prefactor | integration
status: ready-to-build     # needs-triage | needs-info | needs-decision | ready-to-build | building | verifying | needs-review | settled
blocked_by: [S1]
blocked_reason: null       # 非 null 时 status 必须为 needs-triage
claimed_by: null
claimed_at: null
baseline_ref: person-verification-records@3
round: 0
harness: null              # prefactor 必填
flow: []                   # integration 必填
updated_at: <ISO>
---

## Goal
## Relation        relation + 证据
## Scan            查了哪里、候选、排除项与理由（原始日志在 .tmp）
## State Contract  screen/state/origin/hooks/setup 摘要 + 基线引用
## Structure Decisions
| region | state | origin | means | target | reason | flag | approved_by |

## Unknowns        已解决的 unknown：问题、结论、证据
## Deviations
## Approvals       每次 Human 决定一行：动作、时间、结论、content hash / 证据 hash
## Rounds          每轮一行：rNN、各层结论、报告路径
```

### 4.5 Design Map

```markdown
## Destination        Human 确认
## Notes              设计来源、登记的基线、组件目录位置、固定偏好
## Decisions so far   - [决策或基线名称](link)：一句话概述
## Not yet specified
## Out of scope       - 内容：理由
```

Frontier 不在地图中手写，由切片 frontmatter 推算：`status` 未结束、`blocked_by` 全部 `settled`、`claimed_by` 为空。

### 4.6 组件目录条目

```yaml
name: StatCard
path: src/components/StatCard
generation: gen2
language: [accent-bar, glow-background, state-semantics:success/warn/error]
regions_used_in: []
harness: null            # prefactor 可用的渲染入口，如 storybook id
notes: ""
approved_by: human
```

### 4.7 Design Reading

```yaml
source: { kind, refs, fidelity }
screens: [{ id, states: [] }]
regions: [{ id, screen, state, role: preserve|delta|unknown, source_anchor, dom_anchor }]
components: [{ name, evidence_refs, catalog_match }]
language: { tokens, spacing, typography, state_semantics, generation }
interactions: [{ from, event, to }]
unknowns: [{ question, blocks }]
```

Design Reading 可再生，存于 `.tmp/`。其中需 Human 确认的结论（`fidelity`、`relation`、screen/state 集合与 setup）必须落入基线或切片审批记录。

### 4.8 状态与状态驱动

- 状态由 `[data-screen]` 与 `[data-state]` 标识；`state marker` 用于断言状态已到达。
- `setup` 是有序配方，步骤类型：
  - `ui-action`：`{kind, action: click|fill|hover|press|select, target, value?}`，`target` 使用稳定选择器（`data-region`、`data-testid`、role+name）；
  - `fixture`：`{kind: fixture, name, params}`，由项目在 bootstrap 时指定的 fixture 提供者解析；
  - `wait`：`{kind: wait, condition}`，如 `selector:...` 或 `network-idle`。
- 状态集合、配方、marker、origin 与 hooks 是基线内容，由 Human 批准；实现必须在 BUILD 中提供 hooks 对应的稳定选择器。
- `origin: source`：该状态在 `source_page.commit` 上已存在。FREEZE 必须在该 commit 上预演 setup 并到达 marker，且 hooks 已存在。
- `origin: introduced`：该状态由本切片新增，或源页面缺少 hooks。FREEZE 只做结构校验（setup 步骤合法、target ⊆ regions ∪ hooks、marker 使用 data-screen/data-state），不预演；首次 VERIFY 第 1 层验证可达性，不可达则回到 `building`。
- 新页面切片的所有状态均为 `introduced`；hooks、setup 与 marker 在基线中固化，BUILD 必须实现，缺失视为结构不通过。

### 4.9 oracle evidence 与可再生产

- `source-snapshot`：从 `source_page.commit` 的工作区截取，存入 `v<N>/oracles/`；oracle 记录 `evidence_sha256` 与 `capture_env`；`source.refs` 必须记录来源版本（Sketch documentVersion、原型文件 hash、截图 hash）。
- `design-export`：导出图存入 `v<N>/oracles/`；oracle 记录 `export {scale, origin}`、`evidence_sha256`、导出工具版本；`origin` 为屏幕 Frame 原点，导出图像素只受 `scale` 影响。
- `golden`：存入 `v<N>/golden/<region>/<state>.png`；`golden/approval.yaml` 记录：

```yaml
version: 4
content_hash: <sha256>           # 批准时基线的 content_hash
regions:
  - region: filter-panel
    state: default
    sha256: <golden 图片 hash>
    threshold_ref: regression.default
    measurements:                # 供后续版本生成断言
      bbox: {x: 240, y: 96, width: 640, height: 48}
      computed: {font-size: 14px, color: var(--color-text-secondary)}
env:                              # 与 meta.yaml 同口径，用于失配检测
  browser: chromium
  browser_version: <major.minor>
  fonts_hash: <sha256>
  dpr: 1
  viewport: {width: 1440, height: 900}
approved_by: human
at: <ISO>
```

重新批准同一版本内的 golden 时，记录旧/新 `sha256` 与理由；旧图由 git 追溯。`human-first-review` 转 `golden` 时，measurements 取 Human 批准该轮时的实际测量值。

已采纳的 golden 同时作为该版本内该 `region × state` 的回归基准：VERIFY 的像素层除 oracle 外还与 golden 对比（§7.1、§7.4）。

- 证据重建规则：`.tmp/exports/` 只是缓存；证据缺失或来源版本变化时，切片回到 `needs-triage`，不得静默重建。

### 4.10 审批与哈希

- `content_hash`：对 `baseline.yaml` 中除 `status` 与 `approvals` 外的全部字段做规范化序列化后取 sha256；审批记录必须与该 hash 一致；工作区路径等环境本地字段不进入内容。
- `assertions.generated.output_hash`：对除 `output_hash` 外的整个断言内容做规范化序列化后取 sha256；生成器必须确定性输出。
- 不存在对 `assertions.yaml` 的手工修改或单独放宽：放宽只能通过基线内容、`rules.yaml`、`thresholds.yaml`、`waivers.yaml` 或 `viewports.yaml` 变更实现，且均需 Human 批准；断言文件只由生成器重写。
- `rules_hash`、`design_md_hash`、`thresholds_hash`、`waivers_hash`、`viewports_hash`：分别对对应文件内容取规范化 sha256；`thresholds.yaml` 的 approvals 记录 `{previous_hash, new_hash, by, at, reason}`。
- `golden_hash`：对当前版本 `golden/approval.yaml` 与所有 golden 图片的规范化清单取 sha256；golden 更新后必须重新生成断言。
- 规范化规则：UTF-8、LF、键排序、数组保持文档顺序、去除注释与空行；由生成器与检查器共用同一实现。

## 5. ENTRY 与 bootstrap

### 5.1 ENTRY 路由

ENTRY 只读，按顺序判断，命中即停：

| # | 条件 | 路由 |
|---|---|---|
| 1 | 项目无 `docs/island/designer/` | bootstrap，完成后重新 ENTRY |
| 2 | 项目根目录无 `DESIGN.md` | CREATE（配套草案 §5），完成后重新 ENTRY |
| 3 | Human 指出某个 `settled` 切片有问题 | reopen 该切片（Human 批准）+ retro |
| 4 | 存在本任务相关、未结束的切片 | Resume |
| 5 | 输入命中某个 active 地图的 Frontier 切片 | work |
| 6 | 输入命中某个基线 `scope`，且单切片可完成 | quick：新建独立切片 |
| 7 | 输入是单切片、预计单会话完成的任务（新页面、组件、局部改动），不命中既有基线 | quick：新建独立切片；CHART 只做最小切片定义 |
| 8 | 输入跨会话或预计两个及以上切片 | chart：提议地图 |
| 9 | 无输入 | 报告状态：Frontier、`needs-decision` 列表、过期 claim |

ENTRY 输出不超过 10 行的状态报告和建议路由，由 Human 确认后进入。

### 5.2 bootstrap

只写设计工件，不改产品代码：

1. 创建 `docs/island/designer/` 骨架、带预设值的 `thresholds.yaml`、`viewports.yaml` 与 `project.yaml`；
2. 用 `git check-ignore` 确认 `.tmp/` 被忽略；否则提议写入 `.git/info/exclude`；
3. 提议在项目 `AGENTS.md` 加入一行 ENTRY 规则，Human 批准后写入；
4. 在 `project.yaml` 记录 fixture 提供者（§4.8）与渲染 harness 形态（§8.2）；未定时写 `TBD`，不阻塞 bootstrap，但会阻塞首个使用它们的切片（§12.1）；
5. 提议一个 `prefactor` 切片用于组件目录初始盘点，不在 bootstrap 内执行。

bootstrap 只在 `docs/island/designer/` 缺失时运行；`DESIGN.md` 的创建由 ENTRY 路由第 2 行统一处理，见配套草案 §5。

## 6. 两层循环

### 6.1 Map Loop

```text
CHART → FRONTIER → WORK（一个切片走一遍 Slice Loop）→ ADVANCE
```

- CHART：确定 Destination（Human 确认），生成切片文件（初始 `needs-triage`）与阻塞关系；决定基线归属与共享关系；不实现任何切片。
- FRONTIER：由 frontmatter 推算可推进切片。
- WORK：一个会话认领并推进一个切片。
- ADVANCE：在 Decisions so far 记一行；Not yet specified 中已能精确定义的问题升级为新切片；全部完成时归档地图。

### 6.2 Slice Loop

| 步骤 | 产出 | 完成条件 |
|---|---|---|
| ENTRY | 状态报告与路由 | Human 确认路由 |
| READ | Design Reading（`.tmp/`） | 来源全部适配；`fidelity` 已由 Human 确认 |
| RELATE | 切片 Relation | 每个判断有证据；`independent` 已获 Human 批准 |
| SCAN | 切片 Scan | 完成 §6.2.1 的最小范围清单并记录候选、排除理由与 `completeness` 证据 |
| DECIDE | 切片 Structure Decisions | 所有 `region × state` 有 `means`；需 Human 的决策已批准 |
| FREEZE | 基线版本（如需）、断言、oracle | 见 §6.3 机械检查；内容变更在此完成升版与级联 |
| BUILD | 代码改动与 state 钩子 | 改动范围不超出 `delta.files`；`data-region` / `data-state` 已提供 |
| VERIFY | `rounds/rNN/report.yaml` | 见 §7 |
| REVIEW | 审批记录 | Human 结论 |
| SETTLE | golden、基线版本、地图记录 | 见 §6.5 |

#### 6.2.1 SCAN 最小范围

固定不得少于：组件目录、同 feature 或同路由相邻页面、全仓组件名搜索、运行页面或源页面实际比对。`Scan` 必须记录每个范围的查询与结果（`completeness`），供 REVIEW 与 Retro 使用。

SCAN 可交给 Researcher，但其产出只能是候选、排除项和证据，写入 `.tmp/island/designer/proposals/`，由 lead 合并进切片。

### 6.3 FREEZE 机械检查

全部满足才能进入 `ready-to-build`：

1. 基线版本就绪：可引用当前 active 版本；若本轮需要新增或修改 screen、state、origin、hooks、region、delta、oracle、`computed_expectations`、`interactions` 或 scope，先在 `v<N+1>` 写入完整候选内容，Human 批准 content_hash，更新 `current.yaml`，旧版本标记 `superseded` 并执行级联，同时把本切片 frontmatter 的 `baseline_ref` 指向新版本；`current.yaml.version` 必须与 `baseline.yaml.status: active` 一致；
2. 每个 `region × state` 恰有一条 oracle；`human-first-review` 的 evidence、evidence_sha256、capture_env 与 threshold_ref 为 null；其余 oracle 的 evidence 存在且 `evidence_sha256` 匹配；`design-export` 有 `export {scale, origin}`、来源版本与 `source_anchor`，且无源页面/golden 的 computed 期望必须有 `computed_expectations`；`source-snapshot` 有 `capture_env`；`golden` 证据在 `golden/` 且 hash 与 `golden/approval.yaml` 一致；
3. screen、state、origin、setup、marker、hooks 字段完整；`origin: source` 的状态已在 `source_page.commit` 上预演并到达 marker；`origin: introduced` 的状态通过结构校验（setup 步骤合法、target ⊆ regions ∪ hooks、marker 使用 data-screen/data-state）；
4. `assertions.yaml` 重新生成后 `output_hash` 一致；`content_hash`、`rules_hash`、`design_md_hash`、`thresholds_hash`、`waivers_hash`、`viewports_hash`、`golden_hash` 当前值一致；
5. 不存在 `blocks` 非空且未解决的 `unknowns`；已解决的 unknown 记录在切片 `## Unknowns`；
6. 需 Human 的条目（`new` / `extend` / `independent` / `DEVIATION` / 基线内容 / golden 更新）均有审批记录；
7. `viewport_ref` 存在于 `viewports.yaml`；阈值、waiver、golden 已绑定当前版本；
8. `prefactor`：`project.yaml` 的 harness 已配置且可打开；`integration`：允许 `baseline_ref: null`，`flow` 每一步解析到 active 页面基线，断言文件 `baseline: null` 且只含 structure / interactions；
9. 所有带 `capture_env` 的 oracle 证据与当前快照环境一致，或已有 Human 批准的失配豁免；
10. 基线内容审批记录的 `content_hash` 与当前内容一致。

阻断时切片进入 `needs-triage`，`blocked_reason` 记录具体项（如 `assertions-stale`、`oracle-missing`、`baseline-superseded`、`env-mismatch`、`harness-pending`）。

### 6.4 BUILD

- 直接模式：lead 实现。
- 派发模式：调用 `yes-subagents` Coder / Coder Plus，映射见 §10.2。
- 实施者发现必须改动 `delta` 以外的内容时，停止并提出 `DEVIATION`，切片回到 `needs-decision`。
- 实现必须提供 `data-region`、`data-screen`、`data-state` 与 setup 所需稳定选择器；缺失视为结构不通过。

### 6.5 SETTLE

1. Human 逐 `region × state` 批准本轮区域截图，并决定该区域是否采纳为 golden：
   - `delta` 区域默认采纳；`preserve` 区域默认保留原 oracle（`source-snapshot`）；
   - `human-first-review` 区域必须采纳，否则切片不能 settled。
2. golden 是验收证据，不是基线内容：写入或更新 `v<N>/golden/<region>/<state>.png` 与 `golden/approval.yaml`（含 measurements、env、sha256），作为该版本内该 `region × state` 的回归基准，golden 更新后重新生成断言（不升版）；同一版本内重新批准时记录旧/新 hash，旧图由 git 追溯，不创建新版本；
3. 例外：把 `human-first-review` oracle 转为 `golden` 属于基线内容变更：创建 `v<N+1>`，oracle kind 改为 `golden`（threshold_ref 默认 `regression.default`），Human 批准 content_hash，更新 `current.yaml`，旧版本标记 `superseded`，并按第 8 步级联；
4. 升版时，未被本轮修改的 `region × state` 的 golden 复制进新版本目录，保留原批准 hash 与 measurements；被修改区域必须由 Human 重新批准；
5. 写入顺序固定为：证据与 golden approval → Human 批准（content hash 或 golden hash）→ `current.yaml` 指针（仅升版时）→ 旧版本状态；任何一步失败，`current.yaml` 不变；
6. 先把本切片置为 `settled`，`baseline_ref` 更新为当前 active 版本，记录审批；
7. 释放 claim，更新 `updated_at`；
8. 若发生升版：把其余引用被 superseded 版本、且状态属于 `ready-to-build` / `building` / `verifying` / `needs-review` / `needs-decision` 的切片级联为 `needs-triage`，`blocked_reason: baseline-superseded`；已 `settled` 切片不自动重开，需 Human reopen 后按当前 active 版本重冻并重批 golden；
9. 地图内切片触发 Map Loop 的 ADVANCE。

## 7. 验收

### 7.1 分层

对切片涉及的每个 `screen × state` 依次执行；层内任一 `region × state` 失败即该层失败，报告聚合：

```text
1 STRUCTURAL   diff 范围、must_import、forbid、各 state 的 regions_present / regions_hidden、interactions
2 GEOMETRY     各 region × state 的 bbox（期望值来自断言）
3 PIXEL        各 region × state 的区域裁图对比：验收 oracle；若已有 golden，另做回归对比
4 INTERPRET    agent 只解读失败区域的 expected | actual | diff 三联图
5 HUMAN        首轮无设计稿区域、golden 更新、阈值外差异、取舍
```

前一层失败即停止，切片状态回到 `building`，`round` 加一。`human-first-review` 区域在首次实现轮只执行第 1、5 层；批准并转为 `golden` 后进入完整分层。

### 7.2 oracle 类型

| 类型 | 适用 | FREEZE 时 | 首轮可执行的层 | 证据存放 |
|---|---|---|---|---|
| `source-snapshot` | `preserve` 区域；`inherit` 的源页面 | 在 `source_page.commit` 截取 | 1–4 | `v<N>/oracles/` |
| `design-export` | 有设计稿、Sketch、`pixel` 原型、Human 声明 pixel 的截图 | 导出并记录 `{scale, origin}`、来源版本与导出工具版本 | 1–4 | `v<N>/oracles/` |
| `golden` | 已有 Human 批准快照的区域；`human-first-review` 批准后转此类型 | 引用当前版本 golden 与测量记录 | 1–4 | `v<N>/golden/` |
| `human-first-review` | 无设计稿、描述类来源、`visual` / `layout` 原型的 delta 区域 | 无需图像 | 1、5；批准后升版转 `golden` | — |

坐标映射：`design-export` 的期望 CSS bbox = `region.source_anchor.frame` 减去屏幕 Frame 原点（`origin`），设计单位与 CSS px 1:1；`scale` 只影响导出图像素，不影响期望 CSS px。`source-snapshot` 的几何期望来自 `source_page.commit` 上的 DOM 测量；`golden` 的几何与 computed 期望来自 `golden/approval.yaml` 的 measurements。所有图像型 oracle 记录 `capture_env`，`design-export` 记录导出工具版本。

### 7.3 来源能力矩阵

`preserve` 区域与来源无关，始终使用 `source-snapshot` 或 `golden`。下表只决定 `delta` 区域。

| 来源 | fidelity | delta oracle | 几何 | 计算样式 | 像素 | 阈值组 |
|---|---|---|---|---|---|---|
| Sketch | pixel | `design-export` + scale 映射 | 期望 bbox（`source_anchor` + export 映射） | `computed_expectations`（Human/design-tokens）；后续 golden 测量 | 是 | `fidelity.*` |
| 原型 HTML | pixel | `design-export`（原生尺寸截图） | 期望 bbox（prototype DOM 测量） | 原型测量或 `computed_expectations`；后续 golden | 是 | `fidelity.*` |
| 原型 HTML | visual | `human-first-review` | 首轮无；批准后转 golden | 首轮无 | 首轮无 | — |
| 原型 HTML | layout | `human-first-review` + `layout` 断言 | 仅 order / align | 首轮无 | 首轮无 | `layout.default` |
| 截图 | pixel（Human 声明 `scale`） | `design-export` | 按声明映射 | 按声明或 `computed_expectations` | 是 | `fidelity.*` |
| 截图 | visual（默认） | `human-first-review` | 首轮无 | 首轮无 | 首轮无 | — |
| 既有页面 | visual（默认） | 有 golden 用 `golden`，否则 `human-first-review`；`preserve` 用 `source-snapshot` | 有 golden 或源页面时是 | 有 golden 或源页面时是 | 是 | `regression.*` |
| Human 描述 | visual | `human-first-review` | 首轮无 | 首轮无 | 首轮无 | — |

### 7.4 阈值与校准

`thresholds.yaml` 按 ID 引用；区域在 FREEZE 时绑定 `threshold_ref`，VERIFY 期间不可改；阈值内容以 `thresholds_hash` 固化进断言。

| ID | 指标 | 预设 |
|---|---|---|
| `geometry.regression` | bbox 四值取整到 CSS px 后之差 | 0 px |
| `geometry.fidelity` | 位置与尺寸 / 文本块高度 | ±1 px / ±2 px |
| `computed.default` | 属性值规范化后相等 | 完全相等 |
| `layout.default` | 子元素顺序 / 主轴对齐 | 完全相等 |
| `regression.default` | pixelmatch，单像素阈值 0.1，`includeAA: false` | 差异像素数 ≤ `min(max(5, 0.001 × 区域像素数), 500)` |
| `fidelity.graphic` | SSIM | ≥ 0.95 |
| `fidelity.text` | SSIM | ≥ 0.90 |

`regression.default` 同时受面积比例与绝对上下限约束：小区域有绝对下限，避免一像素误报；大区域有绝对上限，避免掩盖可见缺陷。

校准（环境稳定性检查，不是正则化手段）：

- 同一提交、同一环境连续截图 20 次，按区域统计差异像素数，取 p95 作为噪声上界 N；
- 若任一区域的 N 超过该区域在 `regression.default` 下允许的差异像素数，判定环境不稳定：切片 `BLOCKED`（`env-unstable`），不得自动放宽阈值；
- 确需在噪声环境运行时，只能由 Human 批准 `waivers.yaml` 中的 `noise-exception`，记录原因与失效条件；
- 阈值放宽（任何 ID）需 Human 批准并在 `thresholds.yaml` 记录 `{id, previous, new, by, at, reason}`。

waiver：`waivers.yaml` 记录 `{id, region, state, layer, diff, reason, approved_by, at, expires_when}`；waiver 随基线版本失效，不能跨版本继承。阈值外但 Human 接受一次的差异必须落为 waiver，不能口头放行。

golden 回归：存在 golden 的 `region × state`，像素层除 oracle 对比外必须与 golden 对比，阈值 `regression.default`；回归失败与验收失败同样阻断。

环境一致性：VERIFY 时比较 `meta.yaml` 与 golden `approval.yaml` 及所有 `source-snapshot` oracle 的 `capture_env`；浏览器主版本、字体哈希、DPR、viewport 任一不一致即 `BLOCKED`（`env-mismatch`），需 Human 批量重新批准。

### 7.5 快照环境

`rounds/rNN/meta.yaml` 记录：commit SHA、viewport_ref、viewport、DPR、浏览器版本、字体就绪状态与字体哈希、数据 fixture 哈希、时间、来源引用、mask 清单。截图前等待 `document.fonts.ready`，关闭动画、过渡与光标，隐藏滚动条，按 oracle 的 `mask` 覆盖动态内容。

## 8. 切片

### 8.1 原则

1. 纵向：一个切片包含结构、样式、状态与验收。
2. 一个切片只挂一份基线版本。
3. 状态属于验收维度：每个 state 必须有可达 setup 与 marker；同一 screen 的多状态可在一个切片内，但每个 `region × state` 独立验收。
4. 每个切片有自己的区域与 oracle。
5. 规模预设：一个 screen、不超过 3 个状态、不超过 5 个 `delta` 区域；超过则拆分。预设经 eval 调整。
6. 页内交互属于所在 `page` 切片，以状态切换断言验收。

### 8.2 切片类型

| 类型 | 用途 | 必需字段 | 验收 |
|---|---|---|---|
| `page` | 一个 screen 的若干状态 | `baseline_ref` | 完整五层，按 state 迭代 |
| `prefactor` | 被多个切片依赖的共享组件，或组件目录盘点 | `harness`（`project.yaml` 登记：storybook id 或预览路由；未登记时该切片 `needs-decision`）+ `baseline_ref` | 结构与组件自身区域；设计代际判断交 Human；screen 使用 harness 入口 |
| `integration` | 跨 screen 的流程连线 | `flow`（步骤→目标 screen/state）+ 引用的页面基线 | 按流程逐步触发，检查到达的 screen/state 与对应区域断言；默认不生成自有像素 oracle |

`prefactor` 的 screen 使用 harness 入口作为 route，states 默认只有 `default`（setup 为空），marker 为 `[data-screen="<component>"]`，regions 至少包含组件根区域；oracle 由 Human 指定（`design-export` 或 `human-first-review`）。

`integration` 允许 `baseline_ref: null`：FREEZE 只生成 structure / interactions 断言（`baseline: null`），按 `flow` 逐步触发并检查到达的 screen/state；像素与区域断言复用被引用页面基线的断言，不另建 oracle。

两者若需像素基准，由 Human 指定 oracle 后建立基线版本。

### 8.3 状态机

| 从 | 到 | 条件 | 执行者 |
|---|---|---|---|
| `needs-triage` | `needs-info` | 缺来源或证据 | lead |
| `needs-triage` | `needs-decision` | 存在需 Human 的决策 | lead |
| `needs-triage` | `ready-to-build` | 基线版本获批且 FREEZE 机械检查通过 | lead |
| `needs-info` | `needs-triage` | 补到信息 | lead |
| `needs-decision` | `needs-triage` | Human 已决定 | Human 决定，lead 写入 |
| `ready-to-build` | `building` | 认领 | lead |
| `ready-to-build` | `needs-triage` | 基线被 superseded / 断言过期 | 机械 |
| `building` | `verifying` | 实现完成 | lead |
| `building` | `needs-decision` | 提出 `DEVIATION` | 任何人 |
| `building` | `needs-triage` | 断言或基线失效 | 机械 |
| `verifying` | `building` | 第 1–3 层失败 | 机械 |
| `verifying` | `needs-triage` | `BLOCKED`：断言过期、环境失配、oracle 不可用 | 机械 |
| `verifying` | `needs-review` | 第 1–3 层通过（`human-first-review` 区域仅第 1 层） | 机械 |
| `needs-review` | `building` | Human 驳回视觉 | Human 决定，lead 写入 |
| `needs-review` | `needs-decision` | Human 驳回结构或取舍 | Human 决定，lead 写入 |
| `needs-review` | `settled` | Human 批准 | Human 决定，lead 写入 |
| `settled` | `needs-triage` | reopen：Human 指出问题；若基线版本已变化或区域被修改，需按当前版本重冻并重新批准 golden | Human 决定，lead 写入 |
| 任何未结束状态 | `needs-triage` | 引用版本被 superseded | 机械，`blocked_reason: baseline-superseded` |

每次状态转移更新 frontmatter；Human 执行的转移在 Approvals 记一行。`blocked_reason` 只允许出现在 `needs-triage`；离开 `needs-triage` 时必须在同一次写入中置为 null。

### 8.4 认领与并发

- 认领即写 `claimed_by` / `claimed_at`，以 frontmatter 为 CAS：读取到 `claimed_by: null` 才能写入；两个会话同时认领时后写者失败并重新 ENTRY。
- 同一地图同一时刻最多一个未过期 claim；不同地图可并行。
- `claimed_at` 超过 24 小时且 `updated_at` 无变化的 claim，ENTRY 报告为过期，由 Human 决定释放。
- 同一基线被多个切片引用时，基线只在 FREEZE（内容变更）或 SETTLE（`human-first-review` 转 `golden`）升版，并按 §6.3 / §6.5 级联；已 `settled` 切片不被级联，因此不会形成跨地图的反复升版循环。
- 组件目录与 `DESIGN.md` 由 lead 串行写入；不同地图并行时的目录冲突由 lead 在 ADVANCE 合并。

## 9. Retro

触发：Human 指出问题；切片被 reopen；同一切片同类失败连续两轮。

Retro 只产出环境修改提案，不改业务代码：

| 问题 | 提案 | 批准 |
|---|---|---|
| 机械性结构偏离未被拦下 | 生成器默认 `forbid` 规则 | Human |
| 几何反复偏移 | region bbox 断言或区域拆分 | Human |
| 状态 setup 不可达 | setup 配方修正或 state marker 调整 | Human |
| 设计代际误判 | 组件目录 `generation` / `language` 标记 | Human |
| 流程被绕过 | 项目 `AGENTS.md` 的 ENTRY 规则 | Human |
| 范式层面的偏差（优先级、拒绝项、检查项） | `DESIGN.md` 规范级提案；可机械检查时同步 `rules.yaml` | Human |
| 扫描遗漏 | 扫描范围规则或组件目录条目 | lead |

## 10. 与其它能力的边界

### 10.1 sketch-copilot-pro（原 sketch-copilot-plus）

提供 Sketch 事实与截图。已核实（`verified_against`: `/Users/teatao/Projects/skill_sketch-copilot` HEAD `6d702d5`，`skills/pro` v0.2.7，`dispatch-packet-template.md` sha256 `5b19eb9bc0053d30f5b5af43e613c3bd1f8d14b7`，核对日期 2026-10-18；工作区有未提交改动，接入前须重新核对）：该模板已包含 `DESIGN_EVIDENCE`（含 `design_relation`、`preserve`、`delta`）与 `REUSE_MAP`，并保留 `GOAL`、`VERIFY_TARGET`、`LEAD_HANDOFF`、`SUBAGENT_ACK`。

本草案的消费规则：

- `design_relation`、`preserve`、`delta` 只作为 RELATE 与 DECIDE 的证据输入，不直接成为基线；
- `design_relation: variant` 映射为 `inherit` 候选，仍需代码侧确认；
- packet 的派发段落在 `yes-designer` 存在时不作为编排依据；
- 消费的 packet 字段随 skill 版本固定；该 skill 版本变化时，须重新核对本映射并更新 `verified_against`。

packet 字段的调整推迟到 `yes-designer` 完成后，见 §12.2。

### 10.2 yes-subagents

已核实各角色前置条件（`yes-subagents` v0.7.0，与当前工作区一致），映射如下：

| 角色 | 前置要求 | yes-designer 提供 |
|---|---|---|
| Coder Plus | 实现内容 | Structure Decisions + 基线版本 + `delta.files` + states/setup |
| Coder Plus | 验收标准 | Human 批准的 `baseline.yaml@version` + `assertions.yaml`（含 `output_hash`） |
| Coder Plus | 可编辑边界 | `delta.files` + claim 范围 + `forbid` 规则 |
| Coder Plus | 下游接口承诺 | region 契约（`data-region`）、state 契约（`data-screen` / `data-state`）、`must_import`、组件与 token 边界 |
| Coder Plus | Git 策略与 Git 基线 | 派发简报：起始 HEAD、staged / unstaged / untracked 快照、worktree 路径、提交与 ownership 规则 |
| Critic Gate | 唯一权威基线；验收标准须为 Human 认可 | Human 批准的 `baseline.yaml@version` 及其生成断言 |
| Researcher | 明确问题与调查边界 | SCAN 的问题与范围 |

派发简报（handoff）写入 `.tmp/island/designer/dispatch/<slice>-rNN.yaml`，内容为上述映射的字段集合与引用的基线/断言 hash；由 lead 生成，不作为持久真源；`yes-subagents` 是否接受该简报格式属实现验证（§12.4）。

推论：派发模式要求基线已有 Human 批准记录，否则 Critic Gate 将返回 BLOCKED。直接模式同样可以调用 Critic Gate，因为审查者与实现者不同。

当前不需要修改 `yes-subagents`。

### 10.3 DESIGN.md

yes-designer 负责创建与维护项目根目录 `DESIGN.md`。框架、CREATE、GROW 与各步骤接点见配套草案 `2026-10-17-design-md-framework-draft.md`。

- 引用方向：`DESIGN.md` 定义词汇 ← 组件目录 ← 基线；不反向复制。
- 缺失时复制内置模板（中文，含 R-001 至 R-005）；基础版本下代际判为 `unknown` 的情况增多，更多决策交给 Human，流程不阻塞。
- 配套草案与本草案必须联合批准：本草案批准时，配套草案必须处于已批准状态；两者版本号在 `docs/island/designer/` 的记录中绑定。

## 11. 示例：Sketch 多状态界面

输入：列表页（default / filter-open / empty / loading）、新建弹窗（blank / invalid）、详情抽屉（default）与 prototype 连线。

```text
S1  prefactor    StatusTag / FieldRow 与组件目录比对         needs-decision（设计代际）
S2  page         列表页 default + filter-open                 blocked_by S1
S3  page         列表页 empty + loading                       blocked_by S2
S4  page         新建弹窗 blank + invalid，含页内校验交互     blocked_by S1
S5  page         详情抽屉 default                             blocked_by S1
S6  integration  列表 → 弹窗 → 列表刷新；列表 → 抽屉           blocked_by S3 S4 S5

Not yet specified：详情抽屉编辑态（无对应 Frame）
Out of scope：导出功能
```

S2 的推进：

```text
ENTRY    命中地图 person-verification，S2 为 Frontier
READ     Design Reading：source=sketch，fidelity=pixel，screens=[records]，states=[default, filter-open]
RELATE   inherit person-verification-records@3（Human 已批准 relation）
SCAN     组件目录 + 相邻页面 + 全仓搜索：RecordsTable 可 reuse，FilterPanel 可 reuse
DECIDE   骨架 copy；表格 reuse；列定义 delta
FREEZE   基线 v4（新增 state/oracle 属内容变更）：
           screens.records.states = [default(source), filter-open(introduced)]
           oracles: filter-panel@default(source-snapshot) + filter-panel@filter-open(human-first-review)
           Human 批准 content_hash；断言 output_hash 生成并通过校验
BUILD    在 delta.files 内实现；提供 data-region / data-screen / data-state
VERIFY   按 state 迭代：结构 → 几何 → 像素（filter-open 首轮只走结构 + Human）
REVIEW   Human 逐 region × state 批准
SETTLE   golden 写入 v4（不升版）；filter-open 的 human-first-review 转 golden → 创建 v5，Human 批准 content_hash
```

## 12. 待决事项

### 12.1 待定（需 Human 或项目决定）

1. `prefactor` 的渲染 harness 形态（Storybook / 预览路由 / 单测渲染）与组件入口登记方式。bootstrap 先写 `TBD`；首个 prefactor FREEZE 前由 Human 决定，未决定时该切片 `needs-decision`。
2. 数据 fixture 的提供者（项目测试设施 / 轮次内 mock）与 `fixture` 步骤的解析协议。首个使用 `fixture` 的状态在 FREEZE 前必须确定，否则该切片 `needs-decision`。

以上两项不阻塞 bootstrap 与其他切片，只阻塞依赖它们的切片。

### 12.2 推迟到下一阶段

- 触发描述与 `SKILL.md` 打包。
- `sketch-copilot-pro`（原 `sketch-copilot-plus`）的协调调整：packet 字段与 `implement.md`、`verify.md` 的定位，待 `yes-designer` 完成后再调整。

### 12.3 已决定

- 术语以本草案 §2 为准；背景笔记保留原文，并在文首各加一行指向本文 §2 的指针。
- issue #1 仅作参考，不要求逐条映射。
- 配套 `DESIGN.md` 草案与本文联合批准：本文批准时，配套草案必须已批准；版本绑定的记录写入 `docs/island/designer/`。这不是推迟项。
- `means: new` 必须由 Human 在 DECIDE 阶段批准，不再由 lead 自判。
- 状态为一等验收维度；每个 `region × state` 独立 oracle；状态区分 `source` 与 `introduced`。
- 断言由生成器生成，FREEZE 与 VERIFY 校验 `output_hash`；期望值必须有持久出处。
- 基线内容变更在 FREEZE 或 `human-first-review` 转 `golden` 时升版；golden 快照更新不升版但需 Human 批准。
- 所有 oracle 证据、golden、阈值、waiver、viewports 都记录 hash 与环境，并纳入断言 inputs。
- 一个基线绑定一个断点。
- 已 settled 切片不因基线升版自动重开。

### 12.4 待验证（技术验证轮）

- 断言生成器的确定性（同一输入重复生成 `output_hash` 一致）；
- `must_import`、`diff_scope` 能否从 `source_page.commit` 机械推导；
- 运行环境：skill 目录自带 Playwright、pixelmatch，并依赖本机 ImageMagick 7；
- `regression.default` 的面积归一与绝对上下限在真实页面上的误差分布；
- 取整后 0 px 几何断言的稳定性；
- golden measurements 的采集与重放；
- 证据 hash 与 `capture_env` 在真实项目中的校验；
- FREEZE 升版协议与跨地图级联在真实项目中的行为；
- Coder Plus 是否遵守 `delta.files` 边界与 Git 策略，以及是否接受派发简报格式；
- 状态 setup 配方在真实项目中的可执行性与 fixture 对接；
- bootstrap 在真实项目中的写入权限：`.git/info/exclude`、`AGENTS.md` 修改流程与 `assets/DESIGN.template.md` 分发路径；
- eval fixture 的仓库与数据来源。

## 附录 A：Round 3 修复对照

| 编号 | 问题 | v4 修复位置 | 状态 |
|---|---|---|---|
| FATAL-R | golden 与 design-export/Sketch 的期望值出处缺失 | §4.2（oracle 的 evidence_sha256/export/capture_env、region.source_anchor、computed_expectations）、§4.3（期望值出处约束）、§4.9（golden measurements）、§6.3 检查 2 | 已修复 |
| FATAL-N1 | inherit 新状态预演循环 | §2（state origin）、§4.2（states.origin/hooks）、§4.8（source 预演 / introduced 延后）、§6.3 检查 3、§7.1 | 已修复 |
| MAJOR-1 | 版本生命周期与跨地图级联循环 | §6.3 检查 1（FREEZE 升版协议）、§6.5（golden 不升版、仅转换升版）、§8.4（级联不循环）、§11 | 已修复 |
| MAJOR-2 | 证据/豁免 hash 未校验 | §3 不变量 11、§4.2（evidence_sha256）、§4.9（golden sha256/measurements）、§4.3（waivers/viewports/golden hash、regression 条目）、§6.3 检查 2/9、§7.4 | 已修复 |
| MAJOR-3 | content_hash 含工作区路径 | §4.2（删除 worktree 字段）、§4.10（排除环境本地字段） | 已修复 |
| MAJOR-4 | prefactor/integration 不可 FREEZE | §4.4（harness/flow）、§5.2（TBD 占位）、§6.3 检查 8、§8.2（组件 screen 语义、integration baseline null） | 已修复 |
| MAJOR-5 | 附录/§12 收口失真 | 本附录与 §12 按实际状态重写；§12.2 移除配套批准推迟项 | 已修复 |
| MAJOR-6 | 非 golden oracle 无环境证据 | §4.2（capture_env）、§4.9、§6.3 检查 9、§7.4（全量 env 校验） | 已修复 |
| MAJOR-7 | state 契约落点缺失 | §4.2（screens.states.origin/hooks）、§4.4（State Contract）、§4.8、§6.3 检查 3 | 已修复 |
| MAJOR-8 | bootstrap 依赖未决输入 | §5.2（TBD 占位）、§6.3 检查 8（harness-pending）、§12.1（阻塞边界） | 已修复 |
| MINOR | 示例 golden 采纳、baseline_hash/content_hash 命名、blocked_reason 清除、unknowns 记录、golden evidence 路径、截图 pixel 与矩阵、fidelity 枚举 | §2、§4.3、§4.9、§4.10、§7.2、§7.3、§8.3、§11 | 已修复 |
| UNVERIFIED | 5 项 | §12.4 已覆盖；`sketch-copilot-pro` 版本在 §10.1 固定为 HEAD + 版本 + 文件 hash | 已处理或保留为待验证 |
| ESCALATE | 配套草案、sketch 版本、handoff 格式、空 DESIGN.md、旧版本文档 | §10.3（联合批准）、§12.3（背景指针、联合批准）、§10.1（版本固定）、§10.2（格式待验证）；v1/v2/v3 文首加被取代指针；空 `docs/DESIGN.md` 移交 Human | 已处理或已移交 |

## 附录 B：早期修复对照（承继）

| 编号 | 问题 | 状态 |
|---|---|---|
| Round 1 F1 | 切片状态持久化 | v2 修复，v4 保持（§4.4、§4.5、§5.1、§8.3） |
| Round 1 F2 | 冻结门禁可校验 | v2 部分，v4 由 FATAL-2/FATAL-R 补齐 |
| Round 1 F3 | 降级自判、断言自证 | v2 修复；v4 收紧（`new` 一律 Human、断言 hash 与期望值出处校验） |
| Round 1 F4 | 无设计稿与 FREEZE 冲突 | v2 修复，v4 统一到 state 维度（§7.2、§7.3、§6.3） |
| Round 2 FATAL-1 | 多状态验收键无 state | v3 修复，v4 保持并补 origin |
| Round 2 FATAL-2 | 断言不可完整机械执行 | v3 部分，v4 由 FATAL-R 补齐 |
| Round 2 M1–M12 | 见 Round 3 附录 | v3 修复 7 项；v4 补齐 M2/M3/M6/M9 残项与 M11 收口 |
