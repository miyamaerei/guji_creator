# -*- coding: utf-8 -*-
"""一次性生成器：从候选树 + 判定规则产出 leaf_notes_review.json（卫级 88 条括注复核）。"""
import json, io, sys

BASE = '_data/weis/'
cand = json.load(open(BASE + 'candidates_66_old.json', encoding='utf-8'))

# 收集叶级（卫/所）注实例，顺序即复核编号
items = []
def walk(n, path):
    for note in (n.get('notes') or []):
        if n.get('level') in ('卫', '所'):
            items.append({'name': n['name'], 'level': n['level'],
                          'src_loc': n.get('src_loc'), 'note': note,
                          'path': path})
    for ch in n.get('children', []) or []:
        walk(ch, path + ' > ' + str(n.get('name', '')))
walk(cand['tree']['root'], 'root')
assert len(items) == 88, len(items)

Y18 = {'text': '永乐十八年', 'dynasty': '明', 'reign': '永乐', 'year': 18}
WM = lambda why='原文仅“后”字，无纪年': {'text': '未明（%s）' % why, 'dynasty': '明', 'reign': None, 'year': None}

def draft(slot_suffix, era, target, action, category, content, conf, ref, note=''):
    d = {'slot': 'volume66/weis/old/leafnote/' + slot_suffix, 'era': era,
         'target': target, 'action': action, 'category': category,
         'content': content, 'related_evo': None, 'related_opn': None,
         'ref_item': ref, 'confidence': conf}
    if note:
        d['note'] = note
    return d

# 按 (src_loc, name, note) 判定。规则函数返回 (verdict_kind, drafts, rationale, reg_check)
def classify(it):
    name, note, loc = it['name'], it['note'], it['src_loc']
    ref = '%s|%s' % (loc, name)
    # ---- 区块级注（已上）：转块节点 ----
    if note == '已上俱改为亲军':
        return ('BLOCK_REASSIGN', [draft('block.beiping-duisi.qinjun',
            WM('张本注无纪年，实为永乐元年置'), '通州卫及该行已上各卫（燕山左、燕山右、燕山前、大兴左、永清左、永清右、济州、济阳、彭城、通州共十卫）',
            '俱改为亲军', '改称', '已上俱改为亲军', 0.8, '块节点：后军都督府>在外>北平都司（L110）',
            '边界=同注行内前导卫列；亲军=直隶禁卫编制，卫名不改，属隶属/编制性质，取改称并注编制变更')],
        ['按 SKILL.md §6.2/§16-5，「已上…」为区块级注，不得挂段尾卫叶',
         '当前树无「北平都司 L111 卫列」子块节点，转写草稿先行挂块节点，定稿时由打包器建区块节点承载'],
        '不入 REG：编制归属陈述，非制度实体句')
    if note.startswith('后为隆庆卫已上俱属后府'):
        return ('SPLIT_LEAF_AND_BLOCK', [
            draft('LN-juyongguan', WM(), '居庸关千户所', '改称隆庆卫', '改称', '后为隆庆卫', 0.9, ref,
                  '所升卫（千户所→卫），沿革性质为改称；升秩与否无原文秩级依据，不取升秩'),
            draft('block.beiping-duisi.houfu', WM('张本注无纪年'),
                  '该行隆庆卫已上各卫所（蓟州、密云[后为密云后卫]、真定、永平、山海、遵化、隆庆卫/居庸关千户所）',
                  '俱属后军都督府', '改置', '已上俱属后府', 0.8,
                  '块节点：后军都督府>在外>北平都司（L110）',
                  '复合串拆分：前半为居庸关己注，后半「已上」为区块注；边界歧义（密云注已明示属后府）取行级保守边界')],
        ['SKILL.md §16-7 双证据：复合括注按语义拆分，叶注与块注分别转写，src_loc 保留 L111 双证据'],
        '不入 REG：隶属变更事件，非制度实体')
    if note == '俱改调京卫已上俱属后府':
        return ('SPLIT_LEAF_INTO_BLOCK', [
            draft('block.beiping-xing-duisi.diaojing',
            {'text': '未明（改调京卫约在永乐初大宁内徙；BN-01 永乐十八年张本纪年系六府在京注，不径直套用）', 'dynasty': '明', 'reign': None, 'year': None},
            '该行已上各卫（大宁左、大宁右、大宁中、大宁前、大宁后、会州）',
            '俱改调京卫', '移驻', '俱改调京卫', 0.85,
            '块节点：后军都督府>在外>北平行都司（L112）',
            '「改调京卫」与「调北京」同类而时地不同：大宁诸卫内徙约在永乐初，不得径套 BN-01 纪年（坑：纪年补造）'),
            draft('block.beiping-xing-duisi.houfu', WM('张本注无纪年'),
                  '该行已上各卫所（含营州中护卫；范围至会州卫注前）', '俱属后军都督府', '改置',
                  '已上俱属后府', 0.75, '块节点：后军都督府>在外>北平行都司（L112）',
                  '边界歧义：大宁各卫既「俱改调京卫」又「已上俱属后府」，两注层次不同（调京=移驻，属后府=会司归属），并存不矛盾')],
        ['会州卫为该行末带注叶，「已上」两注实为块级信息（SKILL.md §16-5）',
         '移驻纪年统一领自 BN-01，与卫级(调北京)同一口径'],
        '不入 REG')
    if note == '俱为亲军':
        return ('BLOCK_REASSIGN', [draft('block.yanshan-san-huwei',
            WM('原文仅“俱为”无纪年'), '燕山中护卫及该行已上二护卫（燕山左、右、中护卫）',
            '俱为亲军', '改称', '俱为亲军', 0.8, '块节点：后军都督府>在外>北平三护卫（L118）',
            '即永乐后升北平三护卫为亲军卫之事；区块注误挂末叶')],
        ['「俱」为全组性质（该行三护卫皆然），属区块级注（SKILL.md §16-5）'],
        '不入 REG：编制归属陈述')
    if note == '俱革':
        return ('BLOCK_REASSIGN', [draft('block.taiyuan-san-huwei',
            WM('原文仅“俱革”无纪年'), '太原中护卫及该行已上二护卫（太原左、右、中护卫）',
            '俱革', '废置', '俱革', 0.85, '块节点：后军都督府>在外>山西三护卫（L120）',
            '革=废置，建 TME；纪年原文无，不得补造')],
        ['「俱」为全组性质，区块级注误挂末叶（SKILL.md §16-5）'],
        '不入 REG')
    # ---- 三护卫分行注（节点即组）----
    if note.startswith('左改东昌卫'):
        return ('LEAF_GROUP_SPLIT', [
            draft('LN-wuchang-zuo', WM(), '武昌左护卫', '改东昌卫', '改称', '左改东昌卫', 0.9, ref),
            draft('LN-wuchang-you', WM(), '武昌右护卫', '改徐州左卫', '改称', '右改徐州左卫', 0.9, ref),
            draft('LN-wuchang-zhong', WM(), '武昌中护卫', '改武昌护卫', '改称', '中改武昌护卫', 0.9, ref)],
        ['节点「武昌左、右、中三护卫」为组合叶，括注分述三员各改，转写按成员拆三条 C14'],
        '不入 REG')
    if note == '二卫后为营州左、右护卫，改延庆左、右卫':
        return ('LEAF_MULTI', [
            draft('LN-daning-you-1', WM(), '大宁右卫', '后为营州右护卫', '改称', '二卫后为营州左、右护卫', 0.85, ref,
                  '原文“二卫”统指大宁右卫与次行节点，各为左/右护卫之归属依序推断，置信降档'),
            draft('LN-daning-you-2', WM(), '营州左、右护卫', '改延庆左、右卫', '改称', '改延庆左、右卫', 0.85, ref)],
        ['沿革链两跳（卫→护卫→延庆二卫），一条 TME 承载末段、前段入 content 亦可；此处拆两条保沿革链完整'],
        '不入 REG')
    if note == '后为营州中护卫，改宽河卫':
        return ('LEAF_MULTI', [
            draft('LN-daning-hou-1', WM(), '大宁后卫', '后为营州中护卫', '改称', '后为营州中护卫', 0.9, ref),
            draft('LN-daning-hou-2', WM(), '营州中护卫', '改宽河卫', '改称', '改宽河卫', 0.9, ref)],
        ['两跳沿革链，拆两条'],
        '不入 REG')
    # ---- 单事件 ----
    if note == '调北京':
        return ('LEAF', [draft('LN-diaobeijing', Y18, name, '调守北京', '移驻', '调北京', 0.95, ref)],
        ['纪年领自 BN-01 张本行（永乐十八年），卫级不重出年月（原文“其年月不重出”）'],
        '不入 REG')
    if note == '革':
        return ('LEAF', [draft('LN-ge', WM('原文仅括注“革”'), name, '革', '废置', '革', 0.9, ref,
                               '革=废置建 TME；革后该卫在“后定编成”树中的存废由双树对照视图核验')],
        ['SKILL.md §6.2：`(革)` 为沿革注剥离转 C14'],
        '不入 REG')
    if note == '后属行都司':
        dusi = it['path'].split(' > ')[-2]
        xing = {'四川都司': '四川行都司', '陕西都司': '陕西行都司', '湖广都司': '湖广行都司'}.get(
            dusi, '%s→行都司（待核）' % dusi)
        return ('LEAF', [draft('LN-houshu-xingdusi', WM(), name, '改隶%s' % dusi, '改置', '后属行都司', 0.9, ref,
                               '隶属变更（都司→本路行都司），无改额改名')],
        ['改置为枚举内最贴近「改隶」义项（坑：不扩枚举，§12 枚举治理）'],
        '不入 REG')
    RULES1 = {
        '后改为屯卫': ('广宁中护卫', '改广宁中屯卫', '改称', 0.9),
        '后为天津右卫': ('青州左护卫', '后为天津右卫', '改称', 0.9),
        '后为临清卫': ('兖州左护卫', '后为临清卫', '改称', 0.9),
        '后改属后府': ('德州卫', '改属后军都督府', '改置', 0.9),
        '后为神武右卫': ('西安左护卫', '后为神武右卫', '改称', 0.9),
        '后为神武前卫': ('西安中护卫', '后为神武前卫', '改称', 0.9),
        '改西安中护卫': ('西安右卫', '改西安中护卫', '改称', 0.9),
        '改西安右护卫': ('泰山卫', '改西安右护卫', '改称', 0.9),
        '后为甘州后卫': ('甘肃卫', '后为甘州后卫', '改称', 0.9),
        '后为广西护卫': ('桂林左卫', '后为广西护卫', '改称', 0.9),
        '后属中府': ('本卫', '改属中军都督府', '改置', 0.9),
        '后属后府': ('本卫', '改属后军都督府', '改置', 0.9),
        '后为通州卫亲军': ('安吉卫', '后为通州卫（亲军）', '改称', 0.85),
        '后分为保安卫及保安右卫': ('天策卫', '分为保安卫及保安右卫', '裁并', 0.85),
        '后改为龙江左卫': ('龙江卫', '后改为龙江左卫', '改称', 0.9),
        '后为千户所': ('吉安卫', '降为千户所', '改置', 0.9),
        '后为廉州卫': ('廉州千户所', '升为廉州卫', '改置', 0.9),
        '后属兴都留守司': ('沔阳卫', '改隶兴都留守司', '改置', 0.9),
        '后改属兴都留守司': ('德安千户所', '改隶兴都留守司', '改置', 0.9),
        '后俱属行都司': ('襄阳卫、襄阳护卫（“俱”所指两卫，待核）', '俱改隶行都司', '改置', 0.75),
        '三护卫后并彭城卫': ('河南左、中、右三护卫', '并彭城卫', '裁并', 0.9),
    }
    if note in RULES1:
        target, action, cat, conf = RULES1[note]
        tgt = target if target != '本卫' else name
        extra = []
        if note == '后为通州卫亲军':
            extra = ['亲军为编制性质注，随 content 保留；与区块注「已上俱改为亲军」（L111 北平都司）非一事']
        if note == '后俱属行都司':
            extra = ['注云「俱」而节点仅挂襄阳护卫一员，其所指疑为襄阳卫+襄阳护卫两员（襄阳卫单列在前无注），边界存疑降置信']
        return ('LEAF', [draft('LN-single', WM(), tgt, action, cat, note, conf, ref)],
        extra + ['单事件，转一条 C14'], '不入 REG')
    if note == '后改名武定，属后府':
        return ('LEAF_MULTI', [
            draft('LN-lean-1', WM(), '乐安千户所', '改名武定（千户所）', '改称', '后改名武定', 0.9, ref),
            draft('LN-lean-2', WM(), '武定千户所', '属后军都督府', '改置', '属后府', 0.9, ref)],
        ['逗号分述两事（改名+改隶），拆两条'], '不入 REG')
    if note == '后改千户所，属中府':
        return ('LEAF_MULTI', [
            draft('LN-runing-1', WM(), '汝宁卫', '改为千户所', '改置', '后改千户所', 0.9, ref),
            draft('LN-runing-2', WM(), '汝宁千户所', '属中军都督府', '改置', '属中府', 0.9, ref)],
        ['卫降所为机构层级变更，取改置（枚举无「降等」义项）'], '不入 REG')
    if note == '后为密云后卫，属后府':
        return ('LEAF_MULTI', [
            draft('LN-miyun-1', WM(), '密云卫', '后为密云后卫', '改称', '后为密云后卫', 0.9, ref),
            draft('LN-miyun-2', WM(), '密云后卫', '属后军都督府', '改置', '属后府', 0.9, ref)],
        [], '不入 REG')
    if note == '后为涿鹿卫，后属后府':
        return ('LEAF_MULTI', [
            draft('LN-ningguo-1', WM(), '宁国卫', '后为涿鹿卫', '改称', '后为涿鹿卫', 0.9, ref),
            draft('LN-ningguo-2', WM(), '涿鹿卫', '后属后军都督府', '改置', '后属后府', 0.9, ref)],
        [], '不入 REG')
    if note == '改云南右护卫，革':
        return ('LEAF_MULTI', [
            draft('LN-malong-1', WM(), '马隆卫', '改云南右护卫', '改称', '改云南右护卫', 0.9, ref),
            draft('LN-malong-2', WM(), '云南右护卫', '革', '废置', '革', 0.9, ref)],
        ['先改后革两跳链，拆两条'], '不入 REG')
    if note == '后改为宁夏中屯卫，革':
        return ('LEAF_MULTI', [
            draft('LN-hezhou-1', WM(), '和州卫（直隶）', '改为宁夏中屯卫', '改称', '后改为宁夏中屯卫', 0.9, ref),
            draft('LN-hezhou-2', WM(), '宁夏中屯卫', '革', '废置', '革', 0.9, ref)],
        ['先改后革两跳链；注意与陕西都司「宁夏中护卫」（L77 无注）同名系二地，父链消歧（坑 #54）'], '不入 REG')
    if note == '后改云南中护卫，革':
        return ('LEAF_MULTI', [
            draft('LN-xihe-1', WM(), '西河中护卫', '改云南中护卫', '改称', '后改云南中护卫', 0.9, ref),
            draft('LN-xihe-2', WM(), '云南中护卫', '革', '废置', '革', 0.9, ref)],
        ['链式沿革（河中→云南中护卫→革）'], '不入 REG')
    if note == '改西安左护卫，又改神武右卫':
        return ('LEAF_MULTI', [
            draft('LN-huashan-1', WM(), '华山卫', '改西安左护卫', '改称', '改西安左护卫', 0.9, ref),
            draft('LN-huashan-2', WM(), '西安左护卫', '又改神武右卫', '改称', '又改神武右卫', 0.9, ref)],
        ['「又改」明示二跳'], '不入 REG')
    if note == '后为龙虎左卫，隶南京左府':
        return ('LEAF_MULTI', [
            draft('LN-cd-you-1', WM(), '成都右护卫', '后为龙虎左卫', '改称', '后为龙虎左卫', 0.9, ref),
            draft('LN-cd-you-2', WM(), '龙虎左卫', '隶南京左军都督府', '改置', '隶南京左府', 0.9, ref)],
        ['改称+改隶两事；南京左府=南直隶属府，为后定树南京子树对照线索'], '不入 REG')
    if note == '后为豹韬左卫，隶南京前府':
        return ('LEAF_MULTI', [
            draft('LN-cd-zhong-1', WM(), '成都中护卫', '后为豹韬左卫', '改称', '后为豹韬左卫', 0.9, ref),
            draft('LN-cd-zhong-2', WM(), '豹韬左卫', '隶南京前军都督府', '改置', '隶南京前府', 0.9, ref)],
        [], '不入 REG')
    if note == '后为宁番卫，属行都司，革':
        return ('LEAF_MULTI', [
            draft('LN-suzhou-1', WM(), '苏州卫（四川都司下，非南直苏州）', '后为宁番卫', '改称', '后为宁番卫', 0.9, ref),
            draft('LN-suzhou-2', WM(), '宁番卫', '属四川行都司', '改置', '属行都司', 0.9, ref),
            draft('LN-suzhou-3', WM(), '宁番卫', '革', '废置', '革', 0.9, ref)],
        ['三跳链全拆；同名「苏州卫」需父链消歧（坑 #54），target 括注防混读'], '不入 REG')
    if note == '后属行都司，改承天卫':
        return ('LEAF_MULTI', [
            draft('LN-anlu-1', WM(), '安陆卫', '改隶湖广行都司', '改置', '后属行都司', 0.9, ref),
            draft('LN-anlu-2', WM(), '安陆卫（行都司属下）', '改承天卫', '改称', '改承天卫', 0.9, ref)],
        ['承天卫=嘉靖中升安陆州为承天府因改卫名；原文无纪年，era 未明不得补造'], '不入 REG')
    if note == '后为荆州左卫，属行都司，改显陵卫':
        return ('LEAF_MULTI', [
            draft('LN-jz-zuo-1', WM(), '荆州左护卫', '为荆州左卫', '改称', '后为荆州左卫', 0.9, ref),
            draft('LN-jz-zuo-2', WM(), '荆州左卫', '属湖广行都司', '改置', '属行都司', 0.9, ref),
            draft('LN-jz-zuo-3', WM(), '荆州左卫', '改显陵卫', '改称', '改显陵卫', 0.9, ref)],
        ['三跳链全拆；显陵卫沿革与兴都留守司相关，跨事件对照留待 C14 时间线视图'], '不入 REG')
    raise SystemExit('UNCLASSIFIED: %s %s %s' % (loc, name, note))

review = []
stats = {'LEAF': 0, 'LEAF_MULTI': 0, 'LEAF_GROUP_SPLIT': 0, 'SPLIT_LEAF_AND_BLOCK': 0,
         'SPLIT_LEAF_INTO_BLOCK': 0, 'BLOCK_REASSIGN': 0}
tme_total = 0
for i, it in enumerate(items, 1):
    kind, drafts, rationale, reg_check = classify(it)
    stats[kind] += 1
    tme_total += len(drafts)
    review.append({
        'ln_id': 'LN-%02d' % i,
        'src_loc': it['src_loc'],
        'node_path': it['path'],
        'node': '%s（%s）' % (it['name'], it['level']),
        'note_text': it['note'],
        'verdict_kind': kind,
        'verdict_summary': {
            'LEAF': '卫级单事件，转 C14 一条；括注保留于节点 notes（转写互引，不并入卫名）',
            'LEAF_MULTI': '复合括注拆为多事件，各转一条 C14；括注保留于节点 notes',
            'LEAF_GROUP_SPLIT': '组合叶（三护卫）分述注，按成员各转一条 C14',
            'SPLIT_LEAF_AND_BLOCK': '复合串含叶注+区块注：叶注转本卫 C14，区块注提升至块节点',
            'SPLIT_LEAF_INTO_BLOCK': '整串为区块级注误挂叶上：拆分提升为块节点注并转 C14',
            'BLOCK_REASSIGN': '区块级注（「已上」/「俱」）误挂段尾卫叶，提升至块节点 notes，转 C14',
        }[kind],
        'c14_drafts': drafts,
        'rationale': rationale,
        'reg_check': reg_check,
        'c9_check': '不入 C9：无论说主体',
    })

out = {
    'meta': {
        'vol': '66', 'list_ver': 'old', 'lines': 'L52-L120',
        'scope': '卫/所叶节点括注 88 条复核（pilot-plan 阶段二；块级 2 条见 block_notes_review.json）',
        'basis': [
            'references/schemas/bz_schemas.json（C14=TME：TME_CATEGORIES_13、triggers“卷66 括注（调北京=事件）”）',
            'SKILL.md §16-4 括注≠正文、§16-5 已上/数量行为区块级信息、§16-7 双树双证据、§6.2 标记文法表',
            'HANDOFF.md §4-1/4-2 督办口径（(调北京)纪年统一领自 BN-01）',
        ],
        'rule_ai_writes_slots_only': 'AI 只填槽位（slot 字段），tme_id/item_id 由打包器 assign_ids 注入',
        'category_mapping_note': '改隶/改属类事件取 TME_CATEGORIES_13 之「改置」，层级降升（卫↔所）亦取「改置」，不扩枚举（SKILL.md §12 枚举治理）',
        'counter_check': '候选树注实例共 90 = 叶级 88 + 块级 2（BN-01/BN-02 已复核），与 coverage.bracket_notes_total=88 一致，无漂移',
        'stats': {'items': len(review), 'by_kind': stats, 'c14_drafts_total': tme_total},
        'reviewed_at': '2026-10-15',
    },
    'review': review,
}
json.dump(out, open(BASE + 'leaf_notes_review.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('items=%d drafts=%d kinds=%s' % (len(review), tme_total, stats))
