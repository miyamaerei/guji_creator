# -*- coding: utf-8 -*-
"""从《宛署杂记》卷十五原文提取经费明细：①乡试饮馔品物；②乡饮酒礼各席；③殿试登科录纸品物。生成 _nam_ai_15.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷十五.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_15.py'

text = io.open(SRC, encoding='utf-8').read()

def cut(start_kw, end_kw):
    return text[text.index(start_kw):text.index(end_kw)]

# ① 乡试饮馔品物（15-003）
s = cut('乡场饮馔品物，合用', '以上乡场饮馔共银')
items1 = re.findall(r'([^，。；]+?[斤个两只石匹副条坛枝篓件领张]+\d*[零半]*[斤个两只石匹副条坛枝篓件领张]*)', s)
# 简化：按顿号/逗号切，取带数量的段
segs1 = [x.strip('，。；') for x in re.split(r'[，。；]', s) if re.search(r'[\d零一二三四五六七八九十百千万]+[斤个两只石匹副条坛枝篓件领张]', x)]
monthly_tt = segs1

# ② 乡饮酒礼各席（15-007）
s2 = cut('乡饮酒礼，每年二次', '以上共乡饮银计用')
segs2 = [x.strip('，。；') for x in re.split(r'[，。；]', s2) if re.search(r'[\d零一二三四五六七八九十百千万]+[斤个两只石匹副条坛枝篓件领张]', x)]

# ③ 殿试登科录纸品物（15-005）
s3 = cut('御览登科录纸六百张', '以上共该银四百四十六两四钱三分六厘')
segs3 = [x.strip('，。；') for x in re.split(r'[，。；]', s3) if re.search(r'[\d零一二三四五六七八九十百千万]+[斤个两只石匹副条坛枝篓件领张]', x)]

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷十五 15-003/15-007/15-005：名录谱牒层 AI 判定（乡试饮馔品物/乡饮酒礼各席/殿试登科录纸，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "15-003",')
lines.append('        "name": "乡场饮馔品物清单",')
lines.append('        "category": "其他",')
lines.append('        "scope": "万历十九年乡试合用妆花改机米面肉禽鱼果菜油盐酱醋纸笔诸品",')
lines.append('        "entries": ' + repr(monthly_tt[:60]) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "15-007",')
lines.append('        "name": "乡饮酒礼各席品物",')
lines.append('        "category": "其他",')
lines.append('        "scope": "宛平县该管正月分，上席六卓上中席五卓中席二十六卓下席八卓食卓四十五卓品物",')
lines.append('        "entries": ' + repr(segs2[:50]) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "15-005",')
lines.append('        "name": "殿试登科录纸品物",')
lines.append('        "category": "其他",')
lines.append('        "scope": "万历二十年殿试御览登科录纸奏本纸绫罗笔墨砚烛诸品",')
lines.append('        "entries": ' + repr(segs3) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('乡试饮馔:', len(monthly_tt))
print('乡饮酒礼:', len(segs2))
print('殿试品物:', len(segs3))
