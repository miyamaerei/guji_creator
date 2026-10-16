// Summary 归一门：声明值（md / data.js / times.js）↔ 盘上真值（collect_meta.js）逐字段对比
// 用法：node Skills/progress-dashboard-integration/scripts/check_summary.js        → 打印分级报告，ERR>0 时退出码 1
//      node ... --only wzz,mhd                                                    → 只查这几本
//
// 分级：
//   ERR  = 声明与实测矛盾到会让看板说假话（条数/层数/状态对不上、books 登记了却没入库数据）
//   WARN = 口径分歧但两处都能自圆（分卷件 vs 聚合件、卷数三种来源不等）
//   INFO = 已知例外/回填待做（C8/C9 未回填、存量书无单点枚举）
// 纪律：本脚本只读，不改任何声明文件；报告列出的每一条都要人工归一到 Summary 里。
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const HTML = path.join(ROOT, 'Summary/html');
const { collect } = require(path.join(HTML, 'collect_meta.js'));

// ---------- 声明值读取（照看板的老办法：正则取出对象字面量再 eval）----------
function evalGlobal(file, name) {
  const s = fs.readFileSync(path.join(HTML, file), 'utf8');
  const m = s.match(new RegExp('window\\.' + name + '\\s*=\\s*(\\{.*?\\});', 's'));
  if (!m) throw new Error(file + ' 里找不到 window.' + name);
  return eval('(' + m[1] + ')');
}
function readText(p) { return fs.readFileSync(p, 'utf8'); }
// 01_书目总览.md 的一览表按表头认列，不按固定下标（列增减都要改下标的做法已经错过一次：
// 加「卷数」列后老代码把卷数当成底座条目，两家比出一堆假 ERR）
const OV_COLS = { seq: /^#$/, dir: /^目录$/, title: /^书名$/, status: /^状态$/,
  layers: /^层数$/, juans: /^卷数$/, items: /^底座条目$/, records: /^(产出)?记录数/ };
function overviewTable() {
  const rows = {}; let idx = null;
  for (const line of readText(path.join(ROOT, 'Summary/01_书目总览.md')).split(/\r?\n/)) {
    if (!/^\|/.test(line)) { idx = null; continue; }
    const c = line.split('|').slice(1, -1).map(x => x.trim().replace(/`/g, ''));
    if (/^\|[\s-|]+$/.test(line)) continue;
    if (!idx) {                                     // 表头行：认出各字段落在第几列
      const found = {};
      c.forEach((h, i) => { for (const [k, rx] of Object.entries(OV_COLS)) if (rx.test(h)) found[k] = i; });
      if (found.dir !== undefined) idx = found;
      continue;
    }
    if (!/^\d+$/.test(c[idx.seq] ?? '')) continue;   // 数据行 # 列必须是数字（支撑目录表不算）
    const get = k => (idx[k] === undefined ? '' : c[idx[k]]);
    rows[get('dir').replace(/\/$/, '')] = { seq: get('seq'), dir: get('dir'), title: get('title'),
      status: get('status'), layers: get('layers'), juans: get('juans'), items: get('items'), records: get('records') };
  }
  return rows;
}
const num = s => { const m = String(s).replace(/,/g, '').match(/\d+/); return m ? Number(m[0]) : null; };
// Summary/02_各书产出层.md：### N. 《书名》<dir> —— X 层，随后 | 层 | 含义 | 记录数 | 表
// 该表的层名是中文描述（不一定等于盘上层码），所以只比两个口径无关的量：行数（层数）与记录数之和
function md02Table() {
  const out = {}; let cur = null;
  for (const line of readText(path.join(ROOT, 'Summary/02_各书产出层.md')).split(/\r?\n/)) {
    const h = line.match(/^###\s*\d+\.\s*《[^》]*》\s*(\S+)\s*[—-]{1,2}\s*(.*)$/);
    if (h) { cur = h[1].replace(/\/$/, ''); out[cur] = { headerLayers: num(h[2]), rows: [], sum: 0 }; continue; }
    if (!cur) continue;
    if (!/^\|/.test(line) || /^\|[\s-|]+$/.test(line)) continue;
    const c = line.split('|').slice(1, -1).map(x => x.trim());
    if (c.length < 3) continue;
    const head = c[2].match(/^([\d,]+)/);
    const n = head ? Number(head[1].replace(/,/g, '')) : null;
    if (n === null) continue;
    out[cur].rows.push({ label: c[0], count: n }); out[cur].sum += n;
  }
  return out;
}
// data.js 的层数组有两代写法：老书 [层码, 层名, 条数]，新书 {layer, count, covered}
function normLayers(b) {
  return (b.layers || []).map(L => Array.isArray(L)
    ? { code: L[0], name: L[1], count: num(L[2]) }
    : { code: L.layer, name: L.name || L.layer, count: num(L.count), covered: L.covered });
}

function main() {
  const only = (() => { const i = process.argv.indexOf('--only'); return i > 0 ? process.argv[i + 1].split(',') : null; })();
  const meas = collect();
  const DATA = evalGlobal('data.js', 'GDATA');
  const TJ = evalGlobal('times.js', 'GVOLS');
  const OV = overviewTable();
  const M2 = md02Table();
  const rows = [];
  const add = (lv, id, field, decl, real, note) => rows.push({ lv, id, field, decl, real, note });

  // ① 每本书：底座条数 / 层数 / 记录数 / 卷数 / 状态
  for (const b of DATA.books) {
    const id = b.id;
    if (only && only.indexOf(id) < 0) continue;
    const m = meas[id];
    if (!m || m.missing) { add('ERR', id, '目录', b.dir, '缺失', m && m.missing || 'DIRS 里没有这本'); continue; }
    const declItems = num(b.items);
    if (!m.registry) {
      if (declItems !== null) add('WARN', id, '底座条数', b.items, '盘上无 _item_registry.json', 'C3 未落盘：声明值无从校验（不是假话，是缺口）');
    } else if (declItems !== m.registry.items) {
      // 载体来源单独判：书籍json 的「条」是著录粒度（每卷可并 1 条），与 data.js 记的段数本就两口径
      add(declItems === null || m.registry.fromCarrier ? 'WARN' : 'ERR', id, '底座条数', b.items,
        m.registry.items + ' 条（' + m.registry.file + '）',
        m.registry.fromCarrier
          ? '条数取自 书籍json 载体（盘上无 _item_registry.json）——载体条=著录粒度，与声明的分段数是两回事；要对齐先重建载体或落 registry'
          : 'data.js 声明 vs 底座实测对不上');
    } else if (m.registry.fromCarrier) {
      add('INFO', id, '底座来源', '_item_registry.json', '条数取自 书籍json 载体（' + m.registry.file + '）', '§6b 就地路线：切条库就在载体里，C3 落点豁免');
    }
    const decl = normLayers(b);
    const declLayerSum = decl.reduce((a, L) => a + (L.count || 0), 0);
    // 记录数合计只与「注册层」实测比：data.js 没登记的层件不进合计（门另行为它们亮 WARN）
    const reg = Object.values(m.layers.layers).filter(L => L.registered !== false);
    const real = reg.reduce((a, L) => a + L.records, 0);
    const shards = reg.reduce((a, L) => a + L.shardRecords, 0);
    const aggs = reg.reduce((a, L) => a + L.aggRecords, 0);
    if (declLayerSum !== real) {
      add(shards === declLayerSum || aggs === declLayerSum ? 'WARN' : 'ERR', id, '记录数合计', declLayerSum, real,
        '分卷件=' + shards + '，聚合件=' + aggs + '，盘上全量（含未注册）=' + m.layers.total + '（两口径都不合才是真错）');
    }
    const unreg = m.layers.unregistered || [];
    if (unreg.length) {
      add('WARN', id, '未注册层件', 'data.js 无此层', unreg.map(u => u.layer + '=' + u.records).join('，'),
        '盘上是层件、data.js 未登记，故不计入合计：要么补进 layers[]，要么在该书 drift 里写明为何不注册');
    }
    const dmiss = m.layers.declaredMissing || [];
    if (dmiss.length) add('ERR', id, '声明层盘上无', dmiss.join('，'), '层根实测 ' + Object.keys(m.layers.layers).join('，'), 'data.js 声明了盘上不存在的层码');
    if (decl.length !== m.layers.registeredCount) {
      const extra = Object.keys(m.layers.layers).filter(k => !decl.some(L => L.code === k));
      add('WARN', id, '层数', decl.length, m.layers.registeredCount,
        '未注册 [' + extra.join(',') + ']；层根实测 ' + m.layers.layerCount + ' 桶');
    }
    // 逐层记录数（只比同名层）
    for (const L of decl) {
      const R = m.layers.layers[L.code];
      if (!R) continue;
      if (L.count === null) { add('WARN', id, '层 ' + L.code, '非数字声明', '分卷' + R.shardRecords + '/聚合' + R.aggRecords, 'data.js 该层条目写法不是纯数字'); continue; }
      if (R.records !== L.count && R.aggRecords !== L.count) {
        add('ERR', id, '层 ' + L.code, L.count, '分卷' + R.shardRecords + '/聚合' + R.aggRecords, dataLayerName(L));
      }
    }
    // 卷数三口径：times.js 登记 total / 底座 item_id 前缀 / 联邦 volumes 表
    // 前缀多出来的段通常不是「丢了几卷」而是卷首/序/后记/校记——所以判定看「正文 01..total 是否全覆盖」
    const g = TJ[id] || {};
    const prefs = (m.registry && m.registry.volumePrefixes) || [];
    const realJuan = m.registry ? m.registry.volumeCount : null;
    if (g.total != null) {
      const need = []; for (let i = 1; i <= g.total; i++) need.push(String(i).padStart(2, '0'));
      const missJuan = need.filter(p => prefs.indexOf(p) < 0);
      const extras = prefs.filter(p => need.indexOf(p) < 0);
      const fedV = m.federation.in_books ? (m.federation.volumes || 0) : null;
      if (realJuan === null) add('INFO', id, '卷数', 'times.js total=' + g.total, '盘上无底座或非 NN-NNN', '卷数不可由前缀推，以著录口径为准');
      else if (g.total === realJuan) {
        // 书已入库但 volumes 零行 ≠ 「三口径一致」：卷维在库里是空的，按卷查询会查无此卷
        if (fedV === 0) add('WARN', id, '卷数', 'times.js total=' + g.total, '底座前缀=' + realJuan + '，联邦 volumes=0（已入库未建卷行）',
          'items/records 已入库但 volumes 表零行 → 卷维待 volumes.py 补跑');
        else add('INFO', id, '卷数', 'times.js total=' + g.total, '底座前缀=' + realJuan + '，联邦 volumes=' + (fedV === null ? '未入库' : fedV), '三口径一致');
      }
      else if (g.prefixBasis) add('INFO', id, '卷数', 'times.js total=' + g.total, '底座前缀=' + realJuan, 'times.js 已声明前缀口径「' + g.prefixBasis + '」，卷数以著录为准');
      else if (!missJuan.length) add('INFO', id, '卷数', 'times.js total=' + g.total, '底座前缀=' + realJuan + '（正文 01–' + need[need.length - 1] + ' 全覆盖）',
        '盘上另有非正文段 [' + extras.join(',') + ']（卷首/序/后记/校记一类），著录不计卷——两口径本就差这些段');
      else add('WARN', id, '卷数', 'times.js total=' + g.total, '底座前缀=' + realJuan + '，缺正文卷段 [' + missJuan.join(',') + ']，多余 [' + extras.join(',') + ']',
        '两个数说不圆：要么改 times.js，要么修底座 item_id 前缀');
    }
    // 状态 vs 实测阶段
    const st = b.stageStates || [];
    const dv = m.contracts.deliver || {};
    if (st[3] === 2 && m.layers.total === 0) add('ERR', id, '状态·层成品打包', '完成(2)', '层记录 0', '说完成但盘上没有层产物');
    if (st[6] === 2) {
      if (!dv.canonical && !dv.alias && !dv.artifacts && !dv.reports) add('ERR', id, '状态·交付', '完成(2)', '盘上无任何交付物', '说已交付但既无 _deliver/、也无成品件/交付说明/收口报告');
      else if (!dv.canonical) add('WARN', id, '状态·交付', '完成(2)', dv.basis, '交付物实为 ' + ((dv.alias || dv.artifacts || dv.reports || []).slice(0, 2).join('，')) + '（C1 要求落 _deliver/）');
    } else if (dv.canonical) add('INFO', id, '状态·交付', '未完成(' + st[6] + ')', '_deliver/ 已存在', '盘上已交付，状态位落后');
    if (m.federation.in_books && m.federation.records === null) add('ERR', id, '联邦入库', 'books 已登记', 'records 表 0 行', '入库中断');
    // 第 8 段（联邦入库）声明 vs 库里有没有这本书
    const fedDecl = (b.stageStates || [])[7];
    if (fedDecl === undefined) add('WARN', id, '状态·联邦入库', 'stageStates 只有 7 段', '看板 stages 有 8 段', '第 8 段缺位，前端补 0=未做——入库状态在看板上不可见');
    else if (m.federation.in_books && fedDecl !== 2) add('ERR', id, '状态·联邦入库', '未做/在建(' + fedDecl + ')', '库里有：records ' + m.federation.records + ' 行', '已入库却写未做');
    else if (!m.federation.in_books && fedDecl === 2) add('ERR', id, '状态·联邦入库', '完成(2)', 'books 表无此码', '说入库了但库里没有');
    // 01 表 vs data.js 的相互一致性（同书两处声明）
    const ov = OV[b.dir] || Object.values(OV).find(r => r.dir.replace(/\/$/, '') === b.dir);
    if (ov) {
      if (num(ov.items) !== null && num(ov.items) !== declItems) add('ERR', id, '底座条数(01表)', ov.items, 'data.js ' + b.items, '同一本书两份声明不等');
      if (num(ov.layers) !== null && num(ov.layers) !== decl.length) add('WARN', id, '层数(01表)', ov.layers, 'data.js ' + decl.length, '含「N 类」「方案N」等非数字口径');
      if (num(ov.records) !== null && num(ov.records) !== declLayerSum) add('WARN', id, '记录数(01表)', ov.records, 'data.js ' + declLayerSum, '');
      const ovj = num(ov.juans);
      if (ovj !== null) {
        const cmpTo = g.total == null ? realJuan : g.total;
        if (cmpTo === null || cmpTo === undefined) add('INFO', id, '卷数(01表)', ov.juans, 'times.js 未登记，盘上也无 NN-NNN 底座',
          '卷数只有 01 表一处声明（该书无结构化产出），无从对比');
        else if (ovj !== cmpTo) add('ERR', id, '卷数(01表)', ov.juans,
          'times.js ' + (g.total == null ? '未登记' : g.total) + '，底座前缀=' + realJuan, '同一本书两份声明不等');
      }
    } else add('INFO', id, '01 表', '缺行', '', b.dir + ' 不在一览表里');
    // 02 表（逐层记录数）vs data.js vs 盘上——三方对齐才算归一
    const t2 = M2[b.dir];
    if (t2) {
      if (t2.headerLayers !== null && t2.headerLayers !== decl.length) add('WARN', id, '层数(02表)', t2.headerLayers + ' 层', 'data.js ' + decl.length + ' 层，盘上注册 ' + m.layers.registeredCount + ' 层', '');
      // 02 表逐行列的是注册层，口径与 data.js 相同；与盘上全量不同只说明它把未注册层件也抄进来了
      if (t2.rows.length && t2.sum !== declLayerSum) {
        const allSum = m.layers.total;
        const lv = (t2.sum === real || t2.sum === allSum || declLayerSum === real) ? 'ERR' : 'WARN';
        add(lv, id, '记录数(02表)', t2.sum, 'data.js ' + declLayerSum + '，盘上注册 ' + real + '（全量 ' + allSum + '）',
          t2.sum === allSum && real !== allSum ? '02 表把未注册层件也列了 → 与 data.js 口径不同'
            : (declLayerSum === real ? 'data.js 与盘上一致 → 02 表陈旧' : '两处声明都不合盘上实测'));
      }
    } else add('INFO', id, '02 表', '缺节', '', b.dir + ' 不在 02_各书产出层.md 里');
    // C8/C9 载体归属（contract.json v0.3.0：新书 book.meta.json / 存量就地补 书籍json；spine 只给需要条内定位的书）
    const S = m.structure, BJ = S.bookJson;
    if (S.metaFiles.length && BJ) add('ERR', id, 'C8 载体', 'book.meta.json + 书籍json 并存', '同一事实两份真源', 'C8.carriers.ban：二选一，删掉一份（存量留 书籍json，新书留 book.meta.json）');
    if (!S.metaFiles.length) {
      if (BJ) {
        if (BJ.contract === null) add('INFO', id, 'C8 著录', '未回填', '整书页在场但 meta 无「契约」键（augment 未跑过）', BJ.file + '——本轮刻意跳过的书即此形，不是缺陷');
        else {
          if (BJ.contract !== 'book-json/1.1') add('WARN', id, 'C8 载体(1.1)', '契约键=' + BJ.contract, '应为 book-json/1.1', BJ.file + '——重跑 tools/book_json_augment.py');
          if (BJ.absentKeys.length) add('WARN', id, 'C8 载体(1.1)', '缺键 ' + BJ.absentKeys.join('/'), '就地补未齐 8 项', BJ.file + '——重跑 tools/book_json_augment.py 幂等补齐');
          if (BJ.nullsWithoutBasis.length) add('WARN', id, 'C8 null_basis', BJ.nullsWithoutBasis.join('/'), '值为 null 但无 _依据/_来源', 'meta_null_basis：每个 null 都要给理由，区分「没查」与「底本没有」');
        }
      } else add('INFO', id, 'C8 著录', '未回填', '既无 book.meta.json 也无 书籍json meta 块', '新书按 C8 建 book.meta.json；存量按 carriers.stock 就地补');
    }
    if (!S.spineFiles.length) {
      add('INFO', id, 'C9 结构', '无 spine.json',
        BJ ? '载体=书籍json（书→卷→条 ' + (BJ.volumes === null ? '?' : BJ.volumes) + ' 卷就地）' : '无结构载体',
        BJ ? '按 C9.scope.do_not_build，只到卷级即豁免；若该书需条内定位（篇/章/段/句），先在 Phase ② 登记 declared_depth 再建 spine'
           : '新书 Phase ③ 底座切完即生成 spine.json');
    }
    if (m.registry && m.registry.dominantScheme === 'other') add('WARN', id, 'C2 item_id', 'NN-NNN', m.registry.dominantScheme + ' 为主', m.registry.file);
    if (m.registry && m.registry.shadowOnly) add('WARN', id, 'C3 底座落点', '_item_registry.json 在实例根', m.registry.file, '底座住在影子目录：数值真实但落点违 C1/C3，待迁移');
  }

  // ② 联邦库码 ↔ data.js idMap
  const all = meas.__federation_all || {};
  for (const code of (all.codes_in_books || [])) {
    if (!Object.values(all.id_map || {}).includes(code)) add('WARN', 'federation', '书码', 'idMap 未含 ' + code, '库里有', 'data.js idMap 需补该映射');
  }
  for (const [id, code] of Object.entries(all.id_map || {})) {
    if ((all.codes_in_books || []).indexOf(code) < 0) add('INFO', id, '书码', 'idMap=' + code, 'books 表无此码', '未入库，属正常在建');
  }

  print(rows);
  return rows.filter(r => r.lv === 'ERR').length ? 1 : 0;
}
function dataLayerName(L) { return 'data.js 该层名「' + L.name + '」'; }
function print(rows) {
  const by = lv => rows.filter(r => r.lv === lv);
  console.log('实测（collect_meta.js）对声明（Summary/01 + data.js + times.js）\n');
  for (const [lv, label] of [['ERR', '硬不一致——看板正在说假话'], ['WARN', '口径分歧——需要归一写法'], ['INFO', '已知例外 / 待回填']]) {
    const list = by(lv);
    console.log('== ' + lv + '（' + list.length + '）' + label);
    for (const r of list) {
      console.log('  ' + String(r.id).padEnd(5) + String(r.field).padEnd(16) +
        ' 声明 ' + String(r.decl).padEnd(22) + ' 实测 ' + String(r.real) + (r.note ? '\n' + '       ↳ ' + r.note : ''));
    }
    console.log('');
  }
  console.log('合计：ERR ' + by('ERR').length + ' / WARN ' + by('WARN').length + ' / INFO ' + by('INFO').length);
}
if (require.main === module) process.exit(main());
module.exports = { main, evalGlobal, overviewTable, md02Table, normLayers };
