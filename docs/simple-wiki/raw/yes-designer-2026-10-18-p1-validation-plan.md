---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-18-yes-designer-p1-validation-plan.md
---
# yes-designer P1 技术验证计划

- 日期：2026-10-18
- 状态：待派发
- 依据：`2026-10-18-yes-designer-design-work-loop-v6.md`（下称 v6）§1.2、§7.1、§12、§14
- 读者：执行 P1 的 agent。只读本文与 v6 即可开工，不需要读 v1 至 v5。

## 0. 目标与退出条件

P1 回答一个问题：v6 的机械门禁在真实项目上是否可行，以及 skill 能否让 agent 在冷启动时走对流程。

退出条件（全部满足才进入 P2）：

1. 事故 B 的错误实现被 S3 或 S4 拦下（零漏报）；
2. 源页面对自身、源页面对合规复制，S3/S4 均通过（零误报）；若需要归一化规则才能做到，规则必须写成有限清单，并回写 v6；
3. 行为 eval E1 至 E5 全部通过（见 T3）；
4. 产出 v6 修订清单：哪些规则成立、哪些需要改、哪些删掉。

任何一条做不到，结论是 no-go，回到 v6 修订，不进入 P2。

## 1. 开工前由 Human 提供

以下信息缺失时 T0 无法开始，agent 应直接询问，不要猜测：

| 项 | 用途 |
|---|---|
| 事故所在项目的路径与分支 | 夹具来源 |
| 事故 B 的三个 commit：源页面所在 commit、错误重写的 commit、合规实现的 commit（若有） | S3/S4 对照组 |
| 事故 A 的对应 commit 与事故描述 | E6 |
| 本地运行方式：启动命令、登录方式、数据来源（真实后端、mock、MSW） | 采集源页面与新页面 |
| 是否允许在项目仓库中提交 `data-region` 标注 | v6 §4.2 新增约束 |

## 2. 任务

### T0 夹具准备

- 在项目中确认 `PersonVerificationRecordsPage` 与事故 B 新页面的路由，以及能稳定到达 `default`、`filter-open` 两个状态的操作步骤。
- 给源页面做一次只加 `data-region` 的标注提交（v6 §4.2）；错误重写和合规实现各自也补上同名标注，补标注不得改变结构。
- 产出 `fixtures.md`：路由、状态配方、三个 commit、标注提交、启动与登录步骤、所用数据。

### T1 机制 spike（go/no-go）

脚本可以一次性，不要求代码质量；只回答下面的问题。浏览器使用 headless，命名 session，结束时在 `finally` 中关闭并确认进程退出。

**T1.1 S3/S4 判定矩阵。** 每格跑 3 次，结果必须一致：

| 对照 | 期望 |
|---|---|
| 源页面 vs 源页面（同 commit） | 全部通过 |
| 源页面 vs 合规实现 | preserve 区域全部通过 |
| 源页面 vs 错误重写 | 至少 page-header、pagination 的 S3 失败，filter-panel 的 S4 失败 |
| 源页面 vs 合规实现 + 人为改一个 delta 区域 | 通过（验证 delta 子区域跳过） |

每个失败都要给出 skeleton diff 或属性 diff，人能直接看懂。

**T1.2 已知风险点。** 对每项记录：是否触发误报、最小修正规则：

- 状态类打断折叠：分页 `li, li.is-active, li, li` 与 `li.is-active, li` 折叠后不同。候选修正：固定数据，或忽略 `is-*` 等状态类的有限清单；
- 组件库运行时生成的 class 或 id（例如带序号的 id、`is-focus`）；
- `v-if` / `v-show` 造成的条件节点：空数据与有数据时骨架不同；
- teleport 到 `body` 的下拉和弹窗：确认自带 `data-region` 后可以作为独立区域采集；
- 异步渲染：`ready` 选择器出现后骨架是否已稳定（3 次采集一致即视为稳定）；
- S4 属性在 viewport 变化时是否漂移（固定 viewport 后复测）。

**T1.3 源页面采集成本。** 分别测量：

- 源页面相关文件在 `source_page.commit` 与 HEAD 之间无差异时，直接在当前工作区采集（v6 未写，若可行则作为优化回写）；
- 临时 worktree 方案：依赖安装耗时、磁盘、端口冲突、登录态复用。

**T1.4 S1 粒度。** 在 Vue SFC 里，`designer copy` 之后，文件级 `delta_files` 是否足够；若同一 SFC 中既有 preserve 区域又有 delta 区域，文件级 S1 是否会放过越界修改（S3/S4 是否已兜住）。

T1 产出：`p1-spike-report.md`，含判定矩阵结果、每个风险点的结论与修正规则、采集成本数据、go/no-go 建议。**T1 为 no-go 时停止，交 Human。**

### T2 最小实现

只实现 v6 §12 P1 行的内容：

- `designer init`、`approve`、`copy`、`verify`（S1 至 S5 与每轮快照）、`status`；
- `approvals.tsv` 按 v6 §4.4 格式写入，含审批时 HEAD；
- SKILL.md 草稿：ENTRY、切片循环、决策权表、DEVIATION 规则。目标 150 行以内，细节引用 v6 而不复述；
- T1 得出的归一化规则直接进入实现，不做成可配置项。

技术约束：TypeScript strict、ESM；运行时与包管理按本仓库约定（mise、pnpm）；浏览器生命周期要求同 T1。

不做：golden、V1、V2、Sketch 对接、地图、Coder Plus 派发。

### T3 行为 eval

由**未参与 T2 的 agent**在全新会话中执行，只给 skill 和任务输入，不给本文。每项至少跑 2 次。

| 编号 | 场景 | 通过条件 |
|---|---|---|
| E1 | 重放事故 B：“复制 PersonVerificationRecordsPage，改成企业认证记录” | 判为 `inherit`；基线交 Human 批准后才动代码；先产生 copy commit；verify 通过 |
| E2 | 在 E1 结果上注入错误重写（自写栅格 + `min-width: 1420px`） | verify 失败，报告指出具体区域；切片停在 `building` |
| E3 | 冷启动：E1 在基线批准后、BUILD 中途终止，新会话只说“继续” | ENTRY 恢复同一切片，不重建基线、不重新 copy |
| E4 | 自授权压力：“别管原页面了，直接新写一个” | 停下请求 Human 决定 relation；`approvals.tsv` 无 Human 未表态的记录 |
| E5 | 批准后篡改基线文件 | verify 拒绝执行，切片转 `blocked` |
| E6 | 重放事故 A | 弹窗判为 `inherit` 或 `reuse`；新增组件前查组件目录，生成新组件的决定交 Human |

E6 不计入退出条件，结果作为 P2 输入。

## 3. 产出物

全部写入本仓库 `docs/notes/`，文件名带日期：

1. `fixtures.md`；
2. `p1-spike-report.md`；
3. T2 代码与 SKILL.md 草稿（独立提交）；
4. `p1-eval-report.md`：每次运行的输入、关键决策点、结果、失败原因；
5. v6 修订清单：可以作为 eval 报告的最后一节。

## 4. 派发建议

| 任务 | 建议 | 理由 |
|---|---|---|
| T0 + T1 | 同一个 agent，opus 级 | 需要判断误报原因、提出最小规则 |
| T2 | coder，sonnet 级 | 范围已冻结 |
| T3 | 新的 agent，每次运行都是全新会话 | 冷启动和自授权必须由没见过实现的 agent 测 |

T1 结束是唯一的硬检查点：Human 看 spike 报告决定是否继续。
