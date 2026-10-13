# -*- coding: utf-8 -*-
"""把 _nam19_extract.json 清理并生成 _nam_ai_19.py（人工规则+补漏）。"""
import json, io, re

ext = json.load(io.open(r'_src\_nam19_extract.json', encoding='utf-8'))

DROP = {
    '19-002': ['名崇国寺', '主天下寺', '大理寺', '本龙泉寺', '元朝建寺'],
    '19-005': ['相传本观', '万人集观'],
    '19-006': ['归建是庙', '我朝都城隍庙', '额普济药王庙', '护国武安王庙'],
    '19-007': ['戌谷太监建堂'],
    '19-008': [],
    '19-003': [],
    '19-004': [],
}
# 补漏（原文被正则漏抓的专名）
ADD = {
    '19-003': ['古登庵', '五圣庵', '张娘娘庵', '钟寿庵', '永寿庵', '积庆庵', '朝阳庵', '广慧庵', '玉环庵',
               '崇境庵', '三圣庵', '极乐庵', '古赤脚李庵', '郝家庵', '许家庵', '地藏庵', '达摩庵', '永宁庵',
               '胜泉庵', '花园庵', '元通庵', '洪教庵', '慈仁庵', '西林禅庵', '朝月庵', '兴胜庵', '观泉庵',
               '龙凤庵', '圣寿庵', '隆祐庵', '万寿庵'],
    '19-007': ['古佛堂'],
    '19-008': ['内阁祠'],
    '19-002': [],
    '19-004': [],
    '19-005': [],
    '19-006': [],
}
NAMES = {'19-002': ('宛平境内寺二百一十一处', '城内七十二城外一百三十九'),
         '19-003': ('宛平境内庵一百四十处', '城内七十七城外六十三'),
         '19-004': ('宛平境内宫六处', '城内三城外三'),
         '19-005': ('宛平境内观二十一处', '城内七城外十四'),
         '19-006': ('宛平境内庙二百六处', '城内七十七城外一百二十九'),
         '19-007': ('宛平境内堂十三处', '城内四城外九'),
         '19-008': ('宛平境内祠七处', '城内二城外五')}

lines = ['# -*- coding: utf-8 -*-', '"""卷十九 19-002~19-008：名录谱牒层（寺庵宫观庙堂祠全量名单，脚本提取+人工补漏）。"""', 'RECORDS = [']
for key, (nm, sc) in NAMES.items():
    names = [n for n in ext[key] if n not in DROP[key]]
    for a in ADD[key]:
        if a not in names:
            names.append(a)
    # 并入说明：被剔除项归并到哪
    merge = {'名崇国寺': '大隆善寺', '本龙泉寺': '兴德寺', '我朝都城隍庙': '城隍庙',
             '额普济药王庙': '药王庙', '护国武安王庙': '关王庙'}
    lines.append('    {')
    lines.append('        "item_id": %r,' % key)
    lines.append('        "name": %r,' % nm)
    lines.append('        "category": "其他",')
    lines.append('        "scope": %r,' % sc)
    entries = json.dumps(names, ensure_ascii=False)
    lines.append('        "entries": %s,' % entries)
    lines.append('        "ent_ids": [],')
    lines.append('        "confidence": "high",')
    lines.append('    },')
lines.append(']')
io.open(r'_src\_nam_ai_19.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('ok')
for key, nm in NAMES.items():
    print(key, len(ext[key]), '->', len([n for n in ext[key] if n not in DROP[key]]) + len(ADD[key]))
