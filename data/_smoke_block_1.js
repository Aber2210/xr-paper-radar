
"use strict";
const DIMS=[
 {k:"IMP",zh:"问题重要性",w:0.20},{k:"NOV",zh:"方法创新性",w:0.20},
 {k:"TEC",zh:"技术完整度",w:0.15},{k:"EXP",zh:"实验强度",w:0.15},
 {k:"PER",zh:"性能增益",w:0.15},{k:"TRL",zh:"落地成熟度",w:0.08},
 {k:"REP",zh:"可复现与影响力",w:0.07}];
const TRACK_COLORS={"神经渲染":"#7c6cff","重建与SLAM":"#3fbf9f","化身与人体":"#ff7a9e","感知与认知":"#f5a623",
 "内容生成":"#5bc8f5","渲染与显示":"#c588ff","空间计算与UI":"#6ee7b7","交互与输入":"#f97362",
 "触觉与多模态":"#e879c7","世界模型与仿真":"#60a5fa","系统与平台":"#b8c45e","评估与数据集":"#8ab4d8"};
const NONXR_TRACK="—（非 XR）";
const GRADE_COLOR={S:"#f5c542",A:"#5b8cff",B:"#3fbf9f",C:"#8a93a8"};
const SCORE_BG=["#1b2440","#22335c","#2c4a86","#3566b8","#4d86ef"];
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const isXR=p=>p.track!==NONXR_TRACK;
const fmt=v=>(v==null?"—":Number(v).toFixed(2));
function loadDailyHidden(){try{const v=JSON.parse(localStorage.getItem("xrhub.daily.hidden")||"{}");return (v&&typeof v==="object")?v:{}}catch(e){return{}}}
function saveDailyHidden(){try{localStorage.setItem("xrhub.daily.hidden",JSON.stringify(state.daily.hidden))}catch(e){}}
const state={tab:"overview",
  lib:{q:"",track:"",grade:"",ev:"",batch:"",top10:false,flag:false,nonxr:false,sort:"value"},
  dim:{q:"",track:"",grade:"",batch:"",nonxr:false},
  note:{q:"",track:"",sel:null},
  daily:{sort:"date-desc",hidden:loadDailyHidden()}};

/* ---------- tabs ---------- */
document.getElementById("tabs").addEventListener("click",e=>{
  const b=e.target.closest("button[data-tab]");if(!b)return;
  state.tab=b.dataset.tab;
  document.querySelectorAll("nav.tabs button").forEach(x=>x.classList.toggle("active",x===b));
  document.querySelectorAll("section.tab").forEach(s=>s.classList.toggle("active",s.id==="tab-"+state.tab));
  if(state.tab==="daily")renderDaily();
  if(state.tab==="library")renderLibrary();
  if(state.tab==="dim7")renderDim7();
  if(state.tab==="notes")renderNotes();
});

/* ---------- shared svg ---------- */
function radarSVG(scores,size,color){
  size=size||240;color=color||"#5b8cff";
  const cx=size/2,cy=size/2,R=size/2-36,n=7;let g="",dp=[];
  for(let ring=1;ring<=5;ring++){
    const rr=R*ring/5,p=[];
    for(let i=0;i<n;i++){const a=-Math.PI/2+i*2*Math.PI/n;p.push((cx+rr*Math.cos(a)).toFixed(1)+","+(cy+rr*Math.sin(a)).toFixed(1));}
    g+='<polygon points="'+p.join(" ")+'" fill="none" stroke="#263353" stroke-width="1"/>';
  }
  for(let i=0;i<n;i++){
    const a=-Math.PI/2+i*2*Math.PI/n;
    g+='<line x1="'+cx+'" y1="'+cy+'" x2="'+(cx+R*Math.cos(a)).toFixed(1)+'" y2="'+(cy+R*Math.sin(a)).toFixed(1)+'" stroke="#263353"/>';
    const lx=cx+(R+19)*Math.cos(a),ly=cy+(R+19)*Math.sin(a);
    g+='<text x="'+lx.toFixed(1)+'" y="'+ly.toFixed(1)+'" fill="#98a5c0" font-size="11" text-anchor="middle" dominant-baseline="middle">'+DIMS[i].k+'</text>';
    const v=Math.max(0,Math.min(5,scores[DIMS[i].k]||0)),rr=R*Math.max(v,0.12)/5;
    dp.push((cx+rr*Math.cos(a)).toFixed(1)+","+(cy+rr*Math.sin(a)).toFixed(1));
  }
  return '<svg viewBox="0 0 '+size+' '+size+'" width="'+size+'" height="'+size+'">'+g+
    '<polygon points="'+dp.join(" ")+'" fill="'+color+'33" stroke="'+color+'" stroke-width="2"/></svg>';
}
function donutSVG(series,size){
  size=size||210;const r=72,cx=size/2,cy=size/2,C=2*Math.PI*r;
  const total=series.reduce((a,s)=>a+s.value,0)||1;let acc=0,g="";
  series.forEach(s=>{
    const frac=s.value/total;
    g+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+s.color+'" stroke-width="26" '+
       'stroke-dasharray="'+(frac*C-1.5).toFixed(2)+' '+(C-frac*C+1.5).toFixed(2)+'" '+
       'stroke-dashoffset="'+(-acc*C).toFixed(2)+'" transform="rotate(-90 '+cx+' '+cy+')"/>';
    acc+=frac;
  });
  return '<svg viewBox="0 0 '+size+' '+size+'" width="'+size+'" height="'+size+'">'+g+
    '<text x="'+cx+'" y="'+(cy-4)+'" text-anchor="middle" fill="#e8edf7" font-size="22" font-weight="700">'+total+'</text>'+
    '<text x="'+cx+'" y="'+(cy+15)+'" text-anchor="middle" fill="#98a5c0" font-size="11">篇</text></svg>';
}
function trendSVG(rows){
  const W=940,H=250,pl=42,pr=44,pt=14,pb=52;
  const iw=W-pl-pr,ih=H-pt-pb;
  const maxC=Math.max.apply(null,rows.map(r=>r.count).concat([1]));
  const bw=Math.max(10,iw/rows.length-14);
  let g="",xs=[],ys=[];
  rows.forEach((r,i)=>{
    const x=pl+iw*(i+0.5)/rows.length;
    const h=ih*r.count/maxC;
    const col=r.xrCount!=null?"#5b8cff":"#3a4a75";
    g+='<rect x="'+(x-bw/2).toFixed(1)+'" y="'+(pt+ih-h).toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+h.toFixed(1)+'" rx="3" fill="'+col+'" opacity="0.9"><title>'+esc(r.label)+'：新增 '+r.count+' 篇</title></rect>';
    if(r.count>0)g+='<text x="'+x.toFixed(1)+'" y="'+(pt+ih-h-5).toFixed(1)+'" text-anchor="middle" fill="#98a5c0" font-size="10.5">'+r.count+'</text>';
    const yv=r.avg==null?null:pt+ih-ih*r.avg/5;
    if(yv!=null){xs.push(x.toFixed(1));ys.push(yv.toFixed(1));}
    const lb=r.label.length>10?r.label.replace("2026-",""):r.label;
    g+='<text x="'+x.toFixed(1)+'" y="'+(H-30)+'" text-anchor="middle" fill="#6b7a99" font-size="10" transform="rotate(-32 '+x.toFixed(1)+' '+(H-30)+')">'+esc(lb)+'</text>';
  });
  if(xs.length>1)g+='<polyline points="'+xs.map((x,i)=>x+","+ys[i]).join(" ")+'" fill="none" stroke="#f5c542" stroke-width="2"/>';
  xs.forEach((x,i)=>{g+='<circle cx="'+x+'" cy="'+ys[i]+'" r="3" fill="#f5c542"/>';});
  for(let v=0;v<=5;v+=1){
    const y=pt+ih-ih*v/5;
    g+='<line x1="'+pl+'" y1="'+y+'" x2="'+(W-pr)+'" y2="'+y+'" stroke="#1c2742"/>'+
       '<text x="'+(pl-7)+'" y="'+(y+3.5)+'" text-anchor="end" fill="#6b7a99" font-size="10">'+v+'</text>'+
       '<text x="'+(W-pr+7)+'" y="'+(y+3.5)+'" fill="#6b7a99" font-size="10">'+v+'</text>';
  }
  return '<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;height:auto">'+g+'</svg>';
}
function scoreCell(v){
  const t=Math.max(1,Math.min(5,v||0));
  return '<span class="dimcell" style="background:'+SCORE_BG[t-1]+';color:#fff">'+v+'</span>';
}
function miniBars(scores){
  return '<span class="minibar">'+DIMS.map(d=>{
    const v=scores[d.k]||0;
    return '<i style="height:'+Math.max(8,v/5*16)+'px;background:'+SCORE_BG[Math.max(1,Math.min(5,v))-1]+'" title="'+d.k+' '+d.zh+'：'+v+'"></i>';
  }).join("")+'</span>';
}
function trackChip(t){
  const c=TRACK_COLORS[t]||"#8a93a8";
  return '<span class="chip track" style="background:'+c+'1f;color:'+c+';border-color:'+c+'55">'+esc(t)+'</span>';
}
function gradeChip(g){return '<span class="chip '+g+'">'+g+'</span>';}
function evChip(e){
  const cls=e==="FULL"?"ev":(e==="PARTIAL"?"ev PARTIAL":"ev ABSTRACT_ONLY");
  const zh=e==="FULL"?"全文":(e==="PARTIAL"?"部分":"摘要");
  return '<span class="chip '+cls+'" title="证据等级 '+esc(e)+'">'+zh+'</span>';
}

/* ---------- overview ---------- */
function renderOverview(){
  const P=DATA.papers,xr=P.filter(isXR),nonxr=P.length-xr.length;
  const full=P.filter(p=>p.evidence==="FULL").length;
  const dates=P.map(p=>p.date).filter(Boolean).sort();
  const tracks={};xr.forEach(p=>tracks[p.track]=(tracks[p.track]||0)+1);
  const grades={S:0,A:0,B:0,C:0};xr.forEach(p=>grades[p.grade]=(grades[p.grade]||0)+1);
  const evs={};P.forEach(p=>evs[p.evidence]=(evs[p.evidence]||0)+1);
  const kpi=(v,k,sub)=>'<div class="kpi"><div class="v">'+v+(sub?'<small>'+sub+'</small>':'')+'</div><div class="k">'+k+'</div></div>';
  let h='<div class="kpis">'+
    kpi(xr.length,"XR 核心收录","/ 含非XR "+P.length)+
    kpi(DATA.notes.length,"原子笔记")+
    kpi(full,"全文精读","L0/L1")+
    kpi(DATA.batches.length,"调度批次")+
    kpi(dates[0].slice(5).replace("-","/")+" — "+dates[dates.length-1].slice(5).replace("-","/"),"覆盖跨度")+
    kpi(P.filter(p=>p.top10).length,"入选 Top10")+
  '</div>';
  const trackSeries=Object.keys(tracks).map(t=>({label:t,value:tracks[t],color:TRACK_COLORS[t]||"#8a93a8"}))
    .sort((a,b)=>b.value-a.value);
  h+='<div class="grid3"><div class="panel"><h3>赛道分布<span class="hint">XR 核心 '+xr.length+' 篇 · 共 '+trackSeries.length+' 赛道</span></h3>'+
     '<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">'+donutSVG(trackSeries)+
     '<div class="legend" style="flex-direction:column;gap:5px;flex:1;min-width:200px">'+trackSeries.map(s=>
       '<span class="it"><span class="dot" style="background:'+s.color+'"></span>'+esc(s.label)+' <b style="color:#e8edf7">'+s.value+'</b></span>').join("")+'</div></div></div>';
  h+='<div class="panel"><h3>等级分布<span class="hint">S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C&lt;3.00</span></h3>'+
     ["S","A","B","C"].map(g=>{
       const v=grades[g]||0,pct=xr.length?(v/xr.length*100):0;
       return '<div class="bar-row"><span class="lb">'+g+' 级</span><div class="bar-track"><div class="bar-fill" style="width:'+pct.toFixed(1)+'%;background:'+GRADE_COLOR[g]+'"></div></div><span class="val">'+v+' 篇 · '+pct.toFixed(0)+'%</span></div>';
     }).join("")+
     '<h3 style="margin-top:16px">证据等级<span class="hint">全文精读覆盖率 '+(P.length?(full/P.length*100).toFixed(0):0)+'%</span></h3>'+
     ["FULL","PARTIAL","ABSTRACT_ONLY"].map(e=>{
       const v=evs[e]||0,pct=P.length?(v/P.length*100):0;
       const c=e==="FULL"?"#3fbf9f":(e==="PARTIAL"?"#f97362":"#f5c542");
       const zh=e==="FULL"?"全文 FULL":(e==="PARTIAL"?"部分 PARTIAL":"摘要 ABSTRACT");
       return '<div class="bar-row"><span class="lb">'+zh+'</span><div class="bar-track"><div class="bar-fill" style="width:'+pct.toFixed(1)+'%;background:'+c+'"></div></div><span class="val">'+v+' 篇 · '+pct.toFixed(0)+'%</span></div>';
     }).join("")+'</div></div>';
  h+='<div class="panel" style="margin-bottom:16px"><h3>批次趋势<span class="hint">柱=当日入选 XR 新稿数 · 线=当批加权均分（右轴 0–5）</span></h3>'+trendSVG(DATA.trend)+'</div>';
  h+='<div class="grid2"><div class="panel"><h3>七维评分体系<span class="hint">固定权重保证跨日可比</span></h3>'+
     '<table class="tb"><tr><th>维度</th><th>含义</th><th>权重</th><th>5 分标准</th></tr>'+
     DIMS.map(d=>'<tr><td class="mono">'+d.k+'</td><td>'+d.zh+'</td><td>'+d.w.toFixed(2)+'</td><td class="tt2">'+esc(DATA.dimDefs[d.k])+'</td></tr>').join("")+
     '</table></div>';
  h+='<div class="panel"><h3>数据口径说明</h3><ul style="margin-left:18px;font-size:12.8px;color:#cfd8ec;line-height:2">'+
     '<li>数据源：arXiv RSS（7 分类）+ API submittedDate 双通道去重，经关键词与人工判读筛选。</li>'+
     '<li>「'+esc(NONXR_TRACK)+'」'+nonxr+' 篇为关键词命中但判读为非 XR 的留存条目（默认不计入核心统计，可切换显示）。</li>'+
     '<li>证据等级：FULL=全文精读；PARTIAL=正文不完整；ABSTRACT_ONLY=仅摘要评分（可信度受限）。</li>'+
     '<li>带 ⚠️ 标记的论文存在局限或路线落后风险，详见各篇笔记与论文库详情。</li>'+
     '<li>每日解读报告 / MOC / 7 维表 / 运行日志原文见「每日解读」页各批次链接。</li></ul></div></div>';
  $("#tab-overview").innerHTML=h;
  $("#hdSub").textContent="累计 "+P.length+" 篇 · 跨度 "+dates[0]+" ~ "+dates[dates.length-1]+" · 生成于 "+DATA.meta.generated;
  $("#cntDaily").textContent=DATA.batches.length;
  $("#cntLib").textContent=P.length;
  $("#cntDim").textContent=P.length;
  $("#cntNotes").textContent=DATA.notes.length;
}

/* ---------- daily ---------- */
function prow(p,i){
  const ni=DATA.noteIndex[p.id];
  const badges=[];
  if(p.top10)badges.push('<span class="chip top10" style="transform:scale(.82)">TOP10</span>');
  if(p.evidence)badges.push(evChip(p.evidence));
  if(p.outdated||(p.flags&&p.flags.length))badges.push('<span class="chip warn" style="transform:scale(.82)" title="'+esc((p.flags||[]).join("；")||"方法路线落后")+'">⚠️</span>');
  if(ni!=null)badges.push('<button class="btn" data-gonote="'+ni+'">📖 笔记</button>');
  return '<div class="prow"><span class="rk">'+(i+1)+'</span>'+
    '<a class="pname" href="https://arxiv.org/abs/'+p.id+'" target="_blank" title="'+esc(p.title_zh)+'">'+esc(p.title_zh)+'</a>'+
    '<span class="chip '+p.grade+'" style="transform:scale(.82)">'+p.grade+'</span>'+
    '<span class="mono pv">'+fmt(p.value)+'</span>'+
    '<span class="pbadges">'+badges.join("")+'</span></div>';
}
const DAILY_SORTS=[["date-desc","排序：时间 新→旧"],["date-asc","排序：时间 旧→新"],
  ["count-desc","排序：新稿数 多→少"],["count-asc","排序：新稿数 少→多"],
  ["avg-desc","排序：均分 高→低"],["avg-asc","排序：均分 低→高"],["max-desc","排序：最高分 高→低"]];
function dailySorted(){
  const arr=DATA.batches.slice();
  const skAsc=(a,b)=>{const x=a._sort||[a.key,0],y=b._sort||[b.key,0];
    if(x[0]!==y[0])return x[0]<y[0]?-1:1;return x[1]-y[1];};
  const skDesc=(a,b)=>{const x=a._sort||[a.key,0],y=b._sort||[b.key,0];
    if(x[0]!==y[0])return x[0]<y[0]?1:-1;return x[1]-y[1];};
  const num=(av,bv,desc)=>{const a=(av==null?Infinity:av),b=(bv==null?Infinity:bv);if(a===b)return 0;return desc?(b-a):(a-b);};
  switch(state.daily.sort){
    case "date-asc":arr.sort(skAsc);break;
    case "count-desc":arr.sort((a,b)=>(b.papers.length-a.papers.length)||skDesc(a,b));break;
    case "count-asc":arr.sort((a,b)=>(a.papers.length-b.papers.length)||skAsc(a,b));break;
    case "avg-desc":arr.sort((a,b)=>num(a.avg,b.avg,true)||skDesc(a,b));break;
    case "avg-asc":arr.sort((a,b)=>num(a.avg,b.avg,false)||skAsc(a,b));break;
    case "max-desc":arr.sort((a,b)=>num(a.max,b.max,true)||skDesc(a,b));break;
    default:arr.sort(skDesc);
  }
  return arr;
}
function dailyInfoHTML(){
  return '<span class="info-wrap"><button class="info-btn" data-info="daily" title="数据口径说明">i</button>'+
    '<span class="info-pop" id="info-daily">论文清单以各日 <b>7 维对比表</b>（papers/daily/&lt;日期&gt;/7dim-table.md）为权威来源，registry 作富化；默认按抓取时间倒序，可用左侧排序下拉切换；卡片右上角箭头可<b>隐藏 / 显示</b>单个抓取日（浏览器本地记忆，刷新不丢）。<br>⚠️ = 路线落后或局限警示 · 📖 = 有原子笔记 · TOP10 = 当日入选前十</span></span>';
}
function dailyFiltersHTML(){
  const hidCount=DATA.batches.filter(b=>state.daily.hidden[b.key]).length;
  return '<div class="filters">'+
    '<select id="dailySort" data-dailysort title="排序方式">'+DAILY_SORTS.map(s=>'<option value="'+s[0]+'"'+(state.daily.sort===s[0]?" selected":"")+'>'+s[1]+'</option>').join("")+'</select>'+
    '<span id="dailyShowall">'+(hidCount?'<button class="btn" data-showall title="恢复所有被隐藏的抓取日">全部显示（'+hidCount+'）</button>':"")+'</span>'+
    '<span class="count" id="dailyCount">共 '+DATA.batches.length+' 个抓取日'+(hidCount?' · 已隐藏 '+hidCount:'')+'</span>'+
    dailyInfoHTML()+'</div>';
}
function refreshDailyChrome(){
  const hidCount=DATA.batches.filter(x=>state.daily.hidden[x.key]).length;
  const c=$("#dailyCount");
  if(c)c.textContent='共 '+DATA.batches.length+' 个抓取日'+(hidCount?' · 已隐藏 '+hidCount:'');
  const sa=$("#dailyShowall");
  if(sa)sa.innerHTML=hidCount?'<button class="btn" data-showall title="恢复所有被隐藏的抓取日">全部显示（'+hidCount+'）</button>':"";
}
function bcardHTML(b){
  const all=(b.papers||[]);
  const hid=!!state.daily.hidden[b.key];
  const top=all.slice(0,5);
  const rest=all.slice(5);
  const g=["S","A","B","C"].map(g=>b.grades[g]?'<span class="chip '+g+'">'+g+' '+b.grades[g]+'</span>':"").join("");
  const note=b.statusNote?'<div class="note">'+b.statusNote+'</div>':"";
  const merged=b.note?'<div class="tt2">※ '+esc(b.note)+'</div>':"";
  const links=[
    b.links.report&&'<a href="'+b.links.report+'" target="_blank">解读报告</a>',
    b.links.moc&&'<a href="'+b.links.moc+'" target="_blank">MOC</a>',
    b.links.table&&'<a href="'+b.links.table+'" target="_blank">7维表</a>',
    b.links.log&&'<a href="'+b.links.log+'" target="_blank">运行日志</a>'].filter(Boolean).join("");
  const body=all.length?
    ('<div class="top">'+top.map(prow).join("")+'</div>'+
     (rest.length?'<button class="btn" data-exp="'+esc(b.key)+'" data-label="展开全部 '+all.length+' 篇 ▾" style="margin-top:6px">展开全部 '+all.length+' 篇 ▾</button>'+
      '<div class="pfull" id="pf-'+esc(b.key)+'" hidden>'+rest.map((p,i)=>prow(p,i+5)).join("")+'</div>':"")):
    '<div class="tt2" style="padding:6px 0">当日无新稿入选（周末 / API 索引停滞，详见运行日志）</div>';
  const refBody=(b.refPapers&&b.refPapers.length)?
    ('<button class="btn" data-exp="ref-'+esc(b.key)+'" data-label="文献库前沿参考 '+b.refPapers.length+' 篇 ▾" style="margin-top:6px">文献库前沿参考 '+b.refPapers.length+' 篇 ▾</button>'+
     '<div class="pfull" id="pf-ref-'+esc(b.key)+'" hidden>'+b.refPapers.map((p,i)=>prow(p,i)).join("")+'</div>'):"";
  const head='<div class="bh"><span class="bd">'+esc(b.label)+'</span>'+
    '<span class="bh-r"><span class="bn">'+(all.length===0?"0 新稿":"XR 新稿 "+all.length)+'</span>'+
    '<button class="eye" data-hide="'+esc(b.key)+'" title="'+(hid?"显示该抓取日":"隐藏该抓取日")+'">'+(hid?"▷":"◁")+'</button></span></div>';
  return '<div class="bcard'+(all.length===0?" empty":"")+(hid?" hidden":"")+'">'+head+
    (hid?'<div class="vhint">内容已隐藏（'+all.length+' 篇'+(b.avg!=null?' · 均分 '+fmt(b.avg):'')+'）· 点击 ◁ 重新显示</div>':
     '<div class="stats">'+g+(b.avg!=null?'<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">均分 '+fmt(b.avg)+'</span>':'')+
     (b.max!=null?'<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">最高 '+fmt(b.max)+'</span>':'')+'</div>'+
     (b.window?'<div class="tt2">'+esc(b.window)+'</div>':"")+body+refBody+merged+note+
     (links?'<div class="links">'+links+'</div>':""))+'</div>';
}
function bindDailySort(){
  const sel=$("#dailySort");
  if(sel)sel.addEventListener("change",()=>{
    if(state.daily.sort!==sel.value){state.daily.sort=sel.value;renderDaily();const s2=$("#dailySort");if(s2)s2.focus();}
  });
}
function renderDaily(){
  $("#tab-daily").innerHTML=dailyFiltersHTML()+'<div class="batch-grid">'+dailySorted().map(bcardHTML).join("")+'</div>';
  bindDailySort();
}

/* ---------- library ---------- */
function libFiltered(){
  const f=state.lib;let P=DATA.papers.filter(p=>f.nonxr||isXR(p));
  if(f.q){const q=f.q.toLowerCase();P=P.filter(p=>(p.title_zh+" "+p.title+" "+p.id+" "+p.track).toLowerCase().includes(q));}
  if(f.track)P=P.filter(p=>p.track===f.track);
  if(f.grade)P=P.filter(p=>p.grade===f.grade);
  if(f.ev)P=P.filter(p=>p.evidence===f.ev);
  if(f.batch)P=P.filter(p=>p.batch===f.batch);
  if(f.top10)P=P.filter(p=>p.top10);
  if(f.flag)P=P.filter(p=>p.flags&&p.flags.length);
  const s=f.sort;
  P=P.slice().sort((a,b)=>s==="value"?b.value-a.value:s==="date"?(b.date>a.date?1:-1):(a.id<b.id?-1:1));
  return P;
}
function renderLibrary(){
  const opts=(arr,all,cur)=>'<option value="">'+all+'</option>'+arr.map(v=>'<option'+(cur===v?" selected":"")+'>'+esc(v)+'</option>').join("");
  const tracks=Object.keys(DATA.facets.tracks),grades=["S","A","B","C"],evs=["FULL","PARTIAL","ABSTRACT_ONLY"],batches=DATA.facets.batches;
  const f=state.lib;
  $("#tab-library").innerHTML=
   '<div class="filters">'+
   '<input type="text" id="libQ" placeholder="搜索题名 / arXiv ID / 赛道…" value="'+esc(f.q)+'">'+
   '<select id="libTrack">'+opts(tracks,"全部赛道",f.track)+'</select>'+
   '<select id="libGrade">'+opts(grades,"全部等级",f.grade)+'</select>'+
   '<select id="libEv">'+opts(evs,"全部证据",f.ev)+'</select>'+
   '<select id="libBatch"><option value="">全部批次</option>'+DATA.facets.batches.map(b=>'<option value="'+esc(b.key)+'"'+(f.batch===b.key?" selected":"")+'>'+esc(b.label)+'（'+b.n+'）</option>').join("")+'</select>'+
   '<select id="libSort"><option value="value"'+(f.sort==="value"?" selected":"")+'>按加权分</option>'+
   '<option value="date"'+(f.sort==="date"?" selected":"")+'>按日期</option>'+
   '<option value="id"'+(f.sort==="id"?" selected":"")+'>按 ID</option></select>'+
   '<label><input type="checkbox" id="libTop10"'+(f.top10?" checked":"")+'> 仅 Top10</label>'+
   '<label><input type="checkbox" id="libFlag"'+(f.flag?" checked":"")+'> 仅带警示</label>'+
   '<label><input type="checkbox" id="libNonXR"'+(f.nonxr?" checked":"")+'> 含非 XR</label>'+
   '<span class="count" id="libCount"></span></div>'+
   '<div class="tw"><table class="tb"><thead><tr><th>ID</th><th>中文题名</th><th>赛道</th><th>档</th><th>加权</th><th>七维</th><th>批次</th><th>证据</th><th>Top10</th></tr></thead>'+
   '<tbody id="libBody"></tbody></table></div>';
  const bind=(id,key,ev)=>{const el=$("#"+id);if(!el)return;el.addEventListener(ev||"input",()=>{f[key]=el.type==="checkbox"?el.checked:el.value;renderLibBody();});};
  bind("libQ","q");bind("libTrack","track","change");bind("libGrade","grade","change");bind("libEv","ev","change");
  bind("libBatch","batch","change");bind("libSort","sort","change");bind("libTop10","top10","change");
  bind("libFlag","flag","change");bind("libNonXR","nonxr","change");
  renderLibBody();
}
function renderLibBody(){
  const P=libFiltered();
  $("#libCount").textContent="共 "+P.length+" 篇";
  $("#libBody").innerHTML=P.map((p,i)=>{
    const noteIdx=DATA.noteIndex[p.id];
    return '<tr class="row" data-pid="'+p.id+'"><td class="mono">'+p.id+'</td>'+
     '<td><div class="tt">'+esc(p.title_zh)+'</div><div class="tt2">'+esc(p.title)+'</div></td>'+
     '<td>'+trackChip(p.track)+'</td><td>'+gradeChip(p.grade)+'</td>'+
     '<td class="mono" style="color:#fff;font-weight:650">'+fmt(p.value)+'</td><td>'+miniBars(p.scores)+'</td>'+
     '<td class="tt2">'+esc(p.batchLabel)+'</td><td>'+evChip(p.evidence)+'</td>'+
     '<td>'+(p.top10?'<span class="chip top10">TOP10</span>':"")+(p.flags&&p.flags.length?' <span class="chip warn" title="'+esc(p.flags.join("；"))+'">⚠️</span>':"")+'</td></tr>'+
     '<tr class="detail" data-d="'+p.id+'" hidden><td colspan="9">'+libDetail(p,noteIdx)+'</td></tr>';
  }).join("");
}
function libDetail(p,noteIdx){
  const flagHtml=(p.flags&&p.flags.length)?'<div class="banner warn">⚠️ 警示：'+p.flags.map(esc).join("；")+'</div>':"";
  const sc=DIMS.map(d=>'<div class="bar-row" style="margin:4px 0"><span class="lb" style="width:132px">'+d.k+' · '+d.zh+'</span>'+
    '<div class="bar-track"><div class="bar-fill" style="width:'+(p.scores[d.k]/5*100)+'%;background:'+GRADE_COLOR[p.grade]+'"></div></div>'+
    '<span class="val" style="width:120px">'+p.scores[d.k]+' / 5 · 权重 '+d.w.toFixed(2)+'</span></div>').join("");
  const btns='<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">'+
    '<a class="btn" href="https://arxiv.org/abs/'+p.id+'" target="_blank">arXiv 原文</a>'+
    (noteIdx!=null?'<button class="btn primary" data-gonote="'+noteIdx+'">📖 查看原子笔记</button>':
      '<span class="tt2">（无原子笔记，证据等级：'+esc(p.evidence)+'）</span>')+'</div>';
  return '<div style="display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start">'+
    '<div>'+radarSVG(p.scores,230,GRADE_COLOR[p.grade])+'</div>'+
    '<div style="flex:1;min-width:300px">'+
    '<div style="font-size:14.5px;font-weight:650;margin-bottom:4px">'+esc(p.title_zh)+'</div>'+
    '<div class="tt2" style="margin-bottom:8px">'+esc(p.title)+'</div>'+
    '<div class="meta" style="display:flex;flex-wrap:wrap;gap:6px">'+trackChip(p.track)+gradeChip(p.grade)+evChip(p.evidence)+
      '<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">提交日 '+p.date+'</span>'+
      '<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">批次 '+esc(p.batchLabel)+'</span>'+
      '<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">抓取 '+esc(p.level)+'</span>'+
      (p.top10?'<span class="chip top10">TOP10</span>':"")+'</div>'+flagHtml+sc+btns+'</div></div>';
}
document.addEventListener("click",e=>{
  const row=e.target.closest("tr.row[data-pid]");
  if(row){
    const d=document.querySelector('tr.detail[data-d="'+row.dataset.pid+'"]');
    if(d)d.hidden=!d.hidden;
    return;
  }
  const gn=e.target.closest("[data-gonote]");
  if(gn){
    state.tab="notes";state.note.sel=+gn.dataset.gonote;state.note.q="";state.note.track="";
    document.querySelectorAll("nav.tabs button").forEach(x=>x.classList.toggle("active",x.dataset.tab==="notes"));
    document.querySelectorAll("section.tab").forEach(s=>s.classList.toggle("active",s.id==="tab-notes"));
    renderNotes();
  }
});

/* ---------- 7 dim table ---------- */
function renderDim7(){
  const f=state.dim;
  const tracks=Object.keys(DATA.facets.tracks),grades=["S","A","B","C"],batches=DATA.facets.batches;
  $("#tab-dim7").innerHTML=
   '<div class="filters">'+
   '<input type="text" id="dimQ" placeholder="搜索题名 / ID…" value="'+esc(f.q)+'">'+
   '<select id="dimTrack">'+'<option value="">全部赛道</option>'+tracks.map(v=>'<option'+(f.track===v?" selected":"")+'>'+esc(v)+'</option>').join("")+'</select>'+
   '<select id="dimGrade">'+'<option value="">全部等级</option>'+grades.map(v=>'<option'+(f.grade===v?" selected":"")+'>'+v+'</option>').join("")+'</select>'+
   '<select id="dimBatch"><option value="">全部批次</option>'+DATA.facets.batches.map(b=>'<option value="'+esc(b.key)+'"'+(f.batch===b.key?" selected":"")+'>'+esc(b.label)+'（'+b.n+'）</option>').join("")+'</select>'+
   '<label><input type="checkbox" id="dimNonXR"'+(f.nonxr?" checked":"")+'> 含非 XR</label>'+
   '<span class="count" id="dimCount"></span></div>'+
   '<div class="axis-legend">'+DIMS.map(d=>'<span><b>'+d.k+'</b> '+d.zh+' · 权重 '+d.w.toFixed(2)+'</span>').join("")+'</div>'+
   '<div class="tw"><table class="tb"><thead><tr><th>#</th><th>ID</th><th>中文题名</th><th>赛道</th><th>档</th><th>加权</th>'+
   DIMS.map(d=>'<th title="'+d.zh+'">'+d.k+'</th>').join("")+'<th>批次</th><th>证据</th></tr></thead><tbody id="dimBody"></tbody></table></div>';
  const bind=(id,key)=>{const el=$("#"+id);el.addEventListener(el.tagName==="SELECT"?"change":"input",()=>{f[key]=el.type==="checkbox"?el.checked:el.value;renderDimBody();});};
  bind("dimQ","q");bind("dimTrack","track");bind("dimGrade","grade");bind("dimBatch","batch");bind("dimNonXR","nonxr");
  renderDimBody();
}
function renderDimBody(){
  const f=state.dim;let P=DATA.papers.filter(p=>f.nonxr||isXR(p));
  if(f.q){const q=f.q.toLowerCase();P=P.filter(p=>(p.title_zh+" "+p.title+" "+p.id).toLowerCase().includes(q));}
  if(f.track)P=P.filter(p=>p.track===f.track);
  if(f.grade)P=P.filter(p=>p.grade===f.grade);
  if(f.batch)P=P.filter(p=>p.batch===f.batch);
  P=P.slice().sort((a,b)=>b.value-a.value||a.id.localeCompare(b.id));
  $("#dimCount").textContent="共 "+P.length+" 篇";
  $("#dimBody").innerHTML=P.map((p,i)=>
    '<tr><td class="tt2">'+(i+1)+'</td><td class="mono">'+p.id+'</td>'+
    '<td><div class="tt">'+esc(p.title_zh)+'</div></td><td>'+trackChip(p.track)+'</td><td>'+gradeChip(p.grade)+'</td>'+
    '<td class="mono" style="color:#fff;font-weight:650">'+fmt(p.value)+'</td>'+
    DIMS.map(d=>'<td>'+scoreCell(p.scores[d.k])+'</td>').join("")+
    '<td class="tt2">'+esc(p.batchLabel)+'</td><td>'+evChip(p.evidence)+'</td></tr>').join("");
}

/* ---------- notes ---------- */
function mdLite(src){
  const lines=String(src).split("\n");let out=[],i=0;
  const inline=s=>esc(s).replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/`([^`]+)`/g,"<code>$1</code>");
  while(i<lines.length){
    const ln=lines[i];
    if(/^\s*$/.test(ln)){i++;continue;}
    if(/^#{3,6}\s+/.test(ln)){
      out.push('<div class="subh">'+inline(ln.replace(/^#{3,6}\s+/,""))+'</div>');i++;continue;
    }
    if(/^\s*\|/.test(ln)){
      const rows=[];
      while(i<lines.length&&/^\s*\|/.test(lines[i])){rows.push(lines[i]);i++;}
      const cells=r=>r.trim().replace(/^\|/,"").replace(/\|$/,"").split("|").map(c=>c.trim());
      const head=cells(rows[0]);
      const isSep=rows[1]&&/^[\s|:-]+$/.test(rows[1]);
      const body=isSep?rows.slice(2):rows.slice(1);
      let t="<table><tr>"+head.map(c=>"<th>"+inline(c)+"</th>").join("")+"</tr>";
      body.forEach(r=>{t+="<tr>"+cells(r).map(c=>"<td>"+inline(c)+"</td>").join("")+"</tr>";});
      out.push(t+"</table>");continue;
    }
    if(/^\s*-\s+/.test(ln)){
      const items=[];
      while(i<lines.length&&/^\s*-\s+/.test(lines[i])){items.push(lines[i].replace(/^\s*-\s+/,""));i++;}
      out.push("<ul>"+items.map(s=>"<li>"+inline(s)+"</li>").join("")+"</ul>");continue;
    }
    const para=[];
    while(i<lines.length&&!/^\s*$/.test(lines[i])&&!/^\s*-\s+/.test(lines[i])&&!/^\s*\|/.test(lines[i])){para.push(lines[i]);i++;}
    out.push("<p>"+inline(para.join(" "))+"</p>");
  }
  return out.join("");
}
function renderNotes(){
  const n=state.note;
  const tracks=Object.keys(DATA.facets.noteTracks);
  const list=DATA.notes.map((nt,i)=>({nt,i})).filter(o=>{
    if(n.track&&o.nt.track!==n.track)return false;
    if(n.q){const q=n.q.toLowerCase();
      return ((o.nt.title_zh||"")+" "+(o.nt.title||"")+" "+o.nt.id+" "+(o.nt.tags||[]).join(" ")).toLowerCase().includes(q);}
    return true;
  });
  $("#tab-notes").innerHTML=
   '<div class="notes-wrap"><div class="nlist"><div class="nhead">'+
   '<input type="text" id="noteQ" placeholder="搜索笔记 / 标签…" value="'+esc(n.q)+'" style="background:#0a0f1c;border:1px solid var(--border2);color:var(--text);border-radius:7px;padding:7px 10px;font-size:12.8px;outline:none;width:100%">'+
   '<select id="noteTrack" style="background:#0a0f1c;border:1px solid var(--border2);color:var(--text);border-radius:7px;padding:6px 9px;font-size:12.5px;outline:none;width:100%">'+
   '<option value="">全部赛道（'+DATA.notes.length+'）</option>'+
   tracks.map(t=>'<option'+(n.track===t?" selected":"")+'>'+esc(t)+'（'+DATA.facets.noteTracks[t]+'）</option>').join("")+'</select>'+
   '<span class="tt2">命中 '+list.length+' 篇</span></div>'+
   '<div class="nitems" id="noteItems">'+
   (list.length?list.map(o=>{const nt=o.nt;
     return '<div class="nitem'+(o.i===n.sel?" sel":"")+'" data-ni="'+o.i+'">'+
      '<div class="nt">'+esc(nt.title_zh||nt.title)+'</div>'+
      '<div class="nm"><span class="chip '+nt.grade+'" style="transform:scale(.82)">'+nt.grade+'</span>'+
      '<span class="mono">'+nt.id+'</span><span>'+fmt(nt.value)+'</span>'+
      (nt.flags&&nt.flags.length?'<span class="chip warn" style="transform:scale(.82)">⚠️</span>':"")+'</div></div>';}).join(""):
     '<div class="placeholder">无匹配笔记</div>')+
   '</div></div><div class="ndetail" id="noteDetail">'+
   (n.sel!=null&&DATA.notes[n.sel]?noteDetail(DATA.notes[n.sel]):'<div class="placeholder">← 从左侧选择一篇原子笔记开始精读<br><span style="font-size:12px">共 '+DATA.notes.length+' 篇结构化笔记（一句话结论 / 方法详解 / 实验与结果 / 创新点 / 局限 / 复现性）</span></div>')+
   '</div></div>';
  $("#noteQ").addEventListener("input",e=>{n.q=e.target.value;renderNotes();});
  $("#noteTrack").addEventListener("change",e=>{n.track=e.target.value;renderNotes();});
}
function noteDetail(nt){
  const p=DATA.paperIndex[nt.id];
  const flagHtml=(nt.flags&&nt.flags.length)?'<div class="banner warn">⚠️ 路线/局限警示（索引进库标记）：'+nt.flags.map(esc).join("；")+'</div>':"";
  const meta='<div class="meta">'+gradeChip(nt.grade)+
    '<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">加权 '+fmt(nt.value)+'</span>'+
    trackChip(nt.track)+evChip(nt.evidence)+
    '<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">提交日 '+nt.date+'</span>'+
    '<span class="chip" style="background:#0d1424;color:#98a5c0;border-color:#263353">批次 '+esc(nt.batchLabel)+'</span>'+
    (nt.tags||[]).map(t=>'<span class="chip" style="background:rgba(124,108,255,.1);color:#b7adff;border-color:rgba(124,108,255,.3)">'+esc(t)+'</span>').join("")+'</div>';
  const secs=(nt.sections||[]).map(s=>'<div class="sec"><h4>'+esc(s.h)+'</h4><div class="bd">'+mdLite(s.body)+'</div></div>').join("");
  const head='<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:flex-start">'+
    '<div style="flex:1;min-width:280px"><h2>'+esc(nt.title_zh||nt.title)+'</h2>'+
    '<div class="tt2" style="margin-top:2px">'+esc(nt.title)+' · <span class="mono">'+nt.id+'</span></div>'+meta+'</div>'+
    '<div style="display:flex;flex-direction:column;gap:6px">'+
    '<a class="btn" href="https://arxiv.org/abs/'+nt.id+'" target="_blank">arXiv 原文</a>'+
    (p&&p.top10?'<span class="chip top10">TOP10 入选</span>':"")+
    (nt.file?'<a class="btn" href="'+nt.file+'" target="_blank">原笔记 .md</a>':"")+'</div></div>';
  return head+flagHtml+secs;
}
document.addEventListener("click",e=>{
  const it=e.target.closest("[data-ni]");
  if(it){state.note.sel=+it.dataset.ni;
    document.querySelectorAll(".nitem").forEach(x=>x.classList.toggle("sel",x===it));
    $("#noteDetail").innerHTML=noteDetail(DATA.notes[state.note.sel]);}
});
document.addEventListener("click",e=>{
  const ex=e.target.closest("[data-exp]");
  if(ex){
    const box=document.getElementById("pf-"+ex.dataset.exp);
    if(box){
      box.hidden=!box.hidden;
      ex.textContent=box.hidden?(ex.dataset.label||"展开 ▾"):"收起 ▴";
    }
  }
});

/* ---------- daily: 排序 / 隐藏 / info ---------- */
document.addEventListener("click",e=>{
  const eye=e.target.closest("[data-hide]");
  if(eye){
    const k=eye.dataset.hide;
    if(state.daily.hidden[k])delete state.daily.hidden[k];else state.daily.hidden[k]=1;
    saveDailyHidden();
    const b=DATA.batches.find(x=>x.key===k);
    const card=eye.closest(".bcard");
    if(b&&card)card.outerHTML=bcardHTML(b); // 原地替换，保留其他卡片的展开状态
    refreshDailyChrome();
    return;
  }
  const sa=e.target.closest("[data-showall]");
  if(sa){state.daily.hidden={};saveDailyHidden();renderDaily();return;}
  const ib=e.target.closest("[data-info]");
  if(ib){
    const pop=document.getElementById("info-"+ib.dataset.info);
    document.querySelectorAll(".info-pop.show").forEach(p=>{if(p!==pop)p.classList.remove("show")});
    if(pop)pop.classList.toggle("show");
    e.stopPropagation();return;
  }
  if(!e.target.closest(".info-wrap"))document.querySelectorAll(".info-pop.show").forEach(p=>p.classList.remove("show"));
});

/* ---------- init ---------- */
$("#foot").innerHTML="数据源：arXiv RSS/API 双通道抓取 → 关键词+判读筛选 → 7 维加权评分 → Top10 全文精读 → 原子笔记 + MOC 知识库。"+
  '本页由 <code>scripts/build_frontend.py</code> 从 <code>papers/library/registry.jsonl</code>（'+DATA.papers.length+' 篇）与 <code>papers/notes/</code>（'+DATA.notes.length+' 篇）自动生成 · '+esc(DATA.meta.generated)+'。';
renderOverview();
