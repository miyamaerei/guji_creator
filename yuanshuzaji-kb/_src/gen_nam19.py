# -*- coding: utf-8 -*-
"""卷十九 寺庵宫观庙堂祠 名录提取（按类别正则提取全量名单，人工核对）。"""
import re, io, json

raw = io.open(r'原文\卷十九.txt', encoding='utf-8').read()
# 按标题切段
segs = {}
for key, title in [('19-002', '△寺'), ('19-003', '△庵'), ('19-004', '△宫'), ('19-005', '△观'), ('19-006', '△庙'), ('19-007', '△堂'), ('19-008', '△祠')]:
    m = re.search(re.escape(title) + r'\n(.*?)(?=\n△|\n尝观|\Z)', raw, re.S)
    segs[key] = m.group(1) if m else ''

suffix = {'19-002': '寺', '19-003': '庵', '19-004': '宫', '19-005': '观', '19-006': '庙', '19-007': '堂', '19-008': '祠'}
out = {}
for key, seg in segs.items():
    su = suffix[key]
    # 名字形态：中文2~5字 + su，前不接"大时雍坊"等坊名内的"坊"字组合——直接取所有候选
    names = re.findall(r'[\u4e00-\u9fff]{2,5}' + su, seg)
    # 去重保序，剔除明显不是专名的（含"创不记年"等上下文干扰）
    seen, uniq = set(), []
    for n in names:
        if n in seen:
            continue
        seen.add(n)
        uniq.append(n)
    # 剔除误抓：以动词/虚词结尾的
    bad = re.compile(r'^(以上|凡|在|其|一|二|三|俱|系|有|无|今|古|年|日|月|见|详|设|即|此|于|为|之|者|所|造|建|创|修|重|敕|赐|请|奏|因|遂|后|前|内|外)')
    uniq = [n for n in uniq if not bad.match(n)]
    out[key] = uniq

io.open(r'_src\_nam19_extract.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items():
    print(k, len(v))
    print(' '.join(v[:40]))
