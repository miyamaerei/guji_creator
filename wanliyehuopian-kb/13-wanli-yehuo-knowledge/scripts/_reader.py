# -*- coding: utf-8 -*-
"""
生成《万历野获编》单文件 HTML 阅读器。

特性：
  - 纯静态、单文件、离线（数据内嵌）
  - 左侧：34 卷 × 1,451 条目导航（可搜索）
  - 右侧：条目详情（原文预览 + 各层结构化记录）
  - 层过滤：只看某层
  - 跨层索引：layer_count 直观显示"这条值多少"

输出：<BASE>/reader.html（随后由 _deliver.py 复制进交付包）
"""
import io, os, sys, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS = ["ents", "rules", "events", "appts", "rels", "opns", "cits", "mings", "tmes", "regs"]
OUT = os.path.join(BASE, "reader.html")

print("=== 生成阅读器 ===")

# ---------- 底座 ----------
reg = json.load(open(os.path.join(BASE, "_item_registry.json"), encoding="utf-8"))
items = reg["records"] if isinstance(reg, dict) else reg
print("底线条目: %d" % len(items))

# ---------- 跨层索引 ----------
join_raw = json.load(open(os.path.join(BASE, "_kg_join.json"), encoding="utf-8"))
join_recs = join_raw["records"] if isinstance(join_raw, dict) else join_raw
JOIN = {r["item_id"]: r for r in join_recs}
print("_kg_join: %d" % len(JOIN))

# ---------- 各层记录（按 item_id 归拢） ----------
by_item = {}
layer_count = {}
for lay in LAYERS:
    d = os.path.join(BASE, "_layers", lay)
    if not os.path.isdir(d):
        continue
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith(".json"):
            continue
        data = json.load(open(os.path.join(d, f), encoding="utf-8"))
        recs = data["records"] if isinstance(data, dict) else data
        for r in recs:
            iid = r.get("item_id")
            if not iid:
                continue
            by_item.setdefault(iid, {}).setdefault(lay, []).append(r)
            n += 1
    layer_count[lay] = n
    print("  %-7s %d" % (lay, n))

# ---------- 构造前端数据 ----------
# 条目：{id, vol, title, sub, preview, lc, layers:{层:条数}}
ent_objs = []
for it in items:
    iid = it.get("item_id")
    lay = by_item.get(iid, {})
    j = JOIN.get(iid, {})
    ent_objs.append({
        "id": iid,
        "vol": it.get("volume"),
        "vname": it.get("volume_name") or "",
        "type": it.get("volume_type") or "",
        "title": it.get("entry_title") or "",
        "sub": it.get("subcategory") or "",
        "preview": (it.get("original") or "")[:300],
        "lc": j.get("layer_count", sum(len(v) for v in lay.values())),
        "n": {k: len(v) for k, v in lay.items()},
    })

# 记录正文：{item_id: {层: [记录...]}} —— 只带展示需要的字段，控制体积
def slim(lay, r):
    out = {"_l": lay}
    for k in ("ent_id", "rule_id", "event_id", "appt_id", "rel_id", "opn_id",
              "cit_id", "ming_id", "tme_id", "reg_id"):
        if k in r:
            out["_id"] = r[k]
            break
    for k, v in r.items():
        if k.startswith("_") or k in ("item_id",):
            continue
        if v in (None, "", [], {}):
            continue
        out[k] = v
    return out

RECS = {}
for iid, lay in by_item.items():
    RECS[iid] = {k: [slim(k, r) for r in v] for k, v in lay.items()}

PAYLOAD = {
    "items": ent_objs,
    "recs": RECS,
    "layers": LAYERS,
    "layerCount": layer_count,
    "totalRecords": sum(layer_count.values()),
    "generated": "2026-10-18",
}
blob = json.dumps(PAYLOAD, ensure_ascii=False, separators=(",", ":"))
print("内嵌数据: %.2f MB" % (len(blob.encode("utf-8")) / 1024 / 1024))

LAYER_CN = {"ents": "实体", "rules": "规则", "events": "事件", "appts": "任职", "rels": "关系",
            "opns": "论说", "cits": "引书", "mings": "纪事", "tmes": "沿革", "regs": "制度"}

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>万历野获编 · 知识库阅读器</title>
<style>
*{box-sizing:border-box}
body{margin:0;font:14px/1.7 "Songti SC","SimSun",Georgia,serif;background:#f6f2e9;color:#2f2a22}
header{background:linear-gradient(180deg,#8b1f1f,#6d1616);color:#f6e7c8;padding:14px 20px;
  display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(0,0,0,.18)}
header h1{margin:0;font-size:19px;letter-spacing:2px}
header .stat{font-size:12.5px;opacity:.88}
header .stat b{color:#ffd98a;font-size:14px}
#wrap{display:flex;height:calc(100vh - 62px)}
#side{width:330px;flex:0 0 330px;border-right:1px solid #ddd0b6;background:#fffdf7;
  display:flex;flex-direction:column}
#search{padding:9px;border-bottom:1px solid #e8ddc7}
#search input{width:100%;padding:7px 10px;border:1px solid #d9cdb6;border-radius:7px;
  font-size:13px;font-family:inherit;background:#fff}
#vols{display:flex;flex-wrap:wrap;gap:4px;padding:8px 9px;border-bottom:1px solid #e8ddc7;
  max-height:88px;overflow:auto;background:#faf6ee}
.vchip{font-size:11.5px;padding:2px 7px;border:1px solid #ddd0b6;border-radius:10px;
  cursor:pointer;background:#fff;color:#5a4f3e}
.vchip.on{background:#8b1f1f;color:#fff;border-color:#8b1f1f}
#list{flex:1;overflow:auto}
.ei{padding:8px 12px;border-bottom:1px solid #f0e8d5;cursor:pointer;transition:.12s}
.ei:hover{background:#fdf6e6}
.ei.on{background:#f7e9c8;border-left:4px solid #8b1f1f;padding-left:8px}
.ei .t{font-size:13.5px;font-weight:600;color:#3a3226}
.ei .m{font-size:11.5px;color:#8a7c66;margin-top:2px;display:flex;gap:8px;flex-wrap:wrap}
.badge{display:inline-block;background:#8b1f1f;color:#fff;border-radius:9px;
  padding:0 6px;font-size:10.5px;line-height:16px}
#main{flex:1;overflow:auto;padding:20px 26px 60px}
h2.eh{margin:0 0 4px;font-size:22px;color:#8b1f1f;letter-spacing:1px}
.eh2{color:#8a7c66;font-size:12.5px;margin-bottom:14px}
.preview{background:#fffdf7;border:1px solid #e8ddc7;border-left:4px solid #a67c00;
  padding:12px 15px;border-radius:0 8px 8px 0;white-space:pre-wrap;font-size:13.5px;
  line-height:1.9;color:#3a3226;margin-bottom:18px}
.lsec{margin:16px 0}
.lsec h3{margin:0 0 8px;font-size:14.5px;color:#8b1f1f;padding-left:9px;
  border-left:4px solid #a67c00;display:flex;align-items:center;gap:8px}
.lsec h3 .cnt{font-size:11.5px;color:#8a7c66;font-weight:400}
.rec{background:#fff;border:1px solid #e8ddc7;border-radius:8px;padding:10px 13px;margin-bottom:8px}
.kv{display:grid;grid-template-columns:104px 1fr;gap:2px 10px;font-size:13px}
.kv .k{color:#8a7c66;font-size:12px;text-align:right;padding-top:2px}
.kv .v{white-space:pre-wrap;word-break:break-word;color:#2f2a22}
.kv .v.hl{color:#8b1f1f}
#empty{color:#8a7c66;text-align:center;padding:60px 0;font-size:14px}
.txtbtn{font-size:11.5px;color:#8b1f1f;cursor:pointer;border:1px solid #ddd0b6;
  border-radius:6px;padding:1px 8px;background:#fffdf7}
.txtbtn:hover{background:#f7e9c8}
.emptymsg{font-size:12px;color:#8a7c66}
</style>
</head>
<body>
<header>
  <h1>《万历野获编》知识库</h1>
  <span class="stat">明·沈德符 ｜ 34 卷 <b id="h-items">0</b> 条目 ｜ <b id="h-recs">0</b> 条结构化记录 ｜ 10 层</span>
</header>
<div id="wrap">
  <div id="side">
    <div id="search"><input id="q" placeholder="搜条目标题 / 内容…"></div>
    <div id="vols"></div>
    <div id="list"></div>
  </div>
  <div id="main"><div id="empty">← 从左侧选择一条笔记</div></div>
</div>
<script>
const D = __PAYLOAD__;
const LAYER_CN = __LAYERCN__;
const ON = "on";
let curVol = null, curId = null, kw = "";

document.getElementById("h-items").textContent = D.items.length.toLocaleString();
document.getElementById("h-recs").textContent  = D.totalRecords.toLocaleString();

/* 卷导航 */
(function(){
  const vols = [...new Set(D.items.map(i=>i.vol))].sort((a,b)=>a-b);
  const box = document.getElementById("vols");
  const all = document.createElement("span");
  all.className="vchip"+ON; all.textContent="全部"; all.onclick=()=>pickVol(null,all);
  box.appendChild(all);
  vols.forEach(v=>{
    const c=document.createElement("span");
    c.className="vchip"; c.textContent="卷"+v;
    c.onclick=()=>pickVol(v,c); box.appendChild(c);
  });
})();
function pickVol(v, el){
  curVol = v;
  document.querySelectorAll(".vchip").forEach(x=>x.classList.remove(ON));
  el.classList.add(ON); renderList();
}
document.getElementById("q").addEventListener("input", e=>{ kw = e.target.value.trim(); renderList(); });

/* 列表 */
function stext(i){
  return (i.title+" "+(i.preview||"")).toLowerCase();
}
function renderList(){
  const box = document.getElementById("list");
  const k = kw.toLowerCase();
  const rows = D.items.filter(i=>
    (curVol===null || i.vol===curVol) && (!k || stext(i).includes(k))
  );
  box.innerHTML = "";
  if(!rows.length){ box.innerHTML = '<div class="emptymsg" style="padding:14px">无匹配条目</div>'; return; }
  rows.forEach(i=>{
    const d=document.createElement("div");
    d.className="ei"+(i.id===curId?(" "+ON):"");
    const layTags = D.layers.filter(L=>i.n[L]).map(L=>LAYER_CN[L]).join("·");
    d.innerHTML = '<div class="t">'+esc(i.title||i.id)+'</div>'
      + '<div class="m"><span>'+i.id+'</span><span>卷'+i.vol+'</span>'
      + (i.sub?'<span>'+esc(i.sub)+'</span>':'')
      + '<span class="badge">'+i.lc+'</span><span>'+layTags+'</span></div>';
    d.onclick=()=>show(i.id);
    box.appendChild(d);
  });
}
const ESCMAP = {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"};
function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return ESCMAP[c]; }); }

/* 详情 */
function show(id){
  curId = id; renderList();
  const it = D.items.find(x=>x.id===id); if(!it) return;
  const recs = D.recs[id] || {};
  const m = document.getElementById("main");
  let h = '<h2 class="eh">'+esc(it.title||it.id)+'</h2>'
        + '<div class="eh2">'+it.id+' ｜ 卷'+it.vol+(it.vname?'（'+esc(it.vname)+'）':'')
        + (it.type?' ｜ '+esc(it.type):'')
        + (it.sub?' ｜ 门类：'+esc(it.sub):'')
        + ' ｜ <b>'+it.lc+'</b> 条记录 ｜ '+Object.values(it.n).reduce((a,b)=>a+b,0)+' 条层记录</div>';
  if(it.preview){
    h += '<div class="preview"><b style="color:#a67c00">原文（前 300 字）</b>\\n'+esc(it.preview)+'…</div>';
  }
  let shown = 0;
  D.layers.forEach(L=>{
    const arr = recs[L]; if(!arr || !arr.length) return;
    shown += arr.length;
    h += '<div class="lsec"><h3>'+LAYER_CN[L]+' <span class="cnt">'+arr.length+' 条 · '+L+'</span></h3>';
    arr.forEach(r=>{
      h += '<div class="rec"><div class="kv">';
      if(r._id) h += '<div class="k">ID</div><div class="v hl">'+esc(r._id)+'</div>';
      Object.keys(r).forEach(k=>{
        if(k.startsWith("_")) return;
        const v = r[k];
        h += '<div class="k">'+esc(k)+'</div><div class="v">'+esc(Array.isArray(v)?v.join("、"):v)+'</div>';
      });
      h += '</div></div>';
    });
    h += '</div>';
  });
  if(!shown) h += '<div class="emptymsg">该条目暂无结构化记录</div>';
  h += '<div style="margin-top:24px"><span class="txtbtn" onclick="window.scrollTo(0,0)">↑ 回到顶部</span></div>';
  m.innerHTML = h; m.scrollTop = 0;
}
renderList();
</script>
</body>
</html>
"""
HTML = HTML.replace("__PAYLOAD__", blob).replace("__LAYERCN__", json.dumps(LAYER_CN, ensure_ascii=False))

open(OUT, "w", encoding="utf-8", newline="").write(HTML)
print("输出: %s" % OUT)
print("大小: %.2f MB" % (os.path.getsize(OUT) / 1024 / 1024))
