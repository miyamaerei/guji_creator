# -*- coding: utf-8 -*-
"""P4-F：生成三种可视化（自包含 HTML，双击即开，无外部依赖）。

产出
----
_deliver/vis_org_tree.html    官制树（衙门 → 属官 → 下属，可折叠搜索）
_deliver/vis_timeline.html    制度演变图（16 主题 × 年代 × 事例数）
_deliver/vis_geo_tree.html    地理管辖图（省 → 府州 → 县 + 卫所/驿站/仓场）

设计
----
* 单文件 HTML，内联 JSON 数据，无 CDN、无网络依赖。
* 树用纯 CSS/JS 折叠，不需要 d3；图用内联 SVG 手绘，避免外部库。
* 所有数据直接从 _layers/*.json 现算，保证与知识库同源。
"""
import json, os, sys, io, re, html
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
OUT = os.path.join(ROOT, "_vis")
os.makedirs(OUT, exist_ok=True)

office_tree = json.load(open("_layers/office_tree.json", encoding="utf-8"))
org_tree = json.load(open("_layers/org_tree.json", encoding="utf-8"))
geo = json.load(open("_layers/geo.json", encoding="utf-8"))
tims = json.load(open("_layers/tim.json", encoding="utf-8"))
rules = json.load(open("_layers/rules.json", encoding="utf-8"))
offices = json.load(open("_layers/office_profiles.json", encoding="utf-8"))
orgs = json.load(open("_layers/org_profiles.json", encoding="utf-8"))

CSS = """
*{box-sizing:border-box}
body{margin:0;font:14px/1.7 "Songti SC","SimSun",Georgia,serif;background:#f6f3ec;color:#2b2620}
header{background:#2b2620;color:#f6f3ec;padding:16px 24px}
header h1{margin:0;font-size:20px;letter-spacing:2px}
header p{margin:4px 0 0;font-size:12px;opacity:.75}
.wrap{max-width:1200px;margin:0 auto;padding:20px}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
input[type=search]{flex:1;min-width:220px;padding:8px 12px;border:1px solid #cbbf9f;
  border-radius:4px;background:#fffdf8;font:inherit}
button{padding:8px 14px;border:1px solid #cbbf9f;background:#fffdf8;border-radius:4px;
  cursor:pointer;font:inherit}
button:hover{background:#f0e9d8}
.stat{font-size:12px;color:#7a6c50}
ul.tree{list-style:none;margin:0;padding-left:18px;border-left:1px dashed #d6cbb0}
ul.tree>li{margin:2px 0}
.node{cursor:pointer;padding:2px 6px;border-radius:3px;display:inline-block}
.node:hover{background:#efe6d0}
.node.leaf{cursor:default;color:#4a4237}
.node.leaf:hover{background:transparent}
.tg{display:inline-block;width:14px;color:#a89874;user-select:none}
.cnt{color:#a89874;font-size:12px;margin-left:6px}
.rank{background:#e8dfc8;color:#5c4a26;border-radius:3px;padding:0 5px;font-size:12px;margin-left:6px}
.hit{background:#ffe9a8}
table{border-collapse:collapse;width:100%;font-size:13px;background:#fffdf8}
th,td{border:1px solid #ddd2b8;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#efe6d0;position:sticky;top:0}
.legend{font-size:12px;color:#7a6c50;margin:8px 0}
.wraphelp{font-size:12px;color:#7a6c50;margin-top:20px;border-top:1px solid #ddd2b8;padding-top:10px}
"""

JS_TREE = """
function toggle(el){
  var li=el.closest('li'); var ul=li.querySelector(':scope>ul');
  if(!ul) return;
  var open=ul.style.display!=='none';
  ul.style.display=open?'none':'';
  var tg=el.querySelector('.tg');
  if(tg) tg.textContent=open?'\\u25b8':'\\u25be';
}
function filter(q){
  q=(q||'').trim();
  var root=document.getElementById('tree');
  var all=root.querySelectorAll('li');
  if(!q){all.forEach(function(li){li.style.display='';});
    root.querySelectorAll('ul').forEach(function(u){u.style.display='none';});
    root.querySelectorAll(':scope>li>ul').forEach(function(u){u.style.display='';});
    root.querySelectorAll('.tg').forEach(function(t){t.textContent='\\u25be';});return;}
  all.forEach(function(li){li.style.display='none';});
  var marked=0;
  all.forEach(function(li){
    var n=li.querySelector(':scope>.node');
    if(!n) return;
    if(n.textContent.indexOf(q)>=0){
      marked++;
      li.style.display='';
      li.querySelectorAll('ul').forEach(function(u){u.style.display='';});
      var p=li.parentElement;
      while(p&&p.tagName==='LI'){p.style.display='';var u=p.parentElement;if(u)u.style.display='';p=u?u.parentElement:null;}
    }
  });
  document.getElementById('hitn').textContent=marked;
}
"""


def esc(s):
    return html.escape(str(s if s is not None else ""))


# ============ 1. 官制树 ============
def render_office_tree():
    def node_html(n, kind):
        name = n.get("office_name") or n.get("org_name") or ""
        kids = n.get("children") or []
        rank = n.get("rank") or ""
        cls = "node leaf" if not kids else "node"
        tg = '<span class="tg">\u25be</span>' if kids else '<span class="tg"></span>'
        badge = f'<span class="rank">{esc(rank)}</span>' if rank else ""
        inner = f'{tg}{esc(name)}{badge}'
        if kids:
            inner += f'<span class="cnt">{len(kids)}</span>'
        click = ' onclick="toggle(this)"' if kids else ""
        out = [f'<li><span class="{cls}"{click}>{inner}</span>']
        if kids:
            out.append("<ul>")
            for c in kids:
                out.append(node_html(c, kind))
            out.append("</ul>")
        out.append("</li>")
        return "".join(out)

    body = []
    body.append("<ul class='tree' id='tree'>")
    body.append("<li><span class='node' onclick=\"toggle(this)\">"
                "<span class='tg'>\u25be</span>翰林院/衙门体系"
                f"<span class='cnt'>{office_tree.get('total_roots')} 根 / "
                f"{office_tree.get('total_offices')} 官</span></span><ul>")
    for r in (office_tree.get("roots") or []):
        body.append(node_html(r, "office"))
    body.append("</ul></li>")
    body.append("<li><span class='node' onclick=\"toggle(this)\">"
                "<span class='tg'>\u25be</span>衙门体系"
                f"<span class='cnt'>{org_tree.get('total_roots')} 根 / "
                f"{org_tree.get('total_orgs')} 衙门</span></span><ul>")
    for r in (org_tree.get("roots") or []):
        body.append(node_html(r, "org"))
    body.append("</ul></li>")
    body.append("</ul>")

    html_out = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>明会典 · 官制树</title><style>{CSS}</style></head><body>
<header><h1>明会典 · 官制树</h1>
<p>正德本《大明会典》 衙门 {org_tree.get('total_orgs')} · 官职 {office_tree.get('total_offices')} ｜
数据源 _layers/office_tree.json + org_tree.json（P4-A 重建）</p></header>
<div class="wrap">
<div class="bar">
<input type="search" placeholder="搜索官名/衙门名（如：尚书、布政使、太仆寺）" oninput="filter(this.value)">
<button onclick="document.querySelector('input').value='';filter('')">重置</button>
<span class="stat">命中 <b id="hitn">0</b> 个节点</span>
</div>
<div class="legend">▸ 折叠 / ▾ 展开 ｜ 灰字为属官/下属数量 ｜ 标签为品级</div>
{''.join(body)}
<div class="wraphelp">
<b>本图怎么读</b>：上层为「衙门体系」（皇帝 → 六部/寺监/都司 → 属衙），
下层为「官职体系」（衙门 → 堂上官 → 属官）。两棵树都由卷 1–2 的建置沿革、
卷 12 的品级名录、卷 3–10 的职掌正文交叉推断，节点点击可折叠。<br>
<b>可信度</b>：office_tree 可达到 {office_tree.get('total_reachable')}/{office_tree.get('total_offices')}
（{office_tree.get('total_reachable')/max(1,office_tree.get('total_offices'))*100:.0f}%），
org_tree 可达 {org_tree.get('total_reachable')}/{org_tree.get('total_orgs')}
（{org_tree.get('total_reachable')/max(1,org_tree.get('total_orgs'))*100:.0f}%）。
</div></div>
<script>{JS_TREE}
document.querySelectorAll('ul.tree ul').forEach(function(u){{u.style.display='none';}});
</script></body></html>"""
    p = os.path.join(OUT, "vis_org_tree.html")
    open(p, "w", encoding="utf-8").write(html_out)
    return p


# ============ 2. 制度演变图 ============
def render_timeline():
    ERA_ORDER = ["洪武", "建文", "永乐", "洪熙", "宣德", "正统", "景泰", "天顺",
                 "成化", "弘治", "正德"]
    # 每个主题 × 年代的 事例数
    theme_era = {}
    for t in tims:
        cnt = Counter()
        vols = set(t.get("volumes") or [])
        for r in rules:
            if r.get("volume") in vols:
                for e in (r.get("era") or []):
                    for era in ERA_ORDER:
                        if era in str(e):
                            cnt[era] += 1
                            break
        theme_era[t["theme"]] = cnt
    themes = [t["theme"] for t in tims]
    maxv = max([v for c in theme_era.values() for v in c.values()] or [1])

    # 手绘热力表（HTML table，比 SVG 更好读）
    rows = []
    head = "".join(f"<th>{e}</th>" for e in ERA_ORDER)
    for t in tims:
        th = t["theme"]
        c = theme_era[th]
        cells = []
        for e in ERA_ORDER:
            v = c.get(e, 0)
            if v == 0:
                cells.append("<td style='background:#faf7f0;color:#c9c0aa'>·</td>")
            else:
                a = 0.15 + 0.85 * (v / maxv)
                cells.append(f"<td style='background:rgba(176,124,38,{a:.2f});"
                             f"color:{'#fff' if a>0.55 else '#3b2f18'};text-align:center'>{v}</td>")
        rows.append(f"<tr><th style='width:120px'>{esc(th)}</th>{''.join(cells)}"
                    f"<td class='stat'>卷 {','.join(str(v) for v in (t.get('volumes') or [])[:12])}"
                    f"{'…' if len(t.get('volumes') or [])>12 else ''}</td></tr>")

    # 年代跨度摘要
    spans = []
    for t in tims:
        ch = t.get("era_chain") or []
        if isinstance(ch, list) and ch:
            spans.append((t["theme"], " → ".join(str(x) for x in ch[:8])))
    span_html = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in spans)

    out = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>明会典 · 制度演变图</title><style>{CSS}</style></head><body>
<header><h1>明会典 · 制度演变图</h1>
<p>{len(tims)} 个制度主题 × {len(ERA_ORDER)} 朝 ｜ 色深 = 该朝事例条数 ｜
数据源 _layers/tim.json + rules.json（P1 重构）</p></header>
<div class="wrap">
<div class="legend">行=制度主题，列=朝代（洪武→正德）。数字为该主题在对应朝代下的
rules 事例条数；「·」表示该朝无事例。最右列为该主题覆盖的卷次。</div>
<table><thead><tr><th>制度主题</th>{head}<th>卷次</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<h3 style="margin-top:26px;font-size:15px">各主题年代链</h3>
<table><thead><tr><th style="width:130px">主题</th><th>年代链（按书内出现序）</th></tr></thead>
<tbody>{span_html}</tbody></table>
<div class="wraphelp">
<b>本图怎么读</b>：横向看一个朝代有哪些制度在动，纵向看一个制度怎么一步步改。
统计口径是「属于该主题卷次范围内的 rules 事例，按其纪年归入朝代」。
纪年无法判定的条目未计入（原书大量条目不标年号）。
</div></div></body></html>"""
    p = os.path.join(OUT, "vis_timeline.html")
    open(p, "w", encoding="utf-8").write(out)
    return p


# ============ 3. 地理管辖图 ============
def render_geo_tree():
    by_id = {g.get("geo_id"): g for g in geo}
    kids = defaultdict(list)
    for g in geo:
        pid = g.get("parent_id")
        if pid and pid in by_id:
            kids[pid].append(g)
    roots = [g for g in geo if not (g.get("parent_id") and g.get("parent_id") in by_id)]
    # 只取 省/直隶 级为根，其余作为子
    LEVELS = ("布政使司", "直隶", "都司", "行都司", "留守司", "宣慰司", "招讨司",
              "长官司", "军民府", "土府", "卫", "所")

    def node_html(g, depth=0):
        name = g.get("name") or ""
        t = g.get("type") or ""
        ks = kids.get(g.get("geo_id"), [])
        garr = g.get("garrisons") or []
        pst = g.get("post_stations") or []
        grn = g.get("granaries") or []
        meta = []
        if t:
            meta.append(t)
        if garr:
            meta.append(f"卫所{len(garr)}")
        if pst:
            meta.append(f"驿站{len(pst)}")
        if grn:
            meta.append(f"仓场{len(grn)}")
        if ks:
            meta.append(f"下辖{len(ks)}")
        badge = f"<span class='cnt'>{esc(' / '.join(meta))}</span>" if meta else ""
        if depth > 4 or not ks:
            return f"<li><span class='node leaf'>{esc(name)}{badge}</span></li>"
        out = [f"<li><span class='node' onclick=\"toggle(this)\">"
               f"<span class='tg'>\u25be</span>{esc(name)}{badge}</span><ul>"]
        for c in sorted(ks, key=lambda x: -(len(kids.get(x.get('geo_id'), [])))):
            out.append(node_html(c, depth + 1))
        out.append("</ul></li>")
        return "".join(out)

    body = ["<ul class='tree' id='tree'>"]
    for r in sorted(roots, key=lambda x: str(x.get("name"))):
        body.append(node_html(r, 0))
    body.append("</ul>")

    lv = Counter(g.get("type") or "?" for g in geo)
    lv_html = "".join(f"<tr><td>{esc(k)}</td><td style='text-align:right'>{v}</td></tr>"
                      for k, v in lv.most_common())
    total_g = sum(len(g.get("garrisons") or []) for g in geo)
    total_p = sum(len(g.get("post_stations") or []) for g in geo)
    total_r = sum(len(g.get("granaries") or []) for g in geo)

    out = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>明会典 · 地理管辖图</title><style>{CSS}</style></head><body>
<header><h1>明会典 · 地理管辖图</h1>
<p>节点 {len(geo)} ｜ 卫所挂靠 {total_g} · 驿站 {total_p} · 仓场 {total_r} ｜
数据源 _layers/geo.json（P2 + P2.5 并层）</p></header>
<div class="wrap">
<div class="bar">
<input type="search" placeholder="搜索地名（如：苏州府、云南、辽东）" oninput="filter(this.value)">
<button onclick="document.querySelector('input').value='';filter('')">重置</button>
<span class="stat">命中 <b id="hitn">0</b> 个节点</span>
</div>
<div class="legend">省/都司 → 府/州/卫 → 县/所 ｜ 灰字为类型与附属机构数 ｜ 默认展开两层</div>
{''.join(body)}
<h3 style="margin-top:26px;font-size:15px">节点类型分布</h3>
<table style="max-width:420px"><thead><tr><th>类型</th><th style="text-align:right">数量</th></tr></thead>
<tbody>{lv_html}</tbody></table>
<div class="wraphelp">
<b>本图怎么读</b>：这是《明会典》正文里出现的**全部**地理与军政建置的管辖关系。
卫所挂靠加了「同省约束」去伪（都司/留守司根 vs 布政司/直隶根须同省），
跨省同名者弃权不猜（50 例）。驿站、递运所、仓场来自卷 39–40 / 119–121 的专门名录，
以 85–90% 的匹配率并入对应府州。
</div></div>
<script>{JS_TREE}
document.querySelectorAll('ul.tree ul').forEach(function(u, i){{u.style.display='none';}});
(function(){{var n=0;document.querySelectorAll('ul.tree>li>ul>li>ul').forEach(function(u){{u.style.display='';n++;}});}})();
</script></body></html>"""
    p = os.path.join(OUT, "vis_geo_tree.html")
    open(p, "w", encoding="utf-8").write(out)
    return p


for fn in (render_office_tree, render_timeline, render_geo_tree):
    p = fn()
    print(f"写出 {p}  {os.path.getsize(p)/1024:.0f} KB")
