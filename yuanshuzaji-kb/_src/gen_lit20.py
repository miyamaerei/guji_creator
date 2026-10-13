# -*- coding: utf-8 -*-
"""卷二十 20-002~20-079 作者诗文：从底座 original 提取作者/官职/题目，生成 lit/nam/ent/appt 骨架。"""
import json, io, re

reg = json.load(io.open(r'_item_registry.json', encoding='utf-8'))
keys = [k for k in sorted(reg) if k.startswith('20-')][1:80]  # 20-002..20-079

def parse(original):
    s = original
    if s.startswith('△'):
        s = s[1:]
    s = re.sub(r'^本朝', '', s)
    # 作者 = 到 ( 或 空格
    m = re.match(r'^([\u4e00-\u9fff·]+)(?:（([^）]*)）)?\s*(.*)$', s)
    if not m:
        return None
    author, paren, rest = m.group(1), m.group(2) or '', m.group(3)
    # 题目 = 到第一个"："前的书名号/题名串
    title = rest.split('：')[0].strip()
    return author, paren, title

rows = []
for k in keys:
    p = parse(reg[k]['original'])
    rows.append((k, p[0], p[1], p[2]))

# ---- lit ----
OFFICE_KW = ['大学士', '学士', '尚书', '都御史', '大司马', '考功郎', '布政', '参政', '副使', '太常寺卿',
             '通政', '府尹', '治中', '录事', '主事', '编修', '检讨', '待诏', '新建伯', '丰城侯', '临淮侯',
             '提学副使', '知县', '兵部', '吏部', '礼部', '工部', '户部', '刑部', '侍郎', '都指挥', '指挥',
             '佥事', '光禄', '大理', '太仆', '鸿胪', '行人', '给事中', '御史', '检校', '评事', '寺卿', '少卿']
LIT = []
NAM_ENTRIES = []
ENTS = []
APPT = []
for k, author, paren, title in rows:
    if '皇帝' in author:
        continue
    typ = '诗'
    if '记' in title:
        typ = '记'
    elif '碑' in title:
        typ = '碑记'
    elif '赋' in title:
        typ = '赋'
    elif '疏' in title or '奏' in title:
        typ = '诏令奏议'
    elif '歌' in title or '行' in title or '篇' in title or '绝句' in title or '引' in title:
        typ = '诗'
    LIT.append({'item_id': k, 'title': title, 'author': author, 'author_ent_ids': [],
                'type': typ, 'content_location': '卷二十·志遗一~五（作者：%s%s）' % (author, '（' + paren + '）' if paren else ''), 'confidence': 'high'})
    NAM_ENTRIES.append('%s（%s）——《%s》' % (author, paren if paren else '籍贯未注', title))
    ENTS.append({'item_id': k, 'text': author, 'type': 'person', 'confidence': 'high'})
    if paren and any(w in paren for w in OFFICE_KW):
        # 官职→机构
        inst = '六部'
        if '大学士' in paren: inst = '内阁'
        elif '学士' in paren or '编修' in paren or '检讨' in paren or '待诏' in paren: inst = '翰林院'
        elif '尚书' in paren or '大司马' in paren: inst = '六部'
        elif '府尹' in paren or '治中' in paren: inst = '顺天府'
        elif '都御史' in paren or '副使' in paren or '巡抚' in paren: inst = '都察院'
        elif '布政' in paren or '参政' in paren or '提学' in paren: inst = '布政司'
        elif '通政' in paren: inst = '通政司'
        elif '太常寺卿' in paren: inst = '太常寺'
        elif '侯' in paren or '伯' in paren or '新建伯' in paren: inst = '五军都督府'
        elif '知县' in paren: inst = '宛平县'
        elif '考功郎' in paren or '吏部郎' in paren: inst = '吏部'
        elif '主事' in paren or '郎中' in paren: inst = '六部'
        elif '詹事府' in paren: inst = '詹事府'
        # 官职词抽取（去籍贯；长词优先，子串剔除）
        OFF = ['大学士', '提学副使', '考功郎', '太常寺卿', '丰城侯', '临淮侯', '新建伯', '吏部郎', '大司马',
               '尚书', '都御史', '布政', '参政', '副使', '通政', '府尹', '治中', '录事', '主事', '编修',
               '检讨', '待诏', '知县', '巡抚', '郎中', '寺卿', '少卿', '侍郎', '学士']
        offs = []
        for w in OFF:
            if w in paren and w not in offs and not any(w in o and o != w for o in offs):
                offs.append(w)
        office = '、'.join(offs) if offs else paren
        APPT.append({'item_id': k, 'person': author, 'person_ent_ids': [], 'office': office,
                     'official_ent_ids': [], 'institution': inst, 'institution_ent_ids': [], 'when': '',
                     'status': '现任', 'evidence': '《%s》作者，原文标注官职：%s' % (title, paren),
                     'evidence_refs': [], 'confidence': 'high'})

# 修正一行笔误
import textwrap
io.open(r'_src\_lit_ai_20.py', 'w', encoding='utf-8').write(
    '# -*- coding: utf-8 -*-\n"""卷二十 20-002~20-079 诗文 78 条：文献资产层（脚本从底座提取，人工核对）。"""\nRECORDS = ' +
    json.dumps(LIT, ensure_ascii=False, indent=1) + '\n')
io.open(r'_src\_ents_ai_20.py', 'w', encoding='utf-8').write(
    '# -*- coding: utf-8 -*-\n"""卷二十 作者人名实体（脚本提取，去重由 build_ent_keys 处理）。"""\nRECORDS = ' +
    json.dumps(ENTS, ensure_ascii=False, indent=1) + '\n')
io.open(r'_src\_appt_ai_20.py', 'w', encoding='utf-8').write(
    '# -*- coding: utf-8 -*-\n"""卷二十 明示官职作者任职（脚本提取）。"""\nRECORDS = ' +
    json.dumps(APPT, ensure_ascii=False, indent=1) + '\n')
io.open(r'_src\_nam_ai_20.py', 'w', encoding='utf-8').write(
    '# -*- coding: utf-8 -*-\n"""卷二十 志遗诗文作者名录。"""\nRECORDS = [{\n    "item_id": "20-002",\n    "name": "志遗诗文集作者名录",\n    "category": "名号称谓",\n    "scope": "卷二十志遗一~五所收诗文作者七十八人（含作者籍贯官职标注）",\n    "entries": ' +
    json.dumps(NAM_ENTRIES, ensure_ascii=False, indent=1) + ',\n    "ent_ids": [],\n    "confidence": "high",\n}]\n')
print('lit', len(LIT), 'ent', len(ENTS), 'appt', len(APPT), 'nam entries', len(NAM_ENTRIES))
for a in APPT:
    print(a['person'], a['office'], a['institution'])
