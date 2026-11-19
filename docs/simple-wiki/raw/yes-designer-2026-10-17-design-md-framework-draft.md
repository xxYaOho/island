---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-17-design-md-framework-draft.md
---
# DESIGN.md 通用框架与维护机制草案

- 日期：2026-10-17
- 版本：0.1（草案）
- 状态：草案，未批准；与 `2026-10-18-yes-designer-design-work-loop-v6.md` 配套（联合批准）
- 参考：`~/Projects/space_design-md/vercel/DESIGN.md`；`~/Projects/space_design-md/design-md/` 下 74 份 Stitch 格式样本

## 1. 定位

项目根目录 `DESIGN.md` 是项目的设计范式总约束：回答"什么是对的、冲突时先保什么"。它对所有 agent 和协作者生效，不依赖 yes-designer 是否加载。

yes-designer 负责它的创建与维护：缺失时从内置模板复制一份最简基础版本；之后在持续推进中，由 Human 按 repo 特性与需求主动修正或补充，或与 agent 沟通后由 agent 补充，见 §6。

三层分工与引用方向：

```text
DESIGN.md（范式，定义词汇）
  ← catalog/（组件事实，引用代际与语言特征）
    ← baselines/（页面实例，引用组件与区域）
```

只允许单向引用：`DESIGN.md` 不写组件路径与 token 数值；组件目录不重新定义代际或 token。

## 2. 两类样本的提炼

| 类型 | 代表 | 回答的问题 | 结构特征 | 可取之处 | 不适用之处 |
|---|---|---|---|---|---|
| 判断手册 | Vercel | 怎么判断、冲突时先保什么 | 语境、优先级、项目接入、工作步骤、视觉体系、拒绝清单、检查顺序 | 优先级排序；"保留调用方既有结构"；要求带理由；有序检查清单；拒绝生成式惯性；未知如实标注后继续 | 品牌报告页专属；369 行偏长 |
| 描述规格 | Stitch 样本（如 ClickHouse） | 长什么样 | YAML token + Overview / Colors / Typography / Layout / Elevation / Shapes / Components / Do's and Don'ts / Responsive / Iteration Guide / Known Gaps | 区块齐全；Known Gaps 诚实记录未知 | frontmatter 内联 token 适合一次性分享；仓库已维护 token 源时会造成双真源 |

通用框架取两者之长：判断部分在前且精简，系统部分只引用仓库真源，保留 Known Gaps 记录未知。

### 2.1 Vercel 优先级的提炼

Vercel 的 6 条优先级去掉品牌报告专属内容后，剩下 5 个通用价值，对应内置默认规则：

| Vercel 原条目 | 通用价值 | 默认规则 |
|---|---|---|
| 1. 保留给定事实、公式、单位、隐私与任务约束 | 事实与约束不可让步 | R-001 |
| 2. 保留调用方框架、路由与既有基础 | 沿用宿主结构 | R-002 |
| 3. 让读者的问题与答案一眼可见 | 任务与层级清晰 | R-003 |
| 4. 通过外壳、字体、网格与克制建立品牌归属 | 在系统内一致地实现 | R-004 |
| 5–6. 拒绝通用默认构图；不削弱层级地打磨细节 | 克制，拒绝生成式惯性 | R-005 |

另取一条工作原则写入模板导语：未知会改变语义时才提问，否则如实标注、写入 Known Gaps 并继续。

### 2.2 Token 引用

- 不在 frontmatter 或正文内联 token 数值；
- 默认引用 Human 提供的一份 `.css` 样式表作为 `token_source`，`DESIGN.md` 中只写 CSS 变量名；
- token 源与其它解析版本（`.json` 等）并存时，具体情况具体处理：由 Human 指定哪一份是 agent 的消费入口，其余不在 `DESIGN.md` 中出现。

## 3. 框架

### 3.1 区块

规范内容的修改权都归 Human：Human 直接编辑，或指示 lead 写入。下表"lead 可直接写"一列是例外。

| # | 区块 | 内容 | 内置模板 | lead 可直接写 |
|---|---|---|---|---|
| 1 | 产品语境 | 用户、使用场景、语气关键词 | 空 | — |
| 2 | 优先级 | 冲突时的保护顺序 | R-001 至 R-005 | — |
| 3 | 设计语言 | 代际定义、标志性特征、当前代际 | 空 | — |
| 4 | 系统基础 | token 源、字体角色、间距、颜色语义、层级、形状 | 只有 token 引用规则 | `token_source` 路径变化后的引用更新 |
| 5 | 组件约定 | 组件目录位置、消费规则（用 X 实现 Y）、状态语义 | 只有目录指针 | 组件目录指针 |
| 6 | 页面范式 | 列表、详情、表单、弹窗等骨架 → 参考基线 | 空表 | 指向新建或升版基线的指针 |
| 7 | 内容与数据 | 密度、表格、数字、空/加载/错误态 | 空 | — |
| 8 | 交互与动效 | 反馈、过渡、焦点、危险操作 | 空 | — |
| 9 | 可访问性与响应式 | 对比度、键盘、断点、主题 | 空 | — |
| 10 | 拒绝清单 | 不允许出现的做法 | 空 | — |
| 11 | 检查顺序 | REVIEW 的有序检查项 | 空（为空时使用 skill 内置顺序） | — |
| 12 | Known Gaps | 尚未确定的问题 | 默认 3 条 | 追加；关闭归 Human |

区块标题在模板中全部保留，即使内容为空：固定的结构让后续补充有确定的落点。

### 3.2 规则编号

每条规则带稳定编号，如 `R-012`，删除后不复用。编号用于：

- `rules.yaml` 中可机械检查的规则通过 `ref` 指回规则编号；
- 切片 Structure Decisions、REVIEW 结论与 Retro 提案引用规则编号；
- `design-md.log.md` 按编号记录来源、证据与审批。

### 3.3 篇幅

- 主文件不超过 200 行，单条规则不超过 2 行；
- 超出预算时，ADVANCE 阶段提出合并、删减或拆分提案；
- 拆分只允许拆到 `docs/design/<topic>.md`，主文件保留一行指针。

### 3.4 内置模板

模板随 skill 分发，位于 `assets/DESIGN.template.md`，语言为中文。内容如下：

```markdown
---
name: <产品名> Design
version: 1
updated: <ISO 日期>
token_source: <待指定：Human 提供的 .css 路径>
catalog: docs/island/designer/catalog/
log: docs/island/designer/design-md.log.md
---

# <产品名> Design

本文件是本项目的设计范式约束。实现任何 UI 前先阅读；冲突时按 §2 处理。
不确定的事项会改变语义时先提问；否则如实标注、写入 §12，并继续。

## 1. 产品语境

## 2. 优先级
冲突时按以下顺序保护：
1. **R-001 事实与约束**：保留数据、业务语义、权限与已给定的约束；不臆造内容、状态或数据。
2. **R-002 沿用宿主**：保留既有框架、页面结构、组件体系与 token；视觉差异不构成重写结构的理由。
3. **R-003 任务清晰**：每个页面与区域先让主任务和主对象一眼可见；层级服务任务，不服务装饰。
4. **R-004 系统内还原**：用 `token_source` 变量与当前代际组件还原设计或参考；与系统冲突时记录差异交 Human，不新造平行样式。
5. **R-005 克制**：在不削弱层级的前提下打磨细节；拒绝无依据的装饰、渐变、徽章、图标与卡片堆叠。

## 3. 设计语言

## 4. 系统基础
- Token：只用 `token_source` 中定义的 CSS 变量，禁止字面量（R-004）。

## 5. 组件约定
- 组件清单与代际见 `catalog/`。

## 6. 页面范式
| 范式 | 参考基线 | 要点 |
|---|---|---|

## 7. 内容与数据

## 8. 交互与动效

## 9. 可访问性与响应式

## 10. 拒绝清单

## 11. 检查顺序

## 12. Known Gaps
- 产品语境未定义（创建于 <日期>）
- 当前设计代际未定义；代际判断按 `unknown` 处理（创建于 <日期>）
- `token_source` 未指定（创建于 <日期>）
```

`token_source` 由 Human 指定后，第 3 条 Known Gap 关闭。

## 4. 机械规则：rules.yaml

`DESIGN.md` 是给人和 agent 读的散文；能机械检查的部分另存为 `docs/island/designer/rules.yaml`，供断言生成器使用。内置默认条目：

```yaml
- id: no-literal-color
  ref: R-004
  check: { kind: grep, pattern: "#[0-9a-fA-F]{3,8}\\b", in: "<delta.files>" }
- id: css-var-defined
  ref: R-004
  requires: token_source
  check: { kind: css-var-exists, source: "<token_source>", in: "<delta.files>" }
```

Human 补充规则后可能出现的条目示例：

```yaml
- id: no-custom-table-container
  ref: R-0xx
  check: { kind: forbid-element, selector: "table:not(.<project-table>)" }
```

- 生成器把 `rules.yaml` 并入 `assertions.yaml` 的 `forbid`，并在 `generated_from` 记录 `rules_hash`；
- `requires` 未满足的条目跳过并在 VERIFY 报告中列出，不视为通过；
- `rules.yaml` 变化后断言视为过期，重新生成即可，无需 Human；
- 删除或放宽规则需要 Human 批准，与 `DESIGN.md` 同步修改。

## 5. CREATE：缺失时创建

ENTRY 发现项目根目录没有 `DESIGN.md` 时：

1. 将 `assets/DESIGN.template.md` 复制到项目根目录，替换产品名（取自 `package.json` 或仓库名）与日期；
2. 写入 `rules.yaml` 默认条目，创建 `design-md.log.md`，记录 `create`（来源：内置模板）；
3. 告知 Human 已创建及 3 条 Known Gaps；
4. 提议在 `AGENTS.md` 加一行指针："实现 UI 前先读 `DESIGN.md`"（Human 批准后写入）。

创建不访谈、不扫描、不推迟、不询问：没有任何先验信息时，最简基础版本比空缺更有用；具体内容在 GROW 中由 Human 补充。

## 6. GROW：持续修正与补充

`DESIGN.md` 在持续推进中由 Human 主导修正与补充。agent 的职责是让每次修改落得准确、可追溯，并与 `rules.yaml`、组件目录、基线保持一致。

### 6.1 修改路径

| 路径 | 场景 | 执行 |
|---|---|---|
| Human 直接编辑 | Human 按 repo 特性或需求直接改文件 | lead 在下次 ENTRY 同步，见 §6.2 |
| Human 指示 agent 补充 | Human 与 agent 沟通后让 agent 补充 | Human 给意图；lead 起草措辞、分配编号、定位区块，展示改动后写入；意图不清时先问 |
| agent 提议 | Retro 或 REVIEW 中发现范式层面的偏差 | 记入 pending，在 Retro 或 ADVANCE 时呈现；Human 采纳后按上一条执行 |
| 自动维护 | §3.1 "lead 可直接写"列 | lead 直接写入，记日志 |

前两条是主路径。agent 提议是补充，不在切片中途打断 Human。

### 6.2 Human 直接编辑后的同步

`design-md.log.md` 记录上次同步时的文件 hash。ENTRY 发现不一致时：

1. 读取 diff，在日志中记为 `human-edit`；
2. 新增规则缺编号时分配编号，并告知 Human；
3. 删除的规则：同步删除 `rules.yaml` 中对应条目，无需再确认；
4. 新增或修改的规则可机械检查时，起草 `rules.yaml` 条目，Human 确认后写入；
5. 新内容与组件目录、基线或其它规则冲突时，列出冲突交 Human；
6. 更新同步 hash。

### 6.3 补充时的仓库线索

Human 指示 agent 补充某个区块时，lead 或 Researcher 可只读扫描仓库，为起草提供带证据的候选：

| 线索 | 对应区块 |
|---|---|
| 框架、UI 库、`package.json` 依赖 | §4、§5 |
| token 样式表候选：Style Dictionary 输出的 `.css`、全局 CSS 变量文件 | §4（`token_source` 候选，不自行认定） |
| 字体、图标库、主题模式 | §4、§9 |
| 现有文档：`AGENTS.md`、README、Storybook、设计相关注释 | 全部 |
| 路由与页面类型 | §6 |
| 组件 import 频次 | §5 与组件目录 |
| 同类组件并存（疑似多代际） | §3 |
| 硬编码色值、自写容器等 | §10 |

扫描结果只是观察：出现频率高不等于规范，可能正是历史偶然或重复实现。候选必须经 Human 确认才进入 `DESIGN.md`。

### 6.4 维护

在 ADVANCE 或地图归档时检查：

- 篇幅是否超出预算；
- 规则间是否冲突：冲突交 Human；
- 规则是否失效（引用的组件、token、基线已不存在）：提出删除提案；
- `rules.yaml` 与 `DESIGN.md` 的编号是否一一对应。

## 7. design-md.log.md

```markdown
## Status
synced_hash: <hash>

## Pending
- [P-007] 新增 R-031：<规则>。来源：S4-r2 Retro。证据：<路径>。

## Log
| 时间 | 编号 | 动作 | 来源 | 批准 |
|---|---|---|---|---|
| <ISO> | R-001..R-005 | create | 内置模板 | — |
| <ISO> | R-018 | human-edit | Human 直接编辑 | human |
| <ISO> | R-019 | add | Human 指示：<意图摘要> | human |
| <ISO> | §6 | pointer | SETTLE S2 → person-verification-records@2 | lead |
```

## 8. 与 Slice Loop 的接点

| 步骤 | 对 DESIGN.md 的使用 |
|---|---|
| ENTRY | 读取；缺失时按 §5 创建；hash 变化时按 §6.2 同步 |
| READ | Design Reading 的 `language` 与 §3、§4 对照；`generation` 取自 §3，§3 为空时为 `unknown` |
| DECIDE | 冲突按 §2 处理；决策引用规则编号 |
| FREEZE | `rules.yaml` 并入断言 |
| VERIFY 第 4 层 / REVIEW | 按 §11 顺序检查，§11 为空时用 skill 内置顺序；结论引用规则编号 |
| SETTLE | 指针级更新 §6 |
| Retro / ADVANCE | 规范级提案与维护检查 |

基础版本下（§3 为空、`token_source` 未指定）：代际判为 `unknown` 的情况增多，更多决策交给 Human；`css-var-defined` 跳过；流程不阻塞。

## 9. 待定

无。

## 10. 已决定

- 不使用 frontmatter 内联 token；默认引用 Human 提供的一份 `.css`，多版本并存时具体处理（§2.2）。
- 生长以 Human 主动修正或指示 agent 补充为主路径，agent 提议为补充（§6.1）。
- 默认规则 R-001 至 R-005 从 Vercel 优先级提炼（§2.1）。
- 缺失时直接复制内置模板，不推迟、不访谈（§5）。
- `DESIGN.md` 默认使用中文；模板内置于 skill 的 `assets/DESIGN.template.md`（§3.4）。
