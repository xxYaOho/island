---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/superpowers/plans/2026-09-18-snapshot-workflow.md
---
# Snapshot Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Human-triggered Snapshot workflow that freezes one or more repository states into persistent worktrees with contextual reports, without creating ZIP archives.

**Architecture:** The workflow owns the Human interview, evidence scope, checkpoint semantics, and report contract. It creates an isolated Git checkpoint commit from the current working tree, anchors it with a `snapshot/<id>` branch, creates a persistent worktree at an internal or Human-provided path, and commits the report there. The current branch and index remain unchanged.

**Tech Stack:** Markdown workflow contract and Git plumbing commands; no new evaluation package or archive script.

---

### Task 1: Add the Snapshot workflow contract

**Files:**
- Create: `skill/workflow/snapshot.md`

- [ ] **Step 1: Define trigger and responsibility**

State that Snapshot runs only after explicit Human request, communicates directly with Human, and is not tied to Strict, Coding, or a particular child-agent role.

- [ ] **Step 2: Define the capture protocol**

Specify the requirement interview, primary/related repository discovery, capture window, parallel-writer disclosure, and isolated checkpoint commit using a temporary index. Define that checkpoint commits may contain incomplete code or unapproved plans and do not imply completion.

- [ ] **Step 3: Define worktree placement and lifecycle**

After checkpoint creation, ask whether to use an external path or the default `~/.worktree/snapshots/<repo>/<snapshot-id>`. Validate that the target is absent or empty, never overwrite it, create a `snapshot/<id>` branch per repository, and keep the worktree persistent for later reproduction.

- [ ] **Step 4: Define report and evidence contents**

Require `REPORT.md`, `evidence/INDEX.md`, and `environment/` in the worktree. Capture exact prompts, payloads, raw outputs, relevant plans/contracts, Git state, runtime/tool versions, and exclusions. Mark unavailable historical evidence as `UNAVAILABLE`; never reconstruct it as first-hand evidence.

- [ ] **Step 5: Define completion and failure behavior**

Commit the report on the snapshot branch, return worktree paths and checkpoint SHAs, and leave primary work untouched. On conflict, index contention, invalid path, or failed checkpoint, preserve the error evidence and report the exact recovery boundary without claiming a complete snapshot.

### Task 2: Register the workflow

**Files:**
- Modify: `skill/SKILL.md`

- [ ] **Step 1: Add the Snapshot trigger to the workflow description**

Document explicit Human phrases such as `snapshot` or “固定当前现场” as the trigger, while preserving the rule that ordinary work does not automatically dispatch it.

- [ ] **Step 2: Add Snapshot to the workflow routing list**

List `workflow/snapshot.md` alongside Coding and Entropy Reducer, and state that it is an evidence/worktree capture workflow rather than an implementation workflow.

### Task 3: Verify the contracts

**Files:**
- Verify: `skill/workflow/snapshot.md`, `skill/SKILL.md`

- [ ] **Step 1: Run structural checks**

```bash
rg -n "Snapshot|snapshot|worktree|temporary index|GIT_INDEX_FILE|REPORT.md|UNAVAILABLE" skill/SKILL.md skill/workflow/snapshot.md
git diff --check
```

Expected: all required lifecycle and safety terms appear, and no whitespace errors are reported.

- [ ] **Step 2: Review scope**

```bash
git diff --stat -- skill/SKILL.md skill/workflow/snapshot.md skill/evals/evals.json
```

Expected: only `SKILL.md` and the new workflow are changed; `evals.json` is untouched.

- [ ] **Step 3: Commit**

```bash
git add skill/SKILL.md skill/workflow/snapshot.md docs/superpowers/plans/2026-09-18-snapshot-workflow.md
git commit -m "feat(workflow): add snapshot worktree capture"
```
