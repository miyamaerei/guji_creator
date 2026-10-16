// 采集器 V3：三域采集（著录 C8 / 结构 C9 / 知识域层产物）——只量盘上真值
// 用法：node Summary/html/collect_meta.js            → 打印一览表 + 写 _meta_out.json
//      node Summary/html/collect_meta.js --json      → 只输出 JSON（供 check_summary.js 消费）
//
// 定位：Summary/ 的 md 与 data.js/times.js 是「声明值」，本采集器量的是「盘上真值」。
//      差集由 Skills/progress-dashboard-integration/scripts/check_summary.js 判定并分级。
// 纪律：只读不写盘上数据文件（唯一输出 _meta_out.json，已 gitignore）；
//      不猜——量不到就报 null，并把「找过哪些路径」一并写进结果（C8 的 null_basis 同源纪律）。
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { DIRS, ROOT, walk, CARRIER_SEG } = require('./collect_times.js');

// ---------- 通用 ----------
function readJson(p) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return null; } }
function sha16(p) { try { return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex').slice(0, 16); } catch (e) { return null; } }
// 影子目录：交付副本 / 构建中间物 / 备份 / 校验输出 / 旧版层 / 阅读器渲染产物——一律不作真值来源
const SHADOW_SEG = /^(_deliver|_build|_work\w*|_extract|_legacy|_backup\w*|_validate|_views|_vis|views|raw|成品|pilot|\w*(_old|_v\d+))$/i;
function isShadow(relPath) { return String(relPath).split(/[\/\\]/).some(s => SHADOW_SEG.test(s)); }
const SHADOW = { test: isShadow };

// 记录数组的常见容器键名：命中即取该键；否则退到「最长数组」并记形状，供门判定（不静默猜）
const RECORD_KEYS = ['records', 'items', 'entries', 'entities', 'annotations', 'docs', 'rows', 'data', 'list'];
// 一个「记录容器」有多少条：数组 → 长度；{层码:[…]} → 各数组之和；{item_id:{…}} → 键数
function containerCount(v) {
  if (Array.isArray(v)) return v.length;
  if (v && typeof v === 'object') {
    const vs = Object.values(v);
    if (!vs.length) return 0;
    if (vs.every(Array.isArray)) return vs.reduce((a, b) => a + b.length, 0);
    if (vs.every(x => x && typeof x === 'object')) return vs.length;
  }
  return null;
}
// 一个 JSON 里有多少条记录；认不出的结构返回 null（不瞎猜）
// 判定顺序即口径优先级，每一档都在 shapes 里留名，门和人都能看到这个数是按哪档算的：
//   array         → 裸数组（明会典多数层）
//   multi-table   → 五子表并置（新官轨范_结构_ai 的 ledgers/times/docs/actors/frauds），逐表求和
//                   必须先于 named:xxx——否则 docs/data/list 既是子表名又是容器名，会只算一张表
//   named:KEY     → {records:[…]} 等标准包装
//   single-array  → 只有一个数组值（{volume, event_count, events:[…]}）：确定量，不是估算
//   whole-dict    → 值是对象字典（{item_id:{…}}）
//   longest-array → 多个数组时取最长（这才是估算，shapes 里单列，门会警告）
function countRecords(j, stat) {
  const note = s => { if (stat) stat[s] = (stat[s] || 0) + 1; };
  if (Array.isArray(j)) { note('array'); return j.length; }
  if (!j || typeof j !== 'object') return null;
  const vals = Object.values(j);
  const arrs = vals.filter(Array.isArray);
  if (arrs.length > 1 && !('records' in j) && !('items' in j)
    && vals.every(v => Array.isArray(v) || v === null || typeof v !== 'object')) {
    note('multi-table'); return arrs.reduce((a, b) => a + b.length, 0);
  }
  for (const k of RECORD_KEYS) {
    if (!(k in j)) continue;
    const n = containerCount(j[k]);
    if (n !== null) { note('named:' + k); return n; }
  }
  if (arrs.length === 1) { note('single-array'); return arrs[0].length; }
  const whole = containerCount(j);
  if (whole !== null) { note('whole-dict'); return whole; }
  if (arrs.length) { note('longest-array'); return Math.max(...arrs.map(a => a.length)); }
  note('unrecognized');
  return null;
}
// item_id 方案：NN-NNN 是 A 线主流（mhd 用三位 NN-NNN）；myt 有 NN-NNN_cNN 子条；
// 部门名/中文标题等非数字方案单独统计——卷数只能从数字前缀推，不能瞎算
const ID_NNN = /^(\d{2,3})-(\d{3})(_c\d+)?/;
function idScheme(k) {
  const m = ID_NNN.exec(k);
  if (m) return m[3] ? 'NNN-NNN-cNN' : 'NNN-NNN';
  if (/^\d{2,3}$/.test(k)) return 'numeric';
  return 'other';
}

// ---------- ① 底座指纹库（C3，C9 的前提）----------
const REG_NAMES = /^(_item_registry|registry)\.json$/;
// 底座有两种落法：字典（key 即 item_id）/ 包壳对象 {records:[...]} 或 {items:[...]}
function registryEntries(j) {
  const arr = Array.isArray(j) ? j : (Array.isArray(j.records) ? j.records : (Array.isArray(j.items) ? j.items : null));
  if (arr) {
    const out = [];
    for (const r of arr) {
      if (!r || typeof r !== 'object') continue;
      out.push([String(r.item_id !== undefined ? r.item_id : (r.id !== undefined ? r.id : r.key)), r]);
    }
    return out;
  }
  if (j && typeof j === 'object') return Object.entries(j).filter(([, v]) => v && typeof v === 'object');
  return [];
}
function collectRegistry(files) {
  const isReg = f => REG_NAMES.test(path.posix.basename(f.r));
  let hit = files.filter(f => isReg(f) && !SHADOW.test(f.r));
  // 只有影子副本时仍要量（水东日记的底座就住在 _extract/），但打 shadowOnly 标记供门判定
  const shadowOnly = !hit.length && files.some(f => isReg(f) && SHADOW.test(f.r));
  if (shadowOnly) hit = files.filter(isReg);
  if (!hit.length) return null;
  const parsed = hit.map(f => {
    const j = readJson(f.p);
    if (!j || typeof j !== 'object') return null;
    const ent = registryEntries(j);
    if (!ent.length) return null;
    const keys = ent.map(e => e[0]);
    const scheme = {};
    keys.forEach(k => { const s = idScheme(k); scheme[s] = (scheme[s] || 0) + 1; });
    const main = Object.entries(scheme).sort((a, b) => b[1] - a[1])[0];
    return { f, ent, keys, scheme, dominant: main ? main[0] : null, mainRatio: keys.length ? main[1] / keys.length : 0 };
  }).filter(Boolean);
  if (!parsed.length) return null;
  // 择优：先按主流 id 方案占比，再按条数——避免旁挂的小样本索引文件冒充主库
  parsed.sort((a, b) => (b.mainRatio - a.mainRatio) || (b.keys.length - a.keys.length));
  const m = parsed[0];
  return Object.assign(summarizeRegistry(m.f, m.ent), {
    others: parsed.slice(1).map(x => ({ file: x.f.r, items: x.keys.length, dominant: x.dominant })),
    ignoredShadow: shadowOnly ? [] : files.filter(f => REG_NAMES.test(path.posix.basename(f.r)) && SHADOW.test(f.r)).map(f => f.r),
    shadowOnly: !!shadowOnly,
  });
}

// 底座条目 → 计量汇总（id 方案 / 字段覆盖 / 卷前缀）：_item_registry 与 书籍json 载体两种来源共用
function summarizeRegistry(f, ent) {
  const fields = {}; const byScheme = {}; const vols = {};
  for (const [k, v] of ent) {
    if (v && typeof v === 'object' && !Array.isArray(v)) for (const fld of Object.keys(v)) fields[fld] = (fields[fld] || 0) + 1;
    const s = idScheme(k);
    byScheme[s] = (byScheme[s] || 0) + 1;
    const mm = ID_NNN.exec(k);
    if (mm) {
      const p = String(Number(mm[1])).padStart(mm[1].length, '0');
      (vols[p] = vols[p] || { items: 0, subitems: 0 }).items++;
      if (mm[3]) vols[p].subitems++;
    }
  }
  const keys = ent.map(e => e[0]);
  const dominant = Object.entries(byScheme).sort((a, b) => b[1] - a[1])[0];
  return {
    file: f.r, items: keys.length, idSchemes: byScheme, dominantScheme: dominant ? dominant[0] : null,
    fieldUnion: Object.keys(fields).sort(), fieldCoverage: fields,
    volumePrefixes: Object.keys(vols).sort((a, b) => Number(a) - Number(b)),
    volumeCount: Object.keys(vols).length,
    noItemIdCount: (byScheme.other || 0) === keys.length ? keys.length : 0,
    hasSubitemIds: Object.keys(byScheme).length > 1,
    registryHash: sha16(f.p),
  };
}

// 结构域回退：实例根没有 _item_registry.json 时，切条库就地住在 书籍json 载体里
// （整书页 volumes[].items 就是条，id 也在条上）——§6b「就地补，不另建文件」的路线，
// 所以载体既量 C8 元数据，也在无 registry 时充当底座计量源。通用规则，不逐本点名。
function registryFromCarrier(files) {
  const bjs = files.filter(f => /(^|\/)书籍json\/[^/]+\.json$/i.test(f.r) && !/\/分卷json\//.test(f.r) && !SHADOW.test(f.r));
  for (const f of bjs) {
    const d = readJson(f.p);
    if (!d || !Array.isArray(d.volumes)) continue;
    const ent = [];
    for (const vol of d.volumes) {
      const items = Array.isArray(vol) ? vol : (vol && vol.items);
      if (!Array.isArray(items)) continue;
      items.forEach((it, i) => {
        if (!it || typeof it !== 'object') return;
        ent.push([it.id || it.item_id || ((vol.no || vol.volume || '00') + '-' + String(i + 1).padStart(3, '0')), it]);
      });
    }
    if (!ent.length) continue;
    return Object.assign(summarizeRegistry(f, ent), { fromCarrier: true });
  }
  return null;
}

// ---------- ② 层产物（知识域）----------
// 探针：目录名像层根（_layers / layers / data / _data），其子目录是短英文层码，
//       或目录内直接放 <层码>_NN.json。影子目录一律排除。
const LAYER_ROOT_NAME = /(^|\/)(_layers|layers|data|_data)$/;
const LAYER_CODE = /^[a-z][a-z0-9]{1,7}$/;
// 文件名推出的层码放宽版（允许 officials / office_profiles 这类长码），用于「同目录住着他层」的改判
const LAYER_CODE2 = /^[a-z][a-z0-9_]{2,15}$/;
const NOT_A_LAYER = /^(vol|v)\d+$|^\d+$|^(node_modules|vendor)$/;
// 层几何声明（不是结果白名单）：探针猜不出来的书，逐本写清「成品放在哪、哪个文件算成品」。
// 只声明几何，不声明数值：盘上有而 data.js 没注册的层件一律进 unregistered 由门列出。
const LAYER_SPEC = {
  // qb：成品叫 归一_<层>.json（registry.md 与 data.js 都这么声明）；_kg_NN/_trl_NN 是同数据的分卷形态，不重复计
  qb: { dir: '.', fileRx: /^归一_.+\.json$/, key: b => b.replace(/\.json$/, '').replace(/^归一_/, '') },
  // xgg：目录用中文书名命名；规则/规则_段落 是规则层的前案与段落辅助索引（成品是 _ai）
  xgg: { dir: '.',
    dirs: { 新官轨范_标注: '标注', 新官轨范_结构_ai: 'struct', 新官轨范_流程_ai: 'proc', 新官轨范_规则_ai: 'rule', 新官轨范_事件_ai: 'event' },
    ignore: { 新官轨范_规则: '规则层手工前案（成品为 新官轨范_规则_ai）', 新官轨范_规则_段落: '段落辅助索引（非语义层）' } },
  // fhs：盘上目录用复数，归一到 data.js/C4 的单数层码（目录名≠注册码本身是 C4 违规，门另行报）
  fhs: { dir: '.', dirs: { ent: 'ent', trl: 'trl', docs: 'doc', opns: 'opn', procs: 'proc', regs: 'reg', rels: 'rel', rules: 'rule', structs: 'struct' } },
  // zp：每层一个 all.json 聚合 + pilot.json 试点；rule 目录三版并存，成品是 rule_final（与 _deliver/rule.json 同数）
  zp: { dir: '_layers', pick: { rule: 'rule_final.json' } },
  // zgz：officials 层住在 structs 目录里，按文件名点名
  zgz: { fileLayer: { 'officials.json': 'officials' } },
  // mhd：_layers 平铺 40+ 个 json；树视图/词表是派生件不是层记录（清洗版/手工版/备份由别版规则自动识别）
  mhd: { dir: '_layers', mode: 'files',
    ignore: { office_tree: '官职树视图（与 office_tree.md 同源，派生渲染件）',
      org_tree: '机构树视图（同上）',
      vocab: '术语倒排词表（name/kind/count/item_ids 索引，非层记录）' } },
  // sdr：层根叫 data/（C1 别名）；data/聚合/ 是各层的聚合副本，计入会翻倍
  sdr: { dir: 'data', ignore: { 聚合: 'data/聚合/ 是各层聚合副本（与分卷件同源），计进合计会翻倍' } },
  // bz：盘上无层成品——_data/weis/ 是 C17 卫所树试点数据（未定稿），不是层产物
  //     声明「无层」而不是让它冒充一层：探针会选中 _data/weis/（_data 命中层根命名）
  bz: { none: '兵志尚未装填：_data/weis/ 是卫所树（C17 候选层）试点数据，非 _layers 成品' },
};
// 层根探针：先按目录归堆（json 文件），再把每个父目录也纳入候选——
// 否则 `_layers/ent/ent_01.json` 会让 `_layers/ent` 冒充层根（层根是它的父）。
function layerRootsProbe(files) {
  const byDir = {};
  for (const f of files) {
    if (!/\.json$/i.test(f.r) || SHADOW.test(f.r)) continue;
    const d = path.posix.dirname(f.r);
    (byDir[d] = byDir[d] || []).push(f);
  }
  const dirs = new Set(Object.keys(byDir));
  for (const d of Object.keys(byDir)) {
    const parts = d.split('/');
    for (let i = parts.length - 1; i > 0; i--) dirs.add(parts.slice(0, i).join('/'));
  }
  const layerChild = s => LAYER_CODE.test(s) && !NOT_A_LAYER.test(s);
  const scored = [...dirs].map(d => {
    const own = byDir[d] || [];
    const children = [...dirs].filter(x => path.posix.dirname(x) === d);
    const coded = children.filter(x => layerChild(path.posix.basename(x)));
    // 子层里的文件（`_layers/ent/*` 的场域）；父根要能把它们全部计入
    const inCoded = coded.reduce((a, c) => a + (byDir[c] || []).length, 0);
    const flat = own.filter(f => /^[a-z][a-z0-9]*(_\d+)?\.json$/i.test(path.posix.basename(f.r))).length;
    const named = LAYER_ROOT_NAME.test('/' + d) ? 4 : 0;
    const viaChildren = coded.length * 6 + inCoded * 0.05;
    const score = named + Math.max(viaChildren, coded.length ? 0 : flat * 1.2);
    const files = coded.length ? own.concat(coded.reduce((a, c) => a.concat(byDir[c] || []), [])) : own;
    return { d, files, fileCount: files.length, codedSubdirs: coded.length, flat, named, score };
  }).filter(x => x.score > 0 && x.files.length)
    .sort((a, b) => b.score - a.score || a.d.length - b.d.length || b.fileCount - a.fileCount);
  return scored;
}
// 层文件名 → {key, agg}：尾部的卷号与「聚合后缀」都剥掉才是层码；
// 剥到过聚合后缀说明这个文件是该层的聚合件（整层一个文件），否则是分卷件（每卷一个）。
// 两者同存且不等时以分卷件为准（聚合件多为派生视图），聚合值一并留在 JSON 里由门判定。
const AGG_TOKEN = /^(all|keys|main|summary|merged|index|indexes|inventory|alias|normalized|norm|归一|汇总|索引|总表|清单)$/i;
// 装配/派生件：住在层根里但不是层（sdr 的 data/join.json 是条目联表，不是知识层）。
// report 不在其列——明会典的 reports（文册勘合）是注册层（C4），不能被当成报告件剔掉。
const ASSEMBLY_KEY = /^(join|_?kg_join|_?coverage\w*|_?stats\w*|_?tmp\w*|_?scratch\w*)$/i;
// 同一层的另一种版本形态（试点/自动稿/清洗版/v2…）：不是新层，也不与成品同计
const VARIANT_TAIL = /^(pilot|sample|demo|auto|v\d+|clean|manual|bak|backup|old|new|full|seed|global|dropped|sequence|tree|links?)$/i;
function splitKey(base) {
  const parts = base.split(/[_-]/);
  let agg = false;
  while (parts.length) {
    const last = parts[parts.length - 1];
    if (/^\d+$/.test(last)) { parts.pop(); continue; }
    if (AGG_TOKEN.test(last)) { agg = true; parts.pop(); continue; }
    break;
  }
  return { key: parts.join('_') || base, agg, onlyTokens: parts.length === 0 };
}
// 注册层集合：data.js 的 books[].layers 声明就是「这本书应该有哪几层」的唯一登记处。
// 盘上有、data.js 没登记的层件 → unregistered（照常测量、照常报数，但不进 totalRegistered）。
// 这是「白名单」的替代：采集器不持有任何例外结论，例外只存在于 data.js 的声明里，
// 由门（check_summary.js）把差额亮出来。为什么这样分：白名单是「关掉眼睛」，
// 声明集是「眼睛睁开但只看登记过的」——后者每次跑管线都会把未登记件重报一遍。
function loadDeclaredLayers() {
  try {
    const vm = require('vm');
    const sandbox = { window: {} };
    vm.createContext(sandbox);
    vm.runInContext(fs.readFileSync(path.join(__dirname, 'data.js'), 'utf8'), sandbox, { filename: 'data.js' });
    const books = (sandbox.window.GDATA || {}).books || [];
    const out = {};
    for (const b of books) out[b.id] = new Set((b.layers || []).map(L => Array.isArray(L) ? L[0] : L.layer).filter(Boolean));
    return out;
  } catch (e) { return {}; }
}
// C8/C9 载体目录（书籍json/）是从 _item_registry.json 派生的成品（整书页 + 分卷片），不是知识层。
// 它必须从层的几何里剔出去：留在探针候选里会选错层根，留在 slice 里会因为
// f.r.slice(prefixOf.length) 不校验前缀而把路径切成乱码 key，冒充「未注册层件」
// （2026-10-16 实见：mhd 明会典_校对版=180、zp 卷json=11、sdr n=78）。
function collectLayersFor(files, spec, declared) {
  files = files.filter(f => !CARRIER_SEG.test(f.r));
  const layers = {}; let root = null; let mode = null; let candidates = [];
  const skippedAssembly = [], variants = [], extras = [], ignored = [];
  const dirAlias = (spec && spec.dirs) || {};      // 盘上目录名 → 注册层码（中文名/别名的书）
  const pick = (spec && spec.pick) || {};          // 层码 → 该层的成品文件名（多版本时人工指定）
  const ignore = (spec && spec.ignore) || {};      // 目录名/文件名 → 不计数并写明原因
  const fileLayer = (spec && spec.fileLayer) || {}; // 文件名 → 它真正属于的层码
  const addJson = (key, p, agg) => {
    const L = layers[key] = layers[key] || { files: 0, skipped: 0, shapes: {}, shards: 0, shardRecords: 0, aggs: 0, aggRecords: 0 };
    const n = countRecords(readJson(p), L.shapes);
    L.files++;
    if (n === null) { L.skipped++; return; }
    if (agg) { L.aggs++; L.aggRecords += n; } else { L.shards++; L.shardRecords += n; }
  };
  // 把一个层根内的 json 归类：成品层 / 同层别版 / 装配件 / 刻意排除件，四类各留痕，不静默丢弃
  function classify(dn, rel, fname) {
    const stem = path.posix.basename(fname, '.json');
    const base = dn || stem;
    if (ignore[base] || ignore[stem] || ignore[rel]) return { a: 'ignore', why: ignore[base] || ignore[stem] || ignore[rel] };
    if (/^_/.test(stem) || ASSEMBLY_KEY.test(stem)) return { a: 'assembly' };
    if (fileLayer[fname]) return { a: 'layer', key: fileLayer[fname], agg: true };
    // 备份件（offices.bak.json）：不是新层，是该层的旧版
    const bak = /^(.+?)\.(bak|backup\d*|old)$/i.exec(stem);
    if (bak) return { a: 'variant', key: dirAlias[bak[1]] || bak[1] };
    const sk = splitKey(stem);
    const last = sk.key.split(/[_-]/).pop();
    // 平铺根：文件名即层码；`<层>_<别版后缀>.json`（offices_clean/rank_sequence）是同层别版，不是新层
    if (dn === null) {
      const toks = stem.split(/[_-]/);
      const tailTok = toks.length > 1 ? toks[toks.length - 1] : null;
      if (tailTok && VARIANT_TAIL.test(tailTok)) return { a: 'variant', key: dirAlias[toks.slice(0, -1).join('_')] || toks.slice(0, -1).join('_') };
      return { a: 'layer', key: dirAlias[sk.key] || sk.key, agg: sk.agg };
    }
    const canon = dirAlias[dn] || dn;
    if (pick[canon] === fname) return { a: 'layer', key: canon, agg: true };
    if (sk.onlyTokens || sk.key === dn) return { a: 'layer', key: canon, agg: sk.agg };
    if (VARIANT_TAIL.test(last) || sk.key.startsWith(dn + '_')) return { a: 'variant', key: canon };
    return { a: 'layer', key: canon, agg: sk.agg };   // 默认归属所在层目录（按卷/按篇命名的文件）
  }
  function place(dn, f) {
    const rel = f.r.slice(prefixOf.length);
    const c = classify(dn, rel, path.posix.basename(f.r));
    if (c.a === 'layer') { addJson(c.key, f.p, c.agg); return; }
    const n = countRecords(readJson(f.p), null);
    if (c.a === 'ignore') { ignored.push({ file: rel, reason: c.why }); return; }
    if (c.a === 'assembly') { skippedAssembly.push(rel); return; }
    if (c.a === 'variant') { variants.push({ file: rel, layer: c.key, records: n }); return; }
    extras.push({ file: rel, key: c.key, records: n });
  }
  let prefixOf = '';
  // 声明「盘上无层成品」：探针仍跑（把候选留下作证据），但一个都不计数——它们进 ignored 并附原因
  if (spec && spec.none) {
    candidates = layerRootsProbe(files);
    for (const c of candidates) for (const f of c.files) if (/\.json$/i.test(f.r)) ignored.push({ file: f.r, reason: spec.none });
    return { root: null, mode: 'declared:none', layers: {}, total: 0, totalRegistered: 0, layerCount: 0, registeredCount: 0,
      unregistered: [], declaredMissing: [...(declared || [])], skipped: 0, skippedAssembly, variants, extras, ignored,
      mismatch: [], candidates: candidates.map(c => c.d), note: spec.none };
  }
  // spec 只声明了文件名归属（zgz 的 officials）而没有声明层根几何时，层根仍由探针定，
  // 探针选出的目录里再按 classify 走——否则 spec.dir 为 undefined 会把路径前缀切错。
  const rootDeclared = !!(spec && (spec.dir || spec.fileRx || spec.dirs || spec.dirRx));
  if (spec && rootDeclared) {
    root = spec.dir; mode = spec.fileRx ? 'files' : 'dirs';
    prefixOf = spec.dir === '.' ? '' : spec.dir + '/';
    if (spec.fileRx) {
      mode = 'files:declared';
      for (const f of files) {
        if (prefixOf && !f.r.startsWith(prefixOf)) continue;
        const rest = f.r.slice(prefixOf.length);
        if (!rest || rest.includes('/')) continue;
        const b = path.posix.basename(rest);
        if (spec.fileRx.test(b)) addJson(spec.key(b), f.p, splitKey(path.posix.basename(b, '.json')).agg);
      }
    } else if (spec.dirRx || spec.dirs) {
      // 声明的目录名（可散落在书内任意层），dirs 与 ignore 的键都算候选目录
      const names = Object.keys(spec.dirs || {}).concat(Object.keys(spec.ignore || {}));
      const rx = spec.dirRx || new RegExp('^(' + names.map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')$');
      const dirs = {};
      for (const f of files) {
        const parts = f.r.split('/');
        for (let i = 0; i < parts.length - 1; i++) {
          if (!rx.test(parts[i]) || SHADOW.test('/' + parts.slice(0, i + 1).join('/'))) continue;
          const d = parts.slice(0, i + 1).join('/');
          (dirs[d] = dirs[d] || []).push(f);
        }
      }
      prefixOf = '';
      for (const [d, fs2] of Object.entries(dirs)) {
        for (const f of fs2) if (/\.json$/i.test(f.r)) place(path.posix.basename(d), f);
      }
      root = '.'; mode = 'dirs:' + Object.keys(dirs).length;
    } else {
      // 单一层根：root 的直接子目录=层（sdr/zp），或 root 内平铺文件=层（mhd）
      const flat = spec.mode === 'files';
      mode = flat ? 'files:declared' : 'subdirs:declared';
      for (const f of files) {
        if (!/\.json$/i.test(f.r) || SHADOW.test(f.r)) continue;
        if (prefixOf && !f.r.startsWith(prefixOf)) continue;
        const rest = f.r.slice(prefixOf.length);
        if (!rest) continue;
        if (flat) { if (rest.includes('/')) continue; place(null, f); }
        else { if (!rest.includes('/')) continue; place(rest.split('/')[0], f); }
      }
    }
  } else {
    candidates = layerRootsProbe(files);
    if (!candidates.length) return { root: null, mode: null, layers: {}, total: 0, totalRegistered: 0, layerCount: 0, registeredCount: 0, unregistered: [], declaredMissing: [...(declared || [])], skipped: 0, skippedAssembly, variants, extras, ignored, mismatch: [], candidates: [], note: '无层根候选（该书可能只有原料，尚未装填）' };
    const chosen = candidates[0];
    root = chosen.d; mode = chosen.codedSubdirs ? 'subdirs' : 'files';
    prefixOf = root === '.' ? '' : root + '/';
    for (const f of chosen.files) {
      if (!/\.json$/i.test(f.r)) continue;
      const rest = f.r.slice(prefixOf.length);
      place(rest.includes('/') ? rest.split('/')[0] : null, f);
    }
  }
  for (const [k, L] of Object.entries(layers)) {
    if (ASSEMBLY_KEY.test(k)) { skippedAssembly.push(k); delete layers[k]; }
  }
  for (const L of Object.values(layers)) {
    // 分卷件优先：聚合件常是派生视图（索引/归一清单），不是层本体。
    // 两者同存且不等时，取分卷件，并把聚合值留给人工判定。
    L.records = L.shards ? L.shardRecords : L.aggRecords;
    L.basis = L.shards && L.aggs
      ? (L.shardRecords === L.aggRecords ? 'shards=aggregate' : 'shards（聚合件=' + L.aggRecords + '，需人工判定）')
      : (L.shards ? 'shards' : (L.aggs ? 'aggregate-only' : 'none'));
    if (L.shards && L.aggs && L.shardRecords !== L.aggRecords) L.agg_mismatch = { shards: L.shardRecords, aggregate: L.aggRecords };
    delete L.counted;
  }
  const total = Object.values(layers).reduce((a, x) => a + x.records, 0);
  const skipped = Object.values(layers).reduce((a, x) => a + x.skipped, 0);
  const mismatch = Object.entries(layers).filter(([, L]) => L.agg_mismatch).map(([k, L]) => k + ' 分卷' + L.shardRecords + '≠聚合' + L.aggRecords);
  // 按 data.js 注册层分账：registered 计入 totalRegistered，unregistered 单列（不静默丢弃、也不静默计入）
  let unregistered = [], declaredMissing = [], totalRegistered = total, registeredCount = Object.keys(layers).length;
  if (declared) {   // 空集也算声明：data.js 说这本书没有层（兵志试点），盘上有层件就是未注册
    for (const [k, L] of Object.entries(layers)) {
      L.registered = declared.has(k);
      if (!L.registered) unregistered.push({ layer: k, records: L.records, basis: L.basis });
    }
    unregistered.sort((a, b) => b.records - a.records);
    const reg = Object.entries(layers).filter(([, L]) => L.registered);
    totalRegistered = reg.reduce((a, [, L]) => a + L.records, 0);
    registeredCount = reg.length;
    declaredMissing = [...declared].filter(k => !(k in layers));
  }
  return { root, mode, layers, total, totalRegistered, layerCount: Object.keys(layers).length,
    registeredCount, unregistered, declaredMissing,
    skipped, skippedAssembly, variants, extras, ignored, mismatch, candidates: candidates.map(c => c.d) };
}

// ---------- ③ 结构脊柱实测（C9 的卷级可得性 + C8/C9 载体归属）----------
// 1.1 就地载体的必备 meta 键（tools/book_json_augment.py 写的 8 项，实测键名不猜）
const BJ_META_KEYS = ['契约', 'book_id', '著者', '朝代', '体裁', '成书年', '底本版本', '数字化', '条字段'];
const BJ_ID_KEYS = ['著者', '作者'];   // 书上已写「作者」的沿用原键，不建同义键
function collectStructure(files, registry) {
  // 原料是否按卷分文件：_src|_source|assets/sources 下的直属文件名带卷号 → 卷级标记存在
  const srcRoots = {};
  for (const f of files) {
    if (SHADOW.test(f.r)) continue;
    const m = f.r.match(/^(.*(?:^|\/)(?:_src|_source|assets\/sources))\/([^/]+)$/);
    if (!m) continue;
    const root = (srcRoots[m[1]] = srcRoots[m[1]] || { files: 0, volumeMarked: 0 });
    root.files++;
    if (/(?:^|[^0-9])(\d{2,3})(?:[-_.]|$)|^卷|卷[0-9一二三四五六七八九十百]+/.test(m[2])) root.volumeMarked++;
  }
  // 书籍json 整书页：书籍json/ 根下的 *.json（分卷json/ 里的分片不是载体）
  let bookJson = null;
  const bjs = files.filter(f => /(^|\/)书籍json\/[^/]+\.json$/i.test(f.r) && !/\/分卷json\//.test(f.r) && !SHADOW.test(f.r));
  for (const f of bjs) {
    const d = readJson(f.p);
    if (!d || typeof d.meta !== 'object' || d.meta === null) continue;
    const mt = d.meta;
    const absents = [], nullsNoBasis = [];
    for (const k of BJ_META_KEYS) {
      if (!(k in mt) && !(k === '著者' && BJ_ID_KEYS.some(x => x in mt))) { absents.push(k); continue; }
      if (mt[k] === null && !mt[k + '_依据'] && !mt[k + '_来源']) nullsNoBasis.push(k);
    }
    bookJson = {
      file: f.r,
      contract: mt['契约'] || null,
      book_id: mt.book_id || null,
      digitization: mt['数字化'] ? (mt['数字化']['形态'] || '有值') : null,
      punctuation: mt['数字化'] && mt['数字化']['标点形态'] ? mt['数字化']['标点形态'] : null,
      volumes: Array.isArray(d.volumes) ? d.volumes.length : null,
      absentKeys: absents, nullsWithoutBasis: nullsNoBasis,
      lookedFor: bjs.map(x => x.r),
    };
    break;
  }
  return {
    juanFromItemPrefix: registry ? registry.volumeCount : null,
    prefixes: registry ? registry.volumePrefixes : null,
    srcRoots: Object.entries(srcRoots).map(([d, v]) => ({ dir: d, files: v.files, volumeMarked: v.volumeMarked })),
    spineFiles: files.filter(f => /(^|\/)spine(\.source)?\.json$/i.test(f.r) && !SHADOW.test(f.r)).map(f => f.r),
    metaFiles: files.filter(f => /(^|\/)book\.meta\.json$/i.test(f.r) && !SHADOW.test(f.r)).map(f => f.r),
    bookJson,
  };
}

// ---------- ④ 著录取证（C8 的 A 级字段来源）----------
const SRC_PRIORITY = [/(^|\/)_src\//, /(^|\/)_source\//, /(^|\/)assets\/sources\//, /(^|\/)(原文|白话文)\//];
// 报告类文件名不是原料：以 _ 或 . 开头、或名字里带校验/清单/汇总字样
const NOT_SOURCE_NAME = /^[_.]|验证|缺漏|清单|报告|汇总|索引|规范|warn|norms|report|tmp|scratch|说明|(README|SKILL|HANDOFF)\.md$/i;
function collectBiblio(files) {
  const rawExt = f => /\.(txt|epub)$/i.test(f.r);
  const cands = files.filter(f => /\.(txt|json|epub|md|html?)$/i.test(f.r) && !SHADOW.test(f.r)
    && (SRC_PRIORITY.some(rx => rx.test(f.r)) || (path.posix.dirname(f.r) === '.' && rawExt(f)))
    && !NOT_SOURCE_NAME.test(path.posix.basename(f.r)))
    .map(f => { const i = SRC_PRIORITY.findIndex(rx => rx.test(f.r)); return { f, rank: i === -1 ? 9 : i }; })
    .sort((a, b) => (a.rank - b.rank) || (b.f.st.size - a.f.st.size));
  const main = cands[0] && cands[0].f;
  let lines = null;
  if (main && /\.(txt|json|md)$/i.test(main.r)) { try { lines = fs.readFileSync(main.p, 'utf8').split(/\r?\n/).length; } catch (e) { } }
  const epub = files.find(f => /_epub_metadata\.json$/.test(f.r) && !SHADOW.test(f.r));
  const ej = epub ? readJson(epub.p) : null;
  return {
    digitization: main ? {
      file: main.r, format: path.extname(main.r).replace('.', '').toLowerCase(),
      bytes: main.st.size, lines, tier: cands[0].rank === 9 ? 'root' : 'declared',
    } : null,
    sourceCandidates: cands.slice(0, 5).map(x => x.f.r),
    epub: ej ? { title: ej.title, creator: ej.creator, language: ej.language, chapters: ej.total_chapters } : null,
    lookedFor: SRC_PRIORITY.map(r => String(r.source)).concat(['<root>/*.txt|epub']),
  };
}

// ---------- ⑤ 联邦库实测（结构域/知识域在库里的落点）----------
// 联邦库用自己的书码（lgs/xgf/…），与 Summary 的目录码不同名空间；
// 只借用 data.js 里声明的 idMap 做 join，join 不上就如实报 null——这本身是门要抓的一类不一致。
function loadIdMap() {
  try {
    const s = fs.readFileSync(path.join(__dirname, 'data.js'), 'utf8');
    const m = s.match(/idMap:\s*\{([^}]*)\}/);
    if (!m) return {};
    return JSON.parse('{' + m[1].replace(/([\w]+)\s*:/g, '"$1":').replace(/'/g, '"').replace(/,\s*$/, '') + '}');
  } catch (e) { return {}; }
}
function federationSnapshot() {
  const db = path.join(ROOT, 'tools/kb-federation/kb.sqlite');
  if (!fs.existsSync(db)) return {};
  try {
    const { execFileSync } = require('child_process');
    const py = 'import sqlite3,json;c=sqlite3.connect(r' + JSON.stringify(db.split('\\').join('/')) + ');' +
      'g=lambda s:{r[0]:r[1] for r in c.execute("select book_id,count(*) from "+s+" group by book_id")};' +
      // layer_catalog.layer_code 全库 100 行都是 NULL（旧装载只写 layer_key），
      // 按 layer_code 数会恒得 0 → 看板长期谎报「库内 0 层」。注册层以 layer_key 计。
      'out={"volumes":g("volumes"),"items":g("items"),"records":g("records")};' +
      'out["layers"]={r[0]:r[1] for r in c.execute("select book_id,count(distinct layer_key) from layer_catalog group by book_id")};' +
      'out["in_books"]=[r[0] for r in c.execute("select book_id from books")];' +
      'print(json.dumps(out))';
    return JSON.parse(execFileSync('python', ['-Xutf8', '-c', py], { encoding: 'utf8' }).trim());
  } catch (e) { return {}; }
}

// ---------- ⑥ 交付实测（C1 说交付目录只叫 _deliver/，但存量书用三种写法交付）----------
// 判「有没有交付物」不能只看目录名：epub、网页阅读器 html、全卷交付说明都是盘上真实成品。
// 因此分三层报：canonical（_deliver/）/ alias（交付物、成品，C1 明令禁用的别名）/ artifacts（其他成品件）。
const DELIVER_ALIAS = /(^|\/)(交付物|成品)\//;
const DELIVER_ARTIFACT = /(^|\/)([^\/]*\.(epub)|[^\/]*交付(说明|报告)[^\/]*\.(txt|md)|[^\/]*阅读器[^\/]*\.html)$/i;
// 收口报告（使用报告 / 项目总结）：志书类书的「交付」历史上就是交这两份 md，算交付但缺交付目录
const DELIVER_REPORT = /(^|\/)([^\/]*(使用报告|项目总结|收官)[^\/]*\.md)$/i;
function collectDeliver(files) {
  const canonical = [], alias = [], artifacts = [], reports = [];
  for (const f of files) {
    if (/(^|\/)_deliver\//.test(f.r)) { canonical.push(f.r); continue; }
    if (DELIVER_ALIAS.test(f.r)) { alias.push(f.r); continue; }
    if (DELIVER_ARTIFACT.test(f.r)) { artifacts.push(f.r); continue; }
    if (SHADOW.test(f.r)) continue;
    if (DELIVER_REPORT.test(f.r)) reports.push(f.r);
  }
  return {
    canonical: canonical.length ? canonical : null,
    alias: alias.length ? alias : null,
    artifacts: artifacts.length ? artifacts : null,
    reports: reports.length ? reports : null,
    any: !!(canonical.length || alias.length || artifacts.length),
    basis: canonical.length ? '_deliver/（合 C1）' : (alias.length ? '别名目录（C1 禁用）' : (artifacts.length ? '仅成品件，无交付目录' : (reports.length ? '仅收口报告，无交付目录/成品件' : '盘上无任何交付物'))),
  };
}

// ---------- 主流程 ----------
function collect() {
  const fed = federationSnapshot();
  const idMap = loadIdMap();
  const declaredMap = loadDeclaredLayers();
  const out = {};
  for (const [id, rel] of Object.entries(DIRS)) {
    const dir = path.join(ROOT, rel);
    if (!fs.existsSync(dir)) { out[id] = { missing: rel }; continue; }
    const files = [];
    walk(dir, (p, r, st) => files.push({ p, r, st }));
    const registry = collectRegistry(files) || registryFromCarrier(files);
    const spec = LAYER_SPEC[id] || null;
    const layers = collectLayersFor(files, spec, declaredMap[id] || null);
    const code = idMap[id] || id;
    const f = k => (fed && fed[k] && fed[k][code] !== undefined ? fed[k][code] : null);
    const inBooks = !!(fed.in_books && fed.in_books.indexOf(code) >= 0);
    const federation = {
      code,
      in_books: inBooks,
      // volumes/items/records 按 book_id 分组，缺键有两种意思：书没入库，或书在库里但该表零行。
      // 混报成「未入库」会让 fhs/ppy/wz/shz/zgz 这种「入库但没建卷行」的书看起来不用管。
      volumes: f('volumes') !== null ? f('volumes') : (inBooks ? 0 : null),
      items: f('items'), records: f('records'), layers: f('layers'),
    };
    const guessed = Object.values(layers.layers).reduce((a, L) => a + ((L.shapes && L.shapes['longest-array']) || 0), 0);
    const deliver = collectDeliver(files);
    const contracts = {
      kg_enums: files.some(f => /(^|\/)_kg_enums\.py$/.test(f.r)),
      deliver_dir: files.some(f => /(^|\/)(_deliver|交付物|成品)\/./.test(f.r)),
      deliver,
      skill_md: files.some(f => /(^|\/)SKILL\.md$/.test(f.r)),
      validate_dir: files.some(f => /(^|\/)_validate\/./.test(f.r)),
      layer_spec_declared: !!spec,
    };
    const warnings = [];
    if (!registry) warnings.push('无底座指纹库（C3）');
    else if (registry.dominantScheme === 'other') warnings.push('item_id 非 NN-NNN（C2）');
    else if (registry.shadowOnly) warnings.push('底座只存在于影子目录（C3 落点异常）');
    else if (registry.noItemIdCount) warnings.push('底座无 item_id 可解析（C2/C9）');
    if (layers.root === null && !(spec && spec.none)) warnings.push('无层根（未装填？）');
    if (layers.skipped) warnings.push(layers.skipped + ' 个层文件结构未识别');
    if (guessed) warnings.push(guessed + ' 个层文件按最长数组估算记录数');
    if (layers.mismatch && layers.mismatch.length) warnings.push('分卷/聚合双计风险：' + layers.mismatch.join('，'));
    if (layers.unregistered.length) warnings.push('未注册层件 ' + layers.unregistered.length + ' 个（不计入合计）：' +
      layers.unregistered.map(u => u.layer + '=' + u.records).join('，'));
    if (layers.declaredMissing && layers.declaredMissing.length) warnings.push('data.js 声明了但盘上无此层：' + layers.declaredMissing.join('，'));
    if (federation.in_books && federation.records === null) warnings.push('books 登记了但 records 表无行（装载中断？）');
    if (!contracts.kg_enums) warnings.push('无单点 _kg_enums.py（C5）');
    if (!contracts.deliver_dir) warnings.push('无交付目录 _deliver/（C6）');
    if (!contracts.skill_md) warnings.push('无实例 SKILL.md（C7）');
    out[id] = {
      repo_dir: rel,
      fileCount: files.length,
      hasAnyFile: files.length > 0,
      biblio: collectBiblio(files),
      registry,
      structure: collectStructure(files, registry),
      layers,
      contracts,
      spec: spec || null,
      federation,
      warnings,
    };
  }
  out.__federation_all = { codes_in_books: (fed.in_books || []).sort(), id_map: idMap };
  return out;
}

function main() {
  const data = collect();
  fs.writeFileSync(path.join(__dirname, '_meta_out.json'), JSON.stringify(data, null, 1));
  if (process.argv.includes('--json')) { console.log(JSON.stringify(data)); return; }
  const pad = (s, n) => String(s === null || s === undefined || s === '' ? '—' : s).padEnd(n);
  console.log('id   文件  底座条 卷(前缀) 原料                                              |层  层记录 库码 库items 库records 库卷');
  for (const [id, b] of Object.entries(data)) {
    if (id === '__federation_all') continue;
    if (b.missing) { console.log(pad(id, 5), 'MISS ' + b.missing); continue; }
    const r = b.registry || {}, ly = b.layers || {}, dig = (b.biblio || {}).digitization || {}, fe = b.federation || {};
    console.log(pad(id, 5), pad(b.fileCount, 6), pad(r.items, 8), pad(r.volumeCount, 9), pad(dig.file, 46),
      '|', pad(ly.layerCount, 3), pad(ly.total, 7), pad(fe.code, 5), pad(fe.items, 9), pad(fe.records, 9), pad(fe.volumes, 5),
      'sha' + pad(r.registryHash, 17));
    if (b.warnings.length) console.log('        ⚠ ' + b.warnings.join('；'));
  }
  console.log('\n口径：卷(前缀)=底座 item_id 数字前缀去重数（C9 实测卷数）；层根=LAYER_SPEC 声明优先，无声明则由探针首选；' +
    '层记录=该根下各层 JSON 的记录和（影子目录不计；同层既有分卷件又有聚合件且不等时取分卷件，两个口径都写进 layers.*）。');
  console.log('注册口径：层码以 data.js books[].layers 的声明为登记册——盘上有而未登记的进 unregistered，照常测量、不计入 totalRegistered。');
  console.log('库*=联邦库 kb.sqlite 实测；「库码」来自 data.js 声明的 idMap（声明值，仅用于 join）。');
  console.log('注：层根多候选见 layers.candidates；未识别结构见 layers.*.shapes；底座旁挂副本见 registry.others / ignoredShadow。');
}
if (require.main === module) main();
module.exports = { collect, countRecords, collectRegistry, collectLayersFor, layerRootsProbe, SHADOW };
