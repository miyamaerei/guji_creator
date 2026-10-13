# -*- coding: utf-8 -*-
"""从《宛署杂记》卷八原文提取慈宁宫各庄地亩细目 + 给爵地银，生成 _nam_ai_08.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷八.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_08.py'

text = io.open(SRC, encoding='utf-8').read()

# ---- 1. 慈宁宫 + 新慈宁宫 各庄地亩细目（'X地共Y亩…共银Z'） ----
ci_start = text.index('傅恭太监下池敬地八顷')
ci_end = text.index('乾清宫原额地一百')
ci_text = text[ci_start:ci_end]
cin = re.findall(r'([^。]+?地[^。]*?共?银[^。]*)', ci_text)
cin = [x.strip('\n ') for x in cin if '地' in x]

# ---- 2. 给爵地银（其节年给爵段） ----
jue_start = text.index('皇亲杜继祖银')
jue_end = text.index('有解进太仓者')
jue_text = text[jue_start:jue_end]
jue = re.findall(r'([^。]+银[^。]*)', jue_text)
jue = [x.strip('\n ') for x in jue if '银' in x]

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷八 08-001：名录谱牒层 AI 判定（慈宁宫地亩/给爵地银，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "08-001",')
lines.append('        "name": "慈宁宫各庄地亩征银细目",')
lines.append('        "category": "其他",')
lines.append('        "scope": "慈宁宫与新慈宁宫各庄户地亩每亩征银共银细目",')
lines.append('        "entries": ' + repr(cin) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "08-001",')
lines.append('        "name": "宛平给爵地银",')
lines.append('        "category": "其他",')
lines.append('        "scope": "节年给爵题准应免地土，由本县征解各爵及自征空文转解者",')
lines.append('        "entries": ' + repr(jue) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('慈宁宫地亩项:', len(cin))
print('给爵地银项:', len(jue))
print('地亩尾3:', cin[-3:])
print('给爵尾3:', jue[-3:])
