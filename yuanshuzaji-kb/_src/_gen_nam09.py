# -*- coding: utf-8 -*-
"""从《宛署杂记》卷九原文提取万历十八年审编马头名册 + 马色，生成 _nam_ai_09.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷九.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_09.py'

text = io.open(SRC, encoding='utf-8').read()

# ---- 1. 万历十八年审编马头四百四十一名（图/关/社/屯分组 + 人名） ----
ma_start = text.index('德胜关一十五名')
ma_end = text.index('如遇外州县解到官马')
ma_text = text[ma_start:ma_end]
groups = re.findall(r'([^。]+?[一二三四五六七八九十百]+名)[：:]([^。]*)', ma_text)
entries = []
for gname, names in groups:
    gname = gname.strip('，。\n ')
    names = names.strip('\n ')
    if gname and names:
        entries.append('%s：%s' % (gname, names))

# ---- 2. 马色二十五种 ----
se_start = text.index('曰银騔')
se_end = text.index('计二十五种')
se_text = text[se_start:se_end]
ma_colors = [x.strip('，、') for x in re.findall(r'[曰、]([^曰、，。]+)', '曰' + se_text)]

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷九 09-001：名录谱牒层 AI 判定（马头名册/马色，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "09-001",')
lines.append('        "name": "万历十八年审编宛平马头名册",')
lines.append('        "category": "其他",')
lines.append('        "scope": "宛平养马户四百四十一名，按坊图屯社分计",')
lines.append('        "entries": ' + repr(entries) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "09-001",')
lines.append('        "name": "马色二十五种",')
lines.append('        "category": "其他",')
lines.append('        "scope": "别马以色之目，凡二十五种",')
lines.append('        "entries": ' + repr(ma_colors) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('马头分组:', len(entries))
print('马色:', len(ma_colors), ma_colors)
