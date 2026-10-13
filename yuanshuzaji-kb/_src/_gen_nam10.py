# -*- coding: utf-8 -*-
"""从《宛署杂记》卷十原文提取奶口季费什物细目，生成 _nam_ai_10.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷十.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_10.py'

text = io.open(SRC, encoding='utf-8').read()

# 奶口季费什物：'煤壹万肆千肆百斤，银拾柒两贰钱捌分；…脚价银捌两。'
n_start = text.index('煤壹万肆千肆百斤')
n_end = text.index('以上每季每县各银')
n_text = text[n_start:n_end]
items = []
for seg in re.split('[；;]', n_text):
    seg = seg.strip('，。\n ')
    if '银' in seg and '以上' not in seg:
        items.append(seg)

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷十 10-001：名录谱牒层 AI 判定（奶口季费什物，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "10-001",')
lines.append('        "name": "奶口季费什物细目",')
lines.append('        "category": "其他",')
lines.append('        "scope": "每季两县各办送礼仪房奶口煤炭杂器什物价银",')
lines.append('        "entries": ' + repr(items) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('什物项:', len(items))
print('尾3:', items[-3:])
