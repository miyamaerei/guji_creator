const { createApp, ref, computed, watch, nextTick } = Vue;
const D = window.GDATA, F = window.FIELDS || {};
const GT = window.GTIMES || {}, GV = window.GVOLS || {};
const GS = window.GSTAGES || [];
const STAGEC = ['#8a8578', '#3f6d9d', '#a67c00', '#3f9d47', '#7a4fa3', '#c0563a', '#8b1f1f'];
const pad2 = n => String(n).padStart(2, '0');
const dObj = ms => { const d = new Date(ms); const dt = d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate());
  return { date: dt, h: d.getHours() + d.getMinutes() / 60, t: dt + ' ' + pad2(d.getHours()) + ':' + pad2(d.getMinutes()) }; };
const NORM = {ents:"ent",evts:"event",events:"event",rels:"rel",trls:"trl",appts:"appt",lits:"lit",chrs:"chr",mems:"mem",
  tmes:"tme",structs:"struct",rules:"rule",regs:"reg",opns:"opn",nams:"nam",objs:"obj",geos:"geo",evos:"evo",hyds:"hyd",
  gars:"gar",ress:"res",frds:"frd",cits:"cit",mings:"ming","标注":"ent",offices:"org_profile",tim_topics:"tim",
  geo_profiles:"geo_profile",org_profiles:"org_profile",office_profiles:"office_profile",person_profiles:"person_profile",
  process_profiles:"process_profile",reports:"report",laws:"rule",rituals:"reg",dress:"obj",inspect:"reg",
  foreign:"reg",materials:"num",org_events:"tme",geo_station:"geo"};
const normKey = k => NORM[k] || k;
const fBase = f => f.replace(/[\[\]{}(（].*/,"");
const fDesc = f => F[fBase(f)] || F[f] || "（说明待补）";

D.books.forEach(b=>{
  b.records = b.layers.reduce((x,l)=>x+(l[2]||0),0);
  const gts=(GT[b.id]||[]).filter(x=>x!=null);
  b.lastRun = gts.length ? dObj(Math.max(...gts)).t : '—';
  let cur=-1, curState=0;
  b.stageStates.forEach((s,i)=>{ if(s>0){cur=i;curState=s;} });
  b.pct = Math.round(b.stageStates.reduce((x,s)=>x+s,0)/(b.stageStates.length*2)*100);
  b.curLabel = cur<0 ? "未开工" : D.stages[cur] + (curState===2?" ✓":" 中");
  b.curState = curState; b.active = cur<0?0:cur+(curState===2?1:0);
  b.layerRows = b.layers.map(l=>{
    const k = normKey(l[0]); const m=(D.fieldMatrix[k]||{})[b.id];
    return {key:l[0], name:l[1], count:l[2].toLocaleString(), fields: m===undefined?null:m};
  });
  const gv = GV[b.id];
  b.vols = gv ? gv.total : null;
  b.volTip = gv ? ('已装填 '+(gv.fill==null?'—':gv.fill)+'/'+gv.total+' · 已打包 '+(gv.pack==null?'—':gv.pack)+(gv.note?' · '+gv.note:'')) : '卷数未登记';
});

const layerBooks = {};
D.books.forEach(b=>b.layers.forEach(l=>{
  const k=normKey(l[0]);
  const hit=(layerBooks[k]=layerBooks[k]||[]).find(x=>x.id===b.id);
  if(!hit) layerBooks[k].push({id:b.id,title:b.title,count:l[2]});
}));
const allLayerKeys = [...new Set([...Object.keys(layerBooks), ...Object.keys(D.fieldMatrix)])];
const groupOf = {}; D.layerGroups.forEach(g=>g.keys.forEach(k=>groupOf[k]=g.name));
const factoryKeys = new Set(["ent","appt","event","rel","lit","cit","obj","cus","opn","ming","nam","geo","reg","trl","rule","struct","proc","doc","mem","chr","tme","frd","evo","hyd","gar","res"]);

function cmpData(key){
  const m = D.fieldMatrix[key]||{};
  const books = Object.keys(m);
  const known = books.filter(b=>m[b]);
  const heat={}; known.forEach(b=>m[b].forEach(f=>heat[f]=(heat[f]||0)+1));
  const fields = Object.keys(heat);
  return {m, books, known, heat, fields, majority: known.length?Math.ceil(known.length/2):2};
}
function layerInfo(k){
  const bs = layerBooks[k]||[]; const cd = cmpData(k);
  const union=[]; const seen=new Set();
  Object.values(cd.m).forEach(fs=>{ if(fs) fs.forEach(x=>{ if(!seen.has(x)){seen.add(x);union.push(x);} }); });
  const bookFields = bs.map(x=>{
    const mine = cd.m[x.id]===undefined?null:cd.m[x.id];
    return {id:x.id,title:x.title,count:x.count,fields:mine,
      uniq: mine?mine.filter(f=>cd.heat[f]===1):[],
      miss: mine?cd.fields.filter(f=>cd.heat[f]===cd.known.length && !mine.includes(f)):[]};
  });
  return { key:k, name:D.layerNames[k]||k, desc:D.layerDesc[k]||"", books:bs,
    total:bs.reduce((x,b)=>x+b.count,0), union, custom:!factoryKeys.has(k), bookFields };
}
function esc(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;"); }
// 外层演示键的中文备注（record 内字段走 F 字段词典；这些 meta 键是看板展示壳，非数据字段）
const META = { layer:"层标识", note:"层说明", is_factory_layer:"是否工厂层库（false=本书自定义层）",
  anchor:"通用锚点（各层共有的字段）", layer_id:"层内主键（打包器分配）",
  record:"record 对象字段（值留空，行尾 // 注释为含义；来自各书数据文件真实采集）",
  produced_by:"产出此层的书 → 记录数", book:"书名（外层展示标签，非数据字段）",
  record_count:"记录条数（外层展示标签）", unique_fields:"该书独有/偏移字段", missing_common:"缺失的共性字段" };
function hlJson(obj){
  let s = esc(JSON.stringify(obj,null,2));
  s = s.replace(/"([^"]*)":/g,'<span class="jk">"$1"</span>:');
  s = s.replace(/: "([^"]*)"/g,': <span class="jv">"$1"</span>');
  // 字段后追加中文备注（// 注释），字段名与结构保持不变
  s = s.split('\n').map(line=>{
    let m = line.match(/^\s*(?:<span class="jk">)?"([^"]+)"(?:<\/span>)?: .+/);
    if(!m) m = line.match(/^\s*(?:<span class="jv">)?"([^"]+)"(?:<\/span>)?,?$/);
    const note = m && (F[m[1]] || F[fBase(m[1])] || META[m[1]]);
    return note ? line + '<span class="jc">　// ' + esc(note) + '</span>' : line;
  }).join('\n');
  return s;
}
function layerJson(L){
  const rec={}; L.union.forEach(f=>rec[f]="");
  const anc={item_id:"",original:"",norm:"","layer_id":"",confidence:""};
  return hlJson({ layer:L.key, note:L.desc, is_factory_layer:!L.custom,
    anchor:anc,
    record: Object.keys(rec).length?rec:"（各书沿工厂契约，未逐字段采集）",
    produced_by:Object.fromEntries(L.books.map(b=>[b.title,b.count])) });
}
function bookLayerJson(k,fb){
  const rec={}; (fb.fields||[]).forEach(f=>rec[f]="");
  return hlJson({ layer:k, book:fb.title, record_count:fb.count,
    record:Object.keys(rec).length?rec:"沿工厂契约（未逐字段采集）",
    unique_fields:fb.uniq.length?fb.uniq:[], missing_common:fb.miss.length?fb.miss:[] });
}

createApp({
  setup(){
    const tab = ref("books");
    const q = ref(""), fStatus = ref(""), fStage = ref(null);
    const cur = ref({});
    const layerQ = ref(""), selLayerKey = ref("ent"), bookOpen = ref([]), layerSel = ref([]), openAllJson = ref(false);
    const cmpLayer = ref("ent"), cmpOnly = ref(""), cmpAnnot = ref(true), cmpOpen = ref([]), cmpSwitch = ref("");

    const stTag = {done:"success", wip:"warning", none:"info"};
    const stTxt2 = {done:"✅ 完成", wip:"🚧 在建", none:"⬜ 无产出"};

    const filteredBooks = computed(()=>D.books.filter(b=>{
      const kw=q.value.trim();
      if(kw && !(b.title+b.dir+b.author+b.genre).includes(kw)) return false;
      if(fStatus.value && b.status!==fStatus.value) return false;
      if(fStage.value!==null && fStage.value!==""){
        let cur2=-1; b.stageStates.forEach((s,i)=>{if(s>0)cur2=i;});
        if(cur2!==fStage.value) return false;
      }
      return true;
    }));

    const allInfo = computed(()=>allLayerKeys.map(layerInfo));
    const filteredLayers = computed(()=>{
      const kw=layerQ.value.trim();
      let ls = allInfo.value;
      if(kw) ls = ls.filter(L=>(L.key+L.name+L.desc+L.union.join("")+L.bookFields.map(x=>x.title).join("")).includes(kw));
      return ls;
    });
    const navGroups = computed(()=>{
      const order = [...D.layerGroups.map(g=>g.name), "其他（归并后散层）"];
      return order.map(name=>({name, list: filteredLayers.value.filter(L=>groupOf[L.key]===name)
        .sort((a,b)=>b.books.length-a.books.length||b.total-a.total)}));
    });
    const selLayer = computed(()=>allInfo.value.find(L=>L.key===selLayerKey.value)||null);
    watch(selLayer, ()=>{ bookOpen.value=[]; layerSel.value=[]; });
    watch(layerSel, v=>{ bookOpen.value=[...v]; });

    const cmpKeys = computed(()=>Object.keys(D.fieldMatrix).filter(k=>Object.keys(D.fieldMatrix[k]).length>=1));
    const cmpDataC = computed(()=>cmpData(cmpLayer.value));
    const cmpBooks = computed(()=>cmpDataC.value.books);
    const cmpKnownIds = computed(()=>cmpDataC.value.known);
    const cmpKnown = computed(()=>cmpDataC.value.known.length);
    const cmpMajority = computed(()=>cmpDataC.value.majority);
    const cmpRows = computed(()=>cmpDataC.value.fields.map(f=>({field:f, heat:cmpDataC.value.heat[f], common:cmpDataC.value.heat[f]>=cmpDataC.value.majority})));
    const uniqOf = id => (cmpDataC.value.m[id]||[]).filter(f=>cmpDataC.value.heat[f]===1);
    const missOf = id => cmpDataC.value.fields.filter(f=>cmpDataC.value.heat[f]===cmpDataC.value.known.length && !(cmpDataC.value.m[id]||[]).includes(f));
    const cmpSummary = computed(()=>cmpKnownIds.value.map(id=>({id,title:bookOf(id).title,uniq:uniqOf(id),miss:missOf(id)})));
    function cmpBookJson(id){
      const rec={}; (cmpDataC.value.m[id]||[]).forEach(f=>rec[f]="");
      return hlJson({ layer:cmpLayer.value, book:bookOf(id).title, record:Object.keys(rec).length?rec:"（未采集）",
        unique_fields:uniqOf(id).length?uniqOf(id):[], missing_common:missOf(id) });
    }
    function stepDesc(b,i){
      const g=GV[b.id], parts=[];
      const ms=b.id&&GT[b.id]&&GT[b.id][i]; if(ms) parts.push(dObj(ms).t);
      if(g&&g.total){ if(i===2) parts.push('装填 '+g.fill+'/'+g.total+' 卷'); if(i===3&&g.pack!=null) parts.push('打包 '+g.pack+'/'+g.total+' 卷'); }
      return parts.join(' · ') || '未执行';
    }
    function volText(b){
      const g=GV[b.id]; if(!g||!g.total) return '';
      let s='共 '+g.total+' 卷 · 装填已到 '+g.fill+' 卷 · '+(g.pack==null?'打包不分卷（成品按部门聚合）':'打包已到 '+g.pack+' 卷');
      if(g.note) s+='　'+g.note;
      return s;
    }
    const tlQ=ref(''), tlStages=ref([0,1,2,3,4,5,6]);
    const tlMode=ref('chart'), tlBook=ref(''), tlChart=ref(null);
    let tlInst=null;
    // 与书目/详情共用同一数据源：GTIMES 阶段时间戳 → 事件流
    function tlEvents(){
      const evs=[];
      Object.keys(GT).forEach(id=>{ const b=bookOf(id); if(!b.title) return;
        (GT[id]||[]).forEach((ms,s)=>{ if(ms==null||!tlStages.value.includes(s)) return;
          evs.push({id,s,ms,t:dObj(ms).t,title:b.title}); }); });
      return evs;
    }
    const tlChartBooks=computed(()=>{ const ids=new Set(tlEvents().map(e=>e.id));
      return D.books.filter(b=>ids.has(b.id)); });
    function renderTlChart(){
      if(tab.value!=='timeline'||tlMode.value==='dom') return;
      const el=tlChart.value; if(!el||!window.echarts) return;
      if(!tlInst||tlInst.dom!==el){ if(tlInst&&!tlInst.isDisposed()) tlInst.dispose(); tlInst=window.echarts.init(el); }
      let evs=tlEvents();
      if(tlMode.value==='one'){
        if(!tlBook.value&&tlChartBooks.value.length) tlBook.value=tlChartBooks.value[0].id;
        evs=evs.filter(e=>e.id===tlBook.value);
      }
      const ids=[...new Set(evs.map(e=>e.id))];
      const names=ids.map(id=>'《'+bookOf(id).title+'》');
      const series=D.stages.map((nm,s)=>({
        name:nm, type:'scatter', symbolSize:tlMode.value==='one'?17:13,
        itemStyle:{color:STAGEC[s], borderColor:'#fffdf7', borderWidth:1.5},
        data:evs.filter(e=>e.s===s).map(e=>({value:[e.ms, ids.indexOf(e.id)], t:e.t, title:e.title}))
      }));
      tlInst.setOption({
        animation:false,
        grid:{left:140,right:40,top:52,bottom:74},
        legend:{top:4,data:D.stages,textStyle:{fontSize:12}},
        tooltip:{formatter:p=>'《'+p.data.title+'》 <b>'+p.seriesName+'</b><br>'+p.data.t},
        xAxis:{type:'time',splitLine:{show:true,lineStyle:{color:'#efe6d3'}},
          axisLabel:{hideOverlap:true,formatter:{year:'{yyyy}',month:'{MM}-{dd}',day:'{MM}-{dd}',hour:'{HH}:{mm}',minute:'{HH}:{mm}',second:'{HH}:{mm}'}}},
        yAxis:{type:'category',data:names,inverse:true,axisLabel:{fontSize:12},splitLine:{show:true,lineStyle:{color:'#efe6d3'}}},
        dataZoom:[{type:'slider',xAxisIndex:0,height:24,bottom:12},{type:'inside',xAxisIndex:0}],
        series
      },true);
      tlInst.resize();
    }
    watch([tab,tlMode,tlStages,tlBook], ()=>{ if(tab.value==='timeline'&&tlMode.value!=='dom') nextTick(renderTlChart); });
    window.addEventListener('resize', ()=>{ if(tlInst&&!tlInst.isDisposed()) tlInst.resize(); });
    const tlDays=computed(()=>{
      const kw=tlQ.value.trim(); const byDay={};
      Object.keys(GT).forEach(id=>{ const b=bookOf(id); if(!b.title) return;
        if(kw && !(b.title+b.dir).includes(kw)) return;
        (GT[id]||[]).forEach((ms,s)=>{ if(ms==null||!tlStages.value.includes(s)) return;
          const o=dObj(ms); (byDay[o.date]=byDay[o.date]||[]).push({id,s,h:o.h,t:o.t}); }); });
      return Object.keys(byDay).sort().map(date=>{
        const evs=byDay[date];
        let h0=Math.floor(Math.min(...evs.map(e=>e.h))), h1=Math.ceil(Math.max(...evs.map(e=>e.h)));
        if(h1-h0<3) h1=h0+3;
        const lanes=[], seen={};
        evs.slice().sort((a,b)=>a.id<b.id?-1:1).forEach(e=>{ if(seen[e.id]==null){seen[e.id]=lanes.length;lanes.push({id:e.id,evs:[]});} lanes[seen[e.id]].evs.push({s:e.s,h:e.h,t:e.t}); });
        const hours=[]; for(let h=h0;h<=h1;h++)hours.push(h);
        return {date,cnt:evs.length,h0,h1,hours,lanes};
      });
    });
    const tlPos=(h,dy)=>((h-dy.h0)/(dy.h1-dy.h0)*100).toFixed(2)+'%';

    function openBook(b){ cur.value=b; tab.value="book"; }
    // 当前流程节点：状态推导与 stages.js 数据结构同源
    const curFlow = computed(()=>{
      const b=cur.value; if(!b.id||!b.stageStates) return null;
      let ci=-1, st=0; b.stageStates.forEach((s,i)=>{ if(s>0){ci=i;st=s;} });
      if(ci<0) return {name:"未开工", state:0, mark:"尚无任何阶段产出（原料也未入库）", next:GS.length?("先做「"+GS[0].name+"」："+GS[0].goal):"—"};
      const g=GS[ci]||{name:D.stages[ci],mark:"",next:""};
      const next = st===1 ? ("本阶段进行中，先做完："+g.next)
        : (ci+1<GS.length ? ("本阶段已完成 ✓，进入「"+GS[ci+1].name+"」："+GS[ci+1].goal) : "全流程已交付，后续以版本增量维护");
      return {name:g.name, state:st, mark:g.mark, next};
    });
    function flowRows(b){
      return GS.map((g,i)=>{
        const stv=(b.stageStates&&b.stageStates[i])||0;
        const ms=b.id&&GT[b.id]?GT[b.id][i]:null;
        let next;
        if(stv===2) next = i+1<GS.length ? ("→ "+GS[i+1].name+"："+GS[i+1].goal) : "交付完成，维护版本增量即可";
        else if(stv===1) next = g.next;
        else next = "待前序阶段完成后进入本步："+g.goal;
        return {i, name:g.name, goal:g.goal, mark:g.mark, st:stv===2?"完成":stv===1?"进行中":"未开始",
          next, time: ms!=null?dObj(ms).t:"—"};
      });
    }
    function stepStatus(i){ const s=cur.value.stageStates&&cur.value.stageStates[i]; return s===2?"success":s===1?"process":"wait"; }
    function bookOf(id){ return D.books.find(x=>x.id===id)||{}; }
    function pickLayer(L){ selLayerKey.value=L.key; openAllJson.value=false; }
    function cmpCellCls(bid,row){
      const cd=cmpDataC.value; const m=cd.m[bid];
      if(!m) return "muted";
      const has=m.includes(row.field);
      if(has && cd.heat[row.field]===1) return "unqdot";
      if(has) return "okdot";
      return cd.heat[row.field]>=cd.majority?"nodot":"";
    }
    function cmpMark(bid,row){
      const cd=cmpDataC.value; const m=cd.m[bid];
      if(!m) return "—";
      const has=m.includes(row.field);
      return has?"✓":(cd.heat[row.field]>=cd.majority?"✗":"");
    }

    const qs=new URLSearchParams(location.search);
    if(qs.get("tab")) tab.value=qs.get("tab");
    if(qs.get("layer")&&D.fieldMatrix[qs.get("layer")]){ cmpLayer.value=qs.get("layer"); selLayerKey.value=qs.get("layer"); }
    if(qs.get("id")){ const b=D.books.find(x=>x.id===qs.get("id")); if(b) openBook(b); }

    return {D,tab,q,fStatus,fStage,filteredBooks,stTag,stTxt2,openBook,cur,stepStatus,stepDesc,volText,curFlow,flowRows,GS,
      layerQ,navGroups,selLayer,pickLayer,bookOpen,layerSel,openAllJson,layerJson,bookLayerJson,
      allLayerKeys,totalPairs:Object.values(layerBooks).reduce((s,v)=>s+v.length,0),
      cmpLayer,cmpOnly,cmpAnnot,cmpOpen,cmpSwitch,cmpKeys,cmpBooks,cmpKnownIds,cmpKnown,cmpMajority,
      cmpRows,cmpSummary,cmpBookJson,cmpCellCls,cmpMark,uniqOf,missOf,bookOf,fDesc,
      tlQ,tlStages,tlDays,tlPos,STAGEC,tlMode,tlBook,tlChart,tlChartBooks};
  }
}).use(ElementPlus).mount("#app");
