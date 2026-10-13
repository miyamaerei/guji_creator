# -*- coding: utf-8 -*-
"""从《宛署杂记》卷十三原文提取万历十六年审编行银坊户细目，生成 _nam_ai_13.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷十三.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_13.py'

text = io.open(SRC, encoding='utf-8').read()

n_start = text.index('奉差科道遵照审编')
n_end = text.index('较之先年，约少银一半')
n_text = text[n_start:n_end]

entries = []
for m in re.finditer(r'([^。；]+?坊|关)(?:该银|银)([^：:]+)[：:]([^。]*)', n_text):
    seg = m.group(0).strip('，。\n ')
    if seg and '户' in seg:
        entries.append(seg)
for m in re.finditer(r'(宛平|大兴)(壹千|叁千)[^。]+?两[^。]*', n_text):
    seg = m.group(0).strip('，。\n ')
    if seg not in entries:
        entries.insert(0, seg)
# 清理：去掉以"奉差"开头与含重复前缀的项
cleaned = []
for e in entries:
    if e.startswith('奉差'):
        continue
    if e not in cleaned:
        cleaned.append(e)
entries = cleaned

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷十三 13-001：名录谱牒层 AI 判定（万历十六年审编行银坊户，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "13-001",')
lines.append('        "name": "万历十六年审编铺行行银坊户细目",')
lines.append('        "category": "其他",')
lines.append('        "scope": "宛平一千七百八十三两六钱、大兴三千三百五十二两七钱，各坊各则（上上~中下）户数",')
lines.append('        "entries": ' + repr(entries) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('坊户项:', len(entries))
for e in entries[:5]:
    print(' ', e[:60])
