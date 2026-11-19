# Snapshot

适用于 Human 主动要求固定当前现场、保留一次争议或反馈发生时的可复现环境。Snapshot 是**现场工作区捕获流程**，不是归档、压缩、质量审查或实现流程；它不绑定 Strict、Coding 或任何特定子代理。

```text
Human 明确触发
  ↓
确认复现目标与相关仓库
  ↓
每个仓库创建 isolated checkpoint commit
  ↓
询问 worktree 存储位置
  ├─ Human 提供外部路径
  └─ 默认 ~/.worktree/snapshots/<repo>/<snapshot-id>
  ↓
创建 snapshot/<snapshot-id> 分支与 worktree
  ↓
在 worktree 写报告、证据和环境资料
  ↓
提交 Snapshot 报告
  ↓
返回路径、commit SHA 和已知限制
```

## 1. 触发与责任

只在 Human 明确提出 `snapshot`、 “固定当前现场”或同等要求时启动。普通工作、Strict 审查、Coding 施工和发现问题本身不会自动触发 Snapshot。

Snapshot 由当前 Orchestrator 直接负责：

- 与 Human 确认未来要复现或判断的问题；
- 判断 primary repository、related repository 和外部证据范围；
- 使用只读命令收集事实；
- 创建不改变当前工作分支的 checkpoint commit；
- 创建并维护持久 worktree；
- 在 worktree 内写入并提交 `REPORT.md`、证据索引和环境资料。

不派遣子代理代替访谈或采集。Snapshot 不修复代码，不重跑原任务，不替 Human 判断问题成因。

## 2. 需求确认

触发后先确认以下内容，确认后直接进入采集，不再增加第二道范围审批：

1. 要固定的现象、争议或反馈是什么；
2. 未来希望回答或复现的具体问题是什么；
3. 哪个仓库是 primary，哪些仓库或文件是 related；
4. 是否存在原始 plan、prompt、派遣 payload、原始输出或其它一手材料；
5. worktree 使用内部默认位置还是 Human 提供的外部路径。

无法取得的历史材料标记为 `UNAVAILABLE`，不得用事后回忆伪写成一手证据。完整聊天 transcript 不默认收录；保存与事件直接相关的原始输入、payload、输出和必要上下文片段。

## 3. 采集边界

### 仓库

Snapshot 支持一个 primary repository 和零个或多个 related repositories。每个仓库分别记录：

- repository path、remote（移除 URL 中的凭据或 token）、branch；
- capture start/end time；
- 当前 `HEAD`、工作区 `status`、staged/unstaged diff；
- submodule 和 LFS 状态（可取得时）；
- 相关的未跟踪源文件或证据文件。

不扫描仓库父目录或整个 Projects 目录。Related repository 只在其 commit、契约文件或未提交状态会影响事件时纳入。

### 环境与证据

收集与事件相关的：

- 原始 plan、约束、背景、prompt、派遣 payload 和原始输出；
- 当时生效的 skill、workflow、agent 契约原文；
- 系统时间、时区、OS、架构、当前目录；
- Git、运行时和相关工具版本；
- 关键只读命令及原始输出；
- 明确的排除项、缺失项和它们对复现的影响。

默认不收集 `.env`、凭据、私钥、钥匙串、真实用户数据、依赖目录、缓存、构建产物、完整进程环境或无关 transcript。发现这些内容可能影响复现时，在报告中记录其存在和未收录原因。

## 4. Checkpoint commit

Checkpoint 可以包含未完成代码、未通过计划和进行中的文档；它只表示现场检查点，不表示功能完成、计划批准或测试通过。

不要在当前工作分支上执行 `git add -A && git commit`。使用本次 Snapshot 独立的临时 index 创建普通 Git commit，避免改变当前分支、当前 `.git/index` 和用户已有 staged 内容：

```bash
snapshot_id="<timestamp>-<slug>"
snapshot_tmp="$(mktemp -d)"
snapshot_index="$snapshot_tmp/index"

GIT_INDEX_FILE="$snapshot_index" git read-tree HEAD
GIT_INDEX_FILE="$snapshot_index" git add -u -- .
GIT_INDEX_FILE="$snapshot_index" git add -- <selected-untracked-path>...

snapshot_tree="$(GIT_INDEX_FILE="$snapshot_index" git write-tree)"
snapshot_parent="$(git rev-parse HEAD)"
snapshot_commit="$(git commit-tree "$snapshot_tree" \
  -p "$snapshot_parent" \
  -m "snapshot: $snapshot_id")"

git update-ref "refs/heads/snapshot/$snapshot_id" "$snapshot_commit"
```

实际执行时必须：

- 为每个 repository 使用独立的临时 index 和临时目录；
- 只显式加入与现场相关的 untracked 文件；
- 检查 `refs/heads/snapshot/<snapshot-id>` 尚不存在，禁止覆盖；
- 在完成或失败时清理临时 index；
- 记录 checkpoint SHA、父 SHA、采集窗口和加入/排除路径；
- 不 push、不删除历史、不修改当前工作分支。

如果仓库存在无法写入 tree 的冲突状态，或 Git 操作失败，不伪造 checkpoint。保留错误、status 和可取得的 patch，在工作流汇报中说明“无 checkpoint commit”；只有 worktree 建立成功后，才能把该限制写入 `REPORT.md`。

子代理或其它进程可以在 Snapshot 期间继续运行。Checkpoint 不是文件系统级原子快照；报告必须记录采集开始/结束时间、已知并行写入和可能的非原子限制。

## 5. Worktree 存储

Checkpoint 创建后询问存储位置：

- Human 提供外部路径：在该路径下创建 `<repo-name>/<snapshot-id>`；
- 未提供外部路径：使用 `~/.worktree/snapshots/<repo-name>/<snapshot-id>`。

目标路径必须不存在或为空。不得覆盖、清空或移动用户已有目录。多仓库使用同一个 `snapshot-id`，每个 repository 各自创建 `snapshot/<snapshot-id>` 分支和 worktree：

```bash
git worktree add \
  "<snapshot-worktree-path>" \
  "snapshot/<snapshot-id>"
```

Worktree 是 Snapshot 的主体，应持久保留供后续 Agent 进入、复现、修改和提交。内部空间和外部空间都写入报告；不创建 ZIP，不复制完整 Git object database。

如果仓库工作区包含大量 tracked 二进制资源，完整检出会产生相应磁盘开销。只有在 Human 接受该成本或指定 sparse checkout 时，才能改变默认的完整代码状态；ignored 的依赖、缓存和构建产物不因创建 worktree 自动复制。

## 6. Worktree 内容与报告

在每个 Snapshot worktree 中至少创建并提交：

```text
REPORT.md
evidence/
  INDEX.md
environment/
```

`REPORT.md` 固定包含：

1. Snapshot 目标和触发背景；
2. 当时观察到的现象；
3. 希望未来回答的问题；
4. repository、branch、checkpoint SHA、worktree 路径和采集窗口；
5. 关键事件时间线；
6. 原始证据和来源；
7. 环境与工具信息；
8. 排除项、`UNAVAILABLE` 项和影响；
9. 进入 worktree 后的回看或复现入口；
10. 非原子采集、并行写入和其它残余限制。

`evidence/INDEX.md` 对每份材料记录：worktree 路径、原始来源、收录理由、原始/事后性质和完整性。报告和证据提交在 Snapshot 分支上，不回写 primary 的当前分支。

## 7. 完成与交付

报告提交完成后，向 Human 返回：

- 每个 repository 的 checkpoint commit SHA；
- 每个 Snapshot branch 和 worktree 路径；
- 报告提交 SHA；
- 已收录和未收录的关键材料；
- 是否存在非原子采集、并行写入或不可复现依赖。

Snapshot 完成不代表问题已经解释、代码已经完成或计划已经通过。后续分析在 Snapshot worktree 中继续，并通过新的 commit 保留推理和验证轨迹。

不修改原始工作区、不提交当前业务分支、不 push 远程、不删除既有 worktree 或历史。`STATUS: DONE` 只表示 Snapshot worktree 和报告已建立；无法创建 checkpoint 或 worktree 时报告具体阻塞边界，不宣称已完成。
