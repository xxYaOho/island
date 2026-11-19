---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/superpowers/plans/2026-09-16-strict-review-intensity.md
---
# Strict Review Intensity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement risk-scaled Strict review intensity while keeping FATAL semantics stable and closing non-blocking MAJOR findings explicitly.

**Architecture:** `critic-strict.md` owns the reviewer input, intensity boundaries, and severity contract. `SKILL.md` owns Orchestrator intensity selection and the MAJOR ledger rule. `workflow/coding.md` consumes the ledger at stage boundaries and prevents open MAJOR items from disappearing at final delivery. The evaluation package is outside this implementation.

**Tech Stack:** Markdown skill contracts, shell-based `rg` and `git diff --check` verification.

---

### Task 1: Update the Strict reviewer contract

**Files:**
- Modify: `skill/subagents/critic-strict.md`

- [ ] **Step 1: Add the optional intensity input and default**

Extend PRECONDITION with `intensity: low | high | max`. Missing intensity resolves to `high`; invalid values return `STATUS: BLOCKED` with WHAT/WHO. Keep the existing round, goal, and FULL/DELTA payload requirements unchanged.

- [ ] **Step 2: Define the three review scopes**

Add concise operating rules for `low`, `high`, and `max`. Make clear that intensity changes active exploration depth, not model identity, effort, finding count, or severity definitions.

- [ ] **Step 3: Replace the severity gate**

Replace automatic evidence-mismatch FATAL language with the three-part FATAL test: material downstream failure, concrete affected decision/deliverable scenario, and no safe deferral or later Gate repair. Define non-blocking factual/document errors as MAJOR or MINOR according to impact.

- [ ] **Step 4: Define the MAJOR output and PASS rule**

Require each MAJOR to state impact and required follow-up. Keep `PASS` when only MAJOR/MINOR remain, and state that the Orchestrator must materialize an explicit closure ledger.

- [ ] **Step 5: Verify the reviewer contract text**

Run:

```bash
rg -n "intensity|FATAL|MAJOR|evidence|STATUS: PASS|STATUS: FAIL" skill/subagents/critic-strict.md
```

Expected: all new intensity and severity rules are present, the old automatic evidence-mismatch FATAL rule is absent, and STATUS remains the final line.

### Task 2: Update Orchestrator selection and MAJOR ledger rules

**Files:**
- Modify: `skill/SKILL.md`

- [ ] **Step 1: Add intensity precedence**

Document `Human explicit > Orchestrator risk selection > default high`, with low-risk and high-risk signals and high as the fallback for mixed or unknown signals.

- [ ] **Step 2: Add ledger obligations after Strict PASS**

Require the Orchestrator to record every MAJOR with issue, impact, owner, closure point, and status. Require closure before direct consumption or final delivery, with `RESOLVED` and Human-approved `ACCEPTED` as the only terminal states.

- [ ] **Step 3: Verify no evaluation package changes are implied**

Run:

```bash
rg -n "intensity|MAJOR|RESOLVED|ACCEPTED|evals.json" skill/SKILL.md
```

Expected: intensity and ledger rules are present; no evals package is referenced.

### Task 3: Make the coding workflow consume the ledger

**Files:**
- Modify: `skill/workflow/coding.md`

- [ ] **Step 1: Define the施工 handoff for MAJOR items**

Clarify that the approved plan handoff includes the MAJOR ledger, that items consumed by the next node must close before consumption, and that non-consumed items may remain open during construction only until final delivery.

- [ ] **Step 2: Define final delivery closure**

Require every MAJOR to be `RESOLVED` or `ACCEPTED` before delivery; an open item that becomes blocking must be reclassified as FATAL and return to Strict lifecycle handling.

- [ ] **Step 3: Verify cross-file contract consistency**

Run:

```bash
rg -n "MAJOR|RESOLVED|ACCEPTED|critic-strict|STATUS: PASS" skill/SKILL.md skill/workflow/coding.md skill/subagents/critic-strict.md
git diff --check
```

Expected: all three files use the same severity and closure vocabulary, and `git diff --check` passes.

### Task 4: Review and commit the implementation

**Files:**
- Verify only: `skill/subagents/critic-strict.md`, `skill/SKILL.md`, `skill/workflow/coding.md`

- [ ] **Step 1: Check the final diff**

Run:

```bash
git diff --stat
git diff -- skill/subagents/critic-strict.md skill/SKILL.md skill/workflow/coding.md
```

Expected: no changes to `skill/evals/evals.json` and no unrelated file changes.

- [ ] **Step 2: Commit the implementation**

```bash
git add skill/subagents/critic-strict.md skill/SKILL.md skill/workflow/coding.md
git commit -m "feat(strict): scale review intensity and severity"
```
