---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-18-yes-designer-p1-eval-report.md
---
# yes-designer P1 验证报告（本轮：skill 门禁复跑）

- 日期：2026-10-18
- 状态：本轮验证完成，待外部顾问讨论
- 读者：未参与实施的顾问
- 关联：`docs/notes/2026-10-18-yes-designer-p1-validation-plan.md`、`docs/notes/2026-10-18-yes-designer-design-work-loop-v6.md`、`skill/SKILL.md`

## 0. 摘要

本轮验证的问题：yes-designer 能否让一个冷启动 agent 在已有代码工程里“基于已有页面实现新页面”，而不是重写；以及新增的差异清单门禁是否能拦住未声明的结构改动。

结论（有限 go）：在事故环境上，带 skill 的 fresh agent 能够走完 ENTRY → BASELINE（Human 批准）→ COPY（copy commit）→ BUILD → VERIFY（S1–S6），最终页面在页骨架、筛选卡、表格框架、分页组件上保持了参考页的实现结果；未声明的表格标题栏也被新门禁拦下并转为显式决策。

顾问反馈后的补强（2026-10-18 晚）：已修嵌套区域跳过、delta_files 归属、copy 走 source commit、分页库组件根节点停止规则；T1 确定性矩阵 G1–G10 已跑通（每组 3 次），S3/S4 的已知分页误报已复现并修正。G9/G10 证明嵌套区域下 S3 可直接拦下新增标题栏，S6 的必要性下降。嵌套区域 R2 只产出 baseline 草案，未执行页面实现与 verify；剩余主要是 E1–E6 行为矩阵与真实项目试点。

## 1. 背景与目标

yes-designer 的目标不是“先写设计文档再由 agent 实现”，而是把设计师已有的页面设计意图落回现有代码结构：优先复制、继承、复用，只有明确 delta 才修改。

本轮不是原 P1 计划的完整执行，而是按 Human 在 2026-10-18 的重新定向做的真实事故环境验证：

- 事故环境来自 `AS_山东监所` 项目的只读副本，裁剪为“数据中心 / 其它”相关路由；
- 参考页为「核销记录」（`/person-verification-records`）与「算法日志」（`/algorithm-log`）；
- 原型为「团访记录」「会见人员记录」两个页面的 3 张截图；
- 任务提示保持简单：“参考已有的算法日志和核销记录，实现新增两个页面”；不告诉 agent 预期目标。

评估时 Human 侧的预期目标（未告知 P1 agent，避免作弊）：

1. 按复制原页面实现，将数据内容调整为原型中的数据；
2. 无副标题（现有页面没有）；
3. 不需要重新实现表格；
4. 操作列占位，点击 toast「尚未实现」；没有明确交互的操作统一归入「尚未实现」；
5. 筛选项真实过滤下方表格；数据源用 mock API，允许补充数据。

## 2. 方法

### 2.1 环境与隔离

- canonical 事故环境：`fixtures/accident-env`，HEAD `eae8b65`（含参考页 `data-region` 标注、团访空白路由）。
- 每次运行使用 APFS clone 到 `fixtures/runs/<run-id>/accident-env`，agent 只在该克隆内工作。
- 预览服务与 Playwright 浏览器均由运行方管理并在结束后关闭；canonical 保持干净。

### 2.2 运行设置

| 轮次 | 运行 | agent | skill 版本状态 | 任务输入 |
|---|---|---|---|---|
| R0 | p1-baseline-01 | fresh teammate，无 skill | 无 | 同一简单提示 + 原型图 |
| R1 | p1-skill-01 | fresh teammate | MVP skill（S1–S5） | 同上 + 使用 skill |
| R2 | p1-skill-02 | fresh teammate | MVP skill + prototype_diff + S6 | 同上 + 使用 skill |

每轮均为全新上下文，不共享前一轮的实现细节。Human（Lead 代理）通过 `send_message` 回答 agent 提问，并在 baseline 上执行或确认 `designer approve`。

### 2.3 门禁

- S1 文件范围：自批准 HEAD 起的改动必须落在 `delta_files`；
- S2 区域存在：约定的 `data-region` 必须全部存在；
- S3 骨架一致：`preserve` 区域的结构骨架与参考页一致；遍历遇到带 `data-region` 的子节点时只输出 `{region}` 占位、不展开；遇到库组件根节点（当前有限清单：`ant-pagination`）只比较根节点 tag/class、不递归内部；
- S4 样式探针：`preserve` 区域的计算样式一致；
- S5 规则：`rules.yaml` 的 delta 文件检查（本轮为空）；
- S6 原型差异声明（R2 新增）：`delta` 区域新增的直接子结构必须在 baseline `prototype_diff` 中声明；
- `prototype_diff` 未决项阻断 approve（R2 新增）；
- `copy` 先检查 baseline 已批准且 blob 未变，文件内容用 `git show <source_page.commit>:<path>` 取，不读工作区；
- 每份 baseline 的 `delta_files` 只列本页面的 target 文件与明确共享文件；包含其他 baseline 的页面文件会被 validation 拒绝。

独立复核：每轮结束后由 Lead 重新运行 typecheck、build 与 `designer verify`，并查看截图。

## 3. 三轮对照结果

### 3.1 R0：无 skill

- 主动提问 3 个（路由归属、数据来源、视觉取舍），未提问副标题与操作列交互。
- 自行添加两个页面的副标题。
- 自行实现详情 Modal 与真实删除（mock DELETE），超出预期交互范围。
- 结构复用为部分：筛选卡基本复制；页面骨架沿用核销页但 class 全部重命名；表格组件实质重写。
- `diff` 与截图见 `fixtures/p1/runs/p1-baseline-01/`。

判定：**partial**。参考页零改动、页面可用，但结构复用不彻底，产品语义靠猜测。

### 3.2 R1：skill（S1–S5）

- 主动提问 6 个，包括副标题与操作列；Human 明确：无副标题、操作占位 + toast「尚未实现」。
- 通过 copy commit 复制参考页 4 个文件，然后按 delta 修改。
- S1–S5 全部通过；无副标题；操作列为占位按钮。
- 遗漏：会见页新增「会见进出记录 / 共 N 条」表格标题栏，未提问、未在 baseline 声明；因 `records-table` 被整体声明为 delta，S3/S4 不检查其内部，verify 未拦住。
- toast 文案使用了代码里的「暂未实现预览, 具体实现参考线上平台」，与要求的「尚未实现」不一致。

判定：**pass（带注意项）**。表格头问题成为后续门禁补强的直接触发点。

### 3.3 R2：skill + prototype_diff + S6

- ENTRY 阶段产出 14 条 `prototype_diff`（团访 7 + 会见 7），全部 open；approve 被正确阻断。
- Human 决策后批准，关键决定：
  - 不实现副标题；
  - 操作列占位 + 精确 toast「尚未实现」；
  - 会见表格标题栏保留，计数取查询结果总数（与分页一致，筛选后 42）；原型「共 8 条」登记为 contradiction，按示意行数处理；
  - 双卡片、actions 行、日期格式、宽表滚动、分页 preserve、空筛选默认均沿用参考页；
  - mock API 新增两个 endpoint，团访 66 条、会见 80 条，原型 9/42 条通过日期筛选复现。
- 2 个 copy commit 后 BUILD，S1–S6 全部通过；Lead 独立复跑 r3 同样全过；typecheck、build 通过。
- S6 实际命中：会见页 `records-table` 唯一新增直接子结构 `header.meeting-personnel-records__frame-header`，已声明并通过；团访页无未声明新增。
- 参考页与共享组件零改动。

判定：**pass**。

### 3.4 T1 机制验证（顾问反馈后补跑）

使用独立静态夹具（`fixtures/t1-matrix/`，AntD 风格分页 class），每组 3 次，结果如下：

| 组 | 场景 | 结果 |
|---|---|---|
| G1 | 参考页 vs 参考页 | PASS ×3 |
| G2 | 合规复制，数据页数与参考页不同 | 首轮 FAIL（S3 pagination 页码 class 误报）×3；修正停止规则后 PASS ×3 |
| G3 | preserve 外框内嵌 delta 子区域，只改子区域 | PASS ×3（依赖本次“嵌套区域占位跳过”修复） |
| G4 | 不 copy，从零写外观相近的页面（含 `min-width: 1420px`） | FAIL ×3（S3 page-header + S4 page-header/filter-panel） |
| G5 | 改 `delta_files` 之外的文件 | FAIL ×3（S1） |
| G6 | 审批后修改 baseline | FAIL ×3（blob 校验） |
| G7 | 未审批就执行 copy | 拒绝执行 |
| G8 | 工作区改动后执行 copy | copy 内容与 source commit 一致（pass） |
| G9 | 外框 `records-table` preserve + 嵌套 `table-body` delta，外框内新增标题栏 | FAIL ×3：S3 直接报 `records-table: children[0].tag: "table" !== "header"`；S6 通过 |
| G10 | 只改嵌套 delta 子区域（表体行） | PASS ×3 |
| G2-real | R2 真实 antd 环境，mock 改为 2 页（参考页 4 页） | PASS ×3（S1–S6；分页 stop rule 未误报） |

G2 的误报定位为：分页库组件的页码项 class 携带页码号，且页码数量随数据变化。已按有限清单规则修正：遇到 `.ant-pagination` 根节点时停止递归，只比较根节点 tag/class。该规则需回写 v6。

G2-real 补充：在真实 antd 环境上复测，先因同交付的会见页文件触发 S1（两份 baseline 同一 HEAD 交付时的固有约束），隔离团访交付后 S1–S6 连续 3 次通过；说明 `.ant-pagination` stop rule 在真实 antd class（含 hash class）下成立，同时说明同一交付多 baseline 时应先提交另一页或分开交付。该证据在 `fixtures/p1/real-antd-g2.json`。

G9/G10 回答了 S6 的必要性问题：在“外框 preserve + 嵌套 delta”的区域划分下，新增标题栏能被 S3 直接拦下，不需要 S6；S6 只在区域被整体划为 delta 且内部新增直接子结构时提供声明检查。是否删除 S6，取决于是否把嵌套区域作为默认划分。

## 4. 结构保持的观察

- 结构保持主要来自 **copy commit**：R1/R2 的页面骨架保留了参考页类名（`verification-page` 系列），filter-panel、records-table、pagination 的框架沿用核销记录；表格内部列与单元格按原型改写，属于已声明 delta。
- 本轮 S3/S4 实际只覆盖 `page-header` 与 `pagination` 两个 preserve 区域；`filter-panel`、`records-table` 在 R1/R2 中被声明为 delta，未被结构门禁检查。R2 的通过不能解释为“整页结构都被验证”。
- R1 agent 自报的相似度（可供参考）：Page.vue 团访 0.96 / class 交集 4-4，会见 0.88 / 4-5；FilterPanel 0.60 / 10-10；RecordsTable 0.46 / 4-15（团访）、0.59 / 4-8（会见）；api.ts 0.76。
- Human 实际查看页面后的判断：新页面在外观样式上比较靠近原页面代码的实现结果；即使存在额外标题栏，也基本保持住；一些小瑕疵可以快速修复。
- 与 R0 的差异：R0 通过重命名页面 class、重写表格组件来“实现新页面”；R1/R2 先 copy 再改 delta，S3/S4 能在 preserve 区域上直接约束。

## 5. 关键发现

1. **“参考已有页面”不足以约束结构**：R0 已经把“参考”理解为“参考布局后自己写”，R1 的 copy commit 才真正把复用变成机械事实。
2. **提问覆盖率是主要指标**：R0 只问了 3 个偏工程的问题，未问副标题与操作交互；R1 问了 6 个，但漏掉表格标题栏与原型内部计数矛盾；R2 列出 14 条 prototype_diff，全部决策点被摆到 Human 面前。答案质量来自 Human，skill 的作用首先是“把该问的问出来”。
3. **原型与参考页的差异必须显式化**：表格标题栏是原型有、参考页没有的结构；R1 静默新增，R2 被 `prototype_diff` 与 S6 拦下。
4. **原型自身可能矛盾**：会见截图标题栏「共 8 条」与分页「共 42 条」不一致；应作为必须提问项，不允许实现时自行取值。
5. **delta 区域的 S3/S4 是空档**：若 baseline 把某区域整体声明为 delta，该区域内部结构不受 S3/S4 约束；S6 只补了直接子结构这一层。
6. **文案型决策也需要门禁**：R1 中 Human 明确回答 toast 文案「尚未实现」，实现时漂移为「暂未实现预览…」；R2 把回答写进 `prototype_diff.decision` 后未再漂移。说明“记录决策”比“对话里说过”更可靠，但尚未做机械校验。
7. **分页通过带巧合**：R2 让两份数据都保持 4 页，S3 才通过；数据页数变化会在旧实现下触发页码 class 误报。T1 G2 已复现并修正。
7. **Human 审批粒度**：R2 有 14 条差异，逐条决策更可靠，但交互成本高于 R1 的 6 个问题；需要讨论批量化方式。

## 6. 限制与未覆盖项

1. 未执行原 P1 计划的完整 E1–E6 行为矩阵；本轮是真实事故环境下的三轮对照 + T1 确定性矩阵，不能直接替代原计划的退出条件。
2. R2 未再跑无 skill 对照（按 Human 决定省略）；R0 的对照条件与 R2 不完全同构。
3. 每个配置只跑一次 fresh agent；模型与采样噪声未评估。
4. S3/S4 的零误报/零漏报矩阵未在每轮重跑；R2 依赖 S1–S6 的当前实现与两份 baseline。
5. S1 仍是文件级；同一 SFC 内既有 preserve 又有 delta 时，S1 可能放过文件内越界修改，依赖 S3/S4/S6 兜底。
6. 页面视觉保真度是人工判断，未做像素比对；本轮结论“外观样式比较靠近原页面”基于人工查看截图。
7. 数据、鉴权、真实后端行为不在本轮范围；mock API 只验证列表页交互；真实项目预览能否带数据渲染仍未验证。
8. C-lite（G9/G10）已执行，确认嵌套区域下 S3 可以直接拦下新增标题栏；嵌套区域 R2 只产出 baseline 草案（团访使用嵌套划分；会见因标题栏把 records-table 标为 delta，并留有一个计数矛盾 open 项），页面实现与 verify 未执行，用户决定不再补做。

## 7. 给顾问的讨论问题

1. `prototype_diff` + S6 的组合是否足以覆盖“原型有、参考页没有”的结构差异？是否需要把 S6 从直接子结构下沉到指定层级，或引入“允许新增区域”的白名单？
2. preserve 区域的最小集合是否应由 skill 强制（例如 page-header / filter-panel / records-table / pagination 默认不得降级为 delta），还是继续由 Human 在 baseline 审批时决定？
3. 原型自身矛盾（计数、文案、状态）是否应统一要求“必须提问”，并在 skill 中写成强制清单？当前只写入了原则，尚未机械校验。
4. 14 条差异逐条 Human 决策是否过重？是否适合按“结构性 / 语义 / 文案”批量批准，或提供默认决策模板？
5. P1 下一步应优先补 E1–E6 行为矩阵，还是先固化本轮的门禁与报告、回写 v6 修订清单？
6. 视觉保真度是否需要一个独立的判定面（截图 diff / 设计 token 校验），还是继续由 Human 目视确认？

## 8. 证据与产出物

### 8.1 本轮代码与 skill

- `skill/SKILL.md`：ENTRY/BASELINE/BUILD/VERIFY 流程；`prototype_diff` 字段说明；S6。
- `docs/notes/2026-10-18-yes-designer-design-work-loop-v6.md` 第 15 节：本轮规则的 v6 补丁。
- `skill/scripts/designer.mjs`：init / approve / copy / verify / status；prototype_diff 校验、未决阻断、S6 实现。
- `skill/package.json`、`skill/package-lock.json`：npm 自包含依赖（playwright 1.64.1、yaml 2.9.1）。

### 8.2 运行证据（gitignored，本机可查）

- `fixtures/p1/runs/p1-skill-02/`
  - `report.md`：R2 运行报告
  - `diff.patch`：从 `eae8b65` 起的完整改动
  - `screenshots/`：团访 / 会见 / toast / 深色主题
  - `rounds/`：两份 baseline 的 S1–S6 报告
- `fixtures/p1/runs/p1-skill-01/`：R1 证据
- `fixtures/p1/runs/p1-baseline-01/`：R0 证据
- 实时看板：`http://127.0.0.1:8787`（运行记录、问答、参考页、运行证据）

### 8.3 环境

- canonical 事故环境：`fixtures/accident-env`，HEAD `eae8b65`，工作树干净。
- 本轮的克隆与预览服务已清理。

## 9. 建议

1. 先由顾问针对第 7 节问题给出判断，再决定是否补 E1–E6；
2. 若结论继续 go：把本轮新增的 `prototype_diff` / open 阻断 / S6 写回 v6 修订清单，并评估是否加入 preserve 最小集合与矛盾强制提问；
3. 若结论需要更严格的视觉保真判定，再单独设计截图/token 对比，不混入本轮结论。
