# -*- coding: utf-8 -*-
"""从《宛署杂记》卷七原文提取黄垡仓各庄户地亩细目 + 廊房各城门间数/廊头名额，生成 _nam_ai_07.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷七.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_nam_ai_07.py'

text = io.open(SRC, encoding='utf-8').read()

# ---- 1. 黄垡仓各庄户地亩细目：'X地Y亩' 逐户（黄垡/东庄营/太子务/庄寨务/朱家务/南家庄/梁家庄/河南村/嘉靖余地）
huang_start = text.index('赵自成地壹顷')
huang_end = text.index('嘉靖二十九年')
huang_text = text[huang_start:huang_end]
huang = re.findall(r'([^，。]+?地[^，。]+?亩[^，。]*)', huang_text)
huang2_start = text.index('王大宁地伍亩')
huang2_end = text.index('以上二项')
huang2_text = text[huang2_start:huang2_end]
huang2 = re.findall(r'([^，。]+?地[^，。]+?亩[^，。]*)', huang2_text)
huang_all = huang + huang2
# 清洗：条目内不应含'征谷'（那是庄级合计行）与句号
huang_all = [x for x in huang_all if '征谷' not in x]

# ---- 2. 廊房各城门间数 + 廊头名额 ----
lang_start = text.index('北安门东大房陆拾陆间')
lang_end = text.index('窃计廊店房')
lang_text = text[lang_start:lang_end]
lang = [re.split('[:：]', x)[0].strip('\n ') for x in re.findall(r'([^，。]+(?:大房|中房|小房|店房)[^，。]*间)', lang_text)]
# 廊头名额
tou_start = text.index('北安门东三名')
tou_end = text.index('每季总约三十一家')
tou_text = text[tou_start:tou_end]
tou = re.findall(r'([^，。]+?[一二三四]+名)', tou_text)

lines = []
lines.append('# -*- coding: utf-8 -*-')
lines.append('"""卷七 07-001/07-002：名录谱牒层 AI 判定（庄户地亩/廊房间数/廊头名额，脚本提取）。"""')
lines.append('RECORDS = [')
lines.append('    {')
lines.append('        "item_id": "07-001",')
lines.append('        "name": "黄垡仓各庄户地亩细目",')
lines.append('        "category": "其他",')
lines.append('        "scope": "黄垡东庄营太子务庄寨务朱家务南家庄梁家庄河南村各庄户垦地亩数",')
lines.append('        "entries": ' + repr(huang_all) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append('    {')
lines.append('        "item_id": "07-002",')
lines.append('        "name": "宛平廊房各城门间数与廊头名额",')
lines.append('        "category": "其他",')
lines.append('        "scope": "皇城四门钟鼓楼廊房分等间数及每处廊头取用名额",')
lines.append('        "entries": ' + repr(lang + tou) + ',')
lines.append('        "ent_ids": [],')
lines.append('        "confidence": "high",')
lines.append('    },')
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print('庄户地亩项:', len(huang_all))
print('廊房/名额项:', len(lang), '+', len(tou))
print('地亩尾3:', huang_all[-3:])
print('廊房尾3:', lang[-3:])
print('名额尾3:', tou[-3:])
