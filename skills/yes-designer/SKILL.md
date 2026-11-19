---
name: yes-designer
description: 在已有前端代码基础上落地 UI 页面：识别参考页面、建立实现基线、先复制再改 delta，并用结构与样式门禁验证。Use when the user asks to 参考/复制/沿用已有页面新增或修改页面、按原型或截图实现列表/表单页、或要求检查页面是否复用了既有结构。
metadata:
  version: 0.1.4
---

# Yes! Designer（MVP）

把设计输入落到既有代码结构上。默认继承；没有证据的独立重写必须由 Human 批准。

## 硬规则

1. 先读参考页面和工程约定，再动代码；不凭截图从零写结构。
2. relation 默认 `inherit`；`independent` 或新建结构必须 Human 明确批准。
3. 先 `designer copy` 生成 copy commit，再只改 `delta_files`。
4. `designer verify` 通过前不得交付；失败按区域报告修。
5. Human 决策必须写入 `approvals.tsv`，不靠对话记忆。
6. 原型与参考页的差异必须逐条登记为 `prototype_diff`；原型自身矛盾（如两个计数不一致）必须提问，不得自行取值。
7. `delta` 只取最小区域；外框保留、局部修改用嵌套 `data-region` 子区域表达。
8. **Host ASK**：实施前（改 delta / `copy` / 写业务代码）必须经 **Host ASK**——即宿主提供的「向 Human 提问并等待明确答复」能力——拿到明确答复。沉默、漏答、超时自动继续、含糊附和、「先继续看看」但未答该问 ≠ 同意；未决保持阻塞，不得进入 BUILD。
9. 用户曾要求「先确认再实施」时，至少完成一次**设计确认**类 Host ASK（明确允许开始做）后才能 BUILD。
10. ENTRY / BASELINE 产出的 Human 问题一律先走 Host ASK；存在未决问项时不得 `copy`、不得开始实施。ANSWER 只能来自 Human。

## 目标项目工件

- `docs/island/designer/config.yaml`：预览启动命令（`preview.command`）、viewport、DPR；不含预览地址
- `docs/island/designer/approvals.tsv`：Human 审批记录（baseline blob + HEAD）
- `docs/island/designer/baselines/<id>.yaml`：实现基线
- `docs/island/designer/rules.yaml`：可机械检查的规则（可空）
- `.tmp/island/designer/rounds/`：每轮快照与报告（可再生）

## ENTRY

1. 项目没有 `docs/island/designer/`：运行 `designer init`。
2. 识别任务：
   - 用户说“参考 / 复制 / 沿用 X 页面” → 找 X 的路由、页面文件与组件，作为 `source_page`；
   - 目标路由已存在（空白页、待实现页）→ 直接作为 `target`；
   - 目标路由不存在 → 在 `source_page` 同级模块 / 分组下新建路由与导航；
   - 原型、截图只用于 `delta` 区域和数据，不得据此重写 skeleton。
3. 产出「原型差异清单」，逐条记录：新增元素（原型有、参考页无）、缺失元素、内部矛盾、计数/文案语义。每条都必须能落到 baseline 的 `prototype_diff`。
4. 输出 baseline 草案，以及需要 Human 决定的问题（relation、目标路由、delta 范围、差异清单中的未决项）。这些问题须经 **Host ASK** 取得明确答复后再进入实施；不得把未回复当作默许。

## BASELINE

写 `baselines/<id>.yaml`：

- `id`、`relation`、`source_page`（route / files / commit）、`target`（route / files）
- `copy`：源文件到目标文件的显式映射
- `delta_files`：允许改动的文件白名单（必须包含 target 文件）。每份 baseline 只列本页面文件与明确共享文件（路由、导航、mock 等），不得包含其他 baseline 的页面文件。
- `states`：状态 id 与 `ready` 选择器
- `regions`：`data-region` id 与 role（`preserve` / `delta`）
- `prototype_diff`：原型与参考页的逐条差异，`{ id, kind: structural-add | structural-remove | contradiction | semantics, detail, region?, signature?, status: decided | open, decision }`。`structural-add` 必须写 `region` 与该区域直接子元素的签名（如 `header.meeting-personnel-records__frame-header`；嵌套区域写 `region:<id>`）；存在 `open` 项时不得 approve。

参考页缺少 `data-region` 时，先在参考页和目标页补标注（只加属性）。把 baseline 交给 Human，经 Host ASK 确认设计/范围后运行：

```
node <skill>/scripts/designer.mjs approve --baseline docs/island/designer/baselines/<id>.yaml --note "<Human 原话>"
```

## BUILD

前置：相关 Host ASK 均已获明确答复；用户要求「先确认」时须已完成设计确认 ASK。

1. `designer copy --baseline <path>`：先确认 baseline 已批准且 blob 未变，再从 `source_page.commit` 读取源文件复制到目标文件，生成 copy commit。
2. 只改 `delta_files` 内的文件；结构、样式和数据都在此范围内完成。
3. 目标页面必须保留复制来的 `data-region`；新增区域补 `data-region`。

## VERIFY

在当前工作目录用 `config.yaml` 的 `preview.command` 后台启动预览服务，从输出中读取实际地址，再执行：

```
node <skill>/scripts/designer.mjs verify --baseline <path> --url <实际地址>
```

- 预览服务由 lead 启动，也由 lead 关闭；skill 不启动服务，`--url` 没有默认值，不传直接报错。
- **必须使用本次从当前工作目录启动的服务**。端口被占用时开发服务器会自动换端口而不报错；连接既有端口上的服务，可能连到另一个项目或同一项目的另一个 worktree，导致验证错对象。report 记录 `url` 与 `cwd` 供 Human 抽查。

- **S1 文件范围**：自批准 HEAD 起，改动文件都在 `delta_files`。
- **S2 区域存在**：每个 state 的 `ready` 与全部 region 都可达。
- **S3 骨架一致**：每个 `preserve` 区域的 skeleton 与参考页同状态一致。遇到带 `data-region` 的子节点只输出 `{region}` 占位、不展开；遇到库组件根节点（当前有限清单：`ant-pagination`）只比较根节点 tag/class，不递归内部。新增清单项必须写回 v6 §15。
- **S4 样式探针**：每个 `preserve` 区域根节点的固定属性与参考页一致。
- **S5 规则**：`rules.yaml` 对 delta 文件的检查（可空）。
- **S6 原型差异声明**：`delta` 区域里新增的直接子结构必须在 `prototype_diff` 中声明，否则 fail。

失败时报告会定位到具体区域；修完重跑。通过后交 Human 看页面。

## 决策权

- baseline 的创建与修改、config / rules 变更：Human；
- `independent`、新建结构、共享组件扩展：Human；
- DEVIATION：任何人可提出，Human 决定；
- Host ASK 的回答（ANSWER）：只能 Human；agent 不得代答或把沉默当作同意。

## 环境

- Node ≥ 22
- 首次运行 `designer init` 会检查 skill 依赖（yaml、playwright），缺失时自动执行 `npm ci`（无 lock 时 `npm install`）；已存在则跳过。也可以手动在 skill 目录执行 `npm install`。
- Chromium 仍需首次执行 `npx playwright install chromium`；verify 需要可用的 Chromium，若浏览器缓存目录不可写，把 `PLAYWRIGHT_BROWSERS_PATH` 指到可写目录。

## 命令

在目标项目根目录执行：

```
node <skill>/scripts/designer.mjs init
node <skill>/scripts/designer.mjs approve --baseline <path> [--note <text>]
node <skill>/scripts/designer.mjs copy --baseline <path> [--force]
node <skill>/scripts/designer.mjs verify --baseline <path> --url <url> [--headed]
node <skill>/scripts/designer.mjs status
```

## 附录：Host ASK 举例（非绑定）

正文只要求使用宿主的「提问并等待明确答复」能力；下表仅为各宿主常见通道举例，**不是**强制 API 名。

| 宿主 | 常见 Host ASK 通道（举例） |
| --- | --- |
| Claude Code | `AskUserQuestion`；方案级确认可优先 `ExitPlanMode` |
| Codex | 各自的 question / confirm / permission 通道 |
| Kimi Code | 等价的提问或确认交互 |
| DeepSeek harness | 等价的 question / confirm / permission 通道 |
| Cursor / Grok 等 | 宿主提供的提问 widget 或明确结构化确认 |

超时自动继续、AFK 跳过、仅勾选未提交等，一律视为**未答复**，保持阻塞。
