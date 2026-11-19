#!/usr/bin/env bash
# 将已知的 Simple Wiki SCHEMA 升级到 bundled 版本；raw 正文永远按原始字节拼回。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REF_SCHEMA="$SCRIPT_DIR/../reference/SCHEMA.md"
INTERMEDIATE_VERSION="v0.5.0"

usage() {
  printf '用法: %s <WIKI_ROOT>\n' "$(basename "$0")" >&2
  exit 1
}

fail() {
  printf 'ERROR=%s\n' "$1" >&2
  exit 1
}

[[ $# -eq 1 ]] || usage
[[ -d "$1" ]] || fail "WIKI_ROOT_NOT_FOUND"
WIKI_ROOT="$(cd "$1" && pwd -P)"
SCHEMA_FILE="$WIKI_ROOT/SCHEMA.md"
RAW_DIR="$WIKI_ROOT/raw"
[[ -f "$SCHEMA_FILE" && -d "$RAW_DIR" ]] || fail "WIKI_ROOT_INCOMPLETE"
[[ -f "$REF_SCHEMA" ]] || fail "BUNDLED_SCHEMA_MISSING"

TMP_FILES=()
new_tmp() {
  NEW_TMP="$(mktemp "${WIKI_ROOT}/.yes-swiki-migrate.XXXXXX")"
  TMP_FILES+=("$NEW_TMP")
}
cleanup() {
  local file
  for file in "${TMP_FILES[@]:-}"; do
    [[ -z "$file" ]] && continue
    if [[ -e "$file" ]]; then rm -f -- "$file"; fi
  done
  return 0
}
trap cleanup EXIT

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

schema_metadata_version() {
  awk '
    NR==1 { if ($0 != "---") exit; infm=1; next }
    infm && /^---[[:space:]]*$/ { exit }
    infm && /^metadata:[[:space:]]*$/ { metadata=1; next }
    infm && metadata && /^[[:space:]]+version:[[:space:]]*/ {
      value=$0; sub(/^[[:space:]]+version:[[:space:]]*/, "", value)
      sub(/[[:space:]]+#.*$/, "", value)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
      print value; exit
    }
    infm && /^[^[:space:]]/ { metadata=0 }
  ' "$1" 2>/dev/null || true
}

schema_has_metadata() {
  awk 'NR==1 { if ($0 != "---") exit; infm=1; next } infm && /^---[[:space:]]*$/ { exit } infm && /^metadata:[[:space:]]*$/ { found=1; exit } END { exit found ? 0 : 1 }' "$1" 2>/dev/null
}

TARGET_VERSION="$(schema_metadata_version "$REF_SCHEMA")"
[[ "$TARGET_VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "BUNDLED_SCHEMA_VERSION_INVALID"

version_compare() {
  local left="$1" right="$2"
  [[ "$left" =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+)$ ]] || return 2
  local l1="${BASH_REMATCH[1]}" l2="${BASH_REMATCH[2]}" l3="${BASH_REMATCH[3]}"
  [[ "$right" =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+)$ ]] || return 2
  local r1="${BASH_REMATCH[1]}" r2="${BASH_REMATCH[2]}" r3="${BASH_REMATCH[3]}"
  if (( l1 < r1 || (l1 == r1 && l2 < r2) || (l1 == r1 && l2 == r2 && l3 < r3) )); then return 1; fi
  if (( l1 > r1 || (l1 == r1 && l2 > r2) || (l1 == r1 && l2 == r2 && l3 > r3) )); then return 3; fi
  return 0
}

marker_line() {
  grep -n -x "$2" "$1" 2>/dev/null | cut -d: -f1
}

extract_managed_core() {
  awk '
    /^<!-- YES_SWIKI_MANAGED_CORE:START -->$/ { emit=1 }
    emit { print }
    /^<!-- YES_SWIKI_MANAGED_CORE:END -->$/ { exit }
  ' "$1"
}

managed_core_matches_bundle() {
  cmp -s <(extract_managed_core "$SCHEMA_FILE") <(extract_managed_core "$REF_SCHEMA")
}

schema_markers_valid() {
  local managed_start managed_end local_start local_end
  managed_start="$(marker_line "$1" '<!-- YES_SWIKI_MANAGED_CORE:START -->')"
  managed_end="$(marker_line "$1" '<!-- YES_SWIKI_MANAGED_CORE:END -->')"
  local_start="$(marker_line "$1" '<!-- YES_SWIKI_LOCAL_EXTENSIONS:START -->')"
  local_end="$(marker_line "$1" '<!-- YES_SWIKI_LOCAL_EXTENSIONS:END -->')"
  [[ "$managed_start" =~ ^[0-9]+$ && "$managed_end" =~ ^[0-9]+$ && "$local_start" =~ ^[0-9]+$ && "$local_end" =~ ^[0-9]+$ ]] || return 1
  (( managed_start < managed_end && managed_end < local_start && local_start < local_end ))
}

bundle_with_version() {
  local version="$1" output="$2"
  awk -v version="$version" '
    /^metadata:[[:space:]]*$/ { metadata=1; print; next }
    metadata && /^[[:space:]]+version:[[:space:]]*/ { print "  version: " version; metadata=0; next }
    { print }
  ' "$REF_SCHEMA" > "$output"
}

render_target_schema() {
  local version="$1" output="$2" extension="$3"
  local template start end
  new_tmp
  template="$NEW_TMP"
  bundle_with_version "$version" "$template"
  start="$(marker_line "$template" '<!-- YES_SWIKI_LOCAL_EXTENSIONS:START -->')"
  end="$(marker_line "$template" '<!-- YES_SWIKI_LOCAL_EXTENSIONS:END -->')"
  [[ "$start" =~ ^[0-9]+$ && "$end" =~ ^[0-9]+$ ]] || fail "BUNDLED_SCHEMA_MARKERS_INVALID"
  head -n "$start" "$template" > "$output"
  [[ -z "$extension" ]] || cat "$extension" >> "$output"
  tail -n "+$end" "$template" >> "$output"
}

extension_from_schema() {
  local output="$1" start end
  start="$(marker_line "$SCHEMA_FILE" '<!-- YES_SWIKI_LOCAL_EXTENSIONS:START -->')"
  end="$(marker_line "$SCHEMA_FILE" '<!-- YES_SWIKI_LOCAL_EXTENSIONS:END -->')"
  [[ "$start" =~ ^[0-9]+$ && "$end" =~ ^[0-9]+$ ]] || fail "SCHEMA_MARKERS_INVALID"
  if (( end > start + 1 )); then
    tail -n "+$((start + 1))" "$SCHEMA_FILE" | head -n "$((end - start - 1))" > "$output"
  else
    : > "$output"
  fi
}

LEGACY_ONE_CHECKSUM="2125389878 5674"
LEGACY_ONE_BYTES=5674
LEGACY_TWO_CHECKSUM="468826216 5030"
LEGACY_TWO_BYTES=5030

legacy_core_prefix() {
  local bytes checksum
  for bytes in "$LEGACY_ONE_BYTES" "$LEGACY_TWO_BYTES"; do
    (( $(wc -c < "$SCHEMA_FILE") >= bytes )) || continue
    checksum="$(head -c "$bytes" "$SCHEMA_FILE" | cksum | awk '{print $1 " " $2}')"
    if [[ "$bytes" == "$LEGACY_ONE_BYTES" && "$checksum" == "$LEGACY_ONE_CHECKSUM" ]]; then
      LEGACY_CORE_BYTES="$bytes"
      return 0
    fi
    if [[ "$bytes" == "$LEGACY_TWO_BYTES" && "$checksum" == "$LEGACY_TWO_CHECKSUM" ]]; then
      LEGACY_CORE_BYTES="$bytes"
      return 0
    fi
  done
  return 1
}

legacy_extension_from_schema() {
  local output="$1"
  tail -c "+$((LEGACY_CORE_BYTES + 1))" "$SCHEMA_FILE" > "$output"
}

SCHEMA_FROM=""
SCHEMA_MODE=""
EXTENSION_FILE=""
if ! schema_has_metadata "$SCHEMA_FILE"; then
  legacy_core_prefix || fail "SCHEMA_CORE_CONFLICT"
  new_tmp
  EXTENSION_FILE="$NEW_TMP"
  legacy_extension_from_schema "$EXTENSION_FILE"
  SCHEMA_FROM="legacy"
  SCHEMA_MODE="legacy"
elif ! SCHEMA_FROM="$(schema_metadata_version "$SCHEMA_FILE")" || [[ ! "$SCHEMA_FROM" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  fail "SCHEMA_VERSION_INVALID"
else
  if version_compare "$SCHEMA_FROM" "$TARGET_VERSION"; then
    SCHEMA_COMPARISON=0
  else
    SCHEMA_COMPARISON=$?
  fi
  [[ $SCHEMA_COMPARISON -ne 3 ]] || fail "SKILL_OUTDATED"
  if ! schema_markers_valid "$SCHEMA_FILE" || ! managed_core_matches_bundle; then
    fail "SCHEMA_CORE_CONFLICT"
  fi
  new_tmp
  EXTENSION_FILE="$NEW_TMP"
  extension_from_schema "$EXTENSION_FILE"
  if [[ $SCHEMA_COMPARISON -eq 0 ]]; then
    SCHEMA_MODE="current"
  else
    SCHEMA_MODE="partial"
  fi
fi

RAW_FILES=()
RAW_INTEGRATED=()
while IFS= read -r raw_file; do
  [[ -z "$raw_file" ]] && continue
  end="$(frontmatter_end "$raw_file")"
  [[ "$end" =~ ^[0-9]+$ ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  [[ "$(fm_count "$raw_file" class)" == "1" && "$(fm_count "$raw_file" ingested)" == "1" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  integrated_count="$(fm_count "$raw_file" integrated)"
  [[ "$integrated_count" == "0" || "$integrated_count" == "1" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  class="$(fm_value "$raw_file" class)"
  ingested="$(fm_value "$raw_file" ingested)"
  integrated="$(fm_value "$raw_file" integrated)"
  [[ "$class" == "material" || "$class" == "evidence" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  [[ "$ingested" == "true" || "$ingested" == "false" ]] || fail "RAW_FRONTMATTER_INVALID:$(basename "$raw_file")"
  expected="$ingested"
  if [[ "$integrated_count" == "1" && "$integrated" != "$expected" ]]; then
    fail "RAW_STATE_CONFLICT:$(basename "$raw_file")"
  fi
  if [[ "$integrated_count" == "0" ]]; then
    RAW_FILES+=("$raw_file")
    RAW_INTEGRATED+=("$expected")
  fi
done < <(find "$RAW_DIR" -maxdepth 1 -type f -name '*.md' -print | sort)

render_raw_with_integrated() {
  local source="$1" integrated="$2" end
  end="$(frontmatter_end "$source")"
  awk -v end="$end" -v integrated="$integrated" '
    NR <= end {
      print
      if ($0 ~ /^ingested:[[:space:]]*/) print "integrated: " integrated
    }
  ' "$source"
  tail -n "+$((end + 1))" "$source"
}

replace_file() {
  local source="$1" replacement="$2" dir base temp
  dir="$(cd "$(dirname "$source")" && pwd -P)"
  base="$(basename "$source")"
  temp="$(mktemp "$dir/.${base}.yes-swiki.XXXXXX")"
  TMP_FILES+=("$temp")
  cp "$replacement" "$temp"
  mv "$temp" "$source"
}

SCHEMA_UPDATED=false
if [[ "$SCHEMA_MODE" != "current" ]]; then
  new_tmp
  staged_schema="$NEW_TMP"
  render_target_schema "$INTERMEDIATE_VERSION" "$staged_schema" "$EXTENSION_FILE"
  replace_file "$SCHEMA_FILE" "$staged_schema"
  SCHEMA_UPDATED=true
fi

RAW_UPDATED=0
if (( ${#RAW_FILES[@]} > 0 )); then
  for index in "${!RAW_FILES[@]}"; do
    new_tmp
    staged_raw="$NEW_TMP"
    render_raw_with_integrated "${RAW_FILES[$index]}" "${RAW_INTEGRATED[$index]}" > "$staged_raw"
    replace_file "${RAW_FILES[$index]}" "$staged_raw"
    RAW_UPDATED=$((RAW_UPDATED + 1))
  done
fi

if [[ "$SCHEMA_MODE" != "current" ]]; then
  new_tmp
  staged_schema="$NEW_TMP"
  render_target_schema "$TARGET_VERSION" "$staged_schema" "$EXTENSION_FILE"
  replace_file "$SCHEMA_FILE" "$staged_schema"
fi

printf 'WIKI_ROOT=%s\n' "$WIKI_ROOT"
printf 'SCHEMA_FROM=%s\n' "$SCHEMA_FROM"
printf 'SCHEMA_TO=%s\n' "$TARGET_VERSION"
printf 'SCHEMA_UPDATED=%s\n' "$SCHEMA_UPDATED"
printf 'RAW_UPDATED=%s\n' "$RAW_UPDATED"
printf 'STATUS=OK\n'
