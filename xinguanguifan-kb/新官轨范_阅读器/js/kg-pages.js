/* =========================================================
 * kg-pages.js —— 《新官轨范》知识阅读器 · 页面层
 * 三个页面：reader（阅读器首页）/ list（总览列表页）/ detail（详情页）
 * 依赖 kg-common.js 的组件与路由。
 * ========================================================= */

/* ========== 通用关联查询 ========== */
function joinOf(iid){ return KG.join[iid]||{}; }
function procsOfItem(iid){ return (KG.join[iid]||{}).proc_ids||[]; }
function eventsOfItem(iid){ return (KG.join[iid]||{}).event_ids||[]; }
function entChip(eid){
  var e=KG.entities[eid]; if(!e) return '';
  return '<span class="ent ent-'+(e.type||'undetermined')+'" data-eid="'+eid+'">'+esc(e.normalized)+'</span>';
}
function sectionCN(sec){
  return {ledgers:'文簿台账',times:'县政时间',docs:'公文生命周期',actors:'角色职责',frauds:'防弊机制'}[sec]||sec;
}

/* ========== reader 页：目录 ========== */
var GROUPS=5, curMaxG=-1, grpOpen={};
function itemGroups(ch){
  var n=Math.ceil(ch.items.length/GROUPS), gs=[];
  for(var g=0;g<n;g++) gs.push({g:g, items:ch.items.slice(g*GROUPS,(g+1)*GROUPS)});
  return gs;
}
function grpRange(grp){
  var a=grp.items[0].iid.slice(3), b=grp.items[grp.items.length-1].iid.slice(3);
  return a+'-'+b;
}
function grpOfItem(iid){ return Math.max(0, Math.floor((parseInt(String(iid).slice(3),10)-1)/GROUPS)); }
function renderToc(){
  if(!Object.keys(grpOpen).length&&!curChNo&&KG.chapters[0]) grpOpen[KG.chapters[0].no]=0;
  var html='';
  var vols={};
  KG.chapters.forEach(function(ch){ (vols[ch.vol]=vols[ch.vol]||[]).push(ch); });
  Object.keys(vols).forEach(function(v){
    var chs=vols[v];
    var volActive=chs.some(function(c){return c.no===curChNo;});
    html+='<div class="vol'+(volActive?' active':'')+'" data-vol="'+v+'">'+v+'<span class="cnt">'+chs.length+' 章</span></div>';
    chs.forEach(function(ch){
      var chActive=(curChNo===ch.no);
      html+='<div class="ch'+(chActive?' active':'')+'" data-ch="'+ch.no+'">'+ch.name+'<span class="cnt">'+ch.items.length+' 条</span></div>';
      itemGroups(ch).forEach(function(grp){
        var open=grpOpen[ch.no]===grp.g;
        var cur=chActive&&curIid&&grp.items.some(function(it){return it.iid===curIid;});
        html+='<div class="grp'+(open?' open':'')+(cur?' cur':'')+'" data-ch="'+ch.no+'" data-g="'+grp.g+'" title="点击展开/收起本组">'+
          '<span class="gico">'+(open?'▾':'▸')+'</span><span class="gx">'+grpRange(grp)+'</span></div>';
        html+='<div class="grp-itms'+(open?' open':'')+'" data-ch="'+ch.no+'" data-g="'+grp.g+'">';
        grp.items.forEach(function(it){
          var j=joinOf(it.iid);
          var tags=[];
          if(j.rule_id) tags.push('R');
          if(j.proc_ids&&j.proc_ids.length) tags.push('P');
          if(j.event_ids&&j.event_ids.length) tags.push('E');
          if(j.struct&&Object.keys(j.struct).length) tags.push('S');
          if(j.ent_ids&&j.ent_ids.length) tags.push('T');
          var badge=ruleBadge(j.rule_id?KG.rules[j.rule_id].type:'');
          html+='<div class="itm'+(it.iid===curIid?' active':'')+'" data-iid="'+it.iid+'"><span class="tx">'+(badge?'['+badge+'] ':'')+it.iid.slice(3)+'. '+esc(itemSummary(it.iid).slice(0,16))+'</span><span class="tag">'+tags.join('/')+'</span></div>';
        });
        html+='</div>';
      });
    });
  });
  $('#toc').innerHTML=html;
}
/* ========== reader 页：正文（懒加载） ========== */
function itemBlockHtml(it){
  var ents=(it.entities||[]).slice().sort(function(a,b){return a.s-b.s;});
  var body='', pos=0;
  for(var k=0;k<ents.length;k++){
    var e=ents[k];
    if(e.s<pos) continue;
    body+=esc(it.text.slice(pos,e.s));
    var cls=e.ty||'undetermined';
    body+='<span class="ent ent-'+cls+'" data-eid="'+(e.eid||'')+'" data-iid="'+it.iid+'" title="'+esc(e.n||'')+'（'+tyLabel(cls)+'，置信度 '+e.c+'）">'+esc(it.text.slice(e.s,e.e))+'</span>';
    pos=e.e;
  }
  body+=esc(it.text.slice(pos));
  var j=joinOf(it.iid);
  var pill='';
  if(j.rule_id) pill+='<span class="pill">规则 '+j.rule_id.slice(6)+'</span>';
  if(j.proc_ids&&j.proc_ids.length) pill+='<span class="pill">流程 '+j.proc_ids.length+'</span>';
  if(j.event_ids&&j.event_ids.length) pill+='<span class="pill">事件 '+j.event_ids.length+'</span>';
  if(j.struct) pill+='<span class="pill">结构 '+Object.keys(j.struct).length+'</span>';
  return '<div class="item-block'+(it.iid===curIid?' active':'')+'" id="blk-'+it.iid+'">'+
    '<div class="item-head" data-iid="'+it.iid+'"><span>'+it.iid+'</span><span class="goto">'+pill+' 点击查全层 →</span></div>'+
    '<div class="item-text">'+body+'</div></div>';
}
function loadGroups(chNo, uptoG){
  var ch=KG.chapters.find(function(c){return c.no===chNo;});
  if(!ch) return;
  var gs=itemGroups(ch);
  for(var g=curMaxG+1; g<=uptoG && g<gs.length; g++){
    var grp=gs[g], block='<div class="grp-block" id="grp-'+ch.no+'-'+g+'">';
    grp.items.forEach(function(it){ block+=itemBlockHtml(it); });
    block+='</div>';
    $('#bodyArea').insertAdjacentHTML('beforeend', block);
    curMaxG=g;
  }
  highlight($('#searchInput').value.trim());
}
/* 覆盖式渲染：清空正文并加载到指定分组（点击分组时调用，避免正文追加） */
function renderBodyTo(chNo, uptoG){
  if(curChNo!==chNo){ curChNo=chNo; renderDetail('ch', chNo); }
  curMaxG=-1;
  $('#bodyArea').innerHTML='';
  $('#bodyArea').scrollTop=0; /* 防止内容缩小后残留滚动位置触发懒加载 */
  loadGroups(chNo, uptoG);
  highlight($('#searchInput').value.trim());
}
function renderBody(chNo){ renderBodyTo(chNo, 0); }
/* 纯滚动定位（组内容由调用方保证已渲染） */
function scrollToItem(iid){
  setTimeout(function(){
    var el=document.getElementById('blk-'+iid);
    if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
  }, 30);
}
/* 只渲染指定分组（单列该组，不加载之前的组；curMaxG 置为该组，滚动可续接下一组） */
function renderBodyGroupOnly(chNo, g){
  if(curChNo!==chNo){ curChNo=chNo; renderDetail('ch', chNo); }
  curMaxG=g;
  $('#bodyArea').innerHTML='';
  $('#bodyArea').scrollTop=0;
  var ch=KG.chapters.find(function(c){return c.no===chNo;});
  if(!ch) return;
  var gs=itemGroups(ch), grp=gs[g];
  if(!grp) return;
  var block='<div class="grp-block" id="grp-'+ch.no+'-'+g+'">';
  grp.items.forEach(function(it){ block+=itemBlockHtml(it); });
  block+='</div>';
  $('#bodyArea').insertAdjacentHTML('beforeend', block);
  highlight($('#searchInput').value.trim());
}
/* 聚焦条目：章头必要时切换；条目所在组未渲染则单列该组；滚动到条目 */
function focusItem(iid){
  var f=findItem(iid); if(!f) return;
  if(curChNo!==f.ch.no){ curChNo=f.ch.no; renderDetail('ch', f.ch.no); }
  var g=grpOfItem(iid);
  if(!document.getElementById('grp-'+f.ch.no+'-'+g)) renderBodyGroupOnly(f.ch.no, g);
  scrollToItem(iid);
}
$('#bodyArea').addEventListener('scroll', function(){
  var el=$('#bodyArea');
  if(el.scrollTop+el.clientHeight >= el.scrollHeight-260){
    var ch=KG.chapters.find(function(c){return c.no===curChNo;});
    var gs=ch?itemGroups(ch):[];
    if(curMaxG < gs.length-1) loadGroups(curChNo, curMaxG+1);
  }
});
/* ========== reader 页：中间 tab + 右侧详情 ========== */
function switchTab(tab){
  var tabs=$('#midTabs').querySelectorAll('.mt');
  for(var i=0;i<tabs.length;i++) tabs[i].classList.toggle('active', tabs[i].getAttribute('data-tab')===tab);
  $('#tabItem').style.display = (tab==='item') ? 'block' : 'none';
  if(tab==='item') renderTabItem(); else $('#tabItem').innerHTML='';
}
function renderTabItem(){
  if(!curIid){ $('#tabItem').innerHTML='<div class="empty">先在左侧或正文点击一个条目，此处显示其全层信息。</div>'; return; }
  $('#tabItem').innerHTML = itemFullTable(curIid, true);
}
/* 右侧详情（reader 页）——现在作为「概览 + 入口」，卡片点击进详情页 */
function renderDetail(kind, id){
  var D=$('#detail');
  if(kind==='ch') return D.innerHTML=chDetail(id);
  if(kind==='item'){ var f=findItem(id); if(f) focusItem(id); return D.innerHTML=itemDetail(id); }
  if(kind==='ent') return D.innerHTML=entDetail(id);
  if(kind==='rule') return D.innerHTML=ruleDetail(id);
  if(kind==='proc') return D.innerHTML=procDetail(id);
  if(kind==='event') return D.innerHTML=eventDetail(id);
  if(kind==='struct') return D.innerHTML=structDetail(id);
}
function showHint(msg){ $('#detail').innerHTML='<div class="empty">'+esc(msg)+'</div>'; }

/* ========== list 页：总览列表 ========== */
var BROWSE_TABS=[['ent','实体'],['rule','规则'],['proc','流程'],['event','事件'],['struct','结构'],['item','条目'],['five','五层贯通']];
var bwState={layer:'ent', filter:null};
/* 规则类型树：1级=6 基类 → 2级=双基类组合 → 3级=三基类 → 4级=四基类，逐级嵌套可展开 */
var RULE_BASE=['禁止型','义务型','允许型','程序型','时限型','处罚型'];
var rtOpen={}; /* 规则树节点展开态 key -> bool */
function ruleSetKey(type){
  var arr=[];
  RULE_BASE.forEach(function(b){ if(String(type||'').indexOf(b)>=0) arr.push(b); });
  return arr.length?arr:['未分类'];
}
function ruleTreeData(){
  var nodes={}, children={};
  for(var rid in KG.rules){
    var arr=ruleSetKey(KG.rules[rid].type);
    var k=arr.join('+');
    if(!nodes[k]){ nodes[k]={arr:arr, exact:0}; children[k]=[]; }
    nodes[k].exact++;
  }
  var root=[];
  Object.keys(nodes).forEach(function(k){
    var arr=nodes[k].arr;
    if(arr.length>1){
      var p=arr.slice(0,arr.length-1).join('+');
      if(nodes[p]) children[p].push(k); else root.push(k);
    } else root.push(k);
  });
  /* 节点计数 = 精确 + 子孙（与过滤语义一致：点击节点显示其全部规则） */
  function total(k){
    if(nodes[k].cnt!==undefined) return nodes[k].cnt;
    var s=nodes[k].exact;
    (children[k]||[]).forEach(function(c){ s+=total(c); });
    nodes[k].cnt=s;
    return s;
  }
  function sortKids(a,b){ return (total(b)-total(a))||(a<b?-1:1); }
  for(var ck in children) children[ck].sort(sortKids);
  root.sort(sortKids);
  return {nodes:nodes, children:children, root:root};
}
function ruleNodeMatches(filterKey, type){
  if(!filterKey) return true;
  var sel=filterKey.split('+'), arr=ruleSetKey(type);
  if(sel.length>arr.length) return false;
  for(var i=0;i<sel.length;i++){ if(sel[i]!==arr[i]) return false; }
  return true;
}
function ruleTreeHtml(){
  var rt=ruleTreeData();
  function rec(keys, depth){
    var h='';
    keys.forEach(function(k){
      var n=rt.nodes[k], kids=rt.children[k]||[];
      var open=!!rtOpen[k];
      var cur=bwState.filter===k;
      h+='<div class="rt-node'+(cur?' cur':'')+'" data-k="'+esc(k)+'" style="padding-left:'+(6+depth*12)+'px">'+
        (kids.length?'<span class="rt-ico">'+(open?'▾':'▸')+'</span>':'<span class="rt-ico"></span>')+
        '<span class="rt-lb">'+esc(k)+'</span><span class="rt-cnt">'+n.cnt+'</span></div>';
      if(kids.length){
        h+='<div class="rt-ch"'+(open?'':' style="display:none"')+'>'+rec(kids, depth+1)+'</div>';
      }
    });
    return h;
  }
  var h='<div class="rt-node'+(bwState.filter===''?' cur':'')+'" data-k=""><span class="rt-ico"></span><span class="rt-lb">全部</span><span class="rt-cnt">'+KG.meta.rules+'</span></div>';
  h+='<div class="rt-ch">'+rec(rt.root, 0)+'</div>';
  return h;
}
function openList(layer){ bwState.layer=layer||'ent'; bwState.filter=null; renderBrowse(); }
function setBwTab(l){ bwState.layer=l; bwState.filter=null; renderBrowse(); }
function bwFilters(){
  var F=[];
  function push(map){ var arr=[]; for(var k in map) arr.push({v:k, label:k, cnt:map[k]}); arr.sort(function(a,b){return b.cnt-a.cnt;}); return arr; }
  var counts={};
  if(bwState.layer==='ent'){
    var c={}; for(var eid in KG.entities){ var t=KG.entities[eid].type||'undetermined'; c[t]=(c[t]||0)+1; }
    var cs=push(c); cs.forEach(function(x){ F.push({v:x.v, label:tyLabel(x.v), cnt:x.cnt}); });
  }
  else if(bwState.layer==='rule'){
    var base=['禁止型','义务型','允许型','程序型','时限型','处罚型'];
    var c={}; base.forEach(function(b){ c[b]=0; });
    for(var rid in KG.rules){ var t=KG.rules[rid].type||''; base.forEach(function(b){ if(t.indexOf(b)>=0) c[b]++; }); }
    var cs=push(c); cs.forEach(function(x){ if(x.cnt) F.push({v:x.v, label:x.label, cnt:x.cnt}); });
  }
  else if(bwState.layer==='proc'){
    var c={}; for(var pid in KG.procs){ var t=KG.procs[pid].event_type||'未分类'; c[t]=(c[t]||0)+1; }
    var cs=push(c); cs.slice(0,14).forEach(function(x){ F.push({v:x.v, label:x.v, cnt:x.cnt}); });
  }
  else if(bwState.layer==='event'){
    var c={}; for(var ev in KG.events){ var t=KG.events[ev].type||'未分类'; c[t]=(c[t]||0)+1; }
    var cs=push(c); cs.slice(0,14).forEach(function(x){ F.push({v:x.v, label:x.v, cnt:x.cnt}); });
  }
  else if(bwState.layer==='struct'){
    [['ledgers','文簿台账'],['times','县政时间'],['docs','公文生命周期'],['actors','角色职责'],['frauds','防弊机制']].forEach(function(s){
      var n=0; for(var sid in KG.structs){ if(KG.structs[sid].section===s[0]) n++; }
      F.push({v:s[0], label:s[1], cnt:n});
    });
  }
  else if(bwState.layer==='item'){
    var c={}; KG.chapters.forEach(function(ch){ c[ch.no]=ch.items.length; });
    var cs=push(c); cs.forEach(function(x){ F.push({v:x.v, label:'第'+x.v.slice(1)+'章', cnt:x.cnt}); });
  }
  var total = bwState.layer==='ent'?KG.meta.entities : bwState.layer==='rule'?KG.meta.rules :
    bwState.layer==='proc'?KG.meta.procs : bwState.layer==='event'?KG.meta.events :
    bwState.layer==='struct'?KG.meta.structs : bwState.layer==='item'?KG.meta.items : KG.meta.join_all_five;
  F.unshift({v:'', label:'全部', cnt:total});
  return F;
}
function bwMatch(f){
  var v=bwState.filter;
  if(!v) return true;
  if(bwState.layer==='ent') return (f.type||'undetermined')===v;
  if(bwState.layer==='rule') return ruleNodeMatches(v, f.type||'');
  if(bwState.layer==='proc') return (f.event_type||'未分类')===v;
  if(bwState.layer==='event') return (f.type||'未分类')===v;
  if(bwState.layer==='struct') return f.section===v;
  if(bwState.layer==='item') return f.no===v;
  return true;
}
function bwCard(kind,id,title,meta,ori){
  return '<div class="bw-card" data-obj="'+kind+'" data-id="'+id+'">'+
    '<div class="t">'+title+'</div>'+(meta?'<div class="meta">'+meta+'</div>':'')+(ori?'<div class="ori">'+esc(ori)+'</div>':'')+'</div>';
}
function bwListHtml(){
  var H='';
  if(bwState.layer==='ent'){
    var groups={};
    for(var eid in KG.entities){ var e=KG.entities[eid]; if(!bwMatch(e)) continue;
      (groups[tyLabel(e.type||'undetermined')]=groups[tyLabel(e.type||'undetermined')]||[]).push(eid);
    }
    var gk=Object.keys(groups).sort();
    gk.forEach(function(g){
      H+='<div class="bw-group">'+esc(g)+'（'+groups[g].length+'）</div><div class="bw-grid">';
      groups[g].forEach(function(eid){ var e=KG.entities[eid];
        H+=bwCard('ent', eid, entChip(eid)+' '+esc(eid),
          '词形：'+esc((e.surfaces||[]).join('、')||'—')+' ｜ 次数：'+e.count+' ｜ 来源：'+esc(e.first_source||''), null);
      });
      H+='</div>';
    });
  }
  else if(bwState.layer==='rule'){
    /* 中间 list：按当前树节点过滤（type 基类集合 ⊇ 节点），再按精确 type 分小组 */
    var rows=[];
    for(var rid in KG.rules){ if(ruleNodeMatches(bwState.filter||'', KG.rules[rid].type||'')) rows.push(rid); }
    rows.sort();
    H+='<div class="bw-rule-note">'+(bwState.filter?esc(bwState.filter):'全部')+' · 共 '+rows.length+' 条规则 · 左侧为 1级基类 → 2级组合 → 3级 → 4级 可展开树</div>';
    var groups={};
    rows.forEach(function(rid2){ var t=KG.rules[rid2].type||'未分类'; (groups[t]=groups[t]||[]).push(rid2); });
    Object.keys(groups).sort(function(a,b){
      var aL=ruleSetKey(a).length, bL=ruleSetKey(b).length;
      return (aL-bL)||(a<b?-1:1);
    }).forEach(function(t){
      H+='<div class="bw-group">'+esc(t)+'（'+groups[t].length+'）</div>';
      groups[t].forEach(function(rid3){ var r=KG.rules[rid3];
        var act=r.obligation_action||r.prohibited_action||r.allowed_action||r.title||r.type||'';
        H+='<div class="bw-rule-row" data-obj="rule" data-id="'+rid3+'"><span class="rid">'+rid3+'</span><span class="act">['+ruleBadge(r.type)+'] '+esc(String(act).slice(0,40))+'</span><span class="meta">'+esc((r.modals||[]).join('/')||'')+' · '+r.confidence+'</span></div>';
      });
    });
  }
  else if(bwState.layer==='proc'){
    var groups={};
    for(var pid in KG.procs){ var p=KG.procs[pid]; if(!bwMatch(p)) continue;
      (groups[p.event_type||'未分类']=groups[p.event_type||'未分类']||[]).push(pid);
    }
    Object.keys(groups).sort().forEach(function(g){
      H+='<div class="bw-group">'+esc(g)+'（'+groups[g].length+'）</div><div class="bw-grid">';
      groups[g].forEach(function(pid){ var p=KG.procs[pid];
        H+=bwCard('proc', pid, esc(pid)+' · '+esc(p.title||'—'),
          '步骤：'+(p.steps||[]).length+' ｜ 事件引用：'+((p.events||[]).length)+' ｜ 置信度：'+p.confidence, p.original);
      });
      H+='</div>';
    });
  }
  else if(bwState.layer==='event'){
    var groups={};
    for(var ev in KG.events){ var e=KG.events[ev]; if(!bwMatch(e)) continue;
      (groups[e.type||'未分类']=groups[e.type||'未分类']||[]).push(ev);
    }
    Object.keys(groups).sort().forEach(function(g){
      H+='<div class="bw-group">'+esc(g)+'（'+groups[g].length+'）</div><div class="bw-grid">';
      groups[g].forEach(function(ev){ var e=KG.events[ev];
        H+=bwCard('event', ev, esc(ev)+' · '+esc(e.title||'—'),
          esc((e.who||[]).join('、')||'—')+' → '+esc(e.action||'')+' → '+esc((e.what||[]).join('、')||'—')+' ｜ 置信度：'+e.confidence, e.original);
      });
      H+='</div>';
    });
  }
  else if(bwState.layer==='struct'){
    var secCN={ledgers:'文簿台账',times:'县政时间',docs:'公文生命周期',actors:'角色职责',frauds:'防弊机制'};
    var groups={};
    for(var sid in KG.structs){ var s=KG.structs[sid]; if(!bwMatch(s)) continue;
      var g=secCN[s.section]||'其他';
      (groups[g]=groups[g]||[]).push(sid);
    }
    Object.keys(groups).sort().forEach(function(g){
      H+='<div class="bw-group">'+esc(g)+'（'+groups[g].length+'）</div><div class="bw-grid">';
      groups[g].forEach(function(sid){ var s=KG.structs[sid];
        var nm=s.name||s.doc_type||s.fraud||s.keyword||'—';
        H+=bwCard('struct', sid, esc(sid)+' · '+esc(nm),
          esc(s.section_cn||'')+' ｜ 来源条目：'+esc(s.item_id||'—')+' ｜ 置信度：'+s.confidence, s.original);
      });
      H+='</div>';
    });
  }
  else if(bwState.layer==='item'||bwState.layer==='five'){
    KG.chapters.forEach(function(ch){
      if(bwState.layer==='item'&&!bwMatch(ch)) return;
      var arr=ch.items.filter(function(it){
        if(bwState.layer==='five'){ var j=joinOf(it.iid); return j.rule_id&&j.proc_ids&&j.proc_ids.length&&j.event_ids&&j.event_ids.length&&j.struct&&j.ent_ids&&j.ent_ids.length; }
        return true;
      });
      if(!arr.length) return;
      H+='<div class="bw-group">'+esc(ch.name)+'（'+arr.length+'）</div><div class="bw-grid">';
      arr.forEach(function(it){
        var j=joinOf(it.iid);
        var tags=[];
        if(j.rule_id) tags.push('R:'+j.rule_id);
        if(j.proc_ids&&j.proc_ids.length) tags.push('P:'+j.proc_ids.length);
        if(j.event_ids&&j.event_ids.length) tags.push('E:'+j.event_ids.length);
        var stn=0; if(j.struct) for(var sec in j.struct) stn+=j.struct[sec].length;
        if(stn) tags.push('S:'+stn);
        if(j.ent_ids&&j.ent_ids.length) tags.push('T:'+j.ent_ids.length);
        H+=bwCard('join', it.iid, esc(it.iid)+' · '+esc(ch.name)+' <span class="pill">'+tags.join(' ')+'</span>',
          esc(itemSummary(it.iid).slice(0,40)), it.text.slice(0,60));
      });
      H+='</div>';
    });
  }
  return H||'<div class="empty">该分类下暂无内容。</div>';
}
function renderBrowse(){
  var mt='';
  BROWSE_TABS.forEach(function(t){
    var n=t[0]==='ent'?KG.meta.entities:t[0]==='rule'?KG.meta.rules:t[0]==='proc'?KG.meta.procs:t[0]==='event'?KG.meta.events:t[0]==='struct'?KG.meta.structs:t[0]==='item'?KG.meta.items:KG.meta.join_all_five;
    mt+='<span class="bw-tab'+(t[0]===bwState.layer?' active':'')+'" data-l="'+t[0]+'">'+t[1]+' <b>'+n+'</b></span>';
  });
  $('#bwTabs').innerHTML=mt;
  $('#bwFilter').innerHTML=bwFilterHtml();
  $('#bwList').innerHTML=bwListHtml();
}
/* 筛选面板：规则层渲染为多级可展开树，其余层保持 chip 列表 */
function bwFilterHtml(){
  var fh='<h4>分类筛选</h4>';
  if(bwState.layer==='rule') return fh+ruleTreeHtml();
  var F=bwFilters();
  F.forEach(function(f){
    fh+='<div class="bf-chip'+(bwState.filter===f.v?' active':'')+'" data-v="'+f.v+'">'+esc(f.label)+'<span class="bf-cnt">'+f.cnt+'</span></div>';
  });
  return fh;
}

/* ========== detail 页：丰富详情（中间主区） ========== */
function entPage(eid){
  var e=KG.entities[eid]; if(!e) return '<div class="empty">未找到实体 '+eid+'</div>';
  var h='<div class="page-title"><span class="pt">实体</span>'+esc(e.normalized)+'<span class="ptid">'+eid+'</span></div>';
  h+='<div class="page-meta">'+tyLabel(e.type)+' ｜ 出现 '+e.count+' 次 ｜ 首见 '+esc(e.first_source||'—')+'</div>';
  h+='<div class="sec-grid">';
  h+='<div class="pcard"><h4>词形</h4><div class="pbody">原文词形：'+(e.surfaces||[]).map(esc).join('、')+'<br>别名映射：'+(e.alias&&e.alias.length?e.alias.map(esc).join('、'):'—')+'</div></div>';
  h+='</div>';
  /* 关联规则 */
  var rules=[]; for(var rid in KG.rules){ var r=KG.rules[rid]; if((r.subject_ent_ids||[]).indexOf(eid)>=0) rules.push(rid); }
  h+='<div class="psec"><h4>关联规则（'+rules.length+'）</h4>';
  if(rules.length){ h+='<div class="sec-grid">'; rules.forEach(function(rid){ h+=ruleCard(rid, KG.rules[rid], false); }); h+='</div>'; }
  else h+='<div class="meta">无（该实体未作为规则主体槽位出现）</div>';
  h+='</div>';
  /* 关联事件 */
  var evs=[]; for(var ev in KG.events){ var evo=KG.events[ev]; if((evo.who_ent_ids||[]).indexOf(eid)>=0) evs.push(ev); }
  h+='<div class="psec"><h4>关联事件（'+evs.length+'）</h4>';
  if(evs.length){ h+='<div class="sec-grid">'; evs.forEach(function(ev){ h+=eventCard(ev, KG.events[ev]); }); h+='</div>'; }
  else h+='<div class="meta">无（该实体未作为事件主体 who_ent_ids 出现）</div>';
  h+='</div>';
  /* 关联结构 */
  var sts=[]; for(var sid in KG.structs){ var s=KG.structs[sid]; if((s.ent_ids||[]).indexOf(eid)>=0) sts.push(sid); }
  h+='<div class="psec"><h4>关联结构（'+sts.length+'）</h4>';
  if(sts.length){ h+='<div class="sec-grid">'; sts.forEach(function(sid){ h+=structCard(sid, KG.structs[sid]); }); h+='</div>'; }
  else h+='<div class="meta">无（该实体未进入结构层 actors 维度）</div>';
  h+='</div>';
  /* 出现条目 */
  h+='<div class="psec"><h4>出现条目</h4>';
  var n=0;
  KG.chapters.forEach(function(ch){
    ch.items.forEach(function(it){
      var hit=(it.entities||[]).some(function(x){return x.eid===eid;});
      if(hit){ n++;
        h+='<div class="card"><div class="t" data-obj="item" data-id="'+it.iid+'">'+it.iid+' · '+ch.name+'</div><div class="meta">'+esc(it.text.slice(0,60))+'…</div></div>';
      }
    });
  });
  if(!n) h+='<div class="meta">无直接标注（可能仅存在于别名/解读层）</div>';
  h+='</div>';
  return h;
}
function rulePage(rid){
  var r=KG.rules[rid]; if(!r) return '<div class="empty">未找到规则 '+rid+'</div>';
  var h='<div class="page-title"><span class="pt">规则</span>'+rid+'<span class="ptid">'+esc(r.title||r.type)+'</span></div>';
  h+='<div class="page-meta">'+esc(r.type||'')+' ｜ 模态：'+(r.modals||[]).join('/')+' ｜ 置信度：'+r.confidence+'</div>';
  h+='<div class="psec"><h4>规则结构（类型 → 槽位树）</h4>'+ruleTypeTree(r)+'</div>';
  h+='<div class="psec"><h4>补充字段</h4>'+ruleSlotsTable(r)+'</div>';
  h+='<div class="psec"><h4>原文</h4>'+oriBlock(r.original, r.item_id)+'</div>';
  /* 来源条目及该条目的流程/事件 */
  var iid='';
  for(var k in KG.join){ if(KG.join[k].rule_id===rid){ iid=k; break; } }
  h+='<div class="psec"><h4>来源条目</h4>';
  if(iid) h+='<div class="card"><div class="t" data-obj="item" data-id="'+iid+'">'+iid+' · '+(findItem(iid)&&findItem(iid).ch?findItem(iid).ch.name:'')+'</div></div>';
  else h+='<div class="meta">—</div>';
  h+='</div>';
  if(iid){
    var procs=procsOfItem(iid), evs=eventsOfItem(iid);
    if(procs.length){ h+='<div class="psec"><h4>关联流程（'+procs.length+'）</h4><div class="sec-grid">';
      procs.forEach(function(pid){ h+=procCard(pid, KG.procs[pid]); }); h+='</div></div>';
    }
    if(evs.length){ h+='<div class="psec"><h4>关联事件（'+evs.length+'）</h4><div class="sec-grid">';
      evs.forEach(function(ev){ h+=eventCard(ev, KG.events[ev]); }); h+='</div></div>';
    }
    if(r.subject_ent_ids&&r.subject_ent_ids.length){
      h+='<div class="psec"><h4>主体实体</h4><div class="pbody">'+r.subject_ent_ids.map(entChip).join(' ')+'</div></div>';
    }
  }
  return h;
}
function procPage(pid){
  var p=KG.procs[pid]; if(!p) return '<div class="empty">未找到流程 '+pid+'</div>';
  var h='<div class="page-title"><span class="pt">流程</span>'+pid+'<span class="ptid">'+esc(p.title||'')+'</span></div>';
  h+='<div class="page-meta">'+esc(p.event_type||'')+' ｜ 步骤 '+(p.steps||[]).length+' ｜ 置信度：'+p.confidence+'</div>';
  /* 大流程图（复用 procFlowHtml 组件主体） */
  h+='<div class="psec"><h4>流程图</h4>';
  h+='<div class="dsec">';
  h+=kv('触发', p.trigger?entify(p.trigger):'—');
  h+=kv('时序', p.timeline?entify(p.timeline):'—');
  if(p.next_process){ h+=kv('下一步', /^XGF-P/.test(p.next_process)?objLink('proc',p.next_process,p.next_process):entify(p.next_process)); }
  if(p.events&&p.events.length) h+=kv('事件引用', p.events.map(function(e){return objLink('event',e,e);}).join('、'));
  h+='</div><div class="flow">';
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
  if(p.analysis) h+='<div class="psec"><h4>分析</h4><div class="pbody">'+esc(p.analysis)+'</div></div>';
  h+='<div class="psec"><h4>原文</h4>'+oriBlock(p.original, procItemId(pid))+'</div>';
  /* 来源条目 + 该条目规则层 */
  var iid=procItemId(pid);
  h+='<div class="psec"><h4>来源条目</h4>';
  if(iid) h+='<div class="card"><div class="t" data-obj="item" data-id="'+iid+'">'+iid+' · '+(findItem(iid)&&findItem(iid).ch?findItem(iid).ch.name:'')+'</div></div>';
  else h+='<div class="meta">—</div>';
  h+='</div>';
  if(iid){
    var j=joinOf(iid);
    if(j.rule_id){ h+='<div class="psec"><h4>来源规则</h4>'+ruleCard(j.rule_id, KG.rules[j.rule_id], false)+'</div>'; }
    if(p.events&&p.events.length){
      h+='<div class="psec"><h4>关联事件（'+p.events.length+'）</h4><div class="sec-grid">';
      p.events.forEach(function(ev){ h+=eventCard(ev, KG.events[ev]); });
      h+='</div></div>';
    }
  }
  return h;
}
function eventPage(eid){
  var e=KG.events[eid]; if(!e) return '<div class="empty">未找到事件 '+eid+'</div>';
  var h='<div class="page-title"><span class="pt">事件</span>'+eid+'<span class="ptid">'+esc(e.title||'')+'</span></div>';
  h+='<div class="page-meta">'+esc(e.type||'')+' ｜ 置信度：'+e.confidence+'</div>';
  h+='<div class="psec"><h4>五元组</h4><div class="pcard">';
  h+=kv('主体 who', entify((e.who||[]).join('、'))+(e.who_ent_ids&&e.who_ent_ids.length?'（'+e.who_ent_ids.join('/')+'）':''));
  h+=kv('动作 action', esc(e.action||''));
  h+=kv('客体 what', entify((e.what||[]).join('、')));
  h+=kv('时间 when', esc(e.when||''));
  h+=kv('地点 where', esc(e.where||''));
  h+='</div></div>';
  if(e.who_ent_ids&&e.who_ent_ids.length){
    h+='<div class="psec"><h4>主体实体</h4><div class="pbody">'+e.who_ent_ids.map(entChip).join(' ')+'</div></div>';
  }
  h+='<div class="psec"><h4>原文</h4>'+oriBlock(e.original, eventItemId(eid))+'</div>';
  var iid=eventItemId(eid);
  h+='<div class="psec"><h4>来源条目</h4>';
  if(iid) h+='<div class="card"><div class="t" data-obj="item" data-id="'+iid+'">'+iid+' · '+(findItem(iid)&&findItem(iid).ch?findItem(iid).ch.name:'')+'</div></div>';
  else h+='<div class="meta">—</div>';
  h+='</div>';
  if(iid){
    var procs=procsOfItem(iid);
    if(procs.length){ h+='<div class="psec"><h4>关联流程（'+procs.length+'）</h4><div class="sec-grid">';
      procs.forEach(function(pid){ h+=procCard(pid, KG.procs[pid]); }); h+='</div></div>';
    }
    var j=joinOf(iid);
    if(j.rule_id){ h+='<div class="psec"><h4>来源规则</h4>'+ruleCard(j.rule_id, KG.rules[j.rule_id], false)+'</div>'; }
  }
  return h;
}
function structPage(sid){
  var s=KG.structs[sid]; if(!s) return '<div class="empty">未找到结构 '+sid+'</div>';
  var h='<div class="page-title"><span class="pt">结构</span>'+sid+'<span class="ptid">'+esc(s.section_cn||'')+'</span></div>';
  h+='<div class="page-meta">'+esc(s.name||s.doc_type||s.fraud||s.keyword||'')+' ｜ 置信度：'+s.confidence+'</div>';
  var pairs=[['名称','name'],['类型','doc_type'],['文种','fraud'],['关键词','keyword'],['值','value'],
             ['范围','scope'],['主管','keeper'],['目的','purpose'],['机制','mechanism'],['机制类型','mechanism_type'],
             ['角色类型','role_type'],['隶属','affiliation'],['阶段','stages']];
  h+='<div class="psec"><h4>字段</h4><div class="pcard">';
  pairs.forEach(function(p){
    var v=s[p[1]];
    if(v===undefined||v===null) return;
    if(typeof v==='object') v=JSON.stringify(v);
    h+=kv(p[0], esc(String(v)));
  });
  h+='</div></div>';
  h+='<div class="psec"><h4>原文</h4>'+oriBlock(s.original, s.item_id)+'</div>';
  h+=structAssocHtml(sid, true, true);
  return h;
}
function itemPage(iid){
  var f=findItem(iid); if(!f) return '<div class="empty">未找到条目 '+iid+'</div>';
  var h='<div class="page-title"><span class="pt">条目</span>'+iid+'<span class="ptid">'+esc(f.ch.name)+'</span></div>';
  h+='<div class="psec"><h4>原文</h4>'+itemBlockHtml(f.it)+'</div>';
  h+=itemFullTable(iid, true);
  return h;
}
function chPage(no){
  var ch=KG.chapters.find(function(c){return c.no===no;});
  if(!ch) return '<div class="empty">未找到章 '+no+'</div>';
  var h='<div class="page-title"><span class="pt">章</span>'+ch.name+'<span class="ptid">'+ch.vol+'</span></div>';
  h+='<div class="psec">'+chDetail(no)+'</div>';
  h+='<div class="psec"><h4>章内条目（'+ch.items.length+'）</h4><div class="sec-grid">';
  ch.items.forEach(function(it){
    h+='<div class="card"><div class="t" data-obj="item" data-id="'+it.iid+'">'+it.iid+'</div><div class="meta">'+esc(itemSummary(it.iid).slice(0,50))+'</div></div>';
  });
  h+='</div></div>';
  return h;
}
/* 五层贯通详情页：原文之下直接铺开五层（不依赖再次点击各层引用） */
function joinPage(iid){
  var f=findItem(iid); if(!f) return '<div class="empty">未找到条目 '+iid+'</div>';
  var j=KG.join[iid]||{};
  var h='<div class="page-title"><span class="pt">五层贯通</span>'+iid+'<span class="ptid">'+esc(f.ch.name)+'</span></div>';
  h+='<div class="page-meta">'+esc(f.ch.vol)+' · '+esc(f.ch.name)+' · 该条目五层结构化结果总览</div>';
  h+='<div class="psec"><h4>原文</h4>'+itemBlockHtml(f.it)+'</div>';
  /* 规则层 */
  h+='<div class="psec"><h4>规则层</h4>';
  if(j.rule_id&&KG.rules[j.rule_id]) h+=ruleCard(j.rule_id, KG.rules[j.rule_id], true);
  else h+='<div class="meta">无规则标注（注语类条目）</div>';
  h+='</div>';
  /* 流程层 */
  h+='<div class="psec"><h4>流程层（'+((j.proc_ids||[]).length)+'）</h4>';
  if(j.proc_ids&&j.proc_ids.length){ h+='<div class="sec-grid">';
    j.proc_ids.forEach(function(pid){ var p=KG.procs[pid]; if(!p) return;
      h+='<div class="card"><div class="t" data-obj="proc" data-id="'+pid+'">'+pid+' · '+esc(p.title)+'</div>'+
        '<div class="meta">'+esc(p.event_type||'')+' ｜ 步骤 '+(p.steps||[]).length+' ｜ 置信度：'+p.confidence+'</div>'+
        '<div class="meta">'+(p.steps||[]).map(function(s,i){return (i+1)+'.'+String(s.action||'').slice(0,18);}).join(' → ')+'</div></div>';
    });
    h+='</div>'; }
  else h+='<div class="meta">无流程</div>';
  h+='</div>';
  /* 事件层 */
  h+='<div class="psec"><h4>事件层（'+((j.event_ids||[]).length)+'）</h4>';
  if(j.event_ids&&j.event_ids.length){ h+='<div class="sec-grid">';
    j.event_ids.forEach(function(eid){ var e=KG.events[eid]; if(!e) return;
      h+='<div class="card"><div class="t" data-obj="event" data-id="'+eid+'">'+eid+' · '+esc(e.title)+'</div>'+
        '<div class="meta">'+esc(e.type||'')+' ｜ 置信度：'+e.confidence+'</div>'+
        '<div class="meta">'+esc((e.who||[]).join('、'))+' → '+esc(e.action)+' → '+esc((e.what||[]).join('、'))+(e.when?' ｜ 时间：'+esc(e.when):'')+(e.where?' ｜ 地点：'+esc(e.where):'')+'</div></div>';
    });
    h+='</div>'; }
  else h+='<div class="meta">无事件</div>';
  h+='</div>';
  /* 结构化层 */
  h+='<div class="psec"><h4>结构化层</h4>';
  if(j.struct&&Object.keys(j.struct).length){ h+='<div class="sec-grid">';
    for(var sec in j.struct){ j.struct[sec].forEach(function(sid){ var s=KG.structs[sid]; if(!s) return;
      h+='<div class="card"><div class="t" data-obj="struct" data-id="'+sid+'">'+sid+' · '+esc(s.name||s.doc_type||s.fraud||s.keyword||'')+'</div>'+
        '<div class="meta">'+esc(secCN(sec))+' ｜ 置信度：'+s.confidence+'</div>'+
        '<div class="meta">'+esc(String(s.purpose||s.mechanism||s.keyword||'').slice(0,50))+'</div></div>';
    }); }
    h+='</div>'; }
  else h+='<div class="meta">无结构化标注</div>';
  h+='</div>';
  /* 实体层 */
  h+='<div class="psec"><h4>实体层（'+((j.ent_ids||[]).length)+'）</h4><div class="pbody">';
  var chips='';
  (j.ent_ids||[]).forEach(function(eid){ var e=KG.entities[eid]; if(!e) return;
    chips+='<span class="ent ent-'+(e.type||'undetermined')+'" data-eid="'+eid+'">'+esc(e.normalized)+'</span> ';
  });
  h+=(chips||'<div class="meta">无实体标注</div>')+'</div></div>';
  return h;
}
function renderDetailPage(kind, id){
  var D=$('#detailPage');
  if(kind==='ch') D.innerHTML=chPage(id);
  else if(kind==='item') D.innerHTML=itemPage(id);
  else if(kind==='join') D.innerHTML=joinPage(id);
  else if(kind==='ent') D.innerHTML=entPage(id);
  else if(kind==='rule') D.innerHTML=rulePage(id);
  else if(kind==='proc') D.innerHTML=procPage(id);
  else if(kind==='event') D.innerHTML=eventPage(id);
  else if(kind==='struct') D.innerHTML=structPage(id);
  else D.innerHTML='<div class="empty">未知类型 '+kind+'</div>';
  D.scrollTop=0;
}
/* 路由分发覆写 */
dispatchView=function(page, params){
  var p=parseParams(params);
  /* list 页为独立全宽页面（隐藏左目录，与阅读器分开） */
  document.body.classList.toggle('list-view', page==='list');
  if(page==='list'){ openList(p.layer||'ent'); }
  else if(page==='detail'){ renderDetailPage(p.kind, decodeURIComponent(p.id||'')); }
};
/* 从 list/detail 视图点击目录时先切回阅读器（左目录常驻，观感像页面刷新） */
function ensureReader(){
  if(parseHash().page!=='reader') crumbTo(0);
}

/* ========== 搜索 ========== */
function doSearch(){
  var q=$('#searchInput').value.trim(); if(!q){ $('#searchRes').style.display='none'; return; }
  var mode=$('#searchMode').value;
  var res=[];
  if(mode==='item'||mode==='all'){
    KG.chapters.forEach(function(ch){ ch.items.forEach(function(it){
      if(it.text.indexOf(q)>=0) res.push({k:'条目', iid:it.iid, ch:ch.name, l:it.text.slice(0,44)});
    });});
  }
  if(mode==='ent'||mode==='all'){
    for(var eid in KG.entities){ var e=KG.entities[eid];
      if(e.normalized.indexOf(q)>=0 || (e.surfaces||[]).some(function(s){return s.indexOf(q)>=0;}))
        res.push({k:'实体', eid:eid, l:e.normalized+'（'+tyLabel(e.type)+'）'});
    }
    KG.chapters.forEach(function(ch){ ch.items.forEach(function(it){
      (it.entities||[]).forEach(function(x){ if(x.n===q || x.eid===q) res.push({k:'实体@条目', iid:it.iid, eid:x.eid, l:x.n+' → '+it.iid}); });
    });});
  }
  if(mode==='id'||mode==='all'){
    var q2=q.toUpperCase();
    for(var rid in KG.rules){ if(rid.indexOf(q2)>=0||KG.rules[rid].original.indexOf(q)>=0) res.push({k:'规则', rid:rid, l:KG.rules[rid].title||rid}); }
    for(var pid in KG.procs){ if(pid.indexOf(q2)>=0||(KG.procs[pid].title||'').indexOf(q)>=0) res.push({k:'流程', pid:pid, l:KG.procs[pid].title}); }
    for(var ev in KG.events){ if(ev.indexOf(q2)>=0||(KG.events[ev].title||'').indexOf(q)>=0) res.push({k:'事件', ev:ev, l:KG.events[ev].title}); }
    for(var sid in KG.structs){ var s=KG.structs[sid]; if(sid.indexOf(q2)>=0||(s.name||s.doc_type||s.fraud||'').indexOf(q)>=0) res.push({k:'结构', sid:sid, l:(s.name||s.doc_type||s.fraud||sid)}); }
  }
  res=res.slice(0,60);
  var html='';
  if(!res.length) html='<div class="empty">未找到匹配</div>';
  res.forEach(function(r){
    html+='<div class="sr" data-r=\''+JSON.stringify(r).replace(/'/g,'&#39;')+'\'><span class="k">'+r.k+'</span><span class="l">'+esc(r.l)+'</span></div>';
  });
  $('#searchRes').innerHTML=html; $('#searchRes').style.display='block';
  highlight(q);
}
function gotoRes(r){
  $('#searchRes').style.display='none';
  if(r.k==='条目'){ goDetail('item', r.iid); }
  else if(r.k==='实体'){ goDetail('ent', r.eid); }
  else if(r.k==='实体@条目'){ goDetail('item', r.iid); }
  else if(r.k==='规则'){ goDetail('rule', r.rid); }
  else if(r.k==='流程'){ goDetail('proc', r.pid); }
  else if(r.k==='事件'){ goDetail('event', r.ev); }
  else if(r.k==='结构'){ goDetail('struct', r.sid); }
}
/* ========== 高亮 ========== */
function clearMarks(){
  var marks=document.querySelectorAll('#bodyArea mark');
  for(var i=0;i<marks.length;i++){ var m=marks[i]; m.replaceWith(document.createTextNode(m.textContent)); }
}
function highlight(q){
  clearMarks();
  if(!q) return;
  var walker=document.createTreeWalker($('#bodyArea'), NodeFilter.SHOW_TEXT, null);
  var nodes=[];
  while(walker.nextNode()){
    var t=walker.currentNode;
    if(t.nodeValue.indexOf(q)<0) continue;
    var p=t.parentNode;
    if(p.tagName==='SCRIPT'||p.tagName==='STYLE') continue;
    nodes.push(t);
  }
  nodes.forEach(function(t){
    var frag=document.createDocumentFragment(), s=t.nodeValue, i=0, hit;
    while((hit=s.indexOf(q,i))>=0){
      if(hit>i) frag.appendChild(document.createTextNode(s.slice(i,hit)));
      var mk=document.createElement('mark'); mk.textContent=q; frag.appendChild(mk);
      i=hit+q.length;
    }
    if(i<s.length) frag.appendChild(document.createTextNode(s.slice(i)));
    t.parentNode.replaceChild(frag, t);
  });
}
/* ========== 事件委托 ========== */
document.addEventListener('click', function(ev){
  var t=ev.target;
  if(!t||!t.classList) return;
  var closest=function(sel){ return t.closest?t.closest(sel):null; };
  /* 面包屑回跳 */
  if(t.classList.contains('crumb')){
    crumbTo(parseInt(t.getAttribute('data-i'),10));
    return;
  }
  /* 顶栏统计 → 总览列表页 */
  var sl=closest('.statlink');
  if(t.classList.contains('statlink')||sl){ goList((t.classList.contains('statlink')?t:sl).getAttribute('data-l')); return; }
  /* list 页 */
  var tabEl=closest('.bw-tab');
  if(t.classList.contains('bw-tab')||tabEl){ setBwTab((t.classList.contains('bw-tab')?t:tabEl).getAttribute('data-l')); return; }
  if(t.id==='bwBack'){ goReader(); return; }
  var chip=closest('.bf-chip');
  if(chip){ bwState.filter=chip.getAttribute('data-v'); renderBrowse(); return; }
  /* 规则树节点：点击 = 展开/收起 + 联动过滤（含子级的节点展开其子树） */
  var rtn=closest('.rt-node');
  if(rtn){
    var k=rtn.getAttribute('data-k');
    var ico=rtn.querySelector('.rt-ico');
    var hasKids=ico&&ico.textContent!=='';
    bwState.filter=k;
    if(hasKids) rtOpen[k]=!rtOpen[k];
    renderBrowse();
    return;
  }
  /* 规则行 → 详情页 */
  var row=closest('.bw-rule-row');
  if(row){ var rk=row.getAttribute('data-obj'), rid=row.getAttribute('data-id'); if(rk&&rid) goDetail(rk, rid); return; }
  var bwCard=closest('.bw-card');
  if(bwCard){
    var bk=bwCard.getAttribute('data-obj'), bid=bwCard.getAttribute('data-id');
    if(bk&&bid) goDetail(bk, bid);
    return;
  }
  /* 原文可点 → 来源条目详情页 */
  if(t.classList.contains('ori-link')){
    var k=t.getAttribute('data-obj'), id=t.getAttribute('data-id');
    if(k&&id) goDetail(k, id);
    return;
  }
  /* reader 页目录（含内部文字 span 的 closest 回退） */
  var itm=closest('.itm'), grp=closest('.grp'), chEl=closest('.ch'), volEl=closest('.vol');
  if(itm){
    var iid=itm.getAttribute('data-iid');
    ensureReader();
    var f=findItem(iid);
    if(f){
      curIid=iid;
      Object.keys(grpOpen).forEach(function(k2){ delete grpOpen[k2]; });
      grpOpen[f.ch.no]=grpOfItem(iid);
      renderToc();
      renderDetail('item', iid); /* 内部 renderBody + 滚动到 blk + 右栏 */
    }
    return;
  }
  if(closest('.grp-itms')) return; /* 分组展开区空白处不触发上层章 */
  if(grp){
    var gch=grp.getAttribute('data-ch'), g=parseInt(grp.getAttribute('data-g'),10);
    ensureReader();
    var was=grpOpen[gch]===g;
    Object.keys(grpOpen).forEach(function(k2){ if(k2===gch) delete grpOpen[k2]; });
    if(!was){
      grpOpen[gch]=g;
      renderBodyTo(gch, g); /* 覆盖式：清空正文并加载到该组 */
    }
    renderToc();
    if(!was){
      setTimeout(function(){ var el=document.getElementById('grp-'+gch+'-'+g); if(el) el.scrollIntoView({behavior:'smooth', block:'start'}); }, 30);
    }
    return;
  }
  if(chEl){
    var no=chEl.getAttribute('data-ch');
    ensureReader();
    renderDetail('ch', no);
    renderBody(no);
    Object.keys(grpOpen).forEach(function(k2){ delete grpOpen[k2]; });
    grpOpen[no]=0;
    var ch=KG.chapters.find(function(c){return c.no===no;});
    if(ch&&ch.items.length) curIid=ch.items[0].iid;
    renderToc();
    return;
  }
  if(volEl){
    var v=volEl.getAttribute('data-vol');
    var chs=KG.chapters.filter(function(c){return c.vol===v;});
    if(chs.length){
      ensureReader();
      renderDetail('ch', chs[0].no);
      renderBody(chs[0].no);
      Object.keys(grpOpen).forEach(function(k2){ delete grpOpen[k2]; });
      grpOpen[chs[0].no]=0;
      if(chs[0].items.length) curIid=chs[0].items[0].iid;
      renderToc();
    }
    return;
  }
  /* 实体词（正文 / 卡片 / 详情页） */
  if(t.classList.contains('ent')){
    var eid=t.getAttribute('data-eid');
    if(eid) goDetail('ent', eid); else showHint('该词无实体标注（解读层词形）');
    return;
  }
  /* 卡片标题 / 链接 → 详情页 */
  if(t.classList.contains('t')||t.classList.contains('linkbtn')){
    var k2=t.getAttribute('data-obj'), id2=t.getAttribute('data-id');
    if(k2&&id2) goDetail(k2, id2);
    return;
  }
  /* 中间正文：点击「点击查全层 →」打开详情页；点击条目头 → 右侧条目概览 */
  var head=closest('.item-head');
  if(head){
    var iid3=head.getAttribute('data-iid');
    if(iid3){
      if(t.classList.contains('goto')||closest('.goto')) goDetail('item', iid3);
      else renderDetail('item', iid3);
    }
    return;
  }
  var srEl=closest('.sr');
  if(t.classList.contains('sr')||srEl){
    var s2=t.classList.contains('sr')?t:srEl;
    var r=JSON.parse(s2.getAttribute('data-r').replace(/&#39;/g,"'"));
    gotoRes(r);
    return;
  }
  if(t.classList.contains('mt')){
    switchTab(t.getAttribute('data-tab'));
    return;
  }
});
function showHint2(msg){}
$('#searchBtn').addEventListener('click', doSearch);
$('#searchInput').addEventListener('keydown', function(e){ if(e.key==='Enter') doSearch(); });
$('#searchInput').addEventListener('input', function(){ if($('#searchInput').value.trim()) doSearch(); });
document.addEventListener('click', function(ev){
  if(!ev.target.closest('.search-box')) $('#searchRes').style.display='none';
});
/* ========== 启动 ========== */
renderStat(); renderToc(); renderCrumb();
var first=KG.chapters[0];
if(first&&first.items.length){
  curIid=first.items[0].iid;
  renderDetail('ch', first.no);
  renderBody(first.no);
  renderToc();
}
