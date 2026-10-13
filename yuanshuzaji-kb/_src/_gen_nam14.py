# -*- coding: utf-8 -*-
"""从《宛署杂记》卷十四原文提取经费明细：①太庙正祭按月品物；②陵园各祭坟柴处所。生成 _nam_ai_14.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷十四.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_14.py'

text = io.open(SRC, encoding='utf-8').read()

# ① 太庙正祭按月品物（'正月分，共银…' 至 '十二月分…以上正祭'）
m_start = text.index('太庙每年正祭合用品物')
m_end = text.index('以上正祭，每年除大兴县外')
m_text = text[m_start:m_end]
monthly = []
for seg in re.split(r'(?=正月分|二月分|三月分|四月分|五月分|六月分|七月分|八月分|九月分|十月分|十一月分|十二月分)', m_text):
    seg = seg.strip('\n ')
    if seg.startswith(('正月分', '二月分', '三月分', '四月分', '五月分', '六月分', '七月分', '八月分', '九月分', '十月分', '十一月分', '十二月分')):
        # 保留首句（共该银）+ 品物前 8 项，控制长度
        head = seg.split('。')[0]
        items = re.findall(r'([^；;。]+?，价[^；;。]*)', seg)
        monthly.append(head + '：' + '；'.join(items[:10]))

# ② 陵园各祭坟柴处所（五祭/四祭/二祭 + 坟户）
g_start = text.index('每年合用各陵坟煮牲柴炭')
g_end = text.index('以上每年通共煮牲坟柴银')
g_text = text[g_start:g_end]
graves = []
for m in re.finditer(r'(一年五祭者|一年四祭者|一年二祭者)[^。]*。', g_text):
    graves.append(m.group(0).strip('。\n '))

h_start = text.index('大寿山园户五名')
h_end = text.index('以上各坟户，每名徭编银肆两')
h_text = text[h_start:h_end]
hu = h_text.replace('\n', '').replace('，', '；').strip('。\n ')
if hu:
    graves.append('坟户：' + hu)

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷十四 14-001：名录谱牒层 AI 判定（太庙正祭按月品物/陵园祭处，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "14-002",')
lines.append('        "name": "太庙每年正祭合用品物按月价银",')
lines.append('        "category": "其他",')
lines.append('        "scope": "除大兴县分辨一半外本县该办，正月至十二月每月品物价银",')
lines.append('        "entries": ' + repr(monthly) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "14-003",')
lines.append('        "name": "陵园各祭坟柴处所及坟户",')
lines.append('        "category": "其他",')
lines.append('        "scope": "一年五祭七十九处/四祭三十六处/二祭二十六处及各坟户名数",')
lines.append('        "entries": ' + repr(graves) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('按月品物:', len(monthly))
print('祭处:', len(graves))
