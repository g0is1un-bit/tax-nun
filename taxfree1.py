import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="부가가치세 면세/과세 탐색기", layout="centered")

HTML = r"""
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
const DATA=[{"id":"r001","name":"쌀(미가공)","keywords":["백미","현미","벼"],"category":"농수축산물(미가공)","processed":false,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},{"id":"r002","name":"생채소","keywords":["배추","상추","오이","토마토"],"category":"농수축산물(미가공)","processed":false,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},{"id":"r003","name":"생과일","keywords":["사과","배","포도","감귤"],"category":"농수축산물(미가공)","processed":false,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},{"id":"r004","name":"생선]()

