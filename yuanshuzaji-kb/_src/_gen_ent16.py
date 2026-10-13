# -*- coding: utf-8 -*-
"""从《宛署杂记》卷十六（人物：乡贤/列女/仙释）提取人名清单，生成 _ents_ai_16.py。"""
import re, io

SRC = r'E:\git\ToolBox\guji\yuanshuzaji-kb\原文\卷十六.txt'
OUT = r'E:\git\ToolBox\guji\yuanshuzaji-kb\_src\_ents_ai_16.py'

text = io.open(SRC, encoding='utf-8').read()

names = []
seen = set()

def add(n):
    if n and n not in seen and not re.search(r'[【】○△]', n):
        seen.add(n)
        names.append(n)

# ① 历代乡贤：朝代标记后 "XX，蓟人/宛平人/大都人/幽州人/范阳方城人"
for m in re.finditer(r'([\u4e00-\u9fff]{2,4})，[^，。]{0,12}人[。，]', text):
    n = m.group(1)
    if n in ('马永',):  # 特殊：马永字天锡
        add('马永')
        continue
    add(n)
# ② 马永 字天锡
if '马永字天锡' in text:
    add('马永')
# ③ 寄寓乡贤：万历二十年寄寓乡贤 "孙飦，号立峰，丙辰进士"
for m in re.finditer(r'([\u4e00-\u9fff]{2,4})，号([^，]+)，', text):
    add(m.group(1))
# ④ 列女：岳氏/王氏/余氏/孙氏/马氏/徐氏/司氏/杨氏/郭氏/何氏/刘氏/门氏
for m in re.finditer(r'([\u4e00-\u9fff]{1,3}氏)，', text):
    add(m.group(1))
# ⑤ 仙释：昙无竭，姓李氏 / 丘处机 / 吕氏
for m in re.finditer(r'([\u4e00-\u9fff]{2,4})，[^，。]{0,8}氏', text):
    add(m.group(1))

# 排除朝代名/非人名词
exclude = {'南北朝','本朝','元','唐','周','宋','辽','金'}
names = [n for n in names if n not in exclude]

# 手写补齐缺失（正则可能漏的）
manual = ['徐邈','刘沉','张华','平恒','平鉴','鲁炅','张希崇','边归谠','马全义','马知节','张俭','刘伸','刘仲诲','丁■〈舟丰〉仁','阎公贞','高昌福','马肩龙','董伦','李嘉','甄庸','李侃','李德恢','马永','徐淮','张翰','刘效祖','孙飦','曹子朝','李江','吕鸣珂','董文宷','曹子登','徐维楫','杜其骄','孙錝','赵楫','徐学礼','沈涵','孙鑛','张汝贤','朱国祚','方从哲','杨元祥','吕胤昌','沈凤岐','王岳锡','黄腾春','何选','孙承荣','王嘉谟','林守信','冯有经','章尧相','蔡文会','王爱','康炜','徐继申','马继文','岳氏','王氏','余氏','孙氏','马氏','徐氏','司氏','杨氏','郭氏','何氏','刘氏','门氏','昙无竭','丘处机','吕氏']
for n in manual:
    add(n)

lines = ['# -*- coding: utf-8 -*-',
         '"""卷十六 16-001~16-003：实体层 AI 判定（乡贤/列女/仙释人物，脚本提取+人工核对）。"""',
         'RECORDS = [']
for n in names:
    lines.append('    {"item_id": "16-001", "text": "%s", "type": "person", "confidence": "high"},' % n)
lines.append(']')
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
print('共提取', len(names), '人')
print(names)
