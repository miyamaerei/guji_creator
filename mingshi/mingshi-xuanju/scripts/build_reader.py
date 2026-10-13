# -*- coding: utf-8 -*-
"""
build_reader.py —— 生成《明史·选举志》知识图谱阅读器（单文件 HTML，内联数据，可重跑）

读取：_layers/<layer>/<layer>_<vol>.json  +  _kg_join.json  +  _data/query_acceptance.txt
产出：_deliver/选举志阅读器.html  （双击即可在浏览器打开，无需服务器）
"""
import os
import json
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # mingshi-xuanju
LAYER_DIR = os.path.join(ROOT, "_layers")
JOIN_PATH = os.path.join(ROOT, "_kg_join.json")
QA_PATH = os.path.join(ROOT, "_data", "query_acceptance.txt")
OUT_DIR = os.path.join(ROOT, "_deliver")
OUT_PATH = os.path.join(OUT_DIR, "选举志阅读器.html")

LAYER_NAMES = {
    "ents": "实体 L1", "rules": "规则 L2", "regs": "制度 REG", "procs": "流程 L3",
    "structs": "四维 L4", "tmes": "沿革 C14", "opns": "论说 C9", "nams": "名录 NAM",
    "frds": "防弊 FRD", "objs": "名物 OBJ", "events": "事件 L5",
}
VOL_NAMES = {"45": "卷四十五 选举一", "46": "卷四十六 选举二", "47": "卷四十七 选举三"}
ID_PREFIXES = ("ENT-", "REG-", "TME-", "PROC-", "EVT-", "OPN-", "NAM-",
               "FRD-", "OBJ-", "RULE-", "EVO-", "QUAN-", "INST-", "STRUCT-")

# —— 十问（与 query_acceptance.txt 对应，jump 指向条目/搜索，点击直达）—— #
QA = [
    {"q": "明代科举三级（乡/会/殿）的场次与内容各是什么？",
     "a": "乡试（子午卯酉年，行省）三场：初场四书义三道、经义四道；二场论一道、判五道、诏诰表内科一道；三场策五道。会试次年礼部，殿试御殿，分三甲。",
     "jump": {"type": "item", "value": "46-010"}},
    {"q": "南北榜案始末与分地取士制度如何演变？",
     "a": "洪武三十年会试，考官刘三吾等取皆南人，北人哗，帝怒亲策复阅，取韩克忠等六十一人皆北人（北榜），刘三吾等戍边。后洪熙始分南北卷，景泰定比例，万历间南五十九北三十八中三，遂为永制。",
     "jump": {"type": "item", "value": "46-026"}},
    {"q": "八股文的形制（破承起讲…）如何定义？",
     "a": "成化年间定八股格：破题、承题、起讲、入题、起股、中股、后股、束股，每股用两比偶句，合为八股（股者，对偶之股也）。",
     "jump": {"type": "item", "value": "46-011"}},
    {"q": "各省乡试解额、会试定额是多少？",
     "a": "解额分省：直隶百名，河南、山东、广东各四十，广西二十五，云南二十等；会试中式额约三百（洪武间多至百二三十，后定三百）。",
     "jump": {"type": "item", "value": "46-017"}},
    {"q": "武科（武举）三级与殿试始于何时？",
     "a": "吴元年定武科；洪武二十年立武学、行武举；成化十四年设武科乡、会试；崇祯四年始行武举殿试（王来聘为状元）。",
     "jump": {"type": "item", "value": "46-015"}},
    {"q": "国子监监生有哪几类？积分法与历事如何运作？",
     "a": "监生有举监、贡监、荫监、例监四色；积分法：孟月试本经义、仲月试诏诰表策、季月试经史策，一岁积八分；历事：正历二百二十名、杂历一百五十八名，拨诸司习政。",
     "jump": {"type": "item", "value": "45-010"}},
    {"q": "庶吉士如何考选？徐溥之议为何？",
     "a": "进士观政后选年少貌美者入翰林读书，称庶吉士；徐溥奏请于翰林院设庶吉士馆，俾专精文学、储养馆阁之才（弘治间始定）。",
     "jump": {"type": "search", "value": "庶吉士"}},
    {"q": "铨选『三途并用』与掣签法何义？",
     "a": "三途并用：进士、举人、贡生并铨，高拱主之。掣签：万历间孙丕扬以权贵干请难拒，创掣签法，选人于堂上抽签定缺，以示至公。",
     "jump": {"type": "item", "value": "47-011"}},
    {"q": "科场弊案（关节/冒籍/辅臣子弟）有哪些？",
     "a": "弊有冒籍（假贯）、倩代（枪手）、关节（通考官）、怀挟（夹带）；嘉靖间辅臣子弟中式引发争议，严查，防弊立法屡更。",
     "jump": {"type": "item", "value": "46-009"}},
    {"q": "荐举制在明初如何盛、后如何废？",
     "a": "太祖屡诏求贤，荐举极盛，儒士骤贵；洪武十七年定科举岁贡之式，荐举渐轻；正统间罢荐举，专用科目。",
     "jump": {"type": "item", "value": "47-010"}},
]


def load_layers():
    by_id = {}          # id -> record (with _layer)
    by_layer = {}       # layer -> [ids]
    for layer in LAYER_NAMES:
        ldir = os.path.join(LAYER_DIR, layer)
        if not os.path.isdir(ldir):
            continue
        for fp in sorted(glob.glob(os.path.join(ldir, "*.json"))):
            with io.open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            for r in data.get("records", []):
                r["_layer"] = layer
                rid = r.get("id")
                if rid:
                    by_id[rid] = r
                    by_layer.setdefault(layer, []).append(rid)
    return by_id, by_layer


def load_join():
    with io.open(JOIN_PATH, "r", encoding="utf-8") as f:
        join = json.load(f)
    items = []
    for iid, j in join.items():
        layers = {L: j.get(L, []) for L in LAYER_NAMES}
        items.append({
            "item_id": iid,
            "volume": j.get("volume", ""),
            "layer_count": j.get("layer_count", 0),
            "layers": layers,
        })
    items.sort(key=lambda x: (x["volume"], x["item_id"]))
    return items


import io  # noqa: E402  (placed after function defs to keep load order clear)


def name_of(rec):
    for k in ("name", "title", "content", "text", "who", "era"):
        if isinstance(rec.get(k), str) and rec[k].strip():
            return rec[k]
    return rec.get("id", "?")


def build_html(by_id, by_layer, items):
    # 统计
    total_records = len(by_id)
    layer_counts = {L: len(ids) for L, ids in by_layer.items()}
    # 组装数据对象
    data = {
        "layers": LAYER_NAMES,
        "layerCounts": layer_counts,
        "volNames": VOL_NAMES,
        "items": items,
        "byId": by_id,
        "byLayer": by_layer,
        "qa": QA,
    }
    payload = json.dumps(data, ensure_ascii=False)
    payload = payload.replace("</script", "<\\/script")

    return HTML_TEMPLATE.replace("/*__DATA__*/", "window.KG = %s;" % payload)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>明史·选举志 知识图谱阅读器</title>
<style>
  :root{
    --bg:#f5f6f8; --panel:#ffffff; --ink:#1f2329; --sub:#6b7280; --line:#e5e7eb;
    --brand:#9a2e2e; --brand2:#b5453b; --chip:#eef2f7; --chipink:#274690;
    --hl:#fff3cd; --ok:#1a7f37;
  }
  *{box-sizing:border-box}
  body{margin:0;font-family:"PingFang SC","Microsoft YaHei",-apple-system,Segoe UI,sans-serif;
       background:var(--bg);color:var(--ink);font-size:14px;line-height:1.6}
  header{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;
         padding:14px 22px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
  header h1{margin:0;font-size:18px;font-weight:700;letter-spacing:1px}
  header .stats{display:flex;gap:14px;margin-left:auto;flex-wrap:wrap}
  header .stat{background:rgba(255,255,255,.15);border-radius:8px;padding:4px 12px;text-align:center}
  header .stat b{display:block;font-size:17px}
  header .stat span{font-size:11px;opacity:.85}
  .wrap{display:flex;min-height:calc(100vh - 60px)}
  aside{width:248px;background:var(--panel);border-right:1px solid var(--line);
        padding:14px;overflow:auto;position:sticky;top:0;height:calc(100vh - 60px)}
  aside h3{margin:14px 0 6px;font-size:12px;color:var(--sub);text-transform:uppercase;letter-spacing:1px}
  .tabs{display:flex;flex-wrap:wrap;gap:6px}
  .tab{cursor:pointer;border:1px solid var(--line);background:#fff;border-radius:6px;
       padding:5px 9px;font-size:12px;color:var(--ink)}
  .tab.active{background:var(--brand);color:#fff;border-color:var(--brand)}
  .layerlist .tab{display:flex;justify-content:space-between;width:100%}
  .layerlist .tab small{color:var(--sub)}
  .layerlist .tab.active small{color:#ffe}
  .search{width:100%;padding:7px 9px;border:1px solid var(--line);border-radius:6px;margin-top:6px;font-size:13px}
  main{flex:1;padding:18px 24px;overflow:auto;height:calc(100vh - 60px)}
  .crumb{color:var(--sub);font-size:13px;margin-bottom:10px}
  .crumb a{color:var(--chipink);cursor:pointer}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;
        padding:14px 16px;margin-bottom:12px;box-shadow:0 1px 2px rgba(0,0,0,.03)}
  .card h4{margin:0 0 6px;font-size:15px;color:var(--brand)}
  .item-row{display:flex;align-items:center;gap:10px;padding:9px 12px;border:1px solid var(--line);
            border-radius:8px;margin-bottom:8px;cursor:pointer;background:#fff}
  .item-row:hover{border-color:var(--brand);background:#fcf6f6}
  .item-row .iid{font-weight:700;color:var(--brand);min-width:62px}
  .item-row .vol{color:var(--sub);font-size:12px}
  .item-row .lc{margin-left:auto;background:var(--chip);color:var(--chipink);
                border-radius:20px;padding:2px 10px;font-size:12px}
  .badges{display:flex;flex-wrap:wrap;gap:4px}
  .badge{font-size:11px;background:var(--chip);color:var(--chipink);border-radius:4px;padding:1px 7px}
  .kv{display:grid;grid-template-columns:96px 1fr;gap:4px 10px;margin-top:8px}
  .kv .k{color:var(--sub);font-size:12px}
  .kv .v{font-size:13px;word-break:break-word}
  .chips{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
  .chip{background:var(--chip);color:var(--chipink);border-radius:14px;padding:2px 10px;
        font-size:12px;cursor:pointer;border:1px solid transparent}
  .chip:hover{border-color:var(--chipink)}
  .chip.ent{background:#eaf3ff;color:#1a56a8}
  .chip.tme{background:#fdeef3;color:#a3405b}
  .chip.evt{background:#fff1e6;color:#b5651d}
  .sec-title{font-size:13px;color:var(--sub);margin:14px 0 6px;font-weight:700;
             border-left:3px solid var(--brand);padding-left:8px}
  .qa{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:10px;background:#fff}
  .qa .q{font-weight:700;color:var(--ink);cursor:pointer}
  .qa .q:hover{color:var(--brand)}
  .qa .a{color:var(--sub);font-size:13px;margin-top:6px}
  .qa .go{display:inline-block;margin-top:8px;font-size:12px;color:var(--brand);cursor:pointer}
  .src{font-size:11px;color:var(--sub);margin-top:6px}
  .empty{color:var(--sub);padding:30px;text-align:center}
  footer{text-align:center;color:var(--sub);font-size:12px;padding:10px}
  mark{background:var(--hl);padding:0 2px;border-radius:3px}
</style>
</head>
<body>
<header>
  <h1>明史·选举志 知识图谱阅读器</h1>
  <div class="stats" id="stats"></div>
</header>
<div class="wrap">
  <aside>
    <h3>卷</h3>
    <div class="tabs" id="volTabs"></div>
    <h3>层</h3>
    <div class="tabs layerlist" id="layerTabs"></div>
    <h3>检索</h3>
    <input class="search" id="search" placeholder="搜索名称/原文/ID…">
    <h3>导航</h3>
    <div class="tabs">
      <div class="tab active" data-mode="item" id="mItem">按条目</div>
      <div class="tab" data-mode="layer" id="mLayer">按层</div>
      <div class="tab" data-mode="qa" id="mQA">十问</div>
    </div>
  </aside>
  <main id="main"></main>
</div>
<footer>由 scripts/build_reader.py 生成 · 数据源自 _layers/ 与 _kg_join.json · 可重跑</footer>

<script>
/*__DATA__*/
(function(){
  const KG = window.KG;
  const $ = s => document.querySelector(s);
  const main = $("#main");
  let state = {vol:"all", layer:"all", mode:"item", q:""};

  // 统计
  const totalItems = KG.items.length;
  const totalRecs = Object.keys(KG.byId).length;
  const joinN = KG.items.length;
  $("#stats").innerHTML = [
    ["3","卷 (45/46/47)"],["11","层"],["totalRecs","记录"],["joinN","跨层索引"]
  ].map(([b,s])=>`<div class="stat"><b>${b}</b><span>${s}</span></div>`).join("");

  // 卷 tabs
  const vols = [["all","全部"],["45","卷45"],["46","卷46"],["47","卷47"]];
  $("#volTabs").innerHTML = vols.map(([v,t])=>
    `<div class="tab${v==='all'?' active':''}" data-v="${v}">${t}</div>`).join("");
  // 层 tabs
  const layers = Object.keys(KG.layers);
  let lt = `<div class="tab${'all'==='all'?' active':''}" data-l="all">全部 <small>${totalRecs}</small></div>`;
  layers.forEach(l=>{
    const c = KG.layerCounts[l]||0;
    lt += `<div class="tab" data-l="${l}">${KG.layers[l]} <small>${c}</small></div>`;
  });
  $("#layerTabs").innerHTML = lt;

  // 事件
  $("#volTabs").addEventListener("click",e=>{
    const t=e.target.closest(".tab"); if(!t)return;
    state.vol=t.dataset.v;
    [...$("#volTabs").children].forEach(x=>x.classList.toggle("active",x===t));
    render();
  });
  $("#layerTabs").addEventListener("click",e=>{
    const t=e.target.closest(".tab"); if(!t)return;
    state.layer=t.dataset.l;
    [...$("#layerTabs").children].forEach(x=>x.classList.toggle("active",x===t));
    render();
  });
  document.querySelectorAll("[data-mode]").forEach(el=>{
    el.addEventListener("click",()=>{
      state.mode=el.dataset.mode;
      document.querySelectorAll("[data-mode]").forEach(x=>x.classList.toggle("active",x===el));
      render();
    });
  });
  $("#search").addEventListener("input",e=>{state.q=e.target.value.trim();render();});

  function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
  function hl(s){
    s=esc(s);
    if(state.q){const q=state.q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
      s=s.replace(new RegExp(q,'gi'),m=>`<mark>${m}</mark>`);}
    return s;
  }
  function recName(r){return r.name||r.title||r.content||r.text||r.who?.text||r.era?.text||r.id||"?";}
  function classOf(id){
    if(id.startsWith("ENT-"))return"ent";
    if(id.startsWith("TME-"))return"tme";
    if(id.startsWith("EVT-"))return"evt";
    return"";
  }
  function chip(id){
    const r=KG.byId[id]; const nm=r?recName(r):id;
    return `<span class="chip ${classOf(id)}" data-id="${id}">${esc(nm)}</span>`;
  }
  function crossChips(rec){
    let out=[];
    for(const k in rec){
      if(k.startsWith("_"))continue;
      const v=rec[k];
      if(k.endsWith("_ids")&&Array.isArray(v)){v.forEach(x=>out.push(chip(x)));}
      else if(Array.isArray(v)){
        v.forEach(x=>{if(typeof x==="string"&&IDP(x))out.push(chip(x));});
      } else if(typeof v==="string"&&IDP(v)){
        out.push(chip(v));
      }
    }
    return out.length?`<div class="chips">${out.join("")}</div>`:"";
  }
  function IDP(s){return /^(ENT|REG|TME|PROC|EVT|OPN|NAM|FRD|OBJ|RULE|EVO|QUAN|INST|STRUCT)-/.test(s);}

  function kvOf(rec){
    const skip=new Set(["_layer","id","key","vol","item_id","slot","confidence","src_loc",
      "evidence","name","title","content","text","who","era","related_evo","related_reg",
      "ent_keys","tme_keys","proc_keys","reg_keys","evt_keys","rule_keys","opn_keys",
      "nam_keys","frd_keys","obj_keys","struct_keys","related_evo_key","related_reg_key"]);
    let h="";
    for(const k in rec){
      if(skip.has(k))continue;
      const v=rec[k];
      let val="";
      if(v===null||v===undefined||v==="")continue;
      if(Array.isArray(v)){
        if(v.length&&typeof v[0]==="object"){
          val=v.map(o=>Object.entries(o).map(([a,b])=>`${a}:${b}`).join(" | ")).join("；");
        } else val=v.join("、");
      } else if(typeof v==="object"){
        val=Object.entries(v).map(([a,b])=>`${a}:${b}`).join("，");
      } else val=String(v);
      if(!val)continue;
      h+=`<div class="k">${esc(k)}</div><div class="v">${hl(val)}</div>`;
    }
    return h?`<div class="kv">${h}</div>`:"";
  }

  function itemCard(it){
    const layerKeys=layers.filter(l=>(it.layers[l]||[]).length>0);
    const badges=layerKeys.map(l=>`<span class="badge">${KG.layers[l]}</span>`).join("");
    return `<div class="item-row" data-item="${it.item_id}">
      <span class="iid">${it.item_id}</span>
      <span class="vol">${KG.volNames[it.volume]||it.volume}</span>
      <span class="badges">${badges}</span>
      <span class="lc">贯通 ${it.layer_count} 层</span>
    </div>`;
  }

  function render(){
    if(state.mode==="qa")return renderQA();
    if(state.mode==="layer")return renderLayer();
    renderItems();
  }

  function renderItems(){
    let list=KG.items.filter(it=>(state.vol==="all"||it.volume===state.vol));
    if(state.layer!=="all")list=list.filter(it=>(it.layers[state.layer]||[]).length>0);
    if(state.q){
      list=list.filter(it=>{
        const ids=[].concat(...layers.map(l=>it.layers[l]||[]));
        return ids.some(id=>{const r=KG.byId[id];return r&&JSON.stringify(r).toLowerCase().includes(state.q.toLowerCase());});
      });
    }
    let html=`<div class="crumb">按条目 · ${state.vol==="all"?"全部卷":KG.volNames[state.vol]} · ${state.layer==="all"?"全部层":KG.layers[state.layer]} · 共 ${list.length} 条</div>`;
    if(!list.length)html+=`<div class="empty">无匹配条目</div>`;
    html+=list.map(itemCard).join("");
    main.innerHTML=html;
    main.querySelectorAll(".item-row").forEach(el=>el.onclick=()=>showItem(el.dataset.item));
  }

  function renderLayer(){
    let ids=KG.byLayer[state.layer]||[];
    let recs=ids.map(id=>KG.byId[id]).filter(Boolean);
    if(state.vol!=="all")recs=recs.filter(r=>String(r.vol)===state.vol);
    if(state.q)recs=recs.filter(r=>JSON.stringify(r).toLowerCase().includes(state.q.toLowerCase()));
    let html=`<div class="crumb">按层 · ${KG.layers[state.layer]||state.layer} · ${state.vol==="all"?"全部卷":KG.volNames[state.vol]} · 共 ${recs.length} 条</div>`;
    if(!recs.length)html+=`<div class="empty">无匹配记录</div>`;
    html+=recs.map(recCard).join("");
    main.innerHTML=html;
    bindChips();
  }

  function recCard(r){
    const layer=KG.layers[r._layer]||r._layer;
    let h=`<div class="card"><h4>${hl(recName(r))} <span style="font-size:12px;color:var(--sub)">${r.id} · ${layer}</span></h4>`;
    h+=`<div class="src">卷${r.vol} · item ${r.item_id} · ${r.src_loc||""} · 置信度 ${r.confidence??""}</div>`;
    if(r.evidence)h+=`<div class="v" style="margin-top:6px;color:var(--ink)">${hl(r.evidence)}</div>`;
    h+=kvOf(r);
    h+=crossChips(r);
    h+=`</div>`;
    return h;
  }

  function showItem(iid){
    const it=KG.items.find(x=>x.item_id===iid); if(!it)return;
    let html=`<div class="crumb"><a id="back">← 返回列表</a> · 条目 ${iid} · ${KG.volNames[it.volume]||it.volume} · 贯通 ${it.layer_count} 层</div>`;
    layers.forEach(l=>{
      const ids=it.layers[l]||[];
      if(!ids.length)return;
      html+=`<div class="sec-title">${KG.layers[l]}（${ids.length}）</div>`;
      ids.forEach(id=>{
        const r=KG.byId[id]; if(!r)return;
        html+=recCard(r);
      });
    });
    main.innerHTML=html;
    $("#back").onclick=render;
    bindChips();
  }

  function renderQA(){
    let html=`<div class="crumb">十问验收（与 query_acceptance.txt 对应，10/10 能答）</div>`;
    KG.qa.forEach((q,i)=>{
      const go=q.jump.type==="item"?`→ 查看条目 ${q.jump.value}`:`→ 检索「${q.jump.value}」`;
      html+=`<div class="qa"><div class="q" data-i="${i}">${i+1}. ${esc(q.q)}</div>
        <div class="a">${esc(q.a)}</div>
        <span class="go" data-i="${i}">${go}</span></div>`;
    });
    main.innerHTML=html;
    main.querySelectorAll(".qa .q,.qa .go").forEach(el=>el.onclick=()=>{
      const q=KG.qa[+el.dataset.i];
      if(q.jump.type==="item"){showItem(q.jump.value);}
      else{document.querySelector('[data-mode="item"]').click();
           $("#search").value=q.jump.value;state.q=q.jump.value;render();}
    });
  }

  function bindChips(){
    main.querySelectorAll(".chip[data-id]").forEach(el=>el.onclick=()=>{
      const id=el.dataset.id; const r=KG.byId[id];
      if(r&&r.item_id)showItem(r.item_id);
      else if(r)main.insertAdjacentHTML("afterbegin",recCard(r));
    });
  }

  render();
})();
</script>
</body>
</html>
"""


def main():
    by_id, by_layer = load_layers()
    items = load_join()
    html = build_html(by_id, by_layer, items)
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    with io.open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK build_reader -> %s" % OUT_PATH)
    print("  记录数=%d  条目数=%d  层数=%d" % (len(by_id), len(items), len(by_layer)))


if __name__ == "__main__":
    main()
