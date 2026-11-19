---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-17-yes-designer-design-work-loop-v2.md
---
# yes-designer 设计推进工作流草案 v2

- 日期：2026-10-17
- 状态：草案 v2（Round 2 FAIL）；已被 `2026-10-18-yes-designer-design-work-loop-v6.md` 取代，不视为合同
- 前一版：`2026-10-17-yes-designer-design-work-loop-draft.md`（742 行，Round 1 FAIL）
- 背景材料（历史，术语以本文为准）：
  - `2026-10-16-design-collaboration-architecture.md`
  - `2026-10-17-sketch-copilot-plus-adapter-boundary.md`
- 本版修复对照见文末附录 A。

## 1. 目标与非目标

`yes-designer` 管理并推进设计落地：把任意来源的设计输入转换为统一的 Design Reading，建立并维护持久的实现基线，将设计工作拆成可独立验收的切片，并组织从基线、实现、分层验收到快照沉淀的闭环。

不负责：

- 代替 Human 做视觉品味、设计代际和产品语义的判断；
- 解读 Sketch 原始事实（由 `sketch-copilot-plus` 提供）；
- 通用派发、上下文隔离和工程执行（可选调用 `yes-subagents`）；
- 将原型 HTML 的 DOM 结构直接作为项目结构；
- 依赖 agent 记忆维持跨轮次一致性。

## 2. 术语表

本文术语为唯一权威。背景笔记与 Sketch packet 中的旧术语按下表映射。

| 术语 | 定义 | 旧术语映射 |
|---|---|---|
| `relation` | 当前设计与既有实现的关系：`inherit` / `independent` / `unknown` | `inheritance: copy/extend/variant` 中的关系部分；Sketch `design_relation: variant` 仅作为 `inherit` 的候选证据 |
| `means` | 区域级代码实现手段：`copy` / `reuse` / `extend` / `new` / `blocked` | `decision: reuse/extend/new/blocked` |
| `delta` | 允许改动的白名单：区域 + 文件范围 + 改动类型 | 旧 `delta` 语义相同，但现为白名单 |
| `preserve` | 不再显式列出；`inherit` 下凡不在 `delta` 中的即为保留 | 旧 `preserve` 列表 |
| `region` | 语义区域，身份等于 DOM 上 `data-region` 的值，在基线内唯一 | — |
| `oracle` | 区域对比基准的类型，见 §7.2 | `pixel oracle` |
| `golden` | Human 批准的区域快照，按基线版本归档 | — |
| `generation` | 设计代际标签，由组件目录维护（如 `gen1`、`gen2`）；无法识别时为 `unknown` | `language.generation` |
| Map Loop | 外层：CHART → FRONTIER → WORK → ADVANCE | 原外层 `SETTLE` 改名 `ADVANCE` |
| Slice Loop | 内层：ENTRY → READ → RELATE → SCAN → DECIDE → FREEZE → BUILD → VERIFY → REVIEW → SETTLE | — |
| Resume | ENTRY 命中一个已存在、未结束切片时的路由：读取切片 frontmatter、决策与审批记录后继续 | 原文未定义 |
| lead | 运行 `yes-designer` 的主会话 agent | — |

## 3. 不变量

1. 每轮 UI 任务先执行 ENTRY，读取工件，不依赖对话记忆。
2. 默认 `inherit`；`independent` 必须有证据并经 Human 批准；证据不足为 `unknown`。
3. 切片状态未达 `ready-to-build` 不写 UI 代码。
4. `inherit` 下改动只允许落在 `delta` 白名单内；漏写 `delta` 只会使检查更严。
5. 结构断言由生成器从基线和源页面机械生成，lead 和实施者均不手写。
6. 验收分层执行，前一层失败不进入下一层；视觉通过不能抵消结构失败。
7. golden、基线、断言、阈值的创建与放宽，只能由 Human 批准。
8. `docs/island/designer/` 只由 lead 写入；项目根目录 `DESIGN.md` 由 Human 直接编辑或由 lead 按 Human 指示写入；subagent 只产出提案。

### 3.1 决策权

| 决策 | 决定者 | 记录位置 |
|---|---|---|
| `means: copy / reuse`，附证据 | lead | 切片 Structure Decisions |
| `means: new`，扫描范围完整且无候选 | lead；REVIEW 时单列提示 Human | 同上，标记 `flag: new-without-candidate` |
| `means: new`，存在候选但被排除 | Human | 同上 + 审批记录 |
| `means: extend` 共享组件 | Human | 同上 + 审批记录 |
| `relation` 由 `inherit` 或 `unknown` 改为 `independent` | Human | 切片 Relation + 审批记录 |
| 接受 `DEVIATION` | Human；任何人可提出，实施者不能自批 | 切片 Deviations + 审批记录 |
| 基线创建、升版、失效 | Human | `baseline.yaml` approvals |
| 放宽断言、改阈值、更新 golden | Human | 对应文件 approvals |
| 设计代际是否一致、能否合并 | Human | 组件目录条目 + 切片审批记录 |
| `DESIGN.md` 指针级更新、追加 Known Gaps | lead | `design-md.log.md` |
| `DESIGN.md` 规范内容的修正与补充 | Human（直接编辑或指示 lead） | `design-md.log.md` |

## 4. 工件与存储

### 4.1 存储布局

```text
DESIGN.md                                  项目根目录，设计范式总约束（见配套草案）

docs/island/designer/                      持久，进仓库，仅 lead 写入
  design-md.log.md                         DESIGN.md 的来源、审批与待审队列
  rules.yaml                               可机械检查的规则，按编号指回 DESIGN.md
  catalog/<component>.yaml                 组件目录条目
  baselines/<baseline-id>/
    baseline.yaml                          基线（Human 批准）
    assertions.yaml                        生成的断言（随基线版本）
    golden/v<N>/<region-id>.png            按基线版本 × 区域归档
    golden/v<N>/approval.yaml
  maps/<effort>/map.md                     Design Map
  maps/<effort>/slices/NN-<slug>.md        地图内切片
  slices/<YYMMDD>-<slug>.md                无地图的独立切片
  thresholds.yaml                          阈值预设与校准记录

.tmp/island/designer/                      一次性，被忽略
  readings/<slice>.yaml                    Design Reading
  scans/<slice>.md                         扫描原始日志
  exports/<baseline-id>/                   设计稿导出、源页面快照缓存
  rounds/<slice>/rNN/                      每轮快照、diff、report、meta
  proposals/                               subagent 提案
```

判定依据：后续轮次或协作者需要读取、或包含 Human 确认的内容进 `docs/`；可再生或只服务当前轮次的内容进 `.tmp/`。

所有切片都有切片文件，包括单会话的小改动；Design Map 只在任务跨会话或包含两个及以上切片时创建。

### 4.2 baseline.yaml

```yaml
id: person-verification-records
version: 2
status: active            # active | superseded | expired
scope:
  routes: ["/person-verification/*"]
  maps: []                # 地图内切片默认继承地图 Notes 中登记的基线
  expires_when: ["Human 指定新的来源页面"]
source:
  kind: existing-page     # sketch | prototype-html | screenshot | existing-page | human-description
  refs: []
  fidelity: visual        # pixel | visual | layout
  fidelity_confirmed_by: human
  confirmed_at: <ISO>
source_page:
  route: /person-verification/records
  files: [src/views/PersonVerificationRecordsPage.vue]
  commit: <sha>           # 源页面快照对应的提交
relation: inherit         # inherit | independent；unknown 不进基线
delta:
  - id: columns
    kind: replace         # replace | add | remove
    regions: [table-body, table-header]
    files: ["src/views/<new-page>/columns.ts"]
regions:
  - id: filter-panel      # = data-region 值
    role: preserve        # preserve | delta
    content: graphic      # graphic | text，FREEZE 后不可改
    oracle: source-snapshot
    threshold_ref: regression.default
    mask: []
approvals:
  - action: create        # create | bump | expire | relax
    by: human
    at: <ISO>
    note: ""
```

区域改名或增删视为基线升版。

### 4.3 assertions.yaml

由 skill 内的生成器从 `baseline.yaml` 与 `source_page.commit` 生成，不手写。

```yaml
baseline: person-verification-records@2
generated_from:
  baseline_hash: <hash>
  rules_hash: <hash>
  source_commit: <sha>
structural:
  diff_scope:
    allow: []             # = 所有 delta.files
  must_import: []         # 源页面中被 preserve 区域使用的组件
  forbid: []              # rules.yaml（缺失时用内置默认）+ 基线内 Human 批准的补充
  regions_present: []     # 所有 data-region
geometry:
  - region: filter-panel
    oracle: source-snapshot
    tolerance_ref: geometry.regression
pixel:
  - region: filter-panel
    oracle: source-snapshot
    threshold_ref: regression.default
```

`baseline_hash` 与当前基线不一致时，断言视为过期，VERIFY 返回 BLOCKED。仅 `rules_hash` 变化时重新生成即可，无需 Human。

### 4.4 切片文件

```markdown
---
id: S2
title: 列表页 default
map: <effort>            # 独立切片为 null
kind: page               # page | prefactor | integration
status: ready-to-build
blocked_by: [S1]
claimed_by: null
claimed_at: null
baseline_ref: person-verification-records@2
round: 0
updated_at: <ISO>
---

## Goal
## Relation        relation + 证据
## Scan            查了哪里、候选、排除项与理由（原始日志在 .tmp）
## Structure Decisions
| region | means | target | reason | flag | approved_by |
## Deviations
## Approvals       每次 Human 决定一行：动作、时间、结论
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

Design Reading 可再生，存于 `.tmp/`；其中需 Human 确认的结论（`fidelity`、`relation`）写入基线或切片。

## 5. ENTRY 与 bootstrap

### 5.1 ENTRY 路由

ENTRY 只读，按顺序判断，命中即停：

| # | 条件 | 路由 |
|---|---|---|
| 1 | 项目无 `docs/island/designer/` | bootstrap，完成后重新 ENTRY |
| 2 | Human 指出某个 `settled` 切片有问题 | reopen 该切片 + retro |
| 3 | 存在本任务相关、未结束的切片 | Resume |
| 4 | 输入命中某个 active 地图的 Frontier 切片 | work |
| 5 | 输入命中某个基线 `scope`，且单切片可完成 | quick：新建独立切片 |
| 6 | 输入跨会话或需要两个及以上切片 | chart：提议地图 |
| 7 | 无输入 | 报告状态：Frontier、`needs-decision` 列表、过期 claim |

ENTRY 输出不超过 10 行的状态报告和建议路由，由 Human 确认后进入。

### 5.2 bootstrap

只写设计工件，不改产品代码：

1. 创建 `docs/island/designer/` 骨架和带预设值的 `thresholds.yaml`；
2. 用 `git check-ignore` 确认 `.tmp/` 被忽略；否则提议写入 `.git/info/exclude`；
3. 提议在项目 `AGENTS.md` 加入一行 ENTRY 规则（L2），Human 批准后写入；
4. 提议一个 `prefactor` 切片用于组件目录初始盘点，不在 bootstrap 内执行；
5. 项目根目录没有 `DESIGN.md` 时，从 skill 内置模板 `assets/DESIGN.template.md` 复制最简基础版本，见配套草案 §5。

bootstrap 只在 `docs/island/designer/` 缺失时运行；`DESIGN.md` 的缺失在每次 ENTRY 中独立检查，缺失即创建，不推迟、不访谈。

## 6. 两层循环

### 6.1 Map Loop

```text
CHART → FRONTIER → WORK（一个切片走一遍 Slice Loop）→ ADVANCE
```

- CHART：确定 Destination（Human 确认），生成切片文件（初始 `needs-triage`）和阻塞关系；不实现任何切片。
- FRONTIER：由 frontmatter 推算可推进切片。
- WORK：一个会话认领并推进一个切片。
- ADVANCE：在 Decisions so far 记一行；Not yet specified 中已能精确定义的问题升级为新切片；全部完成时归档地图。

### 6.2 Slice Loop

| 步骤 | 产出 | 完成条件 |
|---|---|---|
| ENTRY | 状态报告与路由 | Human 确认路由 |
| READ | Design Reading（`.tmp/`） | 来源全部适配；`fidelity` 已由 Human 确认 |
| RELATE | 切片 Relation | 每个判断有证据；`independent` 已获 Human 批准 |
| SCAN | 切片 Scan | 列出查过的范围、候选、排除理由 |
| DECIDE | 切片 Structure Decisions | 所有区域有 `means`；需 Human 的决策已批准 |
| FREEZE | `baseline.yaml`、`assertions.yaml`、oracle | 见 §6.3 机械检查 |
| BUILD | 代码改动 | 改动范围不超出 `delta.files` |
| VERIFY | `rounds/rNN/report.yaml` | 见 §7 |
| REVIEW | 审批记录 | Human 结论 |
| SETTLE | golden、基线版本、地图记录 | 见 §6.5 |

SCAN 可交给 Researcher，但其产出只能是候选、排除项和证据，写入 `.tmp/island/designer/proposals/`，由 lead 合并进切片。

### 6.3 FREEZE 机械检查

全部满足才能进入 `ready-to-build`：

- `baseline.yaml` 存在、符合 schema、最新 approvals 为 Human；
- 每个 region 有 `role`、`content`、`oracle`、`threshold_ref`；
- `assertions.yaml` 的 `baseline_hash` 与当前基线一致；
- oracle 可用：`source-snapshot` 已从 `source_page.commit` 截取；`design-export` 已导出；`golden` 存在于当前版本目录；`human-first-review` 无需前置图像；
- 切片 Structure Decisions 中需 Human 的条目已有审批记录。

### 6.4 BUILD

- 直接模式：lead 实现。
- 派发模式：调用 `yes-subagents` Coder / Coder Plus，映射见 §10.2。

实施者发现必须改动 `delta` 以外的内容时，停止并提出 `DEVIATION`，切片回到 `needs-decision`。

### 6.5 SETTLE

- Human 批准的区域截图写入 `golden/v<N>/`，记录 `approval.yaml`；
- 基线需要升版时，由 Human 批准后写入新版本，旧版本标记 `superseded`；
- 引用旧版本、且处于 `building` 或 `verifying` 的其它切片转为 `needs-triage`；
- 释放 claim，更新 `updated_at`；
- 地图内切片触发 Map Loop 的 ADVANCE。

## 7. 验收

### 7.1 分层

```text
1 STRUCTURAL   diff 范围、must_import、forbid、regions_present
2 GEOMETRY     各区域 bbox，取整后比较
3 PIXEL        各区域裁图对比
4 INTERPRET    agent 只解读失败区域的 expected | actual | diff 三联图
5 HUMAN        首轮无设计稿区域、golden 更新、阈值外差异、取舍
```

前一层失败即停止，状态回到 `building`，`round` 加一。

### 7.2 oracle 类型

| 类型 | 适用 | FREEZE 时 | 首轮可执行的层 |
|---|---|---|---|
| `source-snapshot` | `preserve` 区域；源页面在改动前的截图 | 截取 | 1–4 |
| `design-export` | 有设计稿或 `pixel` 原型的 `delta` 区域 | 导出 | 1–4 |
| `golden` | 已有 Human 批准快照的区域 | 引用 | 1–4 |
| `human-first-review` | 无设计稿或来源为描述的 `delta` 区域 | 无需图像 | 1、5；批准后转为 `golden` |

### 7.3 来源能力

| 来源 | delta 区域 oracle | 几何 | 像素 | 阈值组 |
|---|---|---|---|---|
| Sketch | `design-export` | 绝对值 | 是 | `fidelity.*` |
| 原型 HTML，`pixel` | `design-export`（原型区域截图） | 绝对值 | 是 | `fidelity.*` |
| 原型 HTML，`visual` | `human-first-review`；原型截图作为 Human 参考 | 否 | 否 | — |
| 原型 HTML，`layout` | `human-first-review` | 仅顺序与对齐 | 否 | — |
| 截图 | `human-first-review` | 否 | 否 | — |
| 既有页面 | `source-snapshot` | 绝对值 | 是 | `regression.*` |
| Human 描述 | `human-first-review` | 否 | 否 | — |

`preserve` 区域与来源无关，始终使用 `source-snapshot` 或 `golden`。

### 7.4 阈值预设

`thresholds.yaml` 按 ID 引用，区域在 FREEZE 时绑定 `threshold_ref`，VERIFY 期间不可改。

| ID | 指标 | 预设 |
|---|---|---|
| `geometry.regression` | bbox 四值取整到 CSS px 后之差 | 0 |
| `geometry.fidelity` | 位置与尺寸 / 文本块高度 | ±1 px / ±2 px |
| `regression.default` | pixelmatch，单像素阈值 0.1，`includeAA: false` | 差异像素 / 区域像素 ≤ 0.1% |
| `fidelity.graphic` | SSIM | ≥ 0.95 |
| `fidelity.text` | SSIM | ≥ 0.90 |

SSIM 计算参数固定：灰度；两图按 oracle 尺寸对齐，尺寸差超出几何容差时几何层已失败，不进入像素层；工具为 ImageMagick 7 `compare -metric SSIM`。色值、字号、间距优先用 computed style 断言。

校准：首个切片完成后实测回归噪声（同环境连续截图 5 次取最大值）和还原噪声（Human 判定正确区域的 SSIM 分布），阈值取 p95 加余量，写入 `thresholds.yaml` 并经 Human 批准。

### 7.5 快照环境

`rounds/rNN/meta.yaml` 记录：commit SHA、viewport、DPR、浏览器版本、字体就绪状态、数据 fixture 哈希、时间、来源引用。截图前等待 `document.fonts.ready`，关闭动画与光标，动态内容加 mask。渲染环境变化时，所有 golden 需 Human 批量重新批准。

## 8. 切片

### 8.1 原则

1. 纵向：一个切片包含结构、样式、状态与验收。
2. 一个切片只挂一份基线版本。
3. 每个切片有自己的区域与 oracle。
4. 规模预设：一个界面、不超过 3 个状态、不超过 5 个 `delta` 区域；超过则拆分。预设经 eval 调整。
5. 页内交互属于所在 `page` 切片，以状态切换断言验收。

### 8.2 切片类型

| 类型 | 用途 | 验收 |
|---|---|---|
| `page` | 一个界面的若干状态 | 完整五层 |
| `prefactor` | 被多个切片依赖的共享组件，或组件目录盘点 | 结构 + 组件自身区域；设计代际判断交给 Human |
| `integration` | 跨界面的流程连线 | 按流程逐步触发，检查到达的状态；到达后复用对应 `page` 切片的区域断言 |

### 8.3 状态机

| 从 | 到 | 条件 | 执行者 |
|---|---|---|---|
| `needs-triage` | `needs-info` | 缺来源或证据 | lead |
| `needs-triage` | `needs-decision` | 存在需 Human 的决策 | lead |
| `needs-triage` | `ready-to-build` | FREEZE 机械检查通过 | lead |
| `needs-info` | `needs-triage` | 补到信息 | lead |
| `needs-decision` | `needs-triage` | Human 已决定 | Human |
| `ready-to-build` | `building` | 认领 | lead |
| `building` | `verifying` | 实现完成 | lead |
| `building` | `needs-decision` | 提出 `DEVIATION` | 任何人 |
| `verifying` | `building` | 第 1–3 层失败 | 机械 |
| `verifying` | `needs-review` | 第 1–3 层通过（`human-first-review` 区域仅第 1 层） | 机械 |
| `needs-review` | `building` | Human 驳回视觉 | Human |
| `needs-review` | `needs-decision` | Human 驳回结构或取舍 | Human |
| `needs-review` | `settled` | Human 批准 | Human |
| `settled` | `needs-triage` | reopen：发现问题或依赖基线升版 | Human 或 SETTLE 级联 |

每次状态转移更新 frontmatter；Human 执行的转移在 Approvals 记一行。

### 8.4 认领

- 认领时写入 `claimed_by` 与 `claimed_at`；结束会话前释放或更新。
- `claimed_at` 超过 24 小时且 `updated_at` 无变化的 claim，ENTRY 报告为过期，由 Human 决定释放。
- 同一基线被多个切片引用时，基线只在 SETTLE 中升版，并按 §6.5 级联。

## 9. Retro

触发：Human 指出问题；切片被 reopen；同一切片同类失败连续两轮。

Retro 只产出环境修改提案，不改业务代码：

| 问题 | 提案 | 批准 |
|---|---|---|
| 机械性结构偏离未被拦下 | 生成器默认 `forbid` 规则 | Human |
| 几何反复偏移 | 区域拆分或几何断言 | Human |
| 设计代际误判 | 组件目录 `generation` / `language` 标记 | Human |
| 流程被绕过 | 项目 `AGENTS.md` 的 ENTRY 规则 | Human |
| 范式层面的偏差（优先级、拒绝项、检查项） | `DESIGN.md` 规范级提案；可机械检查时同步 `rules.yaml` | Human |
| 扫描遗漏 | 扫描范围规则或组件目录条目 | lead |

## 10. 与其它能力的边界

### 10.1 sketch-copilot-plus

提供 Sketch 事实与截图。已核实：当前 `dispatch-packet-template.md` 已包含 `DESIGN_EVIDENCE`（含 `design_relation`、`preserve`、`delta`）与 `REUSE_MAP`，并保留 `GOAL`、`VERIFY_TARGET`、`LEAD_HANDOFF`、`SUBAGENT_ACK` 等派发段落。

本草案的消费规则：

- `design_relation`、`preserve`、`delta` 只作为 RELATE 与 DECIDE 的证据输入，不直接成为基线；
- `design_relation: variant` 映射为 `inherit` 候选，仍需代码侧确认；
- packet 的派发段落在 `yes-designer` 存在时不作为编排依据。

packet 字段的调整推迟到 `yes-designer` 完成后，见 §12.2。

### 10.2 yes-subagents

已核实各角色前置条件，映射如下：

| 角色 | 前置要求 | yes-designer 提供 |
|---|---|---|
| Coder Plus | 实现内容、验收标准、可编辑边界、下游接口承诺、Git 策略与 Git 基线 | Structure Decisions + `delta`；`assertions.yaml`；`delta.files`；`must_import` 与 preserve 区域；项目 Git 状态 |
| Critic Gate | 唯一权威基线；验收标准须为 Human 认可，编排者自拟的标准视为缺失 | Human 批准的 `baseline.yaml@version` 及其生成断言 |
| Researcher | 明确问题与调查边界 | SCAN 的问题与范围 |

推论：派发模式要求基线已有 Human 批准记录，否则 Critic Gate 将返回 BLOCKED。直接模式同样可以调用 Critic Gate，因为审查者与实现者不同。

当前不需要修改 `yes-subagents`。

### 10.3 DESIGN.md

yes-designer 负责创建与维护项目根目录 `DESIGN.md`。框架、CREATE、GROW 与各步骤接点见配套草案 `2026-10-17-design-md-framework-draft.md`。

- 引用方向：`DESIGN.md` 定义词汇 ← 组件目录 ← 基线；不反向复制。
- 缺失时复制内置模板（中文，含 R-001 至 R-005）；基础版本下代际判为 `unknown` 的情况增多，更多决策交给 Human，流程不阻塞。

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

S2 的推进：Resume → RELATE 命中 `person-verification-records@2`（inherit）→ SCAN 核对候选 → DECIDE（骨架 copy、表格 reuse、列定义在 `delta`）→ FREEZE（截取 source-snapshot、导出 design-export、生成断言）→ BUILD → VERIFY → REVIEW → SETTLE。

## 12. 待决事项

### 12.1 讨论中

- 无。`DESIGN.md` 配套草案的待定项已全部决定。

### 12.2 推迟到下一阶段

- 触发描述与 `SKILL.md` 打包。
- `sketch-copilot-plus` 的协调调整：该 skill 已主动降级，待 `yes-designer` 完成后再调整 packet 字段与 `implement.md`、`verify.md` 的定位。

### 12.3 已决定

- 术语以本草案 §2 为准；背景笔记不再修改。
- issue #1 仅作参考，不要求逐条映射。

### 12.4 待验证（技术验证轮）

- 阈值与文字渲染噪声的实测；
- 取整后 0 px 几何断言的稳定性；
- 方式 A 运行环境：skill 目录自带 Playwright、pixelmatch，并依赖本机 ImageMagick 7；
- `must_import` 与 `diff_scope` 生成器能否从源页面机械推导；
- Coder Plus 是否实际遵守由 `delta.files` 映射的可编辑边界；
- eval fixture 的仓库与数据来源。

## 附录 A：Round 1 修复对照

| 编号 | 问题 | 修复位置 |
|---|---|---|
| F1 | 切片状态无持久载体 | §4.4 frontmatter；§4.5 Frontier 推算；§5.1 ENTRY 读取 |
| F2 | 冻结门禁不可校验 | §4.2–4.4 schema 与路径；§6.3 机械检查 |
| F3 | 降级自判、断言自证 | §3 不变量 4、5；§3.1 决策权；§4.3 生成断言 |
| F4 | 无设计稿首轮与 FREEZE 冲突 | §7.2 oracle 类型；§6.3 |
| M1 | 无回流边与签署记录 | §8.3；§4.4 Approvals |
| M2 | region 身份与 golden 键不稳定 | §2 `region`；§4.1 golden 路径；§4.2 改名即升版 |
| M3 | 基线审批不对称 | §3.1；§4.2 approvals |
| M4 | 词汇无映射 | §2 |
| M5 | 来源能力矩阵缺失 | §7.3 |
| M6 | 阈值可自利选择 | §4.2 `content` 与 `threshold_ref` 冻结；§7.4 |
| M7 | fidelity 落在 `.tmp` | §4.2 `source.fidelity_confirmed_by` |
| M8 | 切片规则与示例矛盾 | §8.2；§11 |
| M9 | 待定清单漏项 | §12 |
| M10 | ENTRY 与 bootstrap 未定义 | §5 |
| M11 | 并发写无所有权 | §3 不变量 8；§8.4 |
| MINOR | 双 SETTLE 同名、Resume、generation、阈值行歧义、切片大小、Retro、Chart | §2；§7.4；§8.1；§9；§6.1 |
| UNVERIFIED | Sketch packet 字段、yes-subagents 入口 | 已核实，见 §10；其余列入 §12.4 |
| ESCALATE | 5 项 | §12 |
