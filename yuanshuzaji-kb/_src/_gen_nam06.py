# -*- coding: utf-8 -*-
"""从《宛署杂记》卷六原文提取坊图地亩/丁数名录，生成 _nam_ai_06.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷六.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_06.py'

text = io.open(SRC, encoding='utf-8').read()

# 地亩：鸣玉坊共地…雁翅社共地…
di_start = text.index('鸣玉坊共地')
di_end = text.index('昔人云')
di_text = text[di_start:di_end]
didi = [x.rstrip('。\n ') for x in re.findall(r'([^，]+共地[^，]+)', di_text)]

# 丁数：鸣玉坊八丁…雁翅社二百五十二丁（徐启东审定段内）
ding_start = text.index('鸣玉坊八丁')
ding_end = text.index('内除优免叁百壹丁')
ding_text = text[ding_start:ding_end]
ding = re.findall(r'([^，]+?[一二三四五六七八九十百千]+丁)', ding_text)

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷六 06-001/06-002：名录谱牒层 AI 判定（坊图地亩/丁数，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "06-001",')
lines.append('        "name": "万历年间宛平各坊图屯社地亩",')
lines.append('        "category": "其他",')
lines.append('        "scope": "嘉隆后坊图屯社地亩分计",')
lines.append('        "entries": ' + repr(didi) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "06-002",')
lines.append('        "name": "万历十七年宛平各坊图屯社丁数",')
lines.append('        "category": "其他",')
lines.append('        "scope": "知县徐启东审定人丁各坊图分计",')
lines.append('        "entries": ' + repr(ding) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('地亩项:', len(didi))
print('丁数项:', len(ding))
print('地亩尾3:', didi[-3:])
print('丁数尾3:', ding[-3:])
