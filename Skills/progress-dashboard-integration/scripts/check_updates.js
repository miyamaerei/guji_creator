// 每书「目录最后更新时间」基线对比器：一眼看出哪些书籍项目自上次记录后动过
// 用法：
//   node check_updates.js            对比 Summary/html/last_seen.json 基线，报有更新的书
//   node check_updates.js --seed     用 git 各书目录最后提交时间初始化基线（新书未提交则记 0）
//   node check_updates.js --update   对比后把当前扫描值写回基线
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const COL = require(path.join(__dirname, '../../../Summary/html/collect_times.js'));
const { DIRS, ROOT, walk } = COL;
const BASE = path.join(ROOT, 'Summary/html/last_seen.json');
const fmt = ms => !ms ? '—' : new Date(ms).toISOString().slice(0, 16).replace('T', ' ');

function scan() {
  const out = {};
  for (const [id, rel] of Object.entries(DIRS)) {
    const dir = path.join(ROOT, rel);
    if (!fs.existsSync(dir)) { out[id] = { max: 0, file: '(目录不存在: ' + rel + ')' }; continue; }
    let max = 0, file = null;
    walk(dir, (p, r, st) => { if (st.mtimeMs > max) { max = st.mtimeMs; file = rel + '/' + r; } });
    out[id] = { max: Math.round(max), file };
  }
  return out;
}

function seedGit() {
  const out = {};
  for (const [id, rel] of Object.entries(DIRS)) {
    let ct = 0;
    try { ct = parseInt(execFileSync('git', ['-C', ROOT, 'log', '-1', '--format=%ct', '--', rel], { encoding: 'utf8' }).trim(), 10) * 1000 || 0; } catch (e) {}
    out[id] = { max: ct, file: ct ? '(git 最后提交)' : '(未入库/无提交记录)' };
  }
  return out;
}

const cur = scan();
if (process.argv.includes('--seed')) {
  fs.writeFileSync(BASE, JSON.stringify({ generated: new Date().toISOString().slice(0, 16).replace('T', ' '), basis: 'git 各目录最后提交', books: seedGit() }, null, 1));
  console.log('基线已按 git 提交时间初始化 → Summary/html/last_seen.json');
} else {
  let base = {};
  try { base = JSON.parse(fs.readFileSync(BASE, 'utf8')).books || {}; } catch (e) { console.log('无基线文件，先跑 --seed 或 --update'); process.exit(0); }
  const upd = [];
  for (const id of Object.keys(cur)) {
    const b = base[id] ? base[id].max : 0;
    if (cur[id].max > b + 60000) upd.push(id);
  }
  if (!upd.length) console.log('自上次基线以来，所有书籍目录均无文件更新。');
  for (const id of upd) {
    const b = base[id] ? base[id].max : 0;
    const newer = [];
    walk(path.join(ROOT, DIRS[id]), (p, r, st) => { if (st.mtimeMs > b + 60000) newer.push([r, st.mtimeMs]); }, path.join(ROOT, DIRS[id]), 0);
    newer.sort((x, y) => y[1] - x[1]);
    console.log(id.padEnd(4), '有更新:', fmt(b), '→', fmt(cur[id].max), '（新改动 ' + newer.length + ' 个文件，最新:', newer.slice(0, 3).map(x => x[0]).join(', ') + (newer.length > 3 ? ' …' : '') + '）');
  }
  if (upd.length) console.log('\n对上面列出的书：核盘卷数/层计数 → 刷新 times.js & data.js（见 SKILL.md 例行刷新）。');
  if (process.argv.includes('--update')) {
    fs.writeFileSync(BASE, JSON.stringify({ generated: new Date().toISOString().slice(0, 16).replace('T', ' '), basis: '目录文件 mtime 扫描', books: cur }, null, 1));
    console.log('基线已更新为当前扫描值。');
  }
}
