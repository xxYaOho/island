---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-18-yes-designer-design-work-loop-v6.md
---
# yes-designer 设计推进工作流 v6（收敛版）

- 日期：2026-10-18
- 版本：0.3（已批准方向，待 P1 验证）
- 状态：Human 已批准方向（2026-10-18），下一步 P1 技术验证；v1 至 v5 已标记为被本文取代
- 前一版：`2026-10-18-yes-designer-design-work-loop-v5.md`（874 行，Round 5 PASS，台账 6 项 MAJOR 未关闭）
- 配套草案：`2026-10-17-design-md-framework-draft.md`（接口不变）
- 与 v5 的差异见 §13。

## 0. 为什么收敛

v1 到 v5 的每轮审查都在追问“是否闭合、是否一致”，修复方式几乎都是增加机制：7 个输入 hash、版本目录搬运、四类 oracle、七层验收、waiver、CAS 认领。文档越来越自洽，但离原始问题越来越远：v5 仍然拦不住“从零重写但视觉等效”的事故 B，因为 `means: copy` 没有派生出任何断言。

v6 回到问题本身，只保留直接服务成功标准的机制。新增机制必须由 eval 中的真实失败证明其必要性。

## 1. 问题与成功标准

### 1.1 问题

- 事故 A：弹窗被从零重写；StatCard 的设计代际被误判。
- 事故 B：Human 明确要求“复制 PersonVerificationRecordsPage 再修改”，agent 仍从零重写，并写出 `min-width: 1420px`。

根因：

1. 复用决定只存在于对话中，不是开工前必须消费的工件；
2. 验收只检查视觉，视觉等效的重写可以通过；
3. agent 可以自行把任务改判为 `new`。

### 1.2 成功标准

1. 重放事故 B：从零重写被结构门禁拦下；按基线复制再修改则通过。
2. 冷启动的新会话仅凭工件即可判断下一步。
3. agent 无法自行批准 `new`、`independent`、修改共享组件或 golden。
4. 已批准区域在后续轮次退化时，被机械发现。

只要做到这四条，即视为成功；不追求设计稿的像素级自动判定。

## 2. 设计原则

1. **判断归 agent 与 Human，机械归脚本。** hash、裁剪、截图、DOM 骨架和差异计算全部由 skill 内的 `designer` 脚本完成，规范不要求 agent 手算或手写。
2. **只在两处设硬门禁。** 一是结构门禁（机械执行），二是 golden 回归门禁（机械执行）。与设计稿的差异只作为测量，不作为门禁；视觉首次验收由 Human 完成。
3. **只持久化 Human 决定过的内容。** 包括基线、golden、`DESIGN.md`、审批日志和切片记录。断言不落盘，每次 VERIFY 从基线即时推导：没有可以手改的对象，也就不存在断言过期。
4. **历史交给 git。** 不建版本目录；审批绑定文件的 git blob hash。
5. **差异按区域计算。** 用 `data-region` 把页面拆成区域，每个区域在每个状态下单独判定。

## 3. 术语

| 术语 | 定义 |
|---|---|
| `relation` | 目标页面与既有实现的关系：`inherit`（默认）或 `independent`（需 Human 批准）。证据不足时直接问 Human |
| `source_page` | `inherit` 时被继承的既有页面：路由、文件、commit |
| `region` | 语义区域，身份为 DOM 上的 `data-region` 值；可以嵌套 |
| `role` | 区域角色：`preserve`（沿用源页面）或 `delta`（允许改动） |
| `means` | 区域的实现手段：`copy` / `reuse <组件>` / `extend <组件>` / `new` |
| `state` | 页面状态，由 `setup` 步骤到达，由 `ready` 选择器确认 |
| `golden` | Human 批准的某个区域在某个状态下的截图，用作回归基准 |
| `copy commit` | `means: copy` 时由脚本原样复制源文件后单独做的一次提交 |
| `skeleton` | 区域 DOM 骨架：标签、排序后的 class、`data-region` 的嵌套结构，不含文本 |
| lead | 运行 `yes-designer` 的主会话 agent |

## 4. 工件

### 4.1 存储布局

```text
DESIGN.md                                项目根目录，设计范式总约束（配套草案）

docs/island/designer/                    持久，进仓库，只由 lead 写入
  config.yaml                            viewport、预览命令、阈值、fixture
  approvals.tsv                          所有 Human 审批，只追加（不用 .log 后缀，避免被常见的 *.log 忽略规则吞掉）
  rules.yaml                             DESIGN.md 的可机械检查规则
  design-md.log.md                       DESIGN.md 的来源与修订记录
  catalog.yaml                           组件目录：路径、设计代际、备注
  baselines/<id>.yaml                    页面基线
  golden/<id>/<region>@<state>.png       golden 截图
  maps/<name>.md                         地图（仅多切片时）
  slices/<YYMMDD>-<slug>.md              切片

.tmp/island/designer/                    一次性，被忽略，可再生
  readings/<slice>.md                    来源解读笔记
  source/<id>/                           源页面骨架与样式采集
  design/<id>/                           设计稿裁剪图
  rounds/<slice>/rNN/                    每轮区域截图、diff、report.yaml、meta.yaml
  dispatch/                              派发简报
```

判定依据：Human 决定过的内容，或无法从仓库再生的内容，进 `docs/`；可以从 commit 或来源重新生成的内容，进 `.tmp/`。

### 4.2 基线

一个页面对应一份基线。它是 Human 批准的唯一对象，涵盖关系、来源、区域和实现手段。

```yaml
id: enterprise-verification-records
relation: inherit                     # inherit | independent
source_page:                          # inherit 时必填
  route: /person-verification/records
  files: [src/views/PersonVerificationRecordsPage.vue]
  commit: <sha>
target:
  route: /enterprise-verification/records
  files: [src/views/EnterpriseVerificationRecordsPage.vue]
delta_files:                          # 允许改动的文件白名单，包括 target.files
  - src/views/EnterpriseVerificationRecordsPage.vue
  - src/api/enterprise-verification.ts
design:                               # 可选；没有设计稿时省略
  kind: sketch                        # sketch | prototype | screenshot
  ref: <Sketch 文档 id + 版本 | 原型文件路径 + hash | 截图 hash>
states:
  - id: default
    ready: '[data-region="table-body"] tbody tr'
  - id: filter-open
    setup: [{click: '[data-region="filter-toggle"]'}]
    ready: '[data-region="filter-fields"]'
regions:
  - id: page-header
    role: preserve
    means: copy
  - id: filter-panel
    role: preserve
    means: reuse FilterPanel
    states: [default, filter-open]    # 缺省为全部状态
  - id: filter-fields                 # 嵌套在 filter-panel 内
    role: delta
    means: copy
    change: 替换筛选项
    states: [filter-open]
  - id: table-body
    role: delta
    means: reuse RecordsTable
    change: 替换列定义与数据源
    design: {default: {layer: <sketch layer id>}}   # 可选：设计稿锚点
    mask: ['[data-col="created-at"]']
  - id: pagination
    role: preserve
    means: copy
```

约束：

- `inherit` 下，凡是不在 `delta` 区域与 `delta_files` 中的内容都视为保留；
- 嵌套区域中，`preserve` 区域的骨架比较会跳过其内部的 `delta` 子区域；
- `design` 锚点的形式：Sketch 用 layer id，原型用选择器，截图用矩形；
- 源页面缺少 `data-region` 时，在基线批准前先做一次只加属性的标注提交，`source_page.commit` 指向该提交。这样 S3/S4 才有可定位的比较对象，copy commit 也会把标注一并带过去；
- teleport 到 `body` 的内容（弹窗、下拉、popover）不在父区域的 DOM 子树内，必须在其根节点上自带 `data-region`，作为独立区域；
- 基线修改后，原审批失效。被修改区域的 golden 由脚本删除，需要 Human 重新批准。

### 4.3 切片

```markdown
---
id: 261018-enterprise-records
baseline: enterprise-verification-records
states: [default, filter-open]
status: building        # todo | blocked | building | review | done
blocked_on: null        # human | info | <slice-id>
depends_on: []
owner: null
round: 2
---

## Goal
## Scan          查过的范围、候选、排除理由
## Rounds        rNN：结构 / 回归 / 设计差异 / Human 结论，报告路径
## Notes         Human 的取舍与理由
```

切片只记录进度与过程，所有决策都在基线中。

### 4.4 审批日志

`approvals.tsv`，制表符分隔，每行一条：

```text
<ISO 时间>  baseline  enterprise-verification-records  <git blob sha>  <HEAD>  human  批准 inherit + 5 个区域
<ISO 时间>  golden    enterprise-verification-records/table-body@default  <png sha>  <HEAD>  human
<ISO 时间>  config    config.yaml  <git blob sha>  <HEAD>  human  回归阈值调整
```

`<HEAD>` 是审批时的仓库 commit，是 S1“自基线批准以来”的 diff 起点。

lead 只能在 Human 明确表态后执行 `designer approve`。脚本能保证的是：审批之后的任何改动都会被发现；它不能保证审批本身真实，这一点依赖 lead 遵守规则，并由 Human 抽查日志。

## 5. 决策权

| 决策 | 决定者 |
|---|---|
| `means: copy` / `reuse`（附 Scan 证据） | lead 提出，随基线一起由 Human 批准 |
| `means: new`、`extend` 共享组件、`relation: independent` | Human（逐项明确批准） |
| 基线的创建与修改 | Human |
| golden 的创建与更新 | Human |
| `config.yaml`、`rules.yaml` 的修改 | Human |
| 实施中需要越出基线（DEVIATION） | 任何人可以提出，Human 决定；实施者不得自批 |
| 设计代际是否一致 | Human |
| `DESIGN.md` 的指针更新、追加 Known Gaps | lead |
| `DESIGN.md` 规范内容的修正与补充 | Human（直接编辑或指示 lead） |

## 6. 流程

### 6.1 ENTRY

每轮 UI 任务先执行，只读：

1. 项目没有 `docs/island/designer/`：执行 `designer init`。根目录缺少 `DESIGN.md` 时，复制内置模板（配套草案 §5）。完成后重新执行 ENTRY。
2. 存在与本任务相关的未完成切片：恢复该切片。
3. 其它情况：新建切片；预计需要两个以上切片时，先提议地图。

无输入时，报告未完成切片、`blocked_on: human` 列表和 Frontier。

### 6.2 切片循环

```text
READ → BASELINE → BUILD → VERIFY → REVIEW → SETTLE
```

| 步骤 | 做什么 | 完成条件 |
|---|---|---|
| READ | 理解来源：区域、状态、交互、组件；写入 `.tmp/readings/` | 区域与状态清单已形成 |
| BASELINE | 判断 relation；SCAN；为每个区域定 role 与 means；写基线；交 Human 批准 | `approvals.tsv` 中有当前 blob 的批准记录 |
| BUILD | `means: copy` 时先执行 `designer copy`，生成 copy commit；再在 `delta_files` 内实现；提供 `data-region` | 实现完成 |
| VERIFY | `designer verify <slice>`，见 §7 | 结构门禁与回归门禁通过 |
| REVIEW | Human 查看区域截图与设计差异 | Human 结论 |
| SETTLE | 对 Human 批准的区域执行 `designer golden`；切片置为 `done`；更新地图 | — |

SCAN 的最小范围：组件目录、同 feature 或同路由的相邻页面、全仓组件名搜索、运行中的页面。结果写入切片的 Scan 段，作为 Human 批准基线时的依据。SCAN 可以交给 Researcher。

实施中发现必须越出基线时，停止并提出 DEVIATION，切片置为 `blocked_on: human`。

### 6.3 状态转移

| 从 | 到 | 条件 |
|---|---|---|
| `todo` | `blocked` | 缺信息、待 Human 决定，或依赖未完成 |
| `todo` / `blocked` | `building` | 基线已批准，且依赖已完成 |
| `building` | `review` | VERIFY 的门禁全部通过 |
| `building` | `blocked` | 出现 DEVIATION，或基线在审批后被改动 |
| `review` | `building` | Human 驳回 |
| `review` | `done` | Human 批准，golden 已写入 |
| `done` | `building` | Human 指出问题后重开 |

## 7. 验收

`designer verify` 从基线即时推导检查项，按以下顺序执行；结构门禁失败时，不进入视觉阶段。

### 7.1 结构门禁（硬门禁）

| 检查 | 规则 | 针对的失败 |
|---|---|---|
| S1 文件范围 | 自基线批准以来改动的文件都在 `delta_files` 内 | 越界修改 |
| S2 区域存在 | 每个状态下，基线中的区域都能通过 `data-region` 找到；`ready` 选择器可达 | 区域缺失、状态不可达 |
| S3 骨架一致 | 每个 `preserve` 区域的 skeleton 与源页面同一状态下的 skeleton 一致 | 视觉等效的重写（事故 B） |
| S4 样式探针 | 每个 `preserve` 区域根节点的固定属性与源页面一致：`display`、`position`、`padding`、`margin`、`gap`、`min-width`、`max-width`、`font-size`、`line-height`、`color`、`background-color`、`border` | `min-width: 1420px` 这类改动 |
| S5 规则 | `rules.yaml` 对 `delta_files` 的检查，如字面色值、未定义 CSS 变量 | 违反 DESIGN.md 约束 |

skeleton 的计算规则：

- 遍历区域子树，记录标签名、排序后的 class、`data-region`；
- 去掉文本节点、`data-v-*` 等作用域属性和其它属性；
- 连续出现的相同兄弟节点折叠为一个，因此行数或数据不同不影响结果。

源页面的骨架与样式由脚本在 `source_page.commit` 的临时 worktree 中采集，存入 `.tmp/source/`，随时可以从 commit 再生。

`relation: independent` 或源页面中不存在的状态没有比较对象，S3 和 S4 不适用，由 Human 验收。

### 7.2 视觉

| 检查 | 性质 | 规则 |
|---|---|---|
| V1 回归 | 硬门禁 | 已有 golden 的区域在对应状态下，与 golden 做像素对比：pixelmatch 单像素阈值 0.1；差异像素数 ≤ `min(max(5, 0.1% × 区域像素数), 500)` |
| V2 设计差异 | 测量 | 带 `design` 锚点的区域，与设计稿裁剪图对齐比例后计算差异，输出差异值和三联图（期望、实际、差异） |

- V2 不设门禁，只设建议停止线（`config.yaml`，默认差异 ≤ 2%）。连续 3 轮没有改善时，交给 Human。
- agent 只解读 V1 失败或 V2 未达停止线的区域的三联图，不做整页读图。
- 环境（浏览器版本、DPR、viewport、字体）与 golden 记录的环境不一致时，V1 跳过并报告 `env-mismatch`，由 Human 决定是否重新采集 golden。
- 页面必须以固定数据渲染（`config.yaml` 中的 fixture 或 `mask`），否则 V1 不可用。

### 7.3 Human

Human 验收以下内容：首次实现的 `delta` 区域、V2 未达停止线的区域、没有比较对象的区域，以及所有取舍。批准后写入 golden，之后由 V1 守护。

### 7.4 每轮快照

每轮把区域截图、diff、`report.yaml` 和 `meta.yaml`（commit、环境、时间）写入 `.tmp/rounds/<slice>/rNN/`，用于前后轮对比。golden 是唯一需要持久化的视觉记录。

## 8. golden

- 位置：`docs/island/designer/golden/<baseline-id>/<region>@<state>.png`，批准记录在 `approvals.tsv`；
- 只在 Human 批准后由 `designer golden` 写入，图片 hash 与环境一并记录；
- 只要页面还在，golden 就一直保留，作为回归基准；页面删除或基线废止时一并删除；
- 基线修改某个区域时，该区域的 golden 由脚本删除，需重新批准；历史版本由 git 追溯。

## 9. 切片与地图

- 一个切片对应一个页面的若干状态：最多 3 个状态、5 个 `delta` 区域，超出则拆分。上限经 eval 调整。
- 页内交互属于所在切片，通过 `states.setup` 表达。
- 共享组件的修改属于 `extend`，需 Human 批准，并在受影响页面的切片中验收。
- 跨页面流程暂不纳入机械验收，由 Human 验收。
- 只有任务包含两个及以上切片时才建地图。地图包含：Destination（Human 确认）、切片清单、Not yet specified、Out of scope。Frontier 是 `depends_on` 全部 `done` 的 `todo` 切片。
- 一个地图同一时刻只有一个 lead（`owner`）。

### 9.1 Retro

Human 指出有问题漏过时，lead 提出改进提案，例如新增 `rules.yaml` 规则、组件目录条目、项目 `AGENTS.md` 的 ENTRY 规则或区域拆分。由 Human 批准；Retro 不改业务代码。

## 10. 与其它能力的边界

- **sketch-copilot-pro**：提供 Sketch 的事实、图层结构和导出图。其 `design_relation`、`preserve`、`delta` 和 `REUSE_MAP` 只作为 BASELINE 的证据输入，不直接成为基线。packet 中的派发段落在 yes-designer 存在时不作为编排依据。
- **原型 HTML**：运行原型来理解界面，并裁剪设计图（锚点是原型中的选择器）。原型的 DOM 不作为项目结构的来源。
- **yes-subagents**：可选执行层，不需要修改。派发 Coder Plus 时，lead 在 `.tmp/dispatch/` 生成简报，包括：已批准的基线与 blob hash（实现内容与验收标准）、`delta_files`（可编辑边界）、`data-region` 与 `reuse` 组件（下游接口承诺）、起始 HEAD 与工作区快照（Git 基线）、只在当前分支追加本地提交（Git 策略）。Critic Gate 以已批准的基线为唯一权威。
- **DESIGN.md**：缺失时复制内置模板；之后的规范内容由 Human 主导生长；可机械检查的部分进入 `rules.yaml`，由 S5 执行。详见配套草案。

## 11. 示例：重放事故 B

```text
输入     复制 PersonVerificationRecordsPage，改成企业认证记录
READ     区域：page-header / filter-panel / filter-fields / table-body / pagination
BASELINE relation=inherit；filter-fields、table-body 为 delta，其余为 preserve
         Human 批准 → approvals.tsv 写入 blob hash
BUILD    designer copy → copy commit；再在 delta_files 内修改

错误路径 agent 自写栅格布局并加了 min-width: 1420px
         S3：page-header、pagination 骨架不一致 → 失败
         S4：filter-panel 的 min-width 不一致 → 失败
         报告指出具体区域；切片停在 building

正确路径 S1–S5 通过 → V2 显示 table-body 差异 1.4% → review
         Human 批准 → table-body@default、filter-fields@filter-open 写入 golden
```

## 12. 分期

| 阶段 | 内容 | 验证 |
|---|---|---|
| P1 | init、ENTRY、基线、审批日志、`designer copy`、S1–S5、每轮快照、Human 验收 | 重放事故 A、B；满足成功标准 1、2、3 |
| P2 | golden、V1 回归、环境记录、fixture 与 mask | 人为制造一次退化，验证能被发现（成功标准 4） |
| P3 | V2 设计差异：Sketch 导出、原型截图、截图裁剪 | 统计停止线与真实差异的关系，校准默认值 |

每个阶段由 eval 验收后再进入下一阶段。P1 不需要像素工具链。

## 13. 相对 v5 的删减

| v5 机制 | v6 处理 | 理由 |
|---|---|---|
| `assertions.yaml`、`output_hash`、7 个输入 hash | 不落盘，VERIFY 即时推导 | 没有可以手改的对象，也不存在过期 |
| `content_hash` 规范化算法 | git blob hash | 由 git 提供确定性 |
| 版本目录 `v<N>`、`current.yaml`、superseded、`copied_from`、级联 | 单文件加 git 历史；修改后审批失效，受影响的 golden 删除 | 版本搬运是 v5 MAJOR 的主要来源 |
| 四类 oracle × 三档 fidelity × 八行来源矩阵 | golden（门禁）、design（测量）、无（Human 首审） | 设计稿与浏览器渲染无法稳定判定，强行设门禁只会导致阈值博弈 |
| 七层验收 | 结构、视觉、Human 三段 | — |
| computed / layout 层、`computed_expectations` | 合并为 preserve 区域的 S4 样式探针；delta 区域交给 S5 和 Human | — |
| geometry 0px、`source_anchors`、`export {scale, origin}` | 归入 V2 测量，属于脚本实现细节 | — |
| SSIM 阈值、`fidelity.*` | 只设建议停止线 | — |
| `waivers.yaml` | Human 接受差异即更新 golden | 豁免与更新基准是同一件事 |
| `thresholds.yaml`、`viewports.yaml` 及其审批 schema | `config.yaml` 一个文件，修改记入审批日志 | — |
| `data-screen`、`data-state`、marker、origin、hooks | `setup` 加 `ready` 选择器；只强制 `data-region` | 减少对产品代码的侵入 |
| 9 个状态、20 条转移 | 5 个状态 | — |
| CAS 认领、24 小时过期 | `owner` 字段，一个地图一个 lead | 实际使用场景是单 Human |
| ENTRY 9 条路由 | 3 条 | — |
| prefactor / integration 切片类型 | 共享组件归入 `extend`；跨页流程由 Human 验收 | 等 eval 证明有需要时再引入 |
| 每份证据的 `capture_env` | 快照 meta 和 golden 各记录一次 | — |
| 跨路由复制时 preserve 区域与源页面做像素对比 | 改为 S3 骨架加 S4 样式探针 | 两个页面的数据不同，像素对比必然误报；preserve 的本义是结构保留 |
| （无） | 新增 copy commit 与 S3 骨架门禁 | v5 未覆盖事故 B |

v5 台账中的 M1 至 M6 都依附于已删除的机制（版本搬运、截图 pixel 模式、env 重批、期望值契约、附录、layout 层），在 v6 中不再适用。

## 14. 待定与待验证

已决（Human，2026-10-18）：批准 v6 方向；不再进行 critic-strict 审查；v1 至 v5 加被取代指针；删除空文件 `docs/DESIGN.md`。

待验证（P1 技术验证，计划见 `2026-10-18-yes-designer-p1-validation-plan.md`）：

- skeleton 折叠规则对真实页面（表格、列表、条件渲染）的误报率；
- S4 探针的属性清单是否足够，是否过严；
- 在 Vue SFC 中，`designer copy` 之后 S1 的文件级判定是否够用，还是需要更细的区域级 diff；
- 在临时 worktree 中按 `source_page.commit` 启动源页面的成本，包括依赖安装和端口；
- Coder Plus 是否接受 §10 的派发简报。

## 15. P1 补丁（2026-10-18）

本节记录 P1 首轮验证与顾问反馈后，对 v6 规则的增补与简化。**与正文冲突时以本节为准**；P1 正式关闭时再把本节合并进正文，形成 v6.1。

### 15.1 基线新增

- 新增 `prototype_diff`：原型与参考页的逐条差异，`kind` 为 `structural-add` / `structural-remove` / `contradiction` / `semantics`；原型自身矛盾（例如两个计数不一致）必须记为 `contradiction` 并提问。
- `structural-add` 必须登记 `region` 与直接子结构签名；`signature` 对嵌套区域使用 `region:<id>`。
- 存在 `status: open` 的 `prototype_diff` 时禁止 `approve`。
- `copy` 的 from/to 映射：先确认 baseline 已批准且 blob 未变，再从 `source_page.commit` 读取源文件，不读工作区。
- 每份 baseline 的 `delta_files` 只列本页面的 target 文件与明确共享文件（路由、导航、mock 等）；包含其他 baseline 页面文件的 baseline 不可批准。

### 15.2 区域与门禁

- 区域划分采用“delta 只取最小区域，局部修改用嵌套子区域”：外层框架可以 preserve，内部字段/列等作为 delta 子区域。
- S3 遍历到带 `data-region` 的子节点时只输出 `{region: id}` 占位、不展开。
- S3 遇到库组件根节点时停止递归，只比较根节点 tag/class。当前有限清单：`ant-pagination`。加入新清单项必须回写本节。
- S6 保留为“delta 区域直接子结构的声明检查”，不向更深层扩展。
- 不规定固定 preserve 列表；preserve 范围仍由 Human 在 baseline 审批时判断。

### 15.3 采集与审批

- 参考页采集继续在当前服务进行，同时检查 `source_page.files` 自 `source_page.commit` 以来是否有改动。已知盲区：`delta_files` 中的共享组件若两边一起变化，该检查无法发现。
- 审批粒度：Lead 预填建议决定；“沿用参考页”类可批量通过；只有新增结构、原型矛盾、没有交互定义的操作三类需要 Human 逐条决定。
- 切片与状态机推迟到 P2；P1 以 `designer status` 与 `approvals.tsv` 判断进度。

### 15.4 暂不做

- 不把 S6 扩展到深层结构；不做文案机械检查；不补 E1–E6，等 T1 与嵌套区域重跑的 R2 结果。
- golden 像素回归、DESIGN.md 模板、切片文件留到 P2。

### 15.5 当前验证状态

- T1 确定性矩阵 G1–G10 已通过（G2 的初始误报已用 15.2 的停止规则修正）。
- 真实 antd 环境 G2 复测：R2 产出 + mock 改为 2 页，S1–S6 连续 3 次通过；`.ant-pagination` 停止规则在真实 antd class（含 hash class）下成立。
- 同交付多 baseline 的约束：S1 自批准 HEAD 起看全量改动；一份交付含两页时，应先提交另一页再批准，或分开交付。
- G9/G10 已确认：在“外框 preserve + 嵌套 delta”的划分下，新增标题栏可由 S3 直接拦下，不依赖 S6；S6 仅对“区域整体 delta + 内部新增直接子结构”提供声明检查。S6 暂保留为过渡守卫。
- 嵌套区域 R2 只产出 baseline 草案，页面实现与 verify 未执行；用户决定视为普通验证结果，不作为 P1 关闭阻断。
