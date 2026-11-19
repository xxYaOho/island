#!/bin/bash
# promote.sh — 向已有计划追加下一层骨架（只追加、不覆盖正文）
# 用法: promote.sh <plan.md> draft|implement
# draft     → 补决策常用节（若缺）+ Draft Plan；state → 草案
# implement → 追加 Implement Plan + Milestone-1 样板；state → 已对齐
# 幂等：目标层已存在则拒绝。
set -euo pipefail

plan="${1:-}"
layer="${2:-}"
if [ -z "$plan" ] || [ -z "$layer" ]; then
  echo "promote.sh: 用法: promote.sh <plan.md> draft|implement" >&2
  exit 64
fi
[ -f "$plan" ] || { echo "promote.sh: 文件不存在: $plan" >&2; exit 66; }

scripts="$(cd "$(dirname "$0")" && pwd)"

set_state() {
  local s="$1"
  if grep -qE '^state:' "$plan"; then
    # portable-ish in-place: rewrite via temp
    local tmp
    tmp="$(mktemp)"
    sed -E "s|^state:.*|state: ${s}|" "$plan" > "$tmp"
    mv "$tmp" "$plan"
  else
    echo "promote.sh: 警告：未找到 frontmatter state 字段，跳过状态更新" >&2
  fi
}

append_fragment() {
  local frag="$1"
  [ -f "$frag" ] || { echo "promote.sh: 层片段缺失: $frag" >&2; exit 66; }
  # ensure trailing newline before append
  if [ -s "$plan" ] && [ "$(tail -c 1 "$plan" | wc -l)" -eq 0 ]; then
    printf '\n' >> "$plan"
  fi
  cat "$frag" >> "$plan"
}

case "$layer" in
  draft)
    if grep -qE '^## Draft Plan[[:space:]]*$' "$plan"; then
      echo "promote.sh: 拒绝：已存在 ## Draft Plan，不重复追加: $plan" >&2
      exit 73
    fi
    # Append decision sections that are missing (by heading), then Draft Plan block from fragment.
    # Fragment includes User Stories … Out of Scope + Draft Plan; skip headings already present.
    frag="$scripts/layers/draft.md"
    [ -f "$frag" ] || { echo "promote.sh: 层片段缺失: $frag" >&2; exit 66; }
    tmp_out="$(mktemp)"
    awk -v planfile="$plan" '
      BEGIN {
        while ((getline line < planfile) > 0) {
          if (line ~ /^## /) {
            t=line; sub(/^##[ \t]+/, "", t); sub(/[ \t]+$/, "", t)
            have[t]=1
          }
        }
        close(planfile)
        skip=0
      }
      /^## / {
        t=$0; sub(/^##[ \t]+/, "", t); sub(/[ \t]+$/, "", t)
        if (t in have) { skip=1; next }
        skip=0
        print
        next
      }
      { if (!skip) print }
    ' "$frag" > "$tmp_out"
    if [ ! -s "$tmp_out" ]; then
      echo "promote.sh: 拒绝：决策节均已存在且无法追加 Draft（异常）: $plan" >&2
      rm -f "$tmp_out"
      exit 73
    fi
    if [ -s "$plan" ] && [ "$(tail -c 1 "$plan" | wc -l)" -eq 0 ]; then
      printf '\n' >> "$plan"
    fi
    cat "$tmp_out" >> "$plan"
    rm -f "$tmp_out"
    set_state "草案"
    echo "promote.sh: 已升层 draft → ${plan}（state: 草案）"
    ;;
  implement)
    if grep -qE '^## Implement Plan[[:space:]]*$' "$plan"; then
      echo "promote.sh: 拒绝：已存在 ## Implement Plan，不重复追加: $plan" >&2
      exit 73
    fi
    if ! grep -qE '^## Draft Plan[[:space:]]*$' "$plan"; then
      echo "promote.sh: 提示：尚无 ## Draft Plan（纯决策升实施时允许）。继续追加实施骨架。" >&2
    fi
    append_fragment "$scripts/layers/implement.md"
    set_state "已对齐"
    echo "promote.sh: 已升层 implement → ${plan}（state: 已对齐）"
    ;;
  *)
    echo "promote.sh: 未知层: ${layer}（仅支持 draft|implement）" >&2
    exit 64
    ;;
esac
