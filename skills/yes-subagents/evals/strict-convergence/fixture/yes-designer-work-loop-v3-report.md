# Round 3 审查反馈（critic-strict）

- 审查对象：`v3/yes-designer-work-loop-v3.md`（796 行，2026-10-18 10:41 版）
- 模式：FULL / intensity=high / Round 3（修正轮 2）
- 结论：`STATUS: FAIL`
- 统计：FATAL 2 / MAJOR 8 / MINOR 6 / UNVERIFIED 5 / ESCALATE 5

---

yes-designer 工作流 v3 — Round 3 / FULL / high 审查
对象：docs/notes/2026-10-18-yes-designer-design-work-loop-v3.md（796 行，2026-10-18 10:41）；行号均为 v3，外部核对另注路径。

## Round 2 台账判定

- **FATAL-1 CLOSED**：screen/state/region 进入术语（§2 45-52）、归档（§4.1 114-116 oracles/golden 含 state）、基线（§4.2 159-202，214 每 region×state 恰一条 oracle）、断言（§4.3 238-286 各层均带 screen/state）、验收迭代（§7.1 514）、示例（§11 715/721）。原失败路径可解。
- **FATAL-2 PARTIAL**：已补 geometry expected bbox/source（§4.3 256-262）、computed（263-272）、layout（273-279）、interactions（250-255）、output_hash（237、§4.10 404/407）与 FREEZE 重生成校验（§6.3 482）。未闭合项：golden 与 design-export/Sketch 的期望值出处缺失 → 见 FATAL-R。
- **M1 CLOSED**：BLOCKED→needs-triage（§8.3 613/616/618）、任何未结束状态级联（624）、§6.5 506、claim CAS 与单 claim（§8.4 630-633）。
- **M2 PARTIAL**：版本目录/current.yaml（§4.1 109-117）、证据持久化（§4.9 378-399）、SETTLE 写序（§6.5 499-508）已建。未闭合：FREEZE 建版本时的指针/superseded/级联协议缺失、current.yaml 与 baseline.status 一致性未校验、§11 726 与 §6.5 500-502 矛盾、跨地图共享基线的反复级联 → MAJOR-1。
- **M3 PARTIAL**：content_hash 绑定（§4.2 203-209、§4.10 403）、golden approval（§4.9 384-397）、thresholds approvals（§7.4 572）已建。未闭合：证据文件/waivers/viewports/thresholds 的哈希未被校验 → MAJOR-2。
- **M4 CLOSED**：面积归一+绝对上下限（§7.4 561/565）、20 次采样与 env-unstable 阻断（569-572）、waiver（574）、一基线一断点（§2 61、§4.2 146）、层内汇总（§7.1 514）、环境一致性（§7.4 576）。非 golden oracle 的 env 证据另见 MAJOR-6。
- **M5 CLOSED**：structural.interactions（§4.3 250-255）、第 1 层纳入 interactions（§7.1 517）、setup/marker 执行语义（§4.8 367-376）、基线 interactions（§4.2 171-176）。
- **M6 PARTIAL**：harness/flow 字段（§4.4 312-313）、§8.2 595-601、§6.3 486 已建。未闭合：integration `baseline_ref: null` 与 FREEZE 检查 1 冲突；prefactor harness 形态仍在 §12.1 待定 → MAJOR-4。
- **M7 CLOSED**：§5.1 新增第 7 行（423）与 DESIGN.md 检查第 2 行（418）。
- **M8 CLOSED**：最小扫描范围+completeness（§6.2.1 469-471）、`new` 一律 Human（§3.1 82）、unknowns 阻断 FREEZE（§6.3 483）。残留见 MINOR-4。
- **M9 PARTIAL**：矩阵按 fidelity 重写（§7.3 541-549）、export 坐标映射（§7.2 535）、layout/computed 阈值（§7.4 559-560）。未闭合：Sketch 首轮 computed 无来源、computed.expected_source 枚举缺 design-export、截图声明 pixel 与 §7.2 design-export 适用不一致、oracle `export` 字段不在 schema → FATAL-R。
- **M10 CLOSED**：human-first-review 的 evidence/threshold_ref 允许 null（§4.2 201/215、§6.3 480）。
- **M11 STILL OPEN**：附录 A 767-787 将各条标为"已修复"，但 FATAL-2 残留与 M2/M3/M6/M9/M11 缺口仍在；附录 A 772/774/775/778/781/783 的映射与实际文本不一致；§12.1/§12.2 与 §5.2/§10.3 相互矛盾 → MAJOR-5。
- **M12 CLOSED**：Coder Plus 五项前置+Git 策略/Git 基线/下游接口承诺/派发简报均已映射（§10.2 671-681）。
- **MINOR（6 项）PARTIAL**：preserve 措辞、L2/方式 A、Human 写入、DESIGN.md 创建路径、allow/规范化哈希已修（§2 44、§5.2 435、§8.3、§5.1 418+§5.2 439、§4.3 239-241+§4.10 403-407）；§11 示例仍与 §6.5 不一致，`baseline_hash` 与 `content_hash` 未显式等同。
- **UNVERIFIED（6 项）PARTIAL**：5 项已归入 §12.4 757-765；§10.1 verified_against 仍无 skill 版本/commit，只有路径+日期（656/663）。
- **ESCALATE（5 项）PARTIAL**：背景指针已加（两文文首，已核对）、空 DESIGN.md 已移交 Human（附录 787）；配套草案联合批准与 sketch-copilot-plus 版本固定仍开放 → ESCALATE。

## FATAL

**FATAL-R（承接 Round 2 FATAL-2：PARTIAL）期望值出处仍缺失，断言集不能完整机械执行**
- 证据：(a) golden：§7.2 535 称几何期望来自"同环境 DOM 测量或抓取记录"，但 §4.9 384-397 的 golden approval 只记录 baseline_hash、region sha256/threshold_ref、env，没有 expected bbox 或 computed props；§4.3 291 又要求 golden oracle 生成 geometry/computed/pixel，而 §4.3 294-295 要求断言可确定性重生成 → 期望值无持久输入。(b) design-export：§4.2 217 与 §4.9 381 要求 oracle 记录 `export: {scale, origin}`，但 §4.2 190-202 的 oracle schema 没有该字段，§6.3 480 也不校验；§4.2 183-189 的 region 无 source anchor/导出坐标，跨源期望 bbox 无法从持久工件推导。(c) Sketch 首轮 computed：§4.3 291 要求 design-export 生成 computed，但 computed.expected_source 仅 source-snapshot|golden|human（§4.3 267）；首轮 Sketch 页面（§11 715 S2）既无 golden 也无 source page（§4.2 153 可 null），"human" 无字段承载 Human 提供的期望属性（baseline 与 §4.4 321 Structure Decisions 表均无 props 列），§7.3 543 写的"来自 golden / 源页面抓取"两者都不存在。
- 失败路径：S2 FREEZE 生成断言时 computed 无期望值来源，只能省略（违反 §4.3 291）或由 lead 自填（自证回潮）；golden 采纳（§6.5 502）后新版本的 geometry/computed 无持久期望值，后续 FREEZE/VERIFY 重生成断言时无法执行第 2 层/computed 层，或按当前实现自测而恒过。
- 受影响决策：FREEZE 断言生成与放行、VERIFY 第 2 层与 computed 层判定、critic-gate 依据的断言是否可信。
- 不可延后：期望值必须来自持久工件或审批记录；golden 采纳与断言生成已是流程核心，事后补字段要重生成所有基线版本断言并重新 Human 批准。附录 A 772 标"已修复"与此不符。

**FATAL-N1（新）inherit 切片的 state 预演循环，新增状态无法通过 FREEZE**
- 证据：§4.8 375 要求"inherit 切片在 FREEZE 时必须在 source_page.commit 上预演 setup 并到达 marker"，§6.3 481 检查 3 重复该要求；§4.8 376 规定源页面缺 data-region/data-state 钩子时"先在 delta 内补齐钩子，或先建 prefactor 切片"；§6.2 463-464 规定 FREEZE 在 BUILD 之前；不变量 3（68）禁止 ready-to-build 前写 UI 代码；不变量 6（71）要求实现提供 data-region/data-screen/data-state；§4.2 159-170 states/marker 是基线内容；§11 715/721 S2 新增 filter-open 状态，§11 702-703 S3 新增 empty/loading。
- 失败路径：inherit 切片引入 source_page.commit 上不存在的状态（filter-open/empty/loading）或缺少钩子时，该 commit 没有对应 marker 与 data-region；检查 3 要求在该 commit 上到达全部 marker，逻辑上不可能；补齐钩子属 UI 代码（§4.8 376 写入 delta），按 §6.2 只能在 FREEZE 之后 BUILD，且不变量 3 不允许提前写 → 循环；prefactor 方案也只能在 prefactor BUILD（FREEZE 之后）后才产生钩子，且新状态本身属于本切片实现。结果：agent 只能伪造预演记录、把 relation 改判 independent（需 Human）或卡在 needs-triage。
- 受影响决策：relation/state 集合批准、FREEZE gate、CHART 的 prefactor 前置顺序。
- 不可延后：这是 state 一等维度的核心门禁契约；修正需区分"源已有状态（可预演）"与"本切片新增状态（首轮 VERIFY 校验）"并重排钩子前置，属 gate 定义变更。

## MAJOR

- **MAJOR-1（M2 残）版本生命周期与升级循环**：§6.2 463 FREEZE 产出新基线版本，§4.2 219 + 不变量 9（74）要求任何内容变更升版且旧版 superseded；但 current.yaml 指针更新、旧版标记与级联只在 SETTLE golden 采纳流程定义（§6.5 502-506）。FREEZE 建版本时谁更新指针、谁标 superseded、谁触发 §8.3 624 的机械级联未定义；§6.3 479 检查 1 不校验 current.yaml 与版本一致，可产生多个 active/陈旧指针。§6.5 500-502 每次 delta 默认采纳即建 v<N+1>，与 FREEZE 建版本叠加，单个切片产生 2 个版本且版本永久保留（不变量 9），Human 需多次 content hash 批准；跨地图共享同一基线（scope.maps，§4.2 144；不同地图可并行，§8.4 631）时，A 地图 settle 升版 → 级联 B 地图未结束切片 → B 重冻再 settle 再升版 → 互相级联，形成反复重冻（livelock）。§11 726"SETTLE golden 写入 v4；若存在 human-first-review oracle，升版 v5"与 §6.5 500-502 矛盾。影响：版本链与级联节奏不可预测。跟进：定义 FREEZE 建版本的指针/superseded/级联协议、current.yaml 一致性校验、跨地图共享基线的版本节奏、修正 §11 示例。
- **MAJOR-2（M3 残）证据与豁免完整性未纳入审批/校验**：golden approval 的 region sha256（§4.9 386-388）没有任何 gate 使用（§6.3 480 只查文件存在）；`oracles/*.png`（§4.1 114）无 hash 或审批绑定（content_hash 只覆盖 baseline.yaml，§4.10 403）；waivers.yaml（§4.1 117、§7.4 574）无 hash 绑定与校验；thresholds approvals（§7.4 572）不绑定 thresholds_hash，§6.3 485 只写"已绑定当前版本"；viewports.yaml（§4.1 106）有 approvals 但无 hash 进入 assertions inputs（§4.3 231-236）也无 FREEZE 检查。失败路径：审批后替换 golden/oracle PNG、改 waiver 或 viewport 定义，无任何门禁发现，下一次比对按被篡改基准放行。跟进：approval 覆盖证据文件 hash，FREEZE/VERIFY 校验，viewports/project 纳入断言 inputs。
- **MAJOR-3 content_hash 可移植性**：§4.10 403 对 baseline.yaml 除 status/approvals 的全部字段取 hash，其中包含 `source_page.worktree`（§4.2 157）等工作区本地值；同一基线在不同工作区/协作者处重算 hash 不同 → §6.3 479 检查 1 失败或审批绑定不可复现。跟进：hash 排除环境本地字段或改为仓库相对路径/规范化输入。
- **MAJOR-4（M6 残）prefactor/integration 仍不可 FREEZE**：§8.2 601 允许 integration `baseline_ref: null` 且只生成结构/交互断言，但 §6.3 479 检查 1 要求 baseline.yaml 存在、active、有 Human content_hash → 直接冲突。prefactor 的 harness 形态是 §12.1 733 的待定项，但 §4.4 312 将其设为必填、§5.2 436 要求 bootstrap 写入 project.yaml、§8.2 598 与 §6.3 486 要求 harness 可用 → 首个 prefactor 无法按合同 FREEZE。§8.2 601"prefactor 的 screen 为 harness 入口"与 §4.2 screens.route（160）无对应字段；"组件自身区域"的 setup/marker/oracle/截图载体未定义。跟进：允许 integration 无基线的独立检查条款、先决定 harness/fixture 形态或允许占位、定义组件级 screen/oracle 语义。
- **MAJOR-5（M11 STILL OPEN）附录 A/§12 收口失真且内部矛盾**：附录 A 767-787 标注"已修复"的 FATAL-2（772）、M2（774）、M3（775）、M6（778）、M9（781）、M11（783）、MINOR（785）、UNVERIFIED（786）、ESCALATE（787）与本审查结果不一致；§12.1 733-734 两项待定与 §5.2 436/§8.2 598/§6.3 486 的依赖矛盾，且 §12.1 736"不阻塞 v3 的流程合同"与 bootstrap 首步（§5.1 417）依赖未决输入冲突；§12.2 742 推迟配套 DESIGN.md 草案最终批准与 §10.3 693"必须联合批准、版本号绑定"矛盾；§12.4 755-765 未列 golden 期望值出处、证据 hash、FREEZE 版本协议、inherit state 预演等设计缺口。影响：Human 依据收口声明批准。跟进：按实际状态重写附录 A/§12，消除 §12 与 §10.3/§5.2/§6.5 的矛盾。
- **MAJOR-6 非 golden oracle 无环境证据**：source-snapshot/design-export 证据（§4.1 114、§4.9 380-381）无抓取环境元数据；§7.4 576 的 env-mismatch 只比较 meta.yaml 与 golden approval.yaml，非 golden oracle 没有对应 env 记录。浏览器/字体/DPR 变化后旧截图比对产生的差异无法归因为环境变化，会被当作代码回归；也无法触发 Human 批量重批。跟进：所有 oracle evidence 记录捕获环境并在 VERIFY 全量校验。
- **MAJOR-7 state 契约落点缺失**：§4.8 375 与 §6.3 481 要求新页面切片把"钩子与 setup 写入 Structure Decisions"，但 §4.4 321 的 Structure Decisions 表只有 region|state|means|target|reason|flag|approved_by，无 setup/hooks 字段；§6.2 462 DECIDE 完成条件也只要求 region×state 有 means。新页面 FREEZE 检查 3 无法由定义工件满足，只能写自由文本 → 不可机械校验。跟进：在 Structure Decisions 或基线中以结构化字段承载 state 钩子/setup。
- **MAJOR-8 bootstrap 依赖未决输入**：§5.2 436 要求 bootstrap 在 project.yaml 记录 fixture 提供者（§4.8 372）与渲染 harness 形态（§8.2），但 §12.1 733-734 明确二者仍待定；bootstrap 是 ENTRY 第 1 行（§5.1 417），首个项目接入即依赖未决输入，只能写占位或中断。跟进：先把这两项定为 bootstrap 可写的最小协议，或把 bootstrap 记录改为可空并在首个 prefactor 前补。

## MINOR

- §11 726 示例的 golden 采纳与 §6.5 500-502 不一致（delta 默认采纳应创建 v<N+1>；示例写入 v4 且仅在 human-first-review 时升版）。
- `baseline_hash`（§4.3 232、§6.3 479/482）与 `content_hash`（§4.10 403）未显式等同，两处检查的哈希对象不同名。
- `blocked_reason` 只允许在 needs-triage（§4.4 307、§8.3 626），但恢复/转移时清除规则未定义。
- `unknowns` 已解决的记录位置未定义（仅 Design Reading `.tmp`，§4.7 362/365；§6.3 483 依赖其不存在）。
- golden oracle 的 `evidence` 路径歧义：§4.1 114 的 oracles/ 只列 source-snapshot/design-export，golden 在 §4.1 115，§4.2 214-215 要求非 human-first-review 必须有 evidence，§6.3 480 只要求文件存在。
- §7.3 547 截图声明 pixel 走 design-export，但 §7.2 531 的 design-export 适用未列截图；§7.3 548-549 对有既有页面/Human 描述的 fidelity 写"—"，与 §4.2 150 必填枚举冲突。

## UNVERIFIED

- §10.1 verified_against（656）只有工作区路径+核对日期，没有 skill 版本/commit/hash；"消费的 packet 字段随 skill 版本固定"（663）无法核对（我核对了当前模板确有 DESIGN_EVIDENCE/design_relation/preserve/delta 与 REUSE_MAP 等字段，但版本未固定）。
- §12.4 757-765 的技术验证项（生成器确定性、must_import 推导、运行环境、setup 可执行性、fixture 协议、eval）在本审查中无法验证。
- prefactor 的 harness（Storybook/预览路由/单测渲染）在目标项目中是否可用未验证（§12.1 733）。
- content_hash 跨机器/工作区复现性未验证（含 worktree 路径，#4.10 403）。
- 配套 DESIGN.md 草案的版本号/批准状态与 §10.3 693 的"版本号绑定"无法核对（该文件仍写"与本 v2 配套"且未批准，见 ESCALATE）。

## ESCALATE

- 配套 `2026-10-17-design-md-framework-draft.md` 状态仍为"草案，未批准"且声明"与 v2 配套"（L4），没有 v3 §10.3 693 所需的版本号；v3 §12.2 742 又将配套最终批准推迟 → 联合批准条款当前不可执行（配套文件不在本次审查范围）。
- sketch-copilot-plus 工作区存在未提交改动；v3 §10.1 的 verified_against 只有路径+日期，无版本/commit，跨 skill 接口"版本固定"无法落地（skill 文件不在审查范围）。
- yes-subagents 的 Coder Plus/Critic Gate 以 go-spec Milestone/dispatch brief 为常态输入；v3 的 `.tmp` dispatch 简报（§10.2 681）能否被角色接受未经实现验证（超出本草案范围）。
- 目标仓库 `docs/DESIGN.md` 仍为空文件；v3 §4.1 将在项目根创建 DESIGN.md 并在 docs/island/designer 建工件，与仓库既有文档布局/AGENTS.md 的关系需 Human 定夺（附录 A 787 已移交）。
- 历史草案 v1/v2 仍保留旧术语，v3 只在两篇背景笔记加指针；v1/v2 未标"被 v3 取代"，后续 agent 仍可能读旧合同（文档维护，不在 v3 正文）。

STATUS: FAIL
