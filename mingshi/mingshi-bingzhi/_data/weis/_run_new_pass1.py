# -*- coding: utf-8 -*-
"""后定编成树（--ver new, L122-251）首解析。
词典隔离：以旧树 377 词为种子写入 wei_name_index_new.json 副本，
把 builder.NAME_INDEX_PATH 重定向到副本 —— 原词典文件全程不动。
"""
import json, io, os, sys

sys.path.insert(0, 'assets/tools')
sys.path.insert(0, 'scripts')
import _weisuo_builder as B

OLD_INDEX = '_data/weis/wei_name_index.json'
NEW_INDEX = '_data/weis/wei_name_index_new.json'

# 1) 种子词典 = 旧树全量（旧树经 AI 复核定稿，词形可信）
seed = json.load(io.open(OLD_INDEX, encoding='utf-8'))['index']
json.dump({'index': seed, 'note': 'new段专用词典副本（种子=旧树377词）'},
          io.open(NEW_INDEX, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 2) 重定向 builder 词典路径（原文件不触碰）
B.NAME_INDEX_PATH = NEW_INDEX

index = B._index_ctx()
assert len(index) == len(seed)

# 3) 括注锚点预扫收词（与 main --save-index 同逻辑）
start, end = 122, 251
lines = B.load_source_lines('66', start, end)
import re
for _no, ln in lines:
    for m in B.BRACKET_RE.finditer(ln):
        head = ln[:m.start()]
        tail = head[-3:]
        for suf in B.ALL_SUFFIXES:
            if tail.endswith(suf):
                name = head[head.rfind(suf) - 12:].strip()
                name = re.sub(r'^.*?([\u4e00-\u9fff]+$)', r'\1', name)
                if name and len(name) <= 12:
                    item = index.setdefault(name, {'count': 0, 'first': None})
                    item['count'] += 1
                    if item['first'] is None:
                        item['first'] = 'L%d' % _no
B.save_name_index(index)  # 写到副本

# 4) 首跑
tree = B.build_candidate_tree(lines, 'new', '66', index)
cov = B.build_coverage(tree, lines, index)
out = {
    'meta': {'vol': '66', 'list_ver': 'new', 'lines': 'L122-L251',
             'note': '规则引擎候选结果，必须经 AI 复核后方可写定稿（SKILL.md §13）',
             'index_isolation': '词典副本 wei_name_index_new.json，种子=旧树377词+new段预扫；原 wei_name_index.json 未动'},
    'tree': tree, 'coverage': cov,
}
os.makedirs('_data/weis', exist_ok=True)
json.dump(out, io.open('_data/weis/candidates_66_new.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print('coverage:', json.dumps({k: cov[k] for k in
      ('determined_count', 'pending_count', 'segment_coverage', 'coverage_ok',
       'bracket_notes_total', 'wei_name_index_size', 'src_lines')}, ensure_ascii=False))
# pending 段清单
pend = []
def walk(n):
    if n.get('ai_review') == 'required':
        pend.append((n.get('src_loc'), n.get('name')))
    for c in n.get('children') or []:
        walk(c)
walk(tree['root'])
print('pending segments:', len(pend))
for s, nm in pend:
    print(' ', s, nm[:60])
print('index size now:', len(json.load(io.open(NEW_INDEX, encoding='utf-8'))['index']))
