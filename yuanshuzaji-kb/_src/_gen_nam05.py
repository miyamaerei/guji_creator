# -*- coding: utf-8 -*-
"""从《宛署杂记》卷五原文提取铺/坊/胡同/村庄名录，生成 _nam_ai_05.py。
胡同按坊分组；村庄全列。提取后人工核对（胡同应与 312 大致吻合）。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷五.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_05.py'

text = io.open(SRC, encoding='utf-8').read()

# ---------- 1. 十二铺 ----------
pu_text = text[text.index('宛平县凡一十二铺'):text.index('古步递曰邮')]
pu = re.findall(r'至?([^、。，里]+铺)', pu_text)
# 手工核对：县前铺/施仁铺/彰义铺/义井铺/芦沟桥铺/新店铺/高店铺/田家庄铺/黄垡铺/石碑铺/双线铺/胡渠铺
pu = ['县前铺','施仁铺','彰义铺','义井铺','芦沟桥铺','新店铺','高店铺','田家庄铺','黄垡铺','石碑铺','双线铺','胡渠铺']

# ---------- 2. 十三坊 ----------
fang_order = ['朝天日中坊','金城坊','河漕坊','鸣玉坊','阜财坊',
              '大时雍坊','小时雍坊','积庆坊','安富坊',
              '发祥坊','北日中坊',
              '宣南坊','宣北坊']
# 原文有"宣北"未见坊名，宣南宣北合称顺城门外坊

# ---------- 3. 胡同按坊分组 ----------
hu_start = text.index('西城朝天日中坊')
hu_end = text.index('城外村庄共三百二十八处')
hu_text = text[hu_start:hu_end]

def extract_hutong(seg):
    """提取 '曰X'/'日X' 形式的胡同名，去重保序（兼容 OCR 曰→日混写）。"""
    names = re.findall(r'[曰日]([^曰日，。]+)', seg)
    out = []
    for n in names:
        n = n.strip().rstrip('、。')
        if not n:
            continue
        # 去掉"铺不全者系革去"等非名文本
        if n.startswith(('一铺','二铺','三铺','四铺','五铺','六铺','七铺','八铺','九铺','十铺','十一铺','十二铺','十三铺','十四铺','十五铺','十六铺','十七铺','十八铺','铺不全')):
            # 可能是"曰一铺"里带出，跳过
            continue
        if n in ('铺不全者系革去','系革去'):
            continue
        # 拆掉行内坐标词："一牌一铺曰X" -> 前面已被"曰"切
        out.append(n)
    return out

# 分段定位各坊
marks = [
    ('西城朝天日中坊', '金城坊'),
    ('金城坊', '河漕坊'),
    ('河漕坊', '鸣玉坊'),
    ('鸣玉坊', '阜财坊'),
    ('阜财坊', '中城大时雍坊'),
    ('中城大时雍坊', '小时雍坊'),
    ('小时雍坊', '积庆坊'),
    ('积庆坊', '安富坊'),
    ('安富坊', '北城发祥坊'),
    ('北城发祥坊', '北日中坊'),
    ('北日中坊', '南城顺城门外宣南坊'),
    ('南城顺城门外宣南坊', '宣南坊'),
    ('宣南坊', '城外村庄'),
]

segs = {}
for i, (a, b) in enumerate(marks):
    ia = hu_text.index(a)
    ib = hu_text.index(b, ia + 1) if b in hu_text[ia+1:] else len(hu_text)
    segs[a] = hu_text[ia:ib]

hutongs = {}
for a, _ in marks:
    if a in segs:
        hutongs[a] = extract_hutong(segs[a])

# 宣南坊：'城外村庄' 不在 hu_text（hu_end 恰在其起点），('宣南坊','城外村庄') 段
# 已从 '宣南坊' 首现（即 '南城顺城门外宣南坊' 内）覆盖到 hu_text 末尾，无需独立修正。
hutongs['宣南坊'] = extract_hutong(hu_text[hu_text.index('宣南坊'):])

# ---------- 4. 村庄 ----------
v_start = text.index('城外村庄共三百二十八处')
v_end = text.index('按：见行城内各坊')
v_text = text[v_start:v_end]
villages = []
for n in re.findall(r'[曰日]([^曰日，。]+)', v_text):
    n = n.strip().rstrip('、。')
    if n:
        villages.append(n)
# 去重保序
seen = set(); vv = []
for x in villages:
    if x not in seen:
        seen.add(x); vv.append(x)

# ---------- 写出 ----------
def py_str_list(lst):
    return '[' + ',\n                    '.join(repr(x) for x in lst) + ']'

groups = {
    '西城五坊胡同': ('05-002', '西城朝天日中坊金城坊河漕坊鸣玉坊阜财坊胡同', [x for f in ['西城朝天日中坊','金城坊','河漕坊','鸣玉坊','阜财坊'] for x in hutongs.get(f, [])]),
    '中城四坊胡同': ('05-002', '中城大时雍坊小时雍坊积庆坊安富坊胡同', [x for f in ['中城大时雍坊','小时雍坊','积庆坊','安富坊'] for x in hutongs.get(f, [])]),
    '北城二坊胡同': ('05-002', '北城发祥坊北日中坊胡同', [x for f in ['北城发祥坊','北日中坊'] for x in hutongs.get(f, [])]),
    '宣南宣北坊胡同': ('05-002', '南城顺城门外宣南宣北坊胡同', hutongs['宣南坊']),
}

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷五 05-001/05-002：名录谱牒层 AI 判定（铺/坊/胡同/村庄，脚本提取+人工核对）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "05-001",')
lines.append('        "name": "宛平十二铺",')
lines.append('        "category": "其他",')
lines.append('        "scope": "宛平县铺递四道铺舍",')
lines.append('        "entries": ' + py_str_list(pu) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "05-002",')
lines.append('        "name": "宛平城内十三坊",')
lines.append('        "category": "其他",')
lines.append('        "scope": "西城全属宛平，中北南三城与大兴分治",')
lines.append('        "entries": ' + py_str_list(fang_order) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
for label, (iid, name, entries) in groups.items():
    lines.append('    {')
    lines.append('        "item_id": "%s",' % iid)
    lines.append('        "name": "%s",' % name)
    lines.append('        "category": "其他",')
    lines.append('        "scope": "%s",' % label)
    lines.append('        "entries": ' + py_str_list(entries) + ',')
    lines.append('        "ent_ids": [],')
    lines.append('        "confidence": "high",')
    lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "05-002",')
lines.append('        "name": "宛平城外村庄",')
lines.append('        "category": "其他",')
lines.append('        "scope": "城外村庄共三百二十八处，六道分布（南/西南/正西/西北/正北/东北）",')
lines.append('        "entries": ' + py_str_list(vv) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
lines.append('')

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

# 统计
print('十二铺:', len(pu))
print('十三坊:', len(fang_order))
for label, (iid, name, entries) in groups.items():
    print('%s: %d' % (label, len(entries)))
print('村庄(去重):', len(vv), '(原文 328)')
