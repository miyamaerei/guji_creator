// 看板进度刷新对比器：跑采集器 → 与现行 times.js 逐阶段对比 → 只报变化
// 用法：node Skills/progress-dashboard-integration/scripts/diff_times.js
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '../../..');
const HTML = path.join(ROOT, 'Summary/html');

spawnSync(process.execPath, [path.join(HTML, 'collect_times.js')], { cwd: HTML, stdio: 'ignore' });

const raw = JSON.parse(fs.readFileSync(path.join(HTML, '_collect_out.json'), 'utf8'));
const tj = fs.readFileSync(path.join(HTML, 'times.js'), 'utf8');
const GT = eval('(' + tj.match(/window\.GTIMES=(\{.*?\});/s)[1] + ')');
const GV = eval('(' + tj.match(/window\.GVOLS=(\{.*?\});/s)[1] + ')');
fs.unlinkSync(path.join(HTML, '_collect_out.json'));

const NAMES = ['原料', '底座', '装填', '打包', '跨层', '验证', '交付'];
const fmt = ms => ms == null ? '—' : new Date(Math.round(ms)).toISOString().slice(0, 16).replace('T', ' ');
let changed = 0;
console.log('== 阶段时间变化（>1 分钟才报；原料列易被 .txt/.json 污染，慎采） ==');
for (const [id, arr] of Object.entries(raw.GTIMES)) {
  const pipe = [6, 4, 3, 5, 2, 1, 0].map(i => arr[i]);
  const old = GT[id] || [];
  const diffs = [];
  pipe.forEach((ms, i) => { if (Math.abs((old[i] || 0) - (ms || 0)) > 60000) diffs.push(NAMES[i] + ': ' + fmt(old[i]) + ' -> ' + fmt(ms)); });
  if (diffs.length) { changed++; console.log(id.padEnd(4), diffs.join(' | ')); }
}
if (!changed) console.log('(无)');

console.log('\n== 卷计数对比（采集器值 vs times.js 校准值；装填=体积/非空启发，需人工复核） ==');
for (const [id, v] of Object.entries(raw.GVOLS)) {
  const g = GV[id] || {};
  const f = v ? v.fill.length : 0, p = v ? v.pack.length : 0;
  const mark = (g.fill != null && f !== g.fill) || (g.pack != null && p !== g.pack) ? ' *不同*' : '';
  console.log(id.padEnd(4), 'fill 采集' + String(f).padEnd(4) + '登记' + String(g.fill == null ? '-' : g.fill).padEnd(4),
    'pack 采集' + String(p).padEnd(4) + '登记' + String(g.pack == null ? '-' : g.pack) + mark);
}
console.log('\n已知盲区（登记值优先，勿直接覆盖）：mhd 按部门聚合不逐卷打包 / xjz 单文件全卷装填 / yhb 装填直写层文件 / bz 仅卷66试点 / dlz 卷44 真空卷');
