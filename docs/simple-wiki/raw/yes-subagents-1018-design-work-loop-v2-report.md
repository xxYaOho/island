---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/1018-strict-case/v2/yes-designer-work-loop-v2-report.md
---
# Round 2 审查反馈（critic-strict）

- 审查对象：`v2/yes-designer-work-loop-v2.md`（538 行，2026-10-18 00:24 版）
- 模式：FULL / intensity=high / Round 2（修正轮 1）
- 结论：`STATUS: FAIL`
- 统计：FATAL 2 / MAJOR 12 / MINOR 6 / UNVERIFIED 6 / ESCALATE 5
- Round 1 台账：F1 CLOSED、F2 PARTIAL、F3 CLOSED、F4 CLOSED

---

yes-designer 工作流 v2 — Round 2 / FULL / high 审查
对象：docs/notes/2026-10-17-yes-designer-design-work-loop-v2.md（538 行，2026-10-18 00:24）；行号均为 v2，外部核对另注路径。

## Round 1 FATAL 台账（Round 2 判定）

- **F1 CLOSED**：§4.4 174-187 切片 frontmatter（status / blocked_by / claimed_by / baseline_ref / round / updated_at）落盘；§4.5 209 Frontier 由 frontmatter 推算；§5.1 243-251 ENTRY 含 Resume / work / reopen 路由；§8.3 401-414 状态转移表。原失败路径（会话 2 无法判断切片是否可推进）可解。
- **F2 PARTIAL**：冻结工件与哈希门禁已建立（§4.2 102-142、§4.3 144-170、§4.1 80-85、§6.3 297-305；不变量 5/7 见 48/50），另一 agent 可验证冻结。但「VERIFY 可执行断言」未闭合：geometry 断言无期望值/测量来源（§4.3 160-163、§7.4 365），computed style 断言无 schema（§7.4 371），断言文件与生成器输出一致性无校验（§6.3 303 只验 baseline_hash）。见 FATAL-2。
- **F3 CLOSED**：不变量 4/5（47-48）、§3.1 55-62（new-with-candidates / extend / independent / DEVIATION 交 Human）、§4.3 146 生成器、§6.3 305。原「SCAN 记排除理由→自写断言」路径被 Human 审批 + 机械断言阻断；扫描完整性残留见 M8。
- **F4 CLOSED**：§7.2 336-343 新增 human-first-review（无需前置图像、首轮 1/5 层、批准后转 golden）；§7.3 345-355 覆盖 Sketch / 原型 pixel / visual / layout / 截图 / 既有页面 / Human 描述；§6.3 304 允许无图 oracle；§8.3 410 按 oracle 类型放行。原「FREEZE 卡死或写空 oracle」路径可解；矩阵内部矛盾见 M9/M10。

## FATAL

**FATAL-1 多状态页的验收键无 state 维度（结构性缺陷）**
- 证据：§8.1-4 386 允许一页 ≤3 状态、§8.2 393 定义 page=一个界面的若干状态、§11 480-481 给出 S2=default+filter-open、S3=empty+loading；但 §2 33 规定 region 身份=data-region 值且在基线内唯一，§4.2 128-134 的 region 无 state 字段，§4.3 160-167 断言按 region 单份，§4.1 83 golden 路径为 golden/v<N>/<region-id>.png（无 state），§4.7 228 Design Reading 的 screen/state 在转成基线时丢失，§7.1 328-329 几何/像素按「各区域」一次。
- 失败路径：S2 的 filter-panel 在 default（收起）与 filter-open（展开）几何/外观不同，基线只能有一条 filter-panel 与一个 oracle；VERIFY 无法指定「哪个状态对比哪个 oracle」——两状态对同一 oracle 必然一真一假，或只截一个状态导致另一状态未验收；golden/v<N>/filter-panel.png 只保存一个状态，后续回归对另一状态失效。
- 受影响决策：FREEZE 的 region/oracle 生成、VERIFY 第 2/3 层判定、golden 归档与后续回归。
- 不可延后：golden 归档布局与断言键需要 state 维度，实现阶段再补会作废已 Human 批准的 golden 与已冻结基线。附录 A 526 称 M2 已由 §2/§4.1/§4.2 修复，但 state 维度未进入任何基线/断言/归档路径，证据—结论不匹配。

**FATAL-2 断言集不可完整机械执行（F2 PARTIAL 的残留）**
- 证据：(a) §4.3 160-163 geometry 断言只有 region/oracle/tolerance_ref，无期望 bbox/测量来源；§7.4 365 只写「bbox 四值取整到 CSS px 后之差」，baseline regions 无 bbox（§4.2 128-134），design-export 是 Sketch/原型导出图、无 CSS px 映射（§7.2 341）；(b) §7.4 371 要求「色值、字号、间距优先用 computed style 断言」，但 assertions.yaml（§4.3 154-167）无对应字段/执行器，§6.3 301-305 也不检查；(c) 不变量 5（48）规定断言由生成器生成、不得手写，但 §6.3 303 只校验 assertions 的 baseline_hash 与基线一致，不校验断言内容等于生成器输出——直接改 assertions.yaml（删 must_import / diff_scope 项）仍可通过 FREEZE。
- 失败路径：VERIFY 第 2 层无基准可算 → 跳过或由 lead 自造；断言被改而门禁仍放行，结构/几何断言的实际强度不可验证。
- 受影响决策：FREEZE 放行、VERIFY 各层结论、critic-gate 所依据的断言是否可信。
- 不可延后：断言 schema 是 v2 自己定义的冻结门禁工件合同（F2 修复本体），实现阶段再扩字段等于改已批准设计，且 §6.3 声称其可机械校验。

## MAJOR

- **M1 状态机/级联覆盖缺口**：§4.3 170 规定断言过期时「VERIFY 返回 BLOCKED」，但 §8.3 401-414 无 BLOCKED 状态/转移；§6.5 318 只级联 building/verifying，§8.3 414 只写 settled 因基线升版回 needs-triage——ready-to-build / needs-review / needs-decision 引用旧版本时无规则；reopen 已 settled 切片（§5.1 246、§8.3 414）未定义是否升版/golden 重批；claim 无原子性（§8.4 420-421，两个 lead 会话可同时认领）。失败路径：S2 settle 升版 v3 时 S5 仍 ready-to-build（冻结在 v2），未被级联，BUILD 后 VERIFY 因 baseline_hash 不一致返回 BLOCKED，无合法状态可写。影响：多切片共享基线时推进不可预测。跟进：补 BLOCKED/重冻转移、覆盖所有引用旧版本状态的级联规则、reopen 基线规则、claim CAS。
- **M2 基线/golden 版本与写序**：§4.1 80-84 为单文件 baseline.yaml/assertions.yaml + golden/v<N>；§4.2 107 status 与 142（仅改名/增删算升版）使旧版本 superseded 无法在单文件模型保存（只能靠 git）；§6.5 316-317 先写 golden/v<N> 再升版，写序与目标版本不明；§7.2 342-343 golden oracle 要求「当前版本目录存在」；human-first-review 批准后转 golden 时 baseline 的 oracle 字段/版本更新未定义；source-snapshot / design-export 存 .tmp（§4.1 93），baseline.source.refs 未要求固定 Sketch 文档版本（§4.2 112-114）。失败路径：S2 写 golden/v2 后升版 v3 → S3 引用 v3 时 FREEZE 查 golden/v3 不存在，卡死或复制旧图；reopen 未升版时 SETTLE 重写 golden/v<N>，覆盖已批准基准且无 superseded 记录；Sketch 文档变化或 .tmp 清理后 design-export oracle 不可重建。影响：golden 闭环在升版处断裂、审批不可回溯。跟进：定义 golden 与版本写序、版本化 baseline/assertions 路径、superseded 记录、oracle 可再生性与来源版本固定。
- **M3 审批可追溯性**：§4.2 135-139 approvals 只有 action/by/at/note，不绑定内容 hash/版本；§6.3 301 只查「最新 approvals 为 Human」；§4.2 142 仅改名/增删触发升版，改 delta.files / region role/content/oracle/threshold_ref 可不升版地改基线并重生成断言；golden approval.yaml 无 schema 且 §6.3 304 只查 golden 存在；thresholds 的 Human 批准（§7.4 373）无记录位置（§4.1 88 只有「校准记录」）；「放宽断言」（不变量 7、§3.1 64）在 assertions.yaml 无 approvals 字段。失败路径：Human 批准 create 后 lead 改 delta.files/region oracle，baseline_hash 变、断言重生成，FREEZE 仍见最新 approval=human 通过；另一会话无法证明当前内容即 Human 所批。影响：冻结门禁可被静默改写。跟进：approvals 绑定内容 hash/版本；定义 golden/thresholds/assertions 的审批工件与 schema。
- **M4 阈值/验收数学仍不可判定（Round-1 M6 残）**：§7.4 367 仍为单一比例「差异像素 / 区域像素 ≤0.1%」，与区域面积无关（24×24→0.58px；1440×900→1296px≈36×36）；§7.4 373 仍是「5 次取最大值 + p95 加余量」（5 样本 p95≈最大值，容差被设到噪声上界）；§7.1 326-334 无「任一区域失败即层失败」的汇总规则；§7.1 331 阈值外差异无 waiver 记录；§7.5 377 未定义 golden 环境元数据与 VERIFY 的失配检测；无 viewport/DPR 矩阵。失败路径：小区域一像素变化即误报，大区域可隐藏约 36×36 的可见缺陷，真实小回归在噪声余量内必过；Human 接受阈值外差异后下一轮重复失败。影响：像素门禁不可信。跟进：面积归一+绝对上下限、汇总判定、waiver 工件、golden 环境元数据与失配检测、viewport 矩阵。
- **M5 交互/状态切换断言缺 schema**：§8.1-5 387 要求「以状态切换断言验收」、§8.2 393 page 验收「完整五层」，但 §4.3 assertions 只有 structural/geometry/pixel（154-167），§7.1 结构层只列 diff 范围 / must_import / forbid / regions_present（327）。失败路径：filter-open / blank / invalid 状态切换无机械验收，Human 漏看即进入 golden，后续无回归保障。影响：纵向切片中的「状态」未纳入门禁。跟进：定义 interaction/state-transition 断言类型与执行环境。
- **M6 prefactor/integration 无验收载体**：§8.2 394-395；§4.1 94 rounds、83 golden、§4.2 source/source_page 都以页面/route 为前提；prefactor 无 page/route 如何渲染截图未定义；integration 的 baseline_ref（§4.4 184）指向哪份基线、是否新建基线、跨基线复用 page 断言/golden 版本未定义；§6.3 304 oracle 可用性对无页面切片无对象。失败路径：S1 在 FREEZE 无法满足 baseline/oracle 检查；S6 无 baseline/断言可生成。影响：两种声明支持的切片类型不可独立验收。跟进：定义组件渲染 harness 与 integration 基线/断言来源。
- **M7 ENTRY 路由缺口**：§5.1 243-251「命中即停」；「单切片、来源不命中现有基线 scope、无地图」的新页面任务无匹配（1 否；2 否；3 通常否；4 否；5 要求命中基线 scope；6 要求跨会话或 ≥2 切片；7 为「无输入」）。失败路径：agent 自行落到 chart/quick 或停在 ENTRY，首步无规范路由。影响：常见新页面任务首步无定义。跟进：补默认/兜底路由与「单切片新页面」路径。
- **M8 F3 残留：扫描完整性自证与 unknown 门禁**：§3.1 58「扫描范围完整且无候选→lead」由 lead 自证；§10.2 461 Researcher 边界由 lead 给；§4.7 232 unknowns[].blocks 无阻断规则，§6.3 299-305 未把 unknowns 列入 FREEZE 条件；§7.1 331 仅 REVIEW 提示 flag。失败路径：lead 定义窄范围→无候选→means new（lead 决定）→机器断言按新结构生成→全过；REVIEW 提示时已实现；未知交互被猜测后进入 golden。影响：F3 的扫描遗漏分支未闭环。跟进：扫描范围下限模板+completeness 证据、unknowns→FREEZE 阻断、或 new-without-candidate 需 Human 预批准。
- **M9 来源/fidelity/oracle 不一致**：§4.2 113-117 任意 source.kind 都有 fidelity；§7.3 353 截图一律 human-first-review（不区分 pixel/visual/layout），§7.2 341 design-export 只覆盖「有设计稿或 pixel 原型」，截图 fidelity=pixel 无 design-export 路径；§7.3 352 layout 行写「几何：仅顺序与对齐」，但 §7.2 343 human-first-review 首轮只执行 1/5 层（几何不执行）且无该断言类型；§7.3 354 既有页面 delta 用 source-snapshot，与 §7.2 343「无设计稿的 delta 用 human-first-review」冲突；design-export 到 CSS px 的坐标/缩放/DPR 映射未定义（§7.2 341、§7.4 366 ±1px）。失败路径：Human 要求截图 pixel 还原仍被降级为 human-first-review，几何/像素层跳过；既有页面 delta 区域对比 source-snapshot 必失败（预期改动被当回归）；Sketch 2x 导出与 CSS px 比较坐标错位。影响：来源矩阵与 fidelity/oracle 语义不一致。跟进：fidelity 纳入矩阵、定义 layout 顺序/对齐断言、像素来源坐标映射、既有页面 delta oracle 规则。
- **M10 human-first-review × FREEZE 冲突**：§6.3 302 要求每个 region 有 threshold_ref；§4.2 128-134 region schema 无 null 约定；§7.3 351-353 这些来源阈值组为「—」；§7.4 363-369 无对应 threshold ID。失败路径：screenshot / visual / layout / human-description 切片 FREEZE 时机械检查不满足，或被迫填不执行的 regression.default。影响：F4 修复点的机械检查自相矛盾。跟进：允许 threshold_ref 为 null 或定义 human-review 阈值 ID。
- **M11 附录 A/§12 收口不成立（证据—结论不匹配）**：附录 A 521-537 将 M2/M3/M6/M8/M9/M10/M11 标为已修复，但 M1-M10 仍存在；§12.1 496「讨论中：无」与实际未决项（多状态键、geometry 期望、BLOCKED 转移、阈值归一、waiver、viewport、prefactor/integration、断言出处）不符；§12.4 508-515 只列技术验证，未列上述设计缺口；附录 A 526 的 M2 修复引用不含 state 维度；537「已核实，见 §10」对 Coder Plus 映射不成立（M12）。影响：Human 依此认为范围闭合而批准。跟进：按实际状态重写附录 A/§12，区分 CLOSED/PARTIAL/OPEN。
- **M12 §10.2 映射不闭合**：§10.2 455-461；对照 yes-subagents `subagents/coder-plus.md` PRECONDITION，Coder Plus 要求 implementation content、acceptance criteria、editable boundary、downstream interface commitments、Git policy、Git baseline（starting HEAD / staged / unstaged / untracked / ownership）与通常的 go-spec Milestone/dispatch brief；§10.2 459「yes-designer 提供」缺 Git policy 与 downstream interface commitments（「must_import 与 preserve 区域」不构成下游接口承诺），Git baseline 只写「项目 Git 状态」。失败路径：按 §10.2 派发 Coder Plus，角色因两项缺失返回 BLOCKED，派发模式不可执行（直接模式仍可用）。影响：§10「已核实」的映射不完整。跟进：补齐两项或声明提供方、写入 dispatch 工件；§10 补证据版本。

## MINOR

- §2 32「preserve 不再显式列出」与 §4.2 130 `role: preserve`、§7.2 340、§7.3 357 冲突（实际取消的是顶层 preserve 列表，region 级仍显式）。
- §5.2 261「（L2）」与 §12.4 512「方式 A」未在 §2 定义（旧版术语残留；附录 A 536 的 MINOR 修复声明不完整）。
- §8.3 405/411-414 把 Human 写为状态转移执行者，与不变量 8（51）「docs/island/designer 仅 lead 写入」字面冲突；应写 Human 决定、lead 写入。
- §5.2 263/265 与配套草案 §5（framework 175-184）重复定义 DESIGN.md 创建时机；仅 DESIGN.md 缺失时该检查不在 §5.1 路由表中。
- §4.3 156 `allow: []` 与注释「= 所有 delta.files」是占位还是生成结果不明；`baseline_hash` 算法/规范化未定义。
- §11 490 示例未展示 baseline 创建/升版的 Human 批准，与 §3.1 63、§6.3 301 不一致。

## UNVERIFIED

- §12.4 512 方式 A 运行环境（skill 自带 Playwright/pixelmatch + 本机 ImageMagick 7）未验证；若不成立，断言生成/执行链失效。
- §12.4 513 `must_import`/`diff_scope` 能否从 source_page.commit 机械推导未验证；这决定 F2 断言生成前提。
- §10.1「已核实」无版本/commit/证据路径；我核对项目内 `skill_sketch-copilot/skills/pro/reference/dispatch-packet-template.md` 确有 DESIGN_EVIDENCE（design_relation / preserve / delta）与 REUSE_MAP、GOAL / VERIFY_TARGET / LEAD_HANDOFF / SUBAGENT_ACK；但模板自述旧 packet 可能含旧列，未验证覆盖全部输入 packet。
- §10.2 对 Critic Gate/Researcher 的前置描述与角色文件一致；但 Coder Plus 的 go-spec Milestone/dispatch brief 工件映射、以及「项目 Git 状态」能否满足其 Git baseline/ownership 要求未验证。
- 阈值实测与文字渲染噪声、取整后 0px 稳定性（§12.4 510-511）无数据。
- 目标项目 `.git/info/exclude` 写入权限、AGENTS.md 修改流程、skill `assets/DESIGN.template.md` 分发路径未验证。

## ESCALATE

- 配套 DESIGN.md 草案状态为「草案，未批准」（framework L4），v2 §5.2/§10.3/§3.1 直接依赖其模板、R-001..R-005、rules.yaml、CREATE/GROW；§12.1 只称其待定项已决定，未声明联合批准/版本绑定 → v2 若先批准，实际行为由未批准文档决定。
- v2 §12.3 505 决定「背景笔记不再修改」，但 2026-10-16 与 adapter note 仍用旧词汇；后续 agent 会读到两套术语，建议在背景笔记加「v2 §2 取代」指针（文档维护，不在 v2 正文）。
- v2 §12.2 501 推迟 sketch-copilot-plus 的 packet / implement.md / verify.md 定位，而 §10.1 已按当前 packet 字段消费；跨 skill 接口无版本锁定，该 skill 0.2.x 变动需同步 v2 映射。
- yes-subagents 面向「approved plan / go-spec Milestone + dispatch brief」，v2 只有切片文件 + Human 批准基线；handoff 工件映射未定义，派发模式可能长期不可用（§10.2 只做前置字段映射）。
- 目标仓库 docs/DESIGN.md 为空文件，v2 §4.1 将在项目根维护 DESIGN.md 并在 docs/island/designer 建工件；与仓库既有文档布局/AGENTS.md 的关系需 Human 定夺。

STATUS: FAIL
