#!/bin/bash
# create.sh — 生成记录层计划骨架：docs/island/plans/YYYY-MM-DD-<slug>.md
# 用法: create.sh <slug>
# 幂等语义：文件已存在则拒绝并说明原因，绝不覆盖——计划是创作起点。
# 模板真源：skill/scripts/SPEC_TEMPLATE.md（仅记录层；升层用 promote.sh）。
set -euo pipefail

slug="${1:-}"
if [ -z "$slug" ]; then
  echo "create.sh: 用法: create.sh <slug>" >&2
  exit 64
fi
case "$slug" in
  *[/*\ ]*|"."|".." )
    echo "create.sh: slug 不合法（禁止路径分隔符、空格与保留名）: $slug" >&2
    exit 64
    ;;
esac

tpl="$(cd "$(dirname "$0")" && pwd)/SPEC_TEMPLATE.md"
[ -f "$tpl" ] || { echo "create.sh: 模板缺失: $tpl" >&2; exit 66; }

if root="$(git rev-parse --show-toplevel 2>/dev/null)"; then :; else root="$(pwd)"; fi
dir="$root/docs/island/plans"
path="$dir/$(date +%F)-$slug.md"

if [ -e "$path" ]; then
  echo "create.sh: 拒绝创建：文件已存在: $path" >&2
  echo "create.sh: 计划是创作起点，已存在内容不可覆盖；如需重建，请先自行移走该文件。" >&2
  exit 73
fi

mkdir -p "$dir"
sed -e "s|^# <Feature> Plan|# ${slug} Plan|" \
    -e "s|^date: YYYY-MM-DD|date: $(date +%F)|" \
    "$tpl" > "$path"

echo "create.sh: 已创建（记录层）: $path"
echo "create.sh: 升层请用: scripts/promote.sh <plan.md> draft|implement"
