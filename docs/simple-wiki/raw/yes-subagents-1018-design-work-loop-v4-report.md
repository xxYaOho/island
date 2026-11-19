---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/1018-strict-case/v4/yes-designer-work-loop-v4-report.md
---
# Round 4 审查反馈（critic-strict）

- 审查对象：`v4/yes-designer-work-loop-v4.md`（857 行，2026-10-18 10:51 版，sha1 `1f7ee57…`）
- 模式：FULL / intensity=high / Round 4（修正轮 3）
- 结论：`STATUS: FAIL`
- 统计：FATAL 1 / MAJOR 7 / MINOR 7 / UNVERIFIED 5 / ESCALATE 5

---

yes-designer 工作流 v4 — Round 4 / FULL / high 审查
对象：docs/notes/2026-10-18-yes-designer-design-work-loop-v4.md（857 行，2026-10-18 10:51，sha1 1f7ee57…）；行号均为 v4，外部核对另注路径。

## Round 3 台账判定

- **FATAL-R PARTIAL**：已补 golden measurements（§4.9 419-442）、design-export 的 `source_anchor`/`export`/`evidence_sha256`/`capture_env`（§4.2 194-220、239-240）、`computed_expectations`（§4.2 221-225）、期望值必须有持久出处的生成器约束（§4.3 322-329）、检查 2（§6.3 528）。未闭合：(i) `computed` 与 `layout` 断言已生成（§4.3 289-305、阈值 §7.4 611-612）但 §7.1 分层（567-572）只执行 STRUCTURAL/GEOMETRY(bbox)/PIXEL/INTERPRET/HUMAN，两类断言没有任何执行层；(ii) design-export 的期望值仍不可按 state 表达：`region.source_anchor`（§4.2 194-201）与 `region.layout` 各只有一个，而 oracle/geometry/layout 断言都按 `region × state`（§4.2 202-220、§4.3 282-305），geometry 期望 = `source_anchor.frame - origin`（§7.2 586）→ 同一 region 的全部 state 共用同一期望 bbox/layout；(iii) design-export 像素对比缺对齐/SSIM 规则：v3 §7.4 的"两图按 oracle 尺寸对齐/灰度/ImageMagick 工具"段落在 v4 §7.4（603-630）被删，§7.2 586 只定义几何映射，actual（DPR 见 §7.5 634）与 export 图（scale 见 §4.9 418）如何归一未定义。见 FATAL-1。
- **FATAL-N1 CLOSED**：新增 state origin（§2 50）、`states.origin/hooks`（§4.2 171-181）、source/introduced 分流与结构校验/首轮可达性（§4.8 411-413）、检查 3（§6.3 529）、State Contract（§4.4 354）、示例 introduced（§11 778）。循环已解：源状态需预演，缺 hooks 或新状态归 introduced，不预演、首轮 VERIFY 验可达。残项见 MAJOR-N1。
- **MAJOR-1 PARTIAL**：已补 FREEZE 升版协议与 baseline_ref 更新（§6.3 527）、golden 不作为基线内容（§6.5 552）、仅 human-first-review 转换升版（§6.5 553）、跨版本 golden 复制（§6.5 554）、settled 不级联（§6.5 558、§8.4 691）、示例修正（§11 784）。未闭合：FREEZE 建新版本时证据/golden/approval 的复制与写序未在检查 1 中定义（§6.3 527 只写"完整候选内容"；§6.5 554 处于 SETTLE 语境）；复制后 golden approval 的 `version`/`content_hash`（§4.9 421-423）语义与检查 7"golden 已绑定当前版本"（§6.3 533）的可校验性未定义；human-first 转换时 golden 先写 v<N>（§6.5 552）再建 v<N+1>（553），转换后 golden 落点/去重未定义；跨地图 in-flight 互相级联仍可能（§8.4 689-691 只排除了 settled）；见 MAJOR-1。
- **MAJOR-2 PARTIAL**：证据 hash 已校验（§6.3 528 evidence_sha256/golden）、`waivers_hash`/`viewports_hash`/`golden_hash` 已进入断言 inputs（§4.3 254-263）、§4.10 453-454 定义。未闭合：thresholds/waivers/viewports/rules 的 Human 审批没有被 FREEZE 校验——检查 6（§6.3 532）只列 new/extend/independent/DEVIATION/基线内容/golden，检查 7（533）措辞模糊；thresholds 的 previous/new hash（§4.10 453）无校验点；修改这些文件后可自动重生成断言（§4.3 327）并通过检查 4（530）。见 MAJOR-2。
- **MAJOR-3 CLOSED**：删除 `worktree`（§4.2 160-164），`content_hash` 排除环境本地字段（§4.10 450）。
- **MAJOR-4 PARTIAL**：已补 prefactor harness 来源与 TBD（§5.2 484、§8.2 652/655、§12.1 791）、integration `baseline_ref: null` 与专用断言（§8.2 657、§6.3 534）。未闭合：integration 复用页面断言只在 FREEZE 时"解析到 active 页面基线"（§6.3 534），未绑定被引用基线的版本；cascade 只针对"引用被 superseded 版本"的切片（§8.3 682、§6.5 558），baseline_ref 为 null 的 integration 不会随页面基线升版被级联 → 复用的断言/区域期望可静默变旧。见 MAJOR-4。
- **MAJOR-5 PARTIAL**：§12 已基本自洽（§12.1 TBD+阻塞边界 791-794、§12.2 移除配套推迟 796-799、§12.3 联合批准 805、§12.4 覆盖新验证项 814-827）；但附录 A 仍把 FATAL-R/MAJOR-1/2/4/6 标为"已修复"（833/835/836/838/840），附录 B 852/857 亦为过度声明 → 证据—结论不匹配。见 MAJOR-5。
- **MAJOR-6 PARTIAL**：已补 `capture_env`（§4.2 209、239）、检查 9（§6.3 535）、§7.4 630 含 source-snapshot env 与 golden approval env。未闭合：`capture_env` 字段无 viewport（§4.2 209），而 §7.4 630 要求比较 viewport；§7.2 586 要求"所有图像型 oracle 记录 capture_env"，但 §7.4 630 只校验 golden 与 source-snapshot，design-export 的 capture_env 语义与校验不一致；env-mismatch 后"Human 批量重新批准"（§7.4 630）的重抓/升版流程未定义（重抓 source-snapshot/design-export 会改 baseline 内容与 evidence_sha256，需升版）。见 MAJOR-6。
- **MAJOR-7 CLOSED**：`states.origin/hooks` 进入基线（§4.2 171-181）、State Contract（§4.4 354）、检查 3（§6.3 529）。
- **MAJOR-8 CLOSED**：bootstrap 写 `TBD` 且只阻塞依赖切片（§5.2 484、§6.3 534、§12.1 791-794）。
- **MINOR（6 项）CLOSED**：§11 784 修正 golden 采纳；`content_hash` 命名（§4.3 255/§6.3 530）；`blocked_reason` 清除（§8.3 684）；unknowns 记录（§4.4 358、§6.3 531）；golden 证据路径（§4.2 238）；截图 pixel 与矩阵（§7.2 582、§7.3 598）；fidelity 枚举（§7.3 600-601）。
- **UNVERIFIED PARTIAL**：5 项已进 §12.4（814-827）；但 §10.1 的固定方式有误（见 MINOR-2/UNVERIFIED-1）。
- **ESCALATE PARTIAL**：配套草案已改与 v4 联合批准（framework L4，已核对）、v1/v2/v3 与背景已加指针（已核对）、空 DESIGN.md 已移交 Human（附录 845）；sketch-copilot-pro 的版本固定不可复现（见 UNVERIFIED-1）、配套草案仍无版本号可与 §10.3 751 的"版本号绑定"对齐。

## FATAL

**FATAL-1（承接 Round 3 FATAL-R：PARTIAL）断言集仍未达到"可完整机械执行"**
- 证据 (i)：`computed`（§4.3 289-298）与 `layout`（§4.3 299-305）断言由生成器产出，阈值 `computed.default`/`layout.default` 已定义（§7.4 611-612），但 §7.1 的五个执行层（567-572）只列 STRUCTURAL/GEOMETRY(bbox)/PIXEL/INTERPRET/HUMAN；两类断言没有层归属，也没有执行/报告规则 → 生成即不被验。
- 证据 (ii)：`region.source_anchor` 与 `region.layout` 各只有一份（§4.2 194-201），而 oracle、geometry、layout 断言均按 `region × state`（§4.2 202-220、§4.3 282-305）；§4.2 240 与 §7.2 586 规定 design-export 的期望 bbox = `source_anchor.frame - origin`。多状态 Sketch/prototype 页面（示例 S2 的 default/filter-open，§11 773/778-779）在同一 region 的不同 state 需要不同 Frame/几何，当前模型只能产出同一份期望；layout 同理。
- 证据 (iii)：design-export 的像素比较缺归一规则：§7.4（603-630）没有 v3 的"两图按 oracle 尺寸对齐/灰度/工具"段落；§7.2 586 只定义几何坐标；§4.9 418 只定义 export 的 `scale/origin` 语义；actual 截图是 DPR 像素（§7.5 634），export 图是设计单位 × scale，尺寸对齐与重采样未定义，SSIM 参数（灰度/工具）不再固定。
- 失败路径：S2 两个 state 的 design-export oracle 生成同一 `expected_bbox`/`layout`；filter-open 的几何断言要么恒失败、要么恒通过（按实现自测）；表头 computed（颜色/字号/内边距）与 layout order/align 从不执行，视觉偏差只能靠像素层或 Human；design-export 像素层在 DPR 2 与 scale 2 的截图上做未定义归一，SSIM 结果不可复现。受影响决策：FREEZE 的断言生成、VERIFY 第 2/3 层判定、critic-gate 的验收依据。
- 不可延后：期望值与执行层是冻结门禁工件合同；实现阶段补 layer 或改 `source_anchor` 粒度会改变已批准的 assertions schema，且已产出的基线版本需重生成/重批。

## MAJOR

- **MAJOR-1 版本生命周期与跨版本搬运仍不闭合**：§6.3 527 的 FREEZE 建版本只写"完整候选内容"，未定义未修改 region×state 的 oracle 证据与 golden/approval 如何复制进 `v<N+1>`、在哪一步复制；§6.5 554 的复制规则位于 SETTLE 语境。复制后 golden approval 的 `version`（§4.9 422）与 `content_hash`（423）是否更新未定义，检查 7"golden 已绑定当前版本"（§6.3 533）因此不可校验；human-first 转换先写 `v<N>/golden`（§6.5 552）再建 `v<N+1>`（553），转换后的 golden 落点与重复版本未定义；跨地图 in-flight 切片可互相"升版→级联→重冻→升版"（§8.4 689-691 只声明 settled 不级联，未排除该循环）。影响：版本目录/审批语义漂移，级联节奏不可预测。跟进：把证据/golden 复制写序并入 FREEZE 检查 1，定义复制后的 approval 元数据与检查 7 的校验式，明确转换落点，给出跨地图 in-flight 级联的收敛/终止规则。
- **MAJOR-2 thresholds/waivers/viewports/rules 的 Human 审批未被门禁校验**：检查 6（§6.3 532）只列 new/extend/independent/DEVIATION/基线内容/golden 更新，未列阈值变更与 waiver；检查 7（533）"阈值、waiver、golden 已绑定当前版本"无具体校验式；thresholds approvals 的 `{previous_hash,new_hash}`（§4.10 453）无检查点。失败路径：改 thresholds/waivers/viewports（断言自动重生成，§4.3 327），检查 4（§6.3 530）因 hash 同步而通过，检查 6 不查这些文件 → 未经 Human 批准的验收放宽进入门禁。跟进：将这些文件的 approval/hash 记录与检查项显式绑定。
- **MAJOR-4 integration 复用页面断言未绑定版本**：§6.3 534 只在 FREEZE 解析 active 页面基线，§8.2 657 复用其断言，但切片/断言未记录被引用基线的 `@version`；§8.3 682 与 §6.5 558 的级联以"引用被 superseded 版本"为条件，baseline_ref 为 null 的 integration 不满足该条件 → 页面基线升版后 integration 的复用断言静默过期，VERIFY 仍按旧/新不定的断言判定。跟进：在 flow/断言中固定被引用页面基线版本，升版时纳入级联。
- **MAJOR-5 附录 A 状态与正文不符（证据—结论不匹配）**：833 FATAL-R"已修复" vs PARTIAL；835 MAJOR-1、836 MAJOR-2、838 MAJOR-4、840 MAJOR-6 标"已修复" vs 本审查 PARTIAL；844 UNVERIFIED"已处理" vs §10.1 固定不可复现（见 MINOR-2）；附录 B 852/857 的"v4 补齐 FATAL-2/FATAL-R/残项"同属过度声明。影响：Human 依据收口表批准。跟进：按 PARTIAL/CLOSED 实况重写附录 A/B。
- **MAJOR-6 env 覆盖仍有缺口**：`capture_env`（§4.2 209）没有 viewport，而 §7.4 630 要求比较 viewport；design-export 的 capture_env 语义（设计工具导出 vs 浏览器抓取）与 §7.4 630 只校验 golden/source-snapshot 不一致；env-mismatch 后"Human 批量重新批准"（§7.4 630）未定义重抓与升版流程（重抓会改 baseline 内容与 evidence_sha256）。影响：跨环境回归无法判定/无法恢复。跟进：补 viewport 与 design-export env 语义，定义 env 重批的 recapture→升版→Human 批准路径。
- **MAJOR-N1 introduced 状态首轮失败没有基线修正回路**：§4.8 412 规定 introduced 状态首次 VERIFY 第 1 层验可达，不可达回到 `building`；但 setup/marker/hooks 是 Human 批准的基线内容（§3.1 92、§4.8 410），修正它需要改基线（升版/needs-decision），§8.3 675 只有 verifying→building，needs-decision 只能从 building 经 DEVIATION（673），而 DEVIATION 定义是"改动 delta 以外的（代码）内容"（§6.4 544）。失败路径：new page 的 setup 目标/顺序与实现冲突或设计本身不成立 → VERIFY 反复失败回 building，缺少"setup/marker 需 Human 修正"的合法转移。另外 §7.1 568 的第 1 层描述未列 marker/reachability（数据在 §4.3 273），与 §4.8 412 的"第 1 层验证可达性"表述不完全对齐。跟进：补 verifying→needs-decision（基线契约错误）转移并在第 1 层显式列出 marker/setup 可达性。
- **MAJOR-N2 golden 同版本更新会静默改写共享断言**：§6.5 552 规定 golden 更新不升版并重生成断言，§4.3 327 允许自动重生成；同版本内的 assertions.yaml 被其它（跨地图并行，§8.4 689）引用该版本的切片共享。某切片 settle 更新 golden 后，另一已 frozen 切片的验收基准被替换，而 §8.3 682/§6.5 558 只在版本 superseded 时级联，§6.3 530 只比对文件内 hash（文件已被重写）→ 冻结切片的验收范围在不被通知的情况下变化。跟进：golden_hash 变化时对引用同版本的未结束切片执行显式刷新/重冻或 BLOCKED（不升版的分支），或把断言按切片冻结。

## MINOR

- §6.3 检查 1"`current.yaml.version` 必须与 `baseline.yaml.status: active` 一致"是类型错配（version vs status），应为 current.yaml.version 与 baseline.yaml.version、current.yaml.status 与 baseline.yaml.status 分别一致。
- §10.1 的 packet"sha256 `5b19eb9bc0053d30f5b5af43e613c3bd1f8d14b7`"实际是 40 位 sha1（工作区文件 sha1 正好为该值；sha256 为 0afdc4f…），且 `skills/pro` 在 HEAD `6d702d5` 中未被跟踪（git status 为 untracked）——"HEAD + v0.2.7 + sha256"的固定方式不能按标注复现（已核对：HEAD=6d702d5、SKILL.md version=0.2.7、模板字段存在）。
- golden oracle 同时生成 oracle 对比与 `regression` 对比（§4.3 313-319、§7.4 628），两者对同一 golden 图使用各自 `threshold_ref`（§4.2 210 vs §4.9 428），优先级/冲突规则未定义。
- `computed_expectations.source: design-tokens`（§4.2 224、§7.3 594）的 token→computed 属性映射未定义。
- `geometry.expected_source: human`（§4.3 286）允许但无持久工件承载 Human 提供的期望 bbox（§4.3 325 只把 human 映射到 `computed_expectations`）。
- `TBD`（§5.2 484、§6.3 534）的 schema/校验语义未定义；harness=TBD 时 FREEZE 失败在 §6.3 538 落到 `needs-triage`，而 §8.2 652/§12.1 791 说该切片 `needs-decision`，状态归属不一致。
- §10.3 751"两者版本号在 docs/island/designer/ 的记录中绑定"，但 v4 与配套草案都没有可引用的版本号字段；§12.4 也未把该绑定列为待验证项。

## UNVERIFIED

- §10.1 的版本固定不可复现：packet hash 标注 sha256 实为 sha1；`skills/pro` 为未跟踪改动（HEAD 中不存在）；v4 自己也注明"工作区有未提交改动，接入前须重新核对"。
- §12.4（814-827）的验证项在本审查中无法执行：生成器确定性、must_import/diff_scope 推导、golden measurements 采集/重放、hash/env 校验、FREEZE 升版与跨地图级联、派发简报接受度。
- prefactor 的 harness（Storybook/预览路由/单测渲染）与 fixture 提供者在真实项目中的可用性未验证（§12.1 791-792）。
- design-export 的 `export {scale, origin}` 由 Human 在 FREEZE 确认（§7.2 586）的交互与工具支持未验证；截图像素声明 scale 的流程同样未验证（§7.3 598）。
- `capture_env` 重抓与升版的重批准流程在真实环境中的可执行性未验证（§7.4 630）。

## ESCALATE

- 配套 `2026-10-17-design-md-framework-draft.md` 已改为"与 v4 配套（联合批准）"（L4，已核对），但仍未批准且无版本号；v4 §10.3 751 的"两者版本号绑定"在 v4 获批时仍不可执行（配套文件不在本次审查范围）。
- sketch-copilot-pro 工作区 `skills/pro` 整体未跟踪、工作树有未提交改动（HEAD 6d702d5 中无该目录）；v4 的跨 skill 固定混合了 HEAD 与未跟踪内容，接口版本锁定需在提交后重做（外部文件，超出 v4 正文）。
- yes-subagents v0.7.0 的版本声明已核对为真；派发简报格式是否被 Coder Plus/Critic Gate 接受仍属 §10.2 739/§12.4 824 的实现验证（外部合同）。
- 空 `docs/DESIGN.md` 已按附录 845 移交 Human；目标仓库文档布局（根 DESIGN.md 与 docs/island）仍待 Human 决定。
- 历史指针已加（v1/v2/v3 与两篇背景；adapter-boundary 文首只有"术语以 v4 §2 为准"一条，无"已被取代"行），建议补齐以统一文档状态。

STATUS: FAIL
