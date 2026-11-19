#!/bin/bash
# split.sh — 将计划真源物化为切片
# 用法: split.sh <plan.md>   →   .tmp/plans-<name>/
# 识别规则（脚本适配文档，skill/scripts/SPEC_TEMPLATE.md 为形态约定）：
#   决策层 = 固定英文节名集合 → Decision.md
#   ## Draft Plan    → Draft.md（设计形状层：结构、契约、文件结构、风险）
#   ## Implement Plan → Implement.md（定稿总览；其余执行层概览节亦归入）
#   ## Milestone-<n>           → Milestone-<n>.md（含其下全部 Task-）
# 更新语义：全量覆盖；已消失节的旧片自动移除；无变更报告。
set -euo pipefail

plan="${1:?用法: split.sh <plan.md>}"
[ -f "$plan" ] || { echo "split.sh: 文件不存在: $plan" >&2; exit 1; }

base="$(basename "$plan")"; base="${base%.md}"
# 切片落位绑定计划文件所在仓库的根（worktree 感知），不绑定 cwd——产物与计划不分离
plan_dir="$(cd "$(dirname "$plan")" && pwd)"
if root="$(git -C "$plan_dir" rev-parse --show-toplevel 2>/dev/null)"; then :; else root="$plan_dir"; fi
out="$root/.tmp/plans-$base"
mkdir -p "$out"

manifest="$(awk -v OUT="$out" '
BEGIN{
  split("Problem Statement|Solution|User Stories|Constraints|Implementation Decisions|Testing Decisions|Out of Scope|Further Notes", D, "|")
  for(i in D) DECSET[D[i]]=1
  fence=0; layer=0; kind=""; buf=""; hdr=""; mnum=""
}
function flush(   n){
  if(kind=="dec") DEC=DEC buf
  else if(kind=="draft") DRFT=DRFT buf
  else if(kind=="ms"){ MS[mnum]=MS[mnum] buf; seen[mnum]=1 }
  else if(kind=="imp") IMP=IMP buf
  kind=""; buf=""
}
/^```/{ fence=!fence; buf=buf $0 ORS; next }
!fence && /^## /{
  t=$0; sub(/^##[ \t]+/,"",t); sub(/[ \t]+$/,"",t)
  if(layer==0 && (t in DECSET)){
    if(kind=="dec"){ flush() } else { hdr=buf }
    kind="dec"
  } else {
    if(kind=="dec"){ flush() }
    else if(layer==0){ hdr=buf }
    else { flush() }
    layer=1
    if(t=="Draft Plan") kind="draft"
    else if(t ~ /^Milestone-[0-9]+$/){ kind="ms"; mnum=t; sub(/^Milestone-/,"",mnum) }
    else kind="imp"
  }
  buf=$0 ORS
  next
}
{ buf=buf $0 ORS }
END{
  flush()
  printf "%s%s", hdr, DEC > (OUT "/Decision.md")
  print "Decision.md"
  if(length(DRFT) > 0){
    printf "%s", DRFT > (OUT "/Draft.md")
    print "Draft.md"
  }
  if(length(IMP) > 0){
    printf "%s", IMP > (OUT "/Implement.md")
    print "Implement.md"
  }
  for(n in seen){ printf "%s", MS[n] > (OUT "/Milestone-" n ".md"); print "Milestone-" n ".md" }
}' "$plan")"

# 移除已消失节的旧片（仅限本目录的 .md）
for f in "$out"/*.md; do
  [ -e "$f" ] || continue
  name="$(basename "$f")"
  if ! printf '%s\n' "$manifest" | grep -qx "$name"; then
    rm -f "$f"
  fi
done
