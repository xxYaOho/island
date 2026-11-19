#!/usr/bin/env bash
# 对明确 raw 批次提交 integrated=true；不创建字段，不扫描全馆。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  printf '用法: %s <raw/file.md...> | --manifest <newline-delimited-file>\n' "$(basename "$0")" >&2
  exit 1
}

fail() {
  printf 'ERROR=%s\n' "$1" >&2
  exit 1
}

resolve_root() {
  local root="${WIKI_ROOT:-}"
  if [[ -z "$root" ]]; then root="$PWD/docs/simple-wiki"; fi
  if [[ "$root" != /* ]]; then root="$PWD/$root"; fi
  [[ -d "$root" ]] || fail "WIKI_ROOT_NOT_FOUND"
  cd "$root" && pwd -P
}

WIKI_ROOT="$(resolve_root)"
RAW_DIR="$WIKI_ROOT/raw"
[[ -d "$RAW_DIR" ]] || fail "WIKI_ROOT_INCOMPLETE"
RAW_DIR_PHYSICAL="$(cd "$RAW_DIR" && pwd -P)"

INPUTS=()
if [[ "${1:-}" == "--manifest" ]]; then
  [[ $# -eq 2 && -f "$2" ]] || usage
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" ]] && continue
    INPUTS+=("$line")
  done < "$2"
else
  [[ $# -gt 0 ]] || usage
  INPUTS=("$@")
fi
[[ ${#INPUTS[@]} -gt 0 ]] || fail "EMPTY_BATCH"

frontmatter_end() {
  awk 'NR==1 { if ($0 != "---") exit 1; next } /^---[[:space:]]*$/ { print NR; exit }' "$1" 2>/dev/null
}

fm_value() {
  awk -v key="$2" '
    NR==1 { if ($0 != "---") exit; infm=1; next }
    infm && /^---[[:space:]]*$/ { exit }
    infm && /^[[:space:]]/ { next }
    infm && index($0, ":") > 0 {
      pos=index($0, ":")
      if (substr($0, 1, pos-1) == key) {
        value=substr($0, pos+1)
        sub(/[[:space:]]+#.*$/, "", value)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
        print value
        exit
      }
    }
  ' "$1" 2>/dev/null || true
}

fm_count() {
  awk -v key="$2" '
    NR==1 { if ($0 != "---") exit; infm=1; next }
    infm && /^---[[:space:]]*$/ { print count+0; exit }
    infm && /^[[:space:]]/ { next }
    infm && index($0, ":") > 0 && substr($0, 1, index($0, ":")-1) == key { count++ }
    END { if (!infm) print 0 }
  ' "$1" 2>/dev/null || true
}

resolve_raw() {
  local input="$1" candidate dir base
  if [[ "$input" == /* ]]; then candidate="$input"; else candidate="$WIKI_ROOT/$input"; fi
  [[ -f "$candidate" && ! -L "$candidate" ]] || return 1
  dir="$(cd "$(dirname "$candidate")" && pwd -P)"
  base="$(basename "$candidate")"
  [[ "$dir" == "$RAW_DIR_PHYSICAL" && "$base" == *.md ]] || return 1
  printf '%s/%s' "$dir" "$base"
}

RAW_FILES=()
RAW_FILE_COUNT=0
for input in "${INPUTS[@]:-}"; do
  [[ -z "$input" ]] && continue
  raw_file="$(resolve_raw "$input")" || fail "RAW_PATH_OUT_OF_SCOPE:$input"
  duplicate=false
  for seen in "${RAW_FILES[@]:-}"; do
    [[ -z "$seen" ]] && continue
    if [[ "$seen" == "$raw_file" ]]; then duplicate=true; break; fi
  done
  if [[ "$duplicate" == false ]]; then
    RAW_FILES+=("$raw_file")
    RAW_FILE_COUNT=$((RAW_FILE_COUNT + 1))
  fi
done
[[ $RAW_FILE_COUNT -gt 0 ]] || fail "EMPTY_BATCH"

TO_MARK=()
ALREADY=0
for raw_file in "${RAW_FILES[@]:-}"; do
  [[ -z "$raw_file" ]] && continue
  end="$(frontmatter_end "$raw_file")"
  [[ "$end" =~ ^[0-9]+$ ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  [[ "$(fm_count "$raw_file" class)" == "1" && "$(fm_count "$raw_file" ingested)" == "1" && "$(fm_count "$raw_file" integrated)" == "1" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  class="$(fm_value "$raw_file" class)"
  ingested="$(fm_value "$raw_file" ingested)"
  integrated="$(fm_value "$raw_file" integrated)"
  [[ "$class" == "material" || "$class" == "evidence" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  [[ "$ingested" == "true" || "$ingested" == "false" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  [[ "$integrated" == "true" || "$integrated" == "false" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  if [[ "$ingested" == "false" && "$integrated" == "true" ]]; then fail "RAW_STATE_INVALID:$(basename "$raw_file")"; fi
  if [[ "$ingested" == "false" ]]; then fail "RAW_NOT_INGESTED:$(basename "$raw_file")"; fi
  if [[ "$integrated" == "true" ]]; then
    ALREADY=$((ALREADY + 1))
  else
    TO_MARK+=("$raw_file")
  fi
done

render_integrated() {
  local source="$1" end
  end="$(frontmatter_end "$source")"
  awk -v end="$end" '
    NR <= end {
      if ($0 ~ /^integrated:[[:space:]]*/) { print "integrated: true" } else { print }
    }
  ' "$source"
  tail -n "+$((end + 1))" "$source"
}

MARKED=0
if [[ "${TO_MARK[0]:-}" != "" ]]; then
  for raw_file in "${TO_MARK[@]:-}"; do
    [[ -z "$raw_file" ]] && continue
    raw_dir="$(cd "$(dirname "$raw_file")" && pwd -P)"
    raw_base="$(basename "$raw_file")"
    temp="$(mktemp "$raw_dir/.${raw_base}.yes-swiki.XXXXXX")"
    if ! render_integrated "$raw_file" > "$temp"; then
      rm -f -- "$temp"
      fail "RAW_WRITE_FAILED:${raw_base}"
    fi
    mv "$temp" "$raw_file"
    MARKED=$((MARKED + 1))
  done
fi

printf 'WIKI_ROOT=%s\n' "$WIKI_ROOT"
printf 'MARKED=%s\n' "$MARKED"
printf 'ALREADY_INTEGRATED=%s\n' "$ALREADY"
printf 'STATUS=OK\n'
