# -*- coding: utf-8 -*-
"""
南直隶密度检测 + 粗切器（Phase 1：粗测定结构）
工作流：粗切（程序剪刀，只切片不解字段）→ 密度检测（判断结构是否够用）
         → 若要补录太多的字段，则重新定结构；否则进入 AI 精修。

产出：
  ../_data/density_check_06_18.csv   密度检测表（决定是否改结构）
  ../_data/cut_slices_06_18.json     粗切产物（AI 精修的输入）
"""
import re, json, os, csv, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import PATHS, atomic_write_json, atomic_write_text

CN_NUM = r'[一二三四五六七八九十百千万零]+'
SRC = PATHS["source"]

def cn2int(s):
    d = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    if s == '十': return 10
    if '十' in s:
        a, c = s.split('十')
        return (d.get(a, 1) if a else 1) * 10 + (d.get(c, 0) if c else 0)
    return d.get(s, 0)

# ---- 读全文 ----
txt = open(SRC, encoding='utf-8').read()
body = txt[:txt.find('总志之属,大清一统志')]

# ---- 卷边界 ----
marks = [(m.start(), cn2int(m.group(1))) for m in re.finditer(r'明一[统綂]志卷([一二三四五六七八九十百]+)', body)]
seen = {}
for pos, v in marks:
    if v not in seen: seen[v] = pos
vols = sorted(seen.items())

def get_vol(v):
    pos = seen.get(v, -1)
    if pos < 0: return ''
    end = next((p for vv, p in vols if vv == v + 1), len(body))
    return body[pos:end]

# ---- 南直隶 卷6-18 ----
VOL_RANGE = range(6, 19)

# 条目头：府名【 / 州名【 / 京城/南京（metro）
ENTRY_RX = re.compile(r'([\u4e00-\u9fff]{2,4}府|[\u4e00-\u9fff]{2,4}州|京城|南京)【')

# section 标题（南直隶通用 20 门 + 京城专用门）
SEC_TITLES = ['建置沿革', '郡名', '形胜', '风俗', '山川', '土产', '公署', '学校', '书院',
              '宫室', '关梁', '关梁', '寺观', '祠庙', '陵墓', '古迹', '名宦', '流寓',
              '人物', '列女', '仙释', '城池', '坛庙', '山陵', '苑囿',
              '文职公署', '武职公署', '藩封']

def cut_entries(vol_text):
    """只做粗切：按条目头切片，不做字段解析。
    硬判据：真正的府/州条目头，其后 400 字符内必有「建置沿革」。
    metro（京城/南京）无建置沿革，单独识别。
    """
    # 1. metro 条目：卷首都城的独立总述段
    metros = []
    for m in re.finditer(r'\n(京城|南京)\n', vol_text):
        metros.append((m.start(), m.group(1)))
    # 2. 府/州条目头：名字 + 【，且后续 400 字内有「建置沿革」
    #    排除公署子项（五军都督府/宗人府/詹事府等，属京城/南京衙署，非府州）
    BLOCK = ('都督府', '宗人府', '詹事府')
    hits = []
    for m in ENTRY_RX.finditer(vol_text):
        name = m.group(1)
        if name.endswith(BLOCK):
            continue
        window = vol_text[m.start():m.start() + 400]
        if '建置沿革' in window:
            hits.append((m.start(), name))
        elif name in ('京城', '南京') and metros:
            hits.append((m.start(), name))
    hits.sort()
    # 去重：相邻 <200 的头（同名嵌套）
    pruned = []
    for p, n in hits:
        if pruned and p - pruned[-1][0] < 200:
            continue
        pruned.append((p, n))
    out = []
    for i, (p, n) in enumerate(pruned):
        end = pruned[i + 1][0] if i + 1 < len(pruned) else len(vol_text)
        out.append({'name': n, 'start': p, 'end': end, 'text': vol_text[p:end]})
    return out

def density_of(entry_text):
    """条目级密度：命中各 section 标题数 + 关键字段命中。"""
    d = {s: entry_text.count(s) for s in SEC_TITLES}
    d['chars'] = len(entry_text)
    d['has_border_4'] = bool(re.search(r'东至.*西至.*南至.*北至', entry_text))
    d['has_capital'] = bool(re.search(r'至(京师|南京)' + CN_NUM + r'里', entry_text))
    d['households_hits'] = len(re.findall(r'编户(' + CN_NUM + r')里', entry_text))
    d['grain_hit'] = bool(re.search(r'粮(' + CN_NUM + r')', entry_text))
    d['cit_marks'] = len(re.findall(r'【[^】]{1,12}】', entry_text))
    return d

# ---- 执行：南直隶 ----
slices = []
rows = []
for v in VOL_RANGE:
    vt = get_vol(v).replace('　', '')
    ents = cut_entries(vt)
    for e in ents:
        dens = density_of(e['text'])
        slices.append({
            'item_id': '%02d-%03d' % (v, len(slices) + 1),
            'volume': v, 'region': '南直隶',
            'name': e['name'],
            'text_len': len(e['text']),
            'text': e['text'],
        })
        rows.append({
            'item_id': slices[-1]['item_id'], 'volume': v, 'region': '南直隶',
            'name': e['name'], 'chars': dens['chars'],
            'border_4': int(dens['has_border_4']),
            'capital': int(dens['has_capital']),
            'households': dens['households_hits'],
            'grain': int(dens['grain_hit']),
            'cit_marks': dens['cit_marks'],
            'persons': dens['名宦'] + dens['流寓'] + dens['人物'] + dens['列女'] + dens['仙释'],
            'mtn': dens['山川'], 'sites': dens['寺观'] + dens['祠庙'] + dens['陵墓'] + dens['古迹'],
        })

# ---- 密度检测结论 ----
os.makedirs(PATHS['data'], exist_ok=True)
n_total = len(rows)
n_borders = sum(r['border_4'] for r in rows)
n_hh = sum(r['households'] for r in rows)
n_grain = sum(r['grain'] for r in rows)
n_person_sections = sum(1 for r in rows if r['persons'] > 0)
n_sec0 = sum(1 for r in rows if r['mtn'] + r['sites'] == 0)

verdict = {
    'region': '南直隶', 'volumes': '6-18',
    'entries_total': n_total,
    'borders_hit': n_borders,
    'households_records': n_hh,
    'grain_hit': n_grain,
    'person_entries': n_person_sections,
    'no_site_no_mtn_entries': n_sec0,
    'avg_chars': sum(r['chars'] for r in rows) // max(1, n_total),
}

# 判定：若四至/编户/粮 命中过低 → 结构可能不适用（要改），若人物段缺失率高 → 需 AI 补录量大
flags = []
if n_total and n_borders / n_total < 0.5:
    flags.append('LOW_BORDERS: 四至命中率 %.0f%% (<50%%) → 需检查条目头正则' % (100 * n_borders / n_total))
if n_total and n_grain / n_total < 0.5:
    flags.append('LOW_GRAIN: 粮额命中率 %.0f%% (<50%%) → 需检查粮额格式' % (100 * n_grain / n_total))
if n_total and n_sec0 / n_total > 0.3:
    flags.append('LOW_SITE_MTN: %.0f%% 条目无山川/古迹段 → 可能切分错误或条目为特殊体' % (100 * n_sec0 / n_total))

# ---- 落盘 ----
atomic_write_json(os.path.join(PATHS['data'], 'cut_slices_06_18.json'), slices)
atomic_write_text(os.path.join(PATHS['data'], 'density_check_06_18.csv'),
                  'item_id,volume,region,name,chars,border_4,capital,households,grain,cit_marks,persons,mtn,sites\n' +
                  '\n'.join(','.join(str(r[k]) for k in ['item_id', 'volume', 'region', 'name', 'chars',
                                                         'border_4', 'capital', 'households', 'grain',
                                                         'cit_marks', 'persons', 'mtn', 'sites'])
                            for r in rows))

print('=== 南直隶 卷6-18 密度检测 ===')
for k, v in verdict.items():
    print('  %s: %s' % (k, v))
print('--- 结构判定 ---')
if flags:
    for f in flags: print('  ⚠ ' + f)
else:
    print('  ✓ 结构可用，进入 AI 精修')
print('  粗切条目: %d → _data/cut_slices_06_18.json' % n_total)
print('  密度表: _data/density_check_06_18.csv')
