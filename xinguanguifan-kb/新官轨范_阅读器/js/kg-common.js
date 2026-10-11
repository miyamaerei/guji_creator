/* =========================================================
 * kg-common.js —— 《新官轨范》知识阅读器 · 共享组件层
 * 职责：数据引用、基础工具、卡片/详情渲染组件、
 *       面包屑导航 + hash 路由。
 * 由 新官轨范阅读器.html 在 data.js 之后引入。
 * ========================================================= */
var KG = window.KG;
var $ = function(s){ return document.querySelector(s); };
function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function findItem(iid){
  for(var i=0;i<KG.chapters.length;i++){
    var ch=KG.chapters[i];
    for(var j=0;j<ch.items.length;j++){ if(ch.items[j].iid===iid) return {ch:ch, it:ch.items[j]}; }
  }
  return null;
}
/* 全局状态 */
var curIid=null, curChNo=null, curEid=null;
var TYPE_COLOR={
  official:['#E3EDFB','#1D4E89'], person:['#F2E6FA','#6B2D8B'], org:['#DDF0EE','#1E6E64'],
  place:['#E4F2E4','#2D6A2D'], document:['#FDEEDC','#9A5B00'], institution:['#EDE6DF','#6E4A2F'],
  behavior:['#FBE3E3','#A12D2D'], object:['#ECECEC','#5A5A5A'], punishment:['#FBDCDC','#8B1A1A'],
  time:['#FFF4D6','#7A5A00'], quantity:['#FBE4EC','#8E2E52'], undetermined:['#F4F2EE','#777']
};
function tyLabel(ty){
  return {official:'职官',person:'人物',org:'机构',place:'地点',document:'文书',institution:'制度',
    behavior:'行为',object:'器物',punishment:'刑罚',time:'时间',quantity:'数量',undetermined:'待定'}[ty]||ty;
}
/* ========== 面包屑 + hash 路由 ========== */
var CRUMBS=[{page:'reader', params:'', label:'阅读器'}];
var VIEWS=['reader','list','detail'];
function pageHash(page, params){ return '/'+page+(params?'?'+params:''); }
function parseParams(params){
  var o={};
  (params||'').split('&').forEach(function(kv){
    if(!kv) return;
    var a=kv.split('='); o[a[0]]=decodeURIComponent(a[1]||'');
  });
  return o;
}
function parseHash(){
  var h=location.hash.replace(/^#\/?/,'');
  var p=h.split('?')[0]||'reader';
  return {page:p, qs:parseParams(h.split('?')[1]||''), raw:location.hash.replace(/^#\/?/,'')};
}
function renderView(){
  var cur=parseHash().page;
  VIEWS.forEach(function(v){
    var el=$('#view-'+v);
    if(el) el.classList.toggle('hidden', v!==cur);
  });
}
function renderCrumb(){
  var h='<span class="crumb" data-i="0" data-page="reader" data-params="">阅读器</span>';
  for(var i=1;i<CRUMBS.length;i++){
    var c=CRUMBS[i];
    h+='<span class="sep">›</span><span class="crumb'+(i===CRUMBS.length-1?' cur':'')+'" data-i="'+i+'" data-page="'+esc(c.page)+'" data-params="'+esc(c.params)+'">'+esc(c.label)+'</span>';
  }
  $('#crumbBar').innerHTML=h;
}
/* 统一导航入口：记录面包屑 + 切 hash + 渲染目标页（同页同参去重） */
function nav(page, params, label){
  params=params||'';
  var top=CRUMBS[CRUMBS.length-1];
  if(top&&top.page===page&&top.params===params) top.label=label||page;
  else CRUMBS.push({page:page, params:params, label:label||page});
  location.hash=pageHash(page, params);
  renderView(); renderCrumb();
  dispatchView(page, params);
}
/* 面包屑回跳 */
function crumbTo(idx){
  CRUMBS=CRUMBS.slice(0, idx+1);
  var top=CRUMBS[CRUMBS.length-1];
  location.hash=pageHash(top.page, top.params);
  renderView(); renderCrumb();
  dispatchView(top.page, top.params);
}
window.addEventListener('hashchange', function(){
  var h=parseHash();
  var rawParams=location.hash.replace(/^#\/?/,'').split('?')[1]||'';
  while(CRUMBS.length>1){
    var top=CRUMBS[CRUMBS.length-1];
    if(top.page===h.page&&top.params===rawParams) break;
    CRUMBS.pop();
  }
  if(!CRUMBS.length) CRUMBS.push({page:h.page, params:rawParams, label:h.page});
  renderView(); renderCrumb();
  dispatchView(h.page, rawParams);
});
/* 目标页分发（由 kg-pages.js 覆写实现） */
function dispatchView(page, params){}
/* 跳详情页（统一入口） */
function kindLabel(kind, id){
  if(kind==='ent'){ var e=KG.entities[id]; return (e?e.normalized:id)+'（实体）'; }
  if(kind==='rule'){ var r=KG.rules[id]; return id+(r&&r.title?' · '+r.title:''); }
  if(kind==='proc'){ var p=KG.procs[id]; return id+(p&&p.title?' · '+p.title:''); }
  if(kind==='event'){ var ev=KG.events[id]; return id+(ev&&ev.title?' · '+ev.title:''); }
  if(kind==='struct'){ var s=KG.structs[id]; return id+(s&&(s.name||s.doc_type||s.fraud||s.keyword)?' · '+(s.name||s.doc_type||s.fraud||s.keyword):''); }
  if(kind==='item'){ var f=findItem(id); return id+(f?' · '+f.ch.name:''); }
  if(kind==='join'){ var f2=findItem(id); return id+(f2?' · '+f2.ch.name:'')+'（五层贯通）'; }
  if(kind==='ch'){ var ch=KG.chapters.find(function(c){return c.no===id;}); return ch?ch.name:id; }
  return id||kind;
}
function goDetail(kind, id){
  nav('detail', 'kind='+kind+'&id='+encodeURIComponent(id), kindLabel(kind, id));
}
var LAYER_LABEL={ent:'实体总览',rule:'规则总览',proc:'流程总览',event:'事件总览',struct:'结构总览',item:'条目总览',five:'五层贯通总览'};
function goList(layer){
  nav('list', 'layer='+(layer||'ent'), LAYER_LABEL[layer||'ent']||'总览');
}
function goReader(){
  crumbTo(0);
}
/* ========== 基础组件 ========== */
function kv(k,v){ return '<div class="kv"><span class="k">'+k+'</span><span class="v">'+(v||'—')+'</span></div>'; }
function objLink(kind,id,label){
  return '<span class="linkbtn" data-obj="'+kind+'" data-id="'+id+'">'+(label||id)+'</span>';
}
/* 原文可点块 */
function oriBlock(text, itemId){
  var body=esc(text||'');
  return '<div class="ori'+(itemId?' ori-link':'')+'"'+(itemId?' data-obj="item" data-id="'+itemId+'" title="点击打开来源条目 '+itemId+'"':'')+'>'+body+'</div>';
}
/* 反查：流程/事件 → 来源条目 */
function procItemId(pid){ for(var iid in KG.join){ if((KG.join[iid].proc_ids||[]).indexOf(pid)>=0) return iid; } return ''; }
function eventItemId(eid){ for(var iid in KG.join){ if((KG.join[iid].event_ids||[]).indexOf(eid)>=0) return iid; } return ''; }
/* 文本实体化：把 agent/who/what 等文本里的已知实体词包成可点击实体 */
function entify(text){
  if(text===undefined||text===null) return '';
  if(typeof text!=='string') text=String(text);
  if(!text) return '';
  var best=null;
  for(var eid in KG.entities){
    var e=KG.entities[eid];
    var names=[e.normalized].concat(e.surfaces||[]);
    for(var i=0;i<names.length;i++){
      var nm=names[i];
      if(nm&&text.indexOf(nm)>=0&&(!best||nm.length>best.nm.length)) best={eid:eid, nm:nm, ty:e.type||'undetermined'};
    }
  }
  if(!best) return esc(text);
  var i=text.indexOf(best.nm);
  return esc(text.slice(0,i))+
    '<span class="ent ent-'+best.ty+'" data-eid="'+best.eid+'">'+esc(best.nm)+'</span>'+
    entify(text.slice(i+best.nm.length));
}
/* 条目摘要：优先取规则动作槽位，其次类型，最后原文开头 */
function itemSummary(iid){
  var j=KG.join[iid];
  var r=j&&j.rule_id?KG.rules[j.rule_id]:null;
  if(r){
    var parts=[];
    ['obligation_action','prohibited_action','allowed_action','deadline','punishment','purpose'].forEach(function(k){
      if(r[k]) parts.push(String(r[k]));
    });
    if(parts.length) return parts.join('；');
    return r.type||'';
  }
  var f=findItem(iid);
  return f?f.it.text.slice(0,12):'';
}
/* 规则类型 -> 短徽标 */
function ruleBadge(type){
  var map={禁止型:'禁',义务型:'须',允许型:'许',程序型:'序',时限型:'限',处罚型:'罚'};
  if(!type) return '';
  var s='';
  for(var k in map){ if(type.indexOf(k)>=0) s+=map[k]; }
  return s||'规';
}
/* ========== 顶栏统计 + 图例 ========== */
function renderStat(){
  var m=KG.meta;
  $('#statLine').innerHTML =
    '<span class="statlink" data-l="item" title="点击浏览全部条目">章 <b>'+m.chapters+'</b></span>'+
    '<span class="statlink" data-l="item" title="点击浏览全部条目">条目 <b>'+m.items+'</b></span>'+
    '<span class="statlink" data-l="ent" title="点击浏览全部实体">实体 <b>'+m.entities+'</b></span>'+
    '<span class="statlink" data-l="rule" title="点击浏览全部规则">规则 <b>'+m.rules+'</b></span>'+
    '<span class="statlink" data-l="proc" title="点击浏览全部流程">流程 <b>'+m.procs+'</b></span>'+
    '<span class="statlink" data-l="event" title="点击浏览全部事件">事件 <b>'+m.events+'</b></span>'+
    '<span class="statlink" data-l="struct" title="点击浏览全部结构条目">结构 <b>'+m.structs+'</b></span>'+
    '<span class="statlink" data-l="five" title="点击查看五层贯通条目">五层贯通 <b>'+m.join_all_five+'</b></span>';
  var html='';
  for(var ty in TYPE_COLOR){
    html += '<span class="lg"><span class="sw" style="background:'+TYPE_COLOR[ty][0]+';border:1px solid '+TYPE_COLOR[ty][1]+'"></span>'+tyLabel(ty)+'</span>';
  }
  var lg=$('#legends');
  if(lg) lg.innerHTML = '<span style="color:#7E2E24;font-weight:700">着色图例（点击词语查关联）</span>' + html;
}
/* ========== 规则类型树（复合类型 → 树形槽位） ========== */
function ruleTypeTree(r){
  var defs=[['禁止型',[['禁止动作',r.prohibited_action],['禁止效果',r.prohibited_effect]]],
            ['义务型',[['义务动作',r.obligation_action]]],
            ['允许型',[['允许动作',r.allowed_action]]],
            ['程序型',[['条件',r.condition],['对象',r.object],['目的',r.purpose]]],
            ['时限型',[['时限',r.deadline]]],
            ['处罚型',[['处罚',r.punishment]]]];
  var h='<div class="rtree">';
  var has=false;
  defs.forEach(function(d){
    var filled=d[1].filter(function(p){ return p[1]!==undefined&&p[1]!==null&&p[1]!==''; });
    if(!filled.length) return;
    has=true;
    h+='<div class="rnode"><span class="rt">'+d[0]+'</span><div class="rslots">';
    filled.forEach(function(p){
      h+='<div class="rslot"><span class="rk">'+p[0]+'</span><span class="rv">'+entify(String(p[1]))+'</span></div>';
    });
    h+='</div></div>';
  });
  h+='</div>';
  return has?h:'<div class="meta">该规则未填充槽位。</div>';
}
/* 规则全槽位表（树之外的其余字段） */
function ruleSlotsTable(r){
  var rows=[['主体', r.subject+(r.subject_ent_ids&&r.subject_ent_ids.length?'（'+r.subject_ent_ids.join('/')+'）':'')],
            ['分析', r.analysis],['来源', r.source],['置信度', r.confidence]];
  var h='<table class="mini"><colgroup><col style="width:20%"><col style="width:80%"></colgroup>';
  rows.forEach(function(rw){ if(rw[1]) h+='<tr><th>'+rw[0]+'</th><td>'+esc(String(rw[1]))+'</td></tr>'; });
  h+='</table>';
  return h;
}
function ruleCard(rid, r, full){
  if(!r) return '';
  var h='<div class="card"><div class="t" data-obj="rule" data-id="'+rid+'">'+rid+' · '+esc(r.title||r.type)+'</div>';
  h+='<div class="meta">类型：'+esc(r.type||'')+' ｜ 模态：'+(r.modals||[]).join('/')+' ｜ 置信度：'+r.confidence+'</div>';
  h+=oriBlock(r.original, r.item_id);
  if(full) h+='<div class="rtree-box">'+ruleTypeTree(r)+ruleSlotsTable(r)+'</div>';
  h+='</div>';
  return h;
}
/* ========== 详情渲染组件（卡片级，供 reader/list/detail 三页复用） ========== */
function chDetail(no){
  var ch=KG.chapters.find(function(c){return c.no===no;});
  if(!ch) return '';
  var ents={}, rules=0, procs=[], evs=[], sts=0, ruleTypes={};
  ch.items.forEach(function(it){
    var j=KG.join[it.iid]||{};
    if(j.rule_id){ rules++; var rt=KG.rules[j.rule_id].type; ruleTypes[rt]=(ruleTypes[rt]||0)+1; }
    (j.proc_ids||[]).forEach(function(pid){ if(procs.indexOf(pid)<0) procs.push(pid); });
    (j.event_ids||[]).forEach(function(eid){ if(evs.indexOf(eid)<0) evs.push(eid); });
    if(j.struct) for(var sec in j.struct) sts+=j.struct[sec].length;
    (it.entities||[]).forEach(function(e){ ents[tyLabel(e.ty||'')]=(ents[tyLabel(e.ty||'')]||0)+1; });
  });
  var h='<div class="dh">'+ch.name+'</div><div class="dsub">'+ch.vol+' · '+ch.no+' · 点击左侧或中间正文可读条目</div>';
  h+=kv('条目数', ch.items.length)+kv('规则', rules)+kv('流程', procs.length)+kv('事件', evs.length)+kv('结构', sts);
  var et=''; for(var t in ents) et+=t+' '+ents[t]+'　';
  h+='<div class="dsec"><h4>实体类型分布</h4>'+et+'</div>';
  var rt=''; for(var r in ruleTypes) rt+=r+' '+ruleTypes[r]+'　';
  if(rt) h+='<div class="dsec"><h4>规则类型分布</h4>'+rt+'</div>';
  h+='<div class="dsec"><h4>流程（'+procs.length+'）</h4>';
  procs.slice(0,15).forEach(function(pid){ var p=KG.procs[pid]; if(!p) return;
    h+='<div class="card"><div class="t" data-obj="proc" data-id="'+pid+'">'+pid+' · '+esc(p.title)+'</div>'+
      '<div class="meta">'+esc(p.event_type||'')+' ｜ 步骤 '+(p.steps||[]).length+'</div></div>';
  });
  if(procs.length>15) h+='<div class="meta">…另有 '+(procs.length-15)+' 条流程，可在顶栏「流程」总览查看。</div>';
  if(!procs.length) h+='<div class="meta">无</div>';
  h+='</div><div class="dsec"><h4>事件（'+evs.length+'）</h4>';
  evs.slice(0,15).forEach(function(eid){ var e=KG.events[eid]; if(!e) return;
    h+='<div class="card"><div class="t" data-obj="event" data-id="'+eid+'">'+eid+' · '+esc(e.title)+'</div>'+
      '<div class="meta">'+esc(e.type||'')+'</div></div>';
  });
  if(evs.length>15) h+='<div class="meta">…另有 '+(evs.length-15)+' 条事件，可在顶栏「事件」总览查看。</div>';
  if(!evs.length) h+='<div class="meta">无</div>';
  h+='</div>';
  return h;
}
function itemFullTable(iid, full){
  var j=KG.join[iid]||{};
  var h='<div class="dh">条目全层 · '+iid+'</div>';
  h+='<div class="dsec"><h4>原文</h4><div class="ori">'+esc((findItem(iid)||{}).it ? findItem(iid).it.text : '')+'</div></div>';
  h+='<div class="dsec"><h4>规则层</h4>';
  if(j.rule_id){ var r=KG.rules[j.rule_id]; h+=ruleCard(j.rule_id, r, full); }
  else h+='<div class="meta">无（02 卷注语无规则）</div>';
  h+='</div><div class="dsec"><h4>流程层（'+((j.proc_ids||[]).length)+'）</h4>';
  (j.proc_ids||[]).forEach(function(pid){ var p=KG.procs[pid]; h+=procCard(pid, p); });
  if(!j.proc_ids||!j.proc_ids.length) h+='<div class="meta">无</div>';
  h+='</div><div class="dsec"><h4>事件层（'+((j.event_ids||[]).length)+'）</h4>';
  (j.event_ids||[]).forEach(function(eid){ var e=KG.events[eid]; h+=eventCard(eid, e); });
  if(!j.event_ids||!j.event_ids.length) h+='<div class="meta">无</div>';
  h+='</div><div class="dsec"><h4>结构化层（'+((j.struct?Object.keys(j.struct).length:0))+'）</h4>';
  if(j.struct) for(var sec in j.struct){ h+='<h4 style="margin-top:6px">'+(sec==='ledgers'?'文簿台账':sec==='times'?'县政时间':sec==='docs'?'公文生命周期':sec==='actors'?'角色职责':'防弊机制')+'</h4>';
    j.struct[sec].forEach(function(sid){ var s=KG.structs[sid]; h+=structCard(sid, s); });
  }
  if(!j.struct||!Object.keys(j.struct).length) h+='<div class="meta">无</div>';
  h+='</div>';
  h+='<div class="dsec"><h4>实体层（'+((j.ent_ids||[]).length)+'）</h4>';
  var chips='';
  (j.ent_ids||[]).forEach(function(eid){
    var e=KG.entities[eid]; if(!e) return;
    chips+='<span class="ent ent-'+(e.type||'undetermined')+'" data-eid="'+eid+'">'+esc(e.normalized)+'</span> ';
  });
  h+=chips||'<div class="meta">无</div>';
  h+='</div>';
  return h;
}
function itemDetail(iid){
  curIid=iid;
  var f=findItem(iid); if(!f) return '';
  var ch=f.ch, j=KG.join[iid]||{};
  var h='<div class="dh">条目 · '+iid+'</div><div class="dsub">'+ch.name+' · 原文见中间正文</div>';
  h+='<div class="dsec"><h4>关联总览</h4>';
  h+=kv('规则', j.rule_id?objLink('rule',j.rule_id,j.rule_id):'—');
  h+=kv('流程', (j.proc_ids||[]).map(function(p){return objLink('proc',p,p);}).join(' ')||'—');
  h+=kv('事件', (j.event_ids||[]).map(function(e){return objLink('event',e,e);}).join(' ')||'—');
  var sts=[]; if(j.struct) for(var sec in j.struct) j.struct[sec].forEach(function(s){sts.push(objLink('struct',s,s));});
  h+=kv('结构', sts.join(' ')||'—');
  h+=kv('实体', (j.ent_ids||[]).map(function(e){return objLink('ent',e,esc((KG.entities[e]||{}).normalized||e));}).join('、')||'—');
  h+='</div>';
  if(j.rule_id){ h+='<div class="dsec"><h4>规则槽位</h4>'+ruleCard(j.rule_id, KG.rules[j.rule_id], true)+'</div>'; }
  return h;
}
function entDetail(eid){
  curEid=eid;
  var e=KG.entities[eid]; if(!e) return '<div class="empty">未找到实体 '+eid+'</div>';
  var h='<div class="dh">实体 · '+esc(e.normalized)+'</div><div class="dsub">'+eid+'</div>';
  h+=kv('类型', tyLabel(e.type))+'<div class="dsec">';
  h+=kv('出现次数', e.count)+kv('首见来源', e.first_source||'')+'</div>';
  h+='<div class="dsec"><h4>词形</h4>';
  h+='<div class="card"><div class="meta">原文词形：'+(e.surfaces||[]).map(esc).join('、')+'</div>'+
     '<div class="meta">别名映射（alias_index）：'+(e.alias&&e.alias.length?e.alias.map(esc).join('、'):'—')+'</div></div></div>';
  var rules=[]; for(var rid in KG.rules){ var r=KG.rules[rid];
    if((r.subject_ent_ids||[]).indexOf(eid)>=0) rules.push(rid);
  }
  if(rules.length){ h+='<div class="dsec"><h4>关联规则（'+(rules.length)+'）</h4>';
    rules.slice(0,12).forEach(function(rid){ var r=KG.rules[rid];
      h+='<div class="card"><div class="t" data-obj="rule" data-id="'+rid+'">'+rid+' · '+esc(r.type)+'</div>'+
        '<div class="meta">'+esc((r.obligation_action||r.prohibited_action||r.allowed_action||'').slice(0,40))+'</div></div>';
    });
    if(rules.length>12) h+='<div class="meta">…另有 '+(rules.length-12)+' 条</div>';
    h+='</div>';
  }
  var evs=[]; for(var ev in KG.events){ var evo=KG.events[ev];
    if((evo.who_ent_ids||[]).indexOf(eid)>=0) evs.push(ev);
  }
  if(evs.length){ h+='<div class="dsec"><h4>关联事件（'+(evs.length)+'）</h4>';
    evs.slice(0,12).forEach(function(ev){ var evo=KG.events[ev];
      h+='<div class="card"><div class="t" data-obj="event" data-id="'+ev+'">'+ev+' · '+esc(evo.title)+'</div>'+
        '<div class="meta">'+esc(evo.type||'')+' ｜ '+esc(evo.action||'')+'</div></div>';
    });
    if(evs.length>12) h+='<div class="meta">…另有 '+(evs.length-12)+' 条</div>';
    h+='</div>';
  }
  var sts=[]; for(var sid in KG.structs){ var s=KG.structs[sid];
    if((s.ent_ids||[]).indexOf(eid)>=0) sts.push(sid);
  }
  if(sts.length){ h+='<div class="dsec"><h4>关联结构（'+(sts.length)+'）</h4>';
    sts.slice(0,12).forEach(function(sid){ var s=KG.structs[sid];
      h+='<div class="card"><div class="t" data-obj="struct" data-id="'+sid+'">'+sid+' · '+esc(s.name||s.keyword||'')+'</div>'+
        '<div class="meta">'+s.section_cn+'</div></div>';
    });
    if(sts.length>12) h+='<div class="meta">…另有 '+(sts.length-12)+' 条</div>';
    h+='</div>';
  }
  h+='<div class="dsec"><h4>出现条目（反查）</h4>';
  var n=0;
  KG.chapters.forEach(function(ch){
    ch.items.forEach(function(it){
      var hit=(it.entities||[]).some(function(x){return x.eid===eid;});
      if(hit){ n++; h+='<div class="card"><div class="t" data-obj="item" data-id="'+it.iid+'">'+it.iid+' · '+ch.name+'</div><div class="meta">'+esc(it.text.slice(0,44))+'…</div></div>'; }
    });
  });
  if(!n) h+='<div class="meta">无直接标注（可能仅存在于别名/解读层）</div>';
  h+='</div>';
  return h;
}
function procCard(pid, p){
  if(!p) return '';
  var h='<div class="card"><div class="t" data-obj="proc" data-id="'+pid+'">'+pid+' · '+esc(p.title)+'</div>';
  h+='<div class="meta">类型：'+esc(p.event_type||'')+' ｜ 步骤：'+(p.steps||[]).length+' ｜ 置信度：'+p.confidence+'</div>';
  h+='<div class="meta">事件引用：'+(p.events||[]).map(function(e){return objLink('event',e,e);}).join('、')||'—'+'</div></div>';
  return h;
}
function procDetail(pid){
  var p=KG.procs[pid];
  var h='<div class="dh">流程 · '+pid+'</div><div class="dsub">'+esc(p.title)+' · '+esc(p.event_type||'')+'</div>';
  h+=kv('触发', p.trigger?entify(p.trigger):'—')+kv('时序', p.timeline?entify(p.timeline):'—')+kv('下一步', p.next_process?objLink('proc',p.next_process,p.next_process):'—');
  if(p.events&&p.events.length) h+=kv('事件引用', p.events.map(function(e){return objLink('event',e,e);}).join('、'));
  h+='<div class="dsec"><h4>步骤（'+(p.steps||[]).length+'）</h4>';
  (p.steps||[]).forEach(function(s,i){
    h+='<div class="step"><span class="no">'+(i+1)+'</span><span class="act">'+esc(s.action||'')+'</span></div>';
    var m=[];
    if(s.state) m.push('状态:'+s.state);
    if(s.agent) m.push('主体:'+entify(s.agent));
    if(s.condition) m.push('条件:'+entify(s.condition));
    if(s.next) m.push('下一步:'+entify(s.next));
    if(m.length) h+='<div class="step"><span class="no"></span><span class="meta">'+m.join(' ｜ ')+'</span></div>';
  });
  h+='</div><div class="dsec"><h4>原文</h4>'+oriBlock(p.original, procItemId(pid))+'</div>';
  return h;
}
/* 流程图绘制（竖排节点 + 条件分支标注） */
function procFlowHtml(pid){
  var p=KG.procs[pid]; if(!p) return '<div class="empty">未找到流程 '+pid+'</div>';
  var h='<div class="dh">流程 · '+pid+'</div><div class="dsub">'+esc(p.title||'')+' · '+esc(p.event_type||'')+'</div>';
  h+='<div class="dsec">';
  h+=kv('触发', p.trigger?entify(p.trigger):'—');
  h+=kv('时序', p.timeline?entify(p.timeline):'—');
  if(p.next_process){ h+=kv('下一步', /^XGF-P/.test(p.next_process)?objLink('proc',p.next_process,p.next_process):entify(p.next_process)); }
  if(p.events&&p.events.length) h+=kv('事件引用', p.events.map(function(e){return objLink('event',e,e);}).join('、'));
  h+='</div>';
  h+='<div class="dsec"><h4>流程步骤（'+(p.steps||[]).length+'）</h4><div class="flow">';
  (p.steps||[]).forEach(function(s,i){
    var m=[];
    if(s.agent) m.push('主体：'+entify(s.agent));
    if(s.state) m.push('状态：'+s.state);
    if(s.object) m.push('对象：'+entify(s.object));
    h+='<div class="fnode"><span class="fno">'+(i+1)+'</span><div class="fbody">'+esc(s.action||'')+
      (m.length?'<div class="fmeta">'+m.join(' ｜ ')+'</div>':'')+'</div></div>';
    if(s.condition) h+='<div class="fbranch">条件：'+entify(s.condition)+'</div>';
    if(i<(p.steps||[]).length-1) h+='<div class="farrow"></div>';
  });
  h+='</div></div>';
  if(p.analysis) h+='<div class="dsec"><h4>分析</h4><div class="meta">'+esc(p.analysis)+'</div></div>';
  h+='<div class="dsec"><h4>原文</h4>'+oriBlock(p.original, procItemId(pid))+'</div>';
  return h;
}
function eventCard(eid, e){
  if(!e) return '';
  var h='<div class="card"><div class="t" data-obj="event" data-id="'+eid+'">'+eid+' · '+esc(e.title)+'</div>';
  h+='<div class="meta">'+esc(e.type||'')+' ｜ 置信度：'+e.confidence+'</div>';
  h+='<div class="meta">'+esc((e.who||[]).join('、'))+' → '+esc(e.action)+' → '+esc((e.what||[]).join('、'))+'</div></div>';
  return h;
}
function eventDetail(eid){
  var e=KG.events[eid];
  var h='<div class="dh">事件 · '+eid+'</div><div class="dsub">'+esc(e.title)+' · '+esc(e.type||'')+'</div>';
  h+='<div class="dsec"><h4>五元组</h4>';
  h+=kv('主体 who', entify((e.who||[]).join('、'))+(e.who_ent_ids&&e.who_ent_ids.length?'（'+e.who_ent_ids.join('/')+'）':''))+
     kv('动作 action', esc(e.action))+kv('客体 what', entify((e.what||[]).join('、')))+
     kv('时间 when', esc(e.when||''))+kv('地点 where', esc(e.where||''))+'</div>';
  h+='<div class="dsec"><h4>原文</h4>'+oriBlock(e.original, eventItemId(eid))+'</div>';
  h+='<div class="dsec"><h4>来源条目</h4>';
  for(var iid in KG.join){ if((KG.join[iid].event_ids||[]).indexOf(eid)>=0){ h+='<div class="card"><div class="t" data-obj="item" data-id="'+iid+'">'+iid+'</div></div>'; break; } }
  h+='</div>';
  return h;
}
function structCard(sid, s){
  if(!s) return '';
  var h='<div class="card"><div class="t" data-obj="struct" data-id="'+sid+'">'+sid+' · '+esc(s.name||s.doc_type||s.fraud||s.keyword||'')+'</div>';
  h+='<div class="meta">'+s.section_cn+' ｜ 置信度：'+s.confidence+'</div>';
  if(s.ent_ids&&s.ent_ids.length) h+='<div class="meta">实体：'+s.ent_ids.map(function(e){return objLink('ent',e,esc((KG.entities[e]||{}).normalized||e));}).join('、')+'</div>';
  h+='</div>';
  return h;
}
function secCN(sec){
  return {ledgers:'文簿台账',times:'县政时间',docs:'公文生命周期',actors:'角色职责',frauds:'防弊机制'}[sec]||sec;
}
/* 结构反查：哪些条目（join.struct）引用了该结构 */
function structRefItems(sid){
  var out=[];
  for(var iid in KG.join){
    var j=KG.join[iid];
    if(j&&j.struct) for(var sec in j.struct){ if(j.struct[sec].indexOf(sid)>=0) out.push({iid:iid, sec:sec}); }
  }
  return out;
}
/* 结构关联区（右栏 dsec / 详情页 psec 共用）：派生规则、规则槽位命中、引用条目、关联流程/事件/实体 */
function structAssocHtml(sid, full, psec){
  var s=KG.structs[sid]; if(!s) return '';
  var W=psec?'psec':'dsec';
  var h='';
  /* 1. 派生规则（该结构由哪条规则产生，其主体/客体槽位即本题） */
  var dr=s.derived_rule;
  if(dr&&KG.rules[dr]){
    h+='<div class="'+W+'"><h4>派生规则（derived_rule）</h4>'+ruleCard(dr, KG.rules[dr], true)+'</div>';
  }
  /* 2. 规则槽位命中：结构名称出现在规则的 主体/客体，或与规则主体实体有交集 */
  var nm=s.name||s.doc_type||s.fraud||s.keyword||'';
  var hits=[], seen={};
  function pushHit(rid, slot){
    var k=rid+'|'+slot; if(seen[k]) return; seen[k]=1; hits.push({rid:rid, slot:slot});
  }
  if(nm&&String(nm).length>=2){
    for(var rid in KG.rules){
      var r=KG.rules[rid];
      if(String(r.subject||'').indexOf(nm)>=0) pushHit(rid, '主体 subject');
      if(String(r.object||'').indexOf(nm)>=0) pushHit(rid, '客体 object');
    }
  }
  var se=s.ent_ids||[];
  if(se.length){
    for(var rid2 in KG.rules){
      var r2=KG.rules[rid2];
      var inter=(r2.subject_ent_ids||[]).filter(function(e){return se.indexOf(e)>=0;});
      if(inter.length) pushHit(rid2, '主体实体 '+inter.join('/'));
    }
  }
  if(hits.length){
    h+='<div class="'+W+'"><h4>规则槽位命中（'+(hits.length)+'）</h4>';
    hits.slice(0,12).forEach(function(x){
      var r=KG.rules[x.rid];
      h+='<div class="card"><div class="t" data-obj="rule" data-id="'+x.rid+'">'+x.rid+' · '+esc(r.type||'')+'</div>'+
        '<div class="meta">槽位：'+esc(x.slot)+' ｜ '+esc(String(r.obligation_action||r.prohibited_action||r.allowed_action||'').slice(0,40))+'</div></div>';
    });
    if(hits.length>12) h+='<div class="meta">…另有 '+(hits.length-12)+' 条，可在「规则总览」查看。</div>';
    h+='</div>';
  }
  /* 3. 引用条目（join 反查全部，含所在章节） */
  var refs=structRefItems(sid);
  h+='<div class="'+W+'"><h4>引用条目（'+(refs.length||1)+'）</h4>';
  if(refs.length){
    refs.forEach(function(x){
      var f=findItem(x.iid);
      h+='<div class="card"><div class="t" data-obj="item" data-id="'+x.iid+'">'+x.iid+' · '+(f?esc(f.ch.name):'')+'</div>'+
        '<div class="meta">维度：'+esc(secCN(x.sec))+(f?' ｜ '+esc(f.ch.vol+' · 第'+f.ch.no.slice(1)+'章'):'')+'</div></div>';
    });
  } else if(s.item_id){
    var f2=findItem(s.item_id);
    h+='<div class="card"><div class="t" data-obj="item" data-id="'+s.item_id+'">'+s.item_id+' · '+(f2?esc(f2.ch.name):'')+'</div>'+
      '<div class="meta">维度：'+esc(s.section_cn||'')+(f2?' ｜ '+esc(f2.ch.vol+' · 第'+f2.ch.no.slice(1)+'章'):'')+'</div></div>';
  } else {
    h+='<div class="meta">无</div>';
  }
  h+='</div>';
  /* 4. 关联流程 / 事件（来源条目所在层） */
  var iid=s.item_id||(refs.length?refs[0].iid:'');
  if(iid){
    var ps=(KG.join[iid]||{}).proc_ids||[], es=(KG.join[iid]||{}).event_ids||[];
    if(ps.length){ h+='<div class="'+W+'"><h4>关联流程（'+ps.length+'）</h4>';
      ps.slice(0,8).forEach(function(pid){ var p=KG.procs[pid]; if(!p) return;
        h+='<div class="card"><div class="t" data-obj="proc" data-id="'+pid+'">'+pid+' · '+esc(p.title||'')+'</div><div class="meta">'+esc(p.event_type||'')+' ｜ 步骤 '+(p.steps||[]).length+'</div></div>';
      });
      if(ps.length>8) h+='<div class="meta">…另有 '+(ps.length-8)+' 条</div>';
      h+='</div>';
    }
    if(es.length){ h+='<div class="'+W+'"><h4>关联事件（'+es.length+'）</h4>';
      es.slice(0,8).forEach(function(eid){ var e=KG.events[eid]; if(!e) return;
        h+='<div class="card"><div class="t" data-obj="event" data-id="'+eid+'">'+eid+' · '+esc(e.title||'')+'</div><div class="meta">'+esc(e.type||'')+'</div></div>';
      });
      if(es.length>8) h+='<div class="meta">…另有 '+(es.length-8)+' 条</div>';
      h+='</div>';
    }
  }
  /* 5. 关联实体 */
  if(s.ent_ids&&s.ent_ids.length){
    var chips='';
    s.ent_ids.forEach(function(eid){
      var e=KG.entities[eid]; if(!e) return;
      chips+='<span class="ent ent-'+(e.type||'undetermined')+'" data-eid="'+eid+'">'+esc(e.normalized)+'</span> ';
    });
    if(chips) h+='<div class="'+W+'"><h4>关联实体（'+s.ent_ids.length+'）</h4><div class="pbody">'+chips+'</div></div>';
  }
  return h;
}
function structDetail(sid){
  var s=KG.structs[sid]; if(!s) return '<div class="empty">未找到结构 '+sid+'</div>';
  var h='<div class="dh">结构 · '+sid+'</div><div class="dsub">'+esc(s.section_cn||'')+'</div>';
  var pairs=[['名称','name'],['类型','doc_type'],['文种','fraud'],['关键词','keyword'],['值','value'],
             ['范围','scope'],['主管','keeper'],['目的','purpose'],['机制','mechanism'],['机制类型','mechanism_type'],
             ['角色类型','role_type'],['隶属','affiliation'],['阶段','stages'],['置信度','confidence']];
  h+='<div class="dsec">';
  pairs.forEach(function(p){
    var v=s[p[1]];
    if(v===undefined||v===null) return;
    if(typeof v==='object') v=JSON.stringify(v);
    h+=kv(p[0], esc(String(v)));
  });
  h+='</div>';
  h+=structAssocHtml(sid, true, false);
  if(s.original) h+='<div class="dsec"><h4>原文</h4>'+oriBlock(s.original, s.item_id)+'</div>';
  return h;
}
function ruleDetail(rid){
  var r=KG.rules[rid];
  var h='<div class="dh">规则 · '+rid+'</div><div class="dsub">'+esc(r.title||'')+'</div>';
  h+=ruleCard(rid, r, true);
  h+='<div class="dsec"><h4>来源条目</h4>';
  for(var iid in KG.join){ if(KG.join[iid].rule_id===rid){ h+='<div class="card"><div class="t" data-obj="item" data-id="'+iid+'">'+iid+'</div></div>'; break; } }
  h+='</div>';
  return h;
}

