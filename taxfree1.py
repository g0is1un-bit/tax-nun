import json
import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="부가가치세 면세/과세 탐색기", layout="centered")

DATA = [
    {"id":"r001","name":"쌀(미가공)","keywords":["백미","현미","벼"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},
    {"id":"r002","name":"생채소","keywords":["배추","상추","오이","토마토"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},
    {"id":"r003","name":"생과일","keywords":["사과","배","포도","감귤"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},
    {"id":"r004","name":"생선·어패류(손질만)","keywords":["생선","활어","손질생선"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 수산물(단순 손질) 면세 취지"},
    # ... 필요시 계속 추가 ...
]

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>부가가치세 면세/과세 탐색기 (HTML)</title>
<style>
  body{margin:0;background:linear-gradient(#fff,#f8fafc);font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,"Noto Sans KR","Malgun Gothic",sans-serif;color:#0f172a}
  .container{max-width:1000px;margin:0 auto;padding:24px}
  h1{font-weight:700;font-size:24px;margin:0 0 8px}
  .sub{color:#64748b;font-size:14px}
  .row{display:flex;gap:8px;align-items:center;margin-top:12px}
  input[type="text"]{flex:1;padding:10px 12px;border:1px solid #e5e7eb;border-radius:10px}
  button.btn{padding:8px 12px;border:1px solid #e5e7eb;border-radius:999px;background:#fff;cursor:pointer}
  .card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:16px}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chip{border:1px solid #e5e7eb;border-radius:999px;padding:4px 10px;font-size:12px;background:#fff;cursor:pointer}
  .chip.active{background:#0f172a;color:#fff;border-color:#0f172a}
  .muted{color:#64748b;font-size:12px}
  .grid{display:grid;grid-template-columns:1fr;gap:10px;margin-top:16px}
  .badge{font-size:11px;padding:3px 8px;border-radius:999px;background:#eef2f7;border:1px solid #e5e7eb;display:inline-block}
  .label{font-size:11px;padding:3px 8px;border-radius:999px;display:inline-block}
  .exempt{background:#d1fae5;color:#065f46}.taxable{background:#fee2e2;color:#991b1b}.zero{background:#e0f2fe;color:#075985}
</style>
</head>
<body>
<div class="container">
  <h1>부가가치세 면세/과세 탐색기 <span class="sub">(HTML)</span></h1>

  <div class="row">
    <input id="q" type="text" placeholder="예: 쌀, 생선, 김치, 라면, 우유…"/>
    <button class="btn" onclick="q.value=''; render()">지우기</button>
  </div>

  <div class="card" style="margin-top:10px">
    <div class="row" style="flex-wrap:wrap;gap:10px">
      <label><input type="checkbox" id="showExempt" checked> 면세</label>
      <label><input type="checkbox" id="showTaxable" checked> 과세</label>
      <label><input type="checkbox" id="showZero" checked> 영세율 라벨</label>
      <span class="muted">카테고리:</span> <div id="cats" class="chips"></div>
      <span class="muted">가공여부:</span> <div id="proc" class="chips"></div>
    </div>
  </div>

  <div id="list" class="grid"></div>
  <div class="muted" style="margin-top:14px">
    ※ 일반 원칙: 미가공 식용 농수축산물 = 면세 / 가공되면 통상 과세 / 영세율은 거래유형에 따름
  </div>
</div>

<script>
const CATEGORIES=["농수축산물(미가공)","식품(가공)","음료·주류","생활필수품","의약·의약외품","미용·사치성","기타"];
const DATA=__DATA__;

const state={q:"",showExempt:true,showTaxable:true,showZero:true,cat:"전체",proc:"all"};
const cats=document.getElementById('cats'), proc=document.getElementById('proc'),
      list=document.getElementById('list'), q=document.getElementById('q'),
      ex=document.getElementById('showExempt'), tx=document.getElementById('showTaxable'), zr=document.getElementById('showZero');

function chip(text,active){const el=document.createElement('button');el.className='chip'+(active?' active':'');el.textContent=text;return el;}
function normalize(s){return s.normalize('NFKD').toLowerCase().replace(/\s+/g,'');}
function scoreRow(row,q){const n=normalize(q);if(!n)return 0;let s=0;for(const f of [row.name,...(row.keywords||[])].map(normalize)){if(f.includes(n))s+=5;} if(row.processed && /가공|볶|정제|조리|통조림|즉석/.test(q)) s+=1; return s;}

function renderCats(){cats.innerHTML='';const all=chip('전체',state.cat==='전체');all.onclick=()=>{state.cat='전체';render();};cats.appendChild(all);
  for(const c of CATEGORIES){const el=chip(c,state.cat===c);el.onclick=()=>{state.cat=c;render();};cats.appendChild(el);} }
function renderProc(){proc.innerHTML='';for(const [v,l] of [['all','전체'],['unprocessed','미가공만'],['processed','가공만']]){const el=chip(l,state.proc===v);el.onclick=()=>{state.proc=v;render();};proc.appendChild(el);} }
function badge(s){const span=document.createElement('span');span.className='label '+(s==='면세'?'exempt':s==='과세'?'taxable':s==='영세율'?'zero':'');span.textContent=s;return span;}

function renderList(){ list.innerHTML='';
  const out=DATA.map(row=>({row,score:scoreRow(row,state.q)})).filter(({row})=>{
    if(!state.showExempt&&row.status==='면세')return false;
    if(!state.showTaxable&&row.status==='과세')return false;
    if(!state.showZero&&row.status==='영세율')return false;
    if(state.cat!=='전체'&&row.category!==state.cat)return false;
    if(state.proc==='processed'&&!row.processed)return false;
    if(state.proc==='unprocessed'&&row.processed)return false;
    return true;}).sort((a,b)=>b.score-a.score||a.row.name.localeCompare(b.row.name)).slice(0,100).map(v=>v.row);

  if(!out.length){const d=document.createElement('div');d.className='muted card';d.textContent='검색 결과가 없습니다. 철자/동의어(예: 달걀→계란)를 시도해 보세요.';list.appendChild(d);return;}
  for(const r of out){const card=document.createElement('div');card.className='card';
    const title=document.createElement('div');title.style.display='flex';title.style.gap='8px';title.style.alignItems='center';
    const h3=document.createElement('div');h3.style.fontWeight='600';h3.textContent=r.name;title.appendChild(h3);title.appendChild(badge(r.status));card.appendChild(title);
    const meta=document.createElement('div');meta.className='muted';meta.style.marginTop='6px';
    const cat=document.createElement('span');cat.className='badge';cat.textContent=r.category;meta.appendChild(cat);
    meta.append(' · ', r.processed?'가공':'미가공');
    if(r.keywords?.length){meta.append(' · 키워드: ', r.keywords.slice(0,4).join(', '), r.keywords.length>4?'…':'');}
    card.appendChild(meta);
    if(r.basis){const det=document.createElement('details');det.style.marginTop='8px';const sum=document.createElement('summary');sum.textContent='근거(메모)';det.append(sum);const d=document.createElement('div');d.textContent=r.basis;d.style.marginTop='4px';det.append(d);card.appendChild(det);}
    list.appendChild(card);}
}

function render(){state.q=q.value;state.showExempt=ex.checked;state.showTaxable=tx.checked;state.showZero=zr.checked;renderCats();renderProc();renderList();}
q.addEventListener('input',render);ex.addEventListener('change',render);tx.addEventListener('change',render);zr.addEventListener('change',render);
window.addEventListener('DOMContentLoaded',render);
</script>
</body></html>
"""



