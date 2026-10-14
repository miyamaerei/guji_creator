// 采集器 V2：阶段执行时间（优先匹配分类）+ 卷进度（装填/打包非空判定）
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');

const DIRS = {
  kzz:'kezuozhuiyu-kb', wzz:'wuzazu-kb', sdr:'shuidongriji-kb', xgg:'xinguanguifan-kb',
  qb:'qubian_kb', fhs:'fuhuiquanshu-kb', ppy:'pingpingyan-kb', lgsz:'shizhenglu-kb',
  zxl:'xuezhenglu-kb', wz:'yuanshuzaji-kb', zgz:'mingshi/mingshi-zhiguanzhi',
  xjz:'mingshi/mingshi-xuanju', mhd:'minghuidian', yhb:'wanliyehuopian-kb',
  xjy:'xianjinyifeng-kb', shz:'mingshi/mingshi-shihuozhi', dlz:'mingshi/mingshi-dilizhi',
  bz:'mingshi/mingshi-bingzhi', scm:'songchuangmengyu-kb', zp:'zhipu-kb',
  xf:'mingshi/mingshi-xingfa',
};

// 阶段优先顺序：交付 > 验证 > 跨层 > 装填 > 底座 > 打包 > 原料（首个命中即归类）
const STAGES = [
  /(^|\/)(_deliver\/|交付物\/|交付报告|交付说明|全量交付)/,
  /(^|\/)(_validate\/|reports\/|验证|验收)/,
  /_kg_join|跨层索引/,
  /_src\/|(_ai_\d+|_vol_\d+|_procs_ai|_struct_ai)[^\/]*\.py|annotate[^\/]*\.py|_extract\/layers\/|_ai\/|新官轨范_[^\/]*_ai\//,
  /_item_registry\.json|_extract\//,
  /_layers\/|(^|\/)data\/(?!_)[a-z_]+\/|归一_|_标注|_kg_\d+\.json/,
  /assets\/sources\/|_source\/|原文\/|白话文\/|\.(txt|json|epub)$/i,
];

function walk(root, cb, dir, depth) {
  dir = dir || root; depth = depth || 0;
  if (depth > 6) return;
  let ents;
  try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return; }
  for (const en of ents) {
    if (en.name.startsWith('__') || en.name.startsWith('.')) continue;
    if (/node_modules|vendor/.test(en.name)) continue;
    const p = path.join(dir, en.name);
    if (en.isDirectory()) { walk(root, cb, p, depth + 1); continue; }
    let st; try { st = fs.statSync(p); } catch (e) { continue; }
    cb(p, path.relative(root, p).replace(/\\/g, '/'), st);
  }
}

// 文件名里抽卷号
function volOf(base) {
  let m = base.match(/_(\d{1,3})\.py$/) || base.match(/_?(\d{1,3})\.json$/) || base.match(/^(\d{1,3})_/);
  if (m) { const n = +m[1]; return n <= 200 ? n : null; }
  return null;
}

function jsonNonEmpty(p) {
  try {
    const j = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (Array.isArray(j)) return j.length > 0;
    if (j && Array.isArray(j.records)) return j.records.length > 0;
    if (j && typeof j === 'object') return Object.keys(j).length > 0;
    return false;
  } catch (e) { return fs.statSync(p).size > 800; }
}

const GTIMES = {}, GVOLS = {};
function main() {
for (const [id, rel0] of Object.entries(DIRS)) {
  const dir = path.join(ROOT, rel0);
  if (!fs.existsSync(dir)) { GTIMES[id] = Array(7).fill(null); GVOLS[id] = null; continue; }
  const stageMax = Array(7).fill(null);
  const files = [];
  walk(dir, (p, r, st) => {
    for (let i = 0; i < STAGES.length; i++) {
      if (STAGES[i].test(r)) { if (stageMax[i] === null || st.mtimeMs > stageMax[i]) stageMax[i] = st.mtimeMs; break; }
    }
    files.push([p, r, st]);
  });
  GTIMES[id] = stageMax;

  // 卷进度：装填=填充源文件（体积>800B 或 json 非空）；打包=层成品 json records 非空
  const fillV = new Set(), packV = new Set();
  for (const [p, r, st] of files) {
    const v = volOf(r.split('/').pop());
    if (v === null || v === 0) continue;
    if (/_src\/|_ai_|_vol_|_extract\/layers\//.test(r)) {
      const ok = st.size > 800 || (/\.json$/.test(r) && jsonNonEmpty(p));
      if (ok) fillV.add(v);
    } else if (/_layers\/|(?:^|\/)data\/(?!_)[a-z_]+\/|归一_|_kg_\d+\.json/.test(r)) {
      if (/\.json$/.test(r) && jsonNonEmpty(p)) packV.add(v);
    }
  }
  GVOLS[id] = { fill: [...fillV].sort((a, b) => a - b), pack: [...packV].sort((a, b) => a - b) };
}

// 汇总打印：卷号集合压缩成区间串
const brief = arr => {
  if (!arr || !arr.length) return '-';
  const s = [...arr].sort((a, b) => a - b); const out = []; let a = s[0], b = s[0];
  for (let i = 1; i < s.length; i++) { if (s[i] === b + 1) b = s[i]; else { out.push(a === b ? a : a + '-' + b); a = b = s[i]; } }
  out.push(a === b ? a : a + '-' + b);
  return out.join(',') + ' (n=' + s.length + ',max=' + b + ')';
};
const fmt = ms => ms == null ? '—' : new Date(ms).toISOString().slice(0, 16).replace('T', ' ');
for (const id of Object.keys(DIRS)) {
  console.log(id.padEnd(4), '| fill:', brief(GVOLS[id] && GVOLS[id].fill).padEnd(22),
    '| pack:', brief(GVOLS[id] && GVOLS[id].pack).padEnd(22),
    '|', GTIMES[id].map(fmt).join(' | '));
}
fs.writeFileSync(path.join(__dirname, '_collect_out.json'), JSON.stringify({ GTIMES, GVOLS }, null, 1));
}
if (require.main === module) main();
module.exports = { DIRS, ROOT, walk, volOf, jsonNonEmpty };
