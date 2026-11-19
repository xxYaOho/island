#!/usr/bin/env node
// yes-designer MVP CLI: init / approve / copy / verify / status
import { execFileSync } from 'node:child_process'
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const DESIGNER_DIR = 'docs/island/designer'
const TMP_DIR = '.tmp/island/designer'
const APPROVALS = join(DESIGNER_DIR, 'approvals.tsv')
const CONFIG = join(DESIGNER_DIR, 'config.yaml')
const RULES = join(DESIGNER_DIR, 'rules.yaml')

const STOP_CLASSES = ['ant-pagination']
const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const skillRequire = createRequire(import.meta.url)
let yamlModule

function yamlLib() {
  if (yamlModule) return yamlModule
  try {
    yamlModule = skillRequire('yaml')
    return yamlModule
  } catch {
    fail('缺少 yaml 依赖：在 skill 目录执行 npm install，或运行 designer init 自动安装')
  }
}

function hasDependency(name) {
  try {
    skillRequire.resolve(name)
    return true
  } catch {
    return false
  }
}

function ensureSkillDeps(args) {
  if (args['skip-install']) return
  const missing = ['yaml', 'playwright'].filter(name => !hasDependency(name))
  if (missing.length === 0) return
  log(`! skill 依赖缺失：${missing.join(', ')}，开始安装...`)
  const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'
  const lockPath = join(SKILL_ROOT, 'package-lock.json')
  const cacheDir = join(SKILL_ROOT, '.cache-npm')
  const env = { ...process.env, npm_config_cache: process.env.npm_config_cache ?? cacheDir }
  const installArgs = existsSync(lockPath)
    ? ['ci', '--no-audit', '--no-fund']
    : ['install', '--no-audit', '--no-fund']
  try {
    execFileSync(npm, installArgs, { cwd: SKILL_ROOT, stdio: 'inherit', env })
  } catch {
    fail(`安装 skill 依赖失败。请在 ${SKILL_ROOT} 手动执行 npm install；若缓存不可写，设置 npm_config_cache。`)
  }
  const stillMissing = ['yaml', 'playwright'].filter(name => !hasDependency(name))
  if (stillMissing.length) fail(`安装后仍缺少依赖：${stillMissing.join(', ')}`)
  log('✓ skill 依赖已安装')
}

const STYLE_PROPS = [
  'display', 'position', 'min-width', 'max-width',
  'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
  'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
  'row-gap', 'column-gap',
  'font-size', 'line-height', 'color', 'background-color',
  'border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
  'border-top-style', 'border-top-color',
]

function log(msg) { console.log(msg) }
function fail(msg) { console.error(`✗ ${msg}`); process.exit(1) }

function git(args, opts = {}) {
  try {
    return execFileSync('git', args, { cwd: process.cwd(), encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim()
  } catch (error) {
    if (opts.allowFail) return null
    const stderr = error.stderr?.toString() || error.message
    throw new Error(`git ${args.join(' ')} 失败: ${stderr}`)
  }
}

function parseArgs(argv) {
  const out = { _: [] }
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg.startsWith('--')) {
      const key = arg.slice(2)
      const next = argv[i + 1]
      if (next !== undefined && !next.startsWith('--')) {
        out[key] = next
        i += 1
      } else {
        out[key] = true
      }
    } else {
      out._.push(arg)
    }
  }
  return out
}

function readYaml(path) {
  return yamlLib().parse(readFileSync(path, 'utf8'))
}

function writeYaml(path, data) {
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, yamlLib().stringify(data), 'utf8')
}

// 只识别启动命令，不记地址：端口可能被占用而自动更换，写死地址会导致 verify 连错对象。
// 识别不出或有多个候选时留空，由 lead 与 Human 确认后填写。
function detectPreviewCommand() {
  const candidates = []
  if (existsSync('mise.toml')) {
    const text = readFileSync('mise.toml', 'utf8')
    if (/^\s*\[tasks\.dev\]/m.test(text) || /^\s*dev\s*=/m.test(text)) candidates.push('mise run dev')
  }
  if (existsSync('package.json')) {
    try {
      const pkg = JSON.parse(readFileSync('package.json', 'utf8'))
      if (pkg.scripts?.dev) {
        const pm = existsSync('pnpm-lock.yaml') ? 'pnpm' : existsSync('yarn.lock') ? 'yarn' : 'npm'
        candidates.push(`${pm} run dev`)
      }
    } catch { /* package.json 无法解析时跳过 */ }
  }
  return candidates
}

function ensureDesignerDir() {
  for (const dir of [DESIGNER_DIR, join(DESIGNER_DIR, 'baselines'), join(DESIGNER_DIR, 'slices'), TMP_DIR]) {
    mkdirSync(dir, { recursive: true })
  }
  if (!existsSync(CONFIG)) {
    const candidates = detectPreviewCommand()
    writeYaml(CONFIG, {
      version: 1,
      router: 'hash',
      preview: { command: candidates.length === 1 ? candidates[0] : null },
      viewport: { width: 1440, height: 900 },
      dpr: 1,
    })
    if (candidates.length === 0) {
      log('! 未识别预览启动命令：请与 Human 确认后填入 config.yaml 的 preview.command')
    } else if (candidates.length > 1) {
      log(`! 预览启动命令有多个候选：${candidates.join('、')}；请与 Human 确认后填入 config.yaml 的 preview.command`)
    }
  }
  if (!existsSync(APPROVALS)) writeFileSync(APPROVALS, '')
  if (!existsSync(RULES)) writeYaml(RULES, { rules: [] })
}

function pageUrl(baseUrl, route, router) {
  const base = baseUrl.replace(/\/+$/, '')
  if (/^https?:/i.test(route)) return route
  if (router === 'hash') return `${base}/#${route}`
  return `${base}${route}`
}

function latestApproval(baselineId) {
  if (!existsSync(APPROVALS)) return null
  const lines = readFileSync(APPROVALS, 'utf8').split('\n').filter(Boolean)
  for (let i = lines.length - 1; i >= 0; i -= 1) {
    const cells = lines[i].split('\t')
    if (cells[1] === 'baseline' && cells[2] === baselineId) {
      return { at: cells[0], blob: cells[3], head: cells[4], note: cells[6] ?? '' }
    }
  }
  return null
}

function validateBaseline(b) {
  const problems = []
  if (!b || typeof b !== 'object') problems.push('baseline 不是对象')
  if (!b.id) problems.push('缺少 id')
  if (!['inherit', 'independent'].includes(b.relation)) problems.push('relation 必须是 inherit 或 independent')
  if (!b.source_page?.route || !b.source_page?.commit || !Array.isArray(b.source_page?.files)) problems.push('source_page 需要 route / files / commit')
  if (!b.target?.route || !Array.isArray(b.target?.files)) problems.push('target 需要 route / files')
  if (!Array.isArray(b.copy)) problems.push('copy 必须是数组')
  if (!Array.isArray(b.delta_files)) problems.push('delta_files 必须是数组')
  if (!Array.isArray(b.states) || b.states.length === 0) problems.push('states 不能为空')
  if (!Array.isArray(b.regions) || b.regions.length === 0) problems.push('regions 不能为空')
  const regionIds = new Set()
  for (const region of b.regions ?? []) {
    if (!region.id || !['preserve', 'delta'].includes(region.role)) problems.push(`region 非法: ${JSON.stringify(region)}`)
    if (regionIds.has(region.id)) problems.push(`region 重复: ${region.id}`)
    regionIds.add(region.id)
  }
  for (const file of b.target?.files ?? []) {
    if (!(b.delta_files ?? []).includes(file)) problems.push(`target 文件不在 delta_files: ${file}`)
  }
  try {
    const dir = join(DESIGNER_DIR, 'baselines')
    if (existsSync(dir)) {
      for (const file of readdirSync(dir)) {
        if (!file.endsWith('.yaml')) continue
        const other = readYaml(join(dir, file))
        if (!other?.id || other.id === b.id) continue
        for (const foreign of other.target?.files ?? []) {
          if ((b.delta_files ?? []).includes(foreign)) problems.push(`delta_files 包含其他 baseline (${other.id}) 的页面文件: ${foreign}（共享文件可保留）`)
        }
      }
    }
  } catch { /* 忽略其他 baseline 的读取问题 */ }
  if (!Array.isArray(b.prototype_diff)) {
    problems.push('prototype_diff 必须是数组（没有差异写 []）')
  } else {
    const kinds = new Set(['structural-add', 'structural-remove', 'contradiction', 'semantics'])
    for (const item of b.prototype_diff) {
      if (!item.id || !kinds.has(item.kind)) problems.push(`prototype_diff 条目非法: ${JSON.stringify(item)}`)
      if (!['decided', 'open'].includes(item.status)) problems.push(`prototype_diff.status 只能是 decided/open: ${item.id}`)
      if (item.status === 'decided' && !item.decision) problems.push(`已决的 prototype_diff 缺少 decision: ${item.id}`)
      if (item.kind === 'structural-add' && (!item.region || !item.signature)) problems.push(`structural-add 需要 region 与 signature: ${item.id}`)
    }
  }
  if (problems.length) fail(`baseline 校验失败:\n- ${problems.join('\n- ')}`)
}

function cmdInit(args) {
  ensureSkillDeps(args)
  ensureDesignerDir()
  log(`✓ 已初始化 ${DESIGNER_DIR}`)
  const ignored = git(['check-ignore', '.tmp/island/designer'], { allowFail: true })
  if (ignored === null) log('! .tmp/island/designer 未被 git 忽略，建议加入 .gitignore')
  log('下一步：写 baselines/<id>.yaml，交 Human 确认后执行 approve。')
}

function cmdApprove(args) {
  const baselinePath = args.baseline
  if (!baselinePath) fail('用法: designer approve --baseline <path> [--note <text>]')
  if (!existsSync(baselinePath)) fail(`baseline 不存在: ${baselinePath}`)
  const baseline = readYaml(baselinePath)
  validateBaseline(baseline)
  const openDiffs = (baseline.prototype_diff ?? []).filter(item => item.status !== 'decided')
  if (openDiffs.length) fail(`prototype_diff 存在未决项，不能 approve:\n- ${openDiffs.map(item => `${item.id} (${item.kind})`).join('\n- ')}`)
  ensureDesignerDir()
  const blob = git(['hash-object', baselinePath])
  const head = git(['rev-parse', 'HEAD'])
  const at = new Date().toISOString()
  const row = [at, 'baseline', baseline.id, blob, head, 'human', args.note ? String(args.note) : ''].join('\t')
  writeFileSync(APPROVALS, readFileSync(APPROVALS, 'utf8') + row + '\n')
  log(`✓ 已记录审批: ${baseline.id}@${blob.slice(0, 8)} (HEAD ${head.slice(0, 8)})`)
  log('提醒：approve 只记录事实，不校验 Human 是否真的确认；必须由 Human 明确同意后调用。')
}

function cmdCopy(args) {
  const baselinePath = args.baseline
  if (!baselinePath) fail('用法: designer copy --baseline <path> [--force]')
  const baseline = readYaml(baselinePath)
  validateBaseline(baseline)
  if (!Array.isArray(baseline.copy) || baseline.copy.length === 0) fail('baseline.copy 为空，没有可复制文件')
  const approval = latestApproval(baseline.id)
  if (!approval) fail(`baseline ${baseline.id} 尚未审批，先执行 approve`)
  const blob = git(['hash-object', baselinePath])
  if (blob !== approval.blob) fail(`baseline 在审批后被修改（当前 ${blob.slice(0, 8)}，审批 ${approval.blob.slice(0, 8)}）`)
  const copied = []
  for (const entry of baseline.copy) {
    if (!entry.from || !entry.to) fail(`copy 条目非法: ${JSON.stringify(entry)}`)
    let content
    try {
      content = execFileSync('git', ['show', `${baseline.source_page.commit}:${entry.from}`], {
        cwd: process.cwd(), encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
      })
    } catch {
      fail(`source_page.commit 中不存在: ${entry.from}`)
    }
    if (!(baseline.delta_files ?? []).includes(entry.to)) fail(`目标文件不在 delta_files: ${entry.to}`)
    if (existsSync(entry.to) && !args.force) fail(`目标文件已存在: ${entry.to}（需要覆盖时加 --force）`)
    mkdirSync(dirname(entry.to), { recursive: true })
    writeFileSync(entry.to, content)
    copied.push(entry.to)
  }
  git(['add', '--', ...copied])
  try {
    git(['commit', '-m', `chore(designer): copy sources for ${baseline.id}`, '--', ...copied])
  } catch {
    fail('copy commit 失败（可能没有实际变化）')
  }
  log(`✓ 已生成 copy commit: ${git(['rev-parse', '--short', 'HEAD'])}`)
  log(`  复制: ${copied.join(', ')}`)
}

function changedFilesSince(head) {
  const committed = (git(['diff', '--name-only', head], { allowFail: true }) ?? '').split('\n').filter(Boolean)
  const untracked = (git(['ls-files', '--others', '--exclude-standard'], { allowFail: true }) ?? '')
    .split('\n')
    .filter(Boolean)
  return [...new Set([...committed, ...untracked])]
}

function isDesignerArtifact(file) {
  return file.startsWith(`${DESIGNER_DIR}/`) || file.startsWith('.tmp/') || file.startsWith('node_modules/')
}

async function loadChromium(args) {
  try {
    const { chromium } = await import('playwright')
    return chromium
  } catch {
    fail('未找到 playwright。请在 skill 目录执行 pnpm install 与 pnpm exec playwright install chromium。')
  }
}

async function capture(browser, config, baseUrl, route, regionIds, readySelector) {
  const context = await browser.newContext({
    viewport: config.viewport ?? { width: 1440, height: 900 },
    deviceScaleFactor: config.dpr ?? 1,
  })
  const page = await context.newPage()
  const url = pageUrl(baseUrl, route, config.router ?? 'hash')
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 })
    if (readySelector) await page.waitForSelector(readySelector, { timeout: 15000 })
    await page.waitForTimeout(300)
    const result = { url, regions: {} }
    for (const id of regionIds) {
      const selector = `[data-region="${id}"]`
      const found = await page.locator(selector).count()
      if (!found) {
        result.regions[id] = { present: false }
        continue
      }
      const skeleton = await page.evaluate(([sel, props, stopClasses]) => {
        const root = document.querySelector(sel)
        if (!root) return null
        const collapse = (items) => {
          const out = []
          for (const item of items) {
            const signature = JSON.stringify(item)
            if (out.length && JSON.stringify(out[out.length - 1]) === signature) continue
            out.push(item)
          }
          return out
        }
        const walk = (el, isRoot = false) => {
          const region = el.getAttribute('data-region') || undefined
          if (!isRoot && region) return { region }
          const classList = Array.from(el.classList).filter(name => !/^(is-|has-)/.test(name)).sort()
          // Library root: its internal items are generated (e.g. page numbers).
          // Compare only the root tag/class; do not recurse into generated children.
          if (stopClasses.some(name => classList.includes(name))) {
            return { tag: el.tagName.toLowerCase(), class: classList, region, stopped: true }
          }
          return {
            tag: el.tagName.toLowerCase(),
            class: classList,
            region,
            children: collapse(Array.from(el.children).map(child => walk(child))),
          }
        }
        const style = getComputedStyle(root)
        const styles = {}
        for (const prop of props) styles[prop] = style.getPropertyValue(prop)
        return { skeleton: walk(root, true), styles }
      }, [selector, STYLE_PROPS, STOP_CLASSES])
      result.regions[id] = { present: true, ...skeleton }
    }
    return result
  } finally {
    await context.close()
  }
}

function firstDiff(a, b, path = '') {
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b)) return `${path}: 类型不同`
    const max = Math.max(a.length, b.length)
    for (let i = 0; i < max; i += 1) {
      const diff = firstDiff(a[i], b[i], `${path}[${i}]`)
      if (diff) return diff
    }
    return null
  }
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const keys = new Set([...Object.keys(a), ...Object.keys(b)])
    for (const key of keys) {
      const diff = firstDiff(a[key], b[key], path ? `${path}.${key}` : key)
      if (diff) return diff
    }
    return null
  }
  return a === b ? null : `${path}: ${JSON.stringify(a)} !== ${JSON.stringify(b)}`
}

async function cmdVerify(args) {
  const baselinePath = args.baseline
  if (!baselinePath || !args.url) {
    fail('用法: designer verify --baseline <path> --url <url> [--headed]\n预览地址没有默认值：用 config.yaml 的 preview.command 在当前工作目录后台启动服务，从输出读取实际地址后传入。')
  }
  const baseline = readYaml(baselinePath)
  validateBaseline(baseline)
  ensureDesignerDir()
  const approval = latestApproval(baseline.id)
  if (!approval) fail(`baseline ${baseline.id} 尚未审批，先执行 approve`)
  const blob = git(['hash-object', baselinePath])
  if (blob !== approval.blob) fail(`baseline 在审批后被修改（当前 ${blob.slice(0, 8)}，审批 ${approval.blob.slice(0, 8)}）`)
  const sourceDrift = (git(['diff', '--name-only', baseline.source_page.commit, '--', ...baseline.source_page.files], { allowFail: true }) ?? '')
    .split('\n').filter(Boolean)
  if (sourceDrift.length) fail(`参考页在 source_page.commit 之后被改动: ${sourceDrift.join(', ')}`)
  const config = readYaml(CONFIG)
  const changed = changedFilesSince(approval.head).filter(file => !isDesignerArtifact(file))
  const s1Files = changed.filter(file => !baseline.delta_files.includes(file))
  const s1 = { ok: s1Files.length === 0, files: s1Files, changed }

  const chromium = await loadChromium(args)
  const browser = await chromium.launch({ headless: !args.headed })
  const states = baseline.states
  const regionIds = baseline.regions.map(region => region.id)
  const preserveIds = baseline.regions.filter(region => region.role === 'preserve').map(region => region.id)
  const deltaIds = baseline.regions.filter(region => region.role === 'delta').map(region => region.id)

  const targetCaptures = {}
  const sourceCaptures = {}
  try {
    for (const state of states) {
      targetCaptures[state.id] = await capture(browser, config, args.url, baseline.target.route, regionIds, state.ready)
      sourceCaptures[state.id] = await capture(browser, config, args.url, baseline.source_page.route, regionIds, state.ready)
    }
  } finally {
    await browser.close()
  }

  const s2Missing = []
  for (const state of states) {
    for (const id of regionIds) {
      if (!targetCaptures[state.id].regions[id]?.present) s2Missing.push(`${state.id}:${id}`)
    }
  }
  const s2 = { ok: s2Missing.length === 0, missing: s2Missing }

  const s3Diffs = []
  const s4Diffs = []
  for (const state of states) {
    for (const id of preserveIds) {
      const target = targetCaptures[state.id].regions[id]
      const source = sourceCaptures[state.id].regions[id]
      if (!target?.present || !source?.present) {
        s3Diffs.push({ state: state.id, region: id, detail: '区域缺失，无法比较' })
        continue
      }
      const skeletonDiff = firstDiff(source.skeleton, target.skeleton)
      if (skeletonDiff) s3Diffs.push({ state: state.id, region: id, detail: skeletonDiff })
      for (const prop of STYLE_PROPS) {
        if ((source.styles?.[prop] ?? '') !== (target.styles?.[prop] ?? '')) {
          s4Diffs.push({ state: state.id, region: id, property: prop, source: source.styles?.[prop], target: target.styles?.[prop] })
        }
      }
    }
  }
  const s3 = { ok: s3Diffs.length === 0, diffs: s3Diffs }
  const s4 = { ok: s4Diffs.length === 0, diffs: s4Diffs }

  const s5Violations = []
  if (existsSync(RULES)) {
    const rules = readYaml(RULES)?.rules ?? []
    for (const rule of rules) {
      if (rule.kind !== 'grep' || !rule.pattern) continue
      const files = (rule.files === 'delta' || rule.files === undefined) ? baseline.delta_files : rule.files
      const re = new RegExp(rule.pattern)
      for (const file of files) {
        if (!existsSync(file)) continue
        const lines = readFileSync(file, 'utf8').split('\n')
        lines.forEach((line, index) => {
          if (re.test(line)) s5Violations.push({ rule: rule.id, file, line: index + 1 })
        })
      }
    }
  }
  const s5 = { ok: s5Violations.length === 0, violations: s5Violations }

  const signatureOf = node => node?.region
    ? `region:${node.region}`
    : `${node.tag}${Array.isArray(node.class) && node.class.length ? '.' + node.class.join('.') : ''}`
  const prototypeDiff = baseline.prototype_diff ?? []
  const s6Violations = []
  for (const state of states) {
    for (const id of deltaIds) {
      const target = targetCaptures[state.id].regions[id]
      const source = sourceCaptures[state.id].regions[id]
      if (!target?.skeleton || !source?.skeleton) continue
      const sourceSignatures = new Set((source.skeleton.children ?? []).map(signatureOf))
      const declared = new Set(
        prototypeDiff
          .filter(item => item.kind === 'structural-add' && item.region === id)
          .map(item => item.signature),
      )
      for (const child of target.skeleton.children ?? []) {
        const signature = signatureOf(child)
        if (!sourceSignatures.has(signature) && !declared.has(signature)) {
          s6Violations.push({ state: state.id, region: id, signature })
        }
      }
    }
  }
  const s6 = { ok: s6Violations.length === 0, violations: s6Violations }

  const ok = s1.ok && s2.ok && s3.ok && s4.ok && s5.ok && s6.ok
  const roundDir = join(TMP_DIR, 'rounds', baseline.id)
  mkdirSync(roundDir, { recursive: true })
  const roundNumber = readdirSync(roundDir).filter(name => /^r\d+$/.test(name)).length + 1
  const outDir = join(roundDir, `r${roundNumber}`)
  mkdirSync(outDir, { recursive: true })
  const report = {
    baseline: baseline.id,
    round: `r${roundNumber}`,
    result: ok ? 'pass' : 'fail',
    head: git(['rev-parse', 'HEAD']),
    url: args.url,
    cwd: process.cwd(),
    s1, s2, s3, s4, s5, s6,
  }
  writeYaml(join(outDir, 'report.yaml'), report)
  writeFileSync(join(outDir, 'target.json'), JSON.stringify(targetCaptures, null, 2))
  writeFileSync(join(outDir, 'source.json'), JSON.stringify(sourceCaptures, null, 2))

  const mark = state => (state ? '✓' : '✗')
  log(`verify ${baseline.id} (${report.round})`)
  log(`  ${mark(s1.ok)} S1 文件范围${s1.ok ? '' : `：${s1.files.join(', ')}`}`)
  log(`  ${mark(s2.ok)} S2 区域存在${s2.ok ? '' : `：${s2.missing.join(', ')}`}`)
  log(`  ${mark(s3.ok)} S3 骨架一致${s3.ok ? '' : ''}`)
  for (const diff of s3Diffs) log(`      - ${diff.state}/${diff.region}: ${diff.detail}`)
  log(`  ${mark(s4.ok)} S4 样式探针`)
  for (const diff of s4Diffs.slice(0, 12)) log(`      - ${diff.state}/${diff.region} ${diff.property}: ${diff.source} -> ${diff.target}`)
  log(`  ${mark(s5.ok)} S5 规则${s5.ok ? '' : `：${s5.violations.map(v => `${v.rule}@${v.file}:${v.line}`).join(', ')}`}`)
  log(`  ${mark(s6.ok)} S6 原型差异声明${s6.ok ? '' : '：'}`)
  for (const violation of s6Violations) log(`      - ${violation.state}/${violation.region}: 未声明的直接子结构 ${violation.signature}`)
  log(`  报告: ${join(outDir, 'report.yaml')}`)
  if (!ok) process.exit(1)
}

function cmdStatus() {
  const baselinesDir = join(DESIGNER_DIR, 'baselines')
  if (!existsSync(baselinesDir)) fail('尚未初始化，先执行 init')
  const files = readdirSync(baselinesDir).filter(name => name.endsWith('.yaml'))
  if (!files.length) { log('没有 baseline'); return }
  for (const file of files) {
    const path = join(baselinesDir, file)
    let baseline
    try { baseline = readYaml(path) } catch { log(`${file}: 无法解析`); continue }
    const approval = latestApproval(baseline.id)
    const blob = git(['hash-object', path], { allowFail: true })
    const approved = approval && approval.blob === blob
    const roundDir = join(TMP_DIR, 'rounds', baseline.id)
    const rounds = existsSync(roundDir) ? readdirSync(roundDir).filter(name => /^r\d+$/.test(name)) : []
    log(`${baseline.id}  relation=${baseline.relation}  approval=${approved ? `yes@${approval.at}` : 'no'}  rounds=${rounds.length}`)
  }
}

async function main() {
  const [command, ...rest] = process.argv.slice(2)
  const args = parseArgs(rest)
  if (!command || command === '--help' || command === '-h') {
    log('用法: designer <init|approve|copy|verify|status> [options]')
    log('        init 会检查 skill 依赖；缺失时自动 npm ci/install。加 --skip-install 可跳过。')
    return
  }
  if (command === 'init') return cmdInit(args)
  if (command === 'approve') return cmdApprove(args)
  if (command === 'copy') return cmdCopy(args)
  if (command === 'verify') return cmdVerify(args)
  if (command === 'status') return cmdStatus()
  fail(`未知命令: ${command}`)
}

try {
  await main()
} catch (error) {
  fail(error instanceof Error ? error.message : String(error))
}
