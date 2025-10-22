# app.py
import streamlit as st
from typing import List, Dict
import unicodedata

st.set_page_config(page_title="부가가치세 면세/과세 탐색기", layout="centered")

# -----------------------------
# 데이터 (보수적 스타터 목록)
# -----------------------------
DATA: List[Dict] = [
    {"id":"r001","name":"쌀(미가공)","keywords":["백미","현미","벼"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},
    {"id":"r002","name":"생채소","keywords":["배추","상추","오이","토마토"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},
    {"id":"r003","name":"생과일","keywords":["사과","배","포도","감귤"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 일반적으로 면세"},
    {"id":"r004","name":"생선·어패류(손질만)","keywords":["생선","활어","손질생선"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 수산물(단순 손질) 면세 취지"},
    {"id":"r005","name":"계란(신선)","keywords":["달걀","란"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 축산물 면세 취지"},
    {"id":"r006","name":"원유(생우유)","keywords":["생유","원유"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 축산물(원유) 면세 취지"},
    {"id":"r007","name":"김치(가공)","keywords":["절임배추"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공식품은 원칙적으로 과세"},
    {"id":"r008","name":"햄·소시지","keywords":["육가공품"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공식품(육가공) 과세"},
    {"id":"r009","name":"빵·과자","keywords":["제과","베이커리"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공식품 과세"},
    {"id":"r010","name":"두부","keywords":["콩두부"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공식품 과세(원재료는 면세라도)"},
    {"id":"r011","name":"우유(살균/멸균)","keywords":["흰우유"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공/처리 식품 과세"},
    {"id":"r012","name":"요구르트·치즈","keywords":["유가공"],"category":"식품(가공)","processed":True,"status":"과세","basis":"유가공식품 과세"},
    {"id":"r013","name":"설탕·소금(정제)","keywords":["백설탕","정제염"],"category":"식품(가공)","processed":True,"status":"과세","basis":"정제/가공식품 과세(일부 예외 존재 가능)"},
    {"id":"r014","name":"라면·즉석식품","keywords":["컵라면","레토르트"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공식품 과세"},
    {"id":"r015","name":"음료(탄산·과즙·커피)","keywords":["음료수","주스"],"category":"음료·주류","processed":True,"status":"과세","basis":"음료류 과세"},
    {"id":"r016","name":"주류(맥주·소주 등)","keywords":["알코올"],"category":"음료·주류","processed":True,"status":"과세","basis":"주류 과세"},
    {"id":"r017","name":"생수(병입)","keywords":["먹는샘물"],"category":"음료·주류","processed":True,"status":"과세","basis":"병입·처리된 음료 과세"},
    {"id":"r018","name":"의약품(일반)","keywords":["해열제","감기약"],"category":"의약·의약외품","processed":True,"status":"과세","basis":"일반 의약품은 통상 과세(개별 예외 확인 필요)"},
    {"id":"r019","name":"의약외품(마스크 등)","keywords":["의약외품"],"category":"의약·의약외품","processed":True,"status":"과세","basis":"의약외품 과세(의료용역 면세와 구분)"},
    {"id":"r020","name":"화장품","keywords":["스킨케어"],"category":"미용·사치성","processed":True,"status":"과세","basis":"미용·사치성 재화 과세"},
    {"id":"r021","name":"금·귀금속(일반거래)","keywords":["귀금속"],"category":"미용·사치성","processed":True,"status":"과세","basis":"일반 내수거래 과세(특례/영세율은 거래유형 참조)"},
    {"id":"r022","name":"생화(절화)","keywords":["꽃"],"category":"생활필수품","processed":False,"status":"과세","basis":"재화 일반 과세(농산물 취급 형태별 예외 가능)"},
    {"id":"r023","name":"미가공 견과류","keywords":["볶지않은 견과"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 식용 농산물 면세 취지"},
    {"id":"r024","name":"볶은 견과류","keywords":["구운 아몬드"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공(볶음) 처리 과세"},
    {"id":"r025","name":"통조림(과일/생선)","keywords":["통조림"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공/보존 처리 과세"},
    {"id":"r026","name":"냉동만두","keywords":["만두"],"category":"식품(가공)","processed":True,"status":"과세","basis":"가공식품 과세"},
    {"id":"r027","name":"도시락/즉석조리식","keywords":["편의점 도시락"],"category":"식품(가공)","processed":True,"status":"과세","basis":"조리/가공식품 과세"},
    {"id":"r028","name":"곡물가루(정제)","keywords":["밀가루","쌀가루"],"category":"식품(가공)","processed":True,"status":"과세","basis":"제분 등 가공 처리 과세(특정 예외 확인)"},
    {"id":"r029","name":"건조과일(무가당)","keywords":["말린 과일"],"category":"식품(가공)","processed":True,"status":"과세","basis":"건조·가공 처리 과세(일부 예외 가능)"},
    {"id":"r030","name":"도축 전 가축","keywords":["생축"],"category":"농수축산물(미가공)","processed":False,"status":"면세","basis":"미가공 축산물 면세 취지"},
]

CATEGORIES = ["전체","농수축산물(미가공)","식품(가공)","음료·주류","생활필수품","의약·의약외품","미용·사치성","기타"]

# -----------------------------
# 유틸
# -----------------------------
def normalize(s: str) -> str:
    """공백 제거 + 소문자 + NFKD 정규화로 간단 퍼지 검색 보정"""
    return unicodedata.normalize("NFKD", s).lower().replace(" ", "")

def score_row(row: Dict, q: str) -> int:
    nQ = normalize(q)
    if not nQ:
        return 0
    score = 0
    fields = [row["name"], *row.get("keywords", [])]
    for f in fields:
        if normalize(f).find(nQ) >= 0:
            score += 5
    # '가공' 관련 키워드가 쿼리에 있으면 가공 항목에 소폭 가중치
    if row.get("processed") and any(k in q for k in ["가공","볶","정제","조리","통조림","즉석"]):
        score += 1
    return score

def badge(text: str, tone: str) -> str:
    # 간단한 뱃지 스타일 (Streamlit HTML 허용)
    bg, fg = {
        "면세": ("#d1fae5","#065f46"),
        "과세": ("#fee2e2","#991b1b"),
        "영세율": ("#e0f2fe","#075985"),
        "기본": ("#eef2f7","#475569"),
    }.get(tone, ("#eef2f7","#475569"))
    return f"<span style='display:inline-block;padding:3px 8px;border-radius:999px;background:{bg};color:{fg};font-size:11px;border:1px solid #e5e7eb;'>{text}</span>"

# -----------------------------
# 사이드바 & 헤더
# -----------------------------
st.title("부가가치세 면세/과세 탐색기")
st.caption("세법 비전문가도 쉽게 품목의 면세/과세 여부를 찾아볼 수 있도록 만든 간단 검색기 (데모)")

with st.sidebar:
    st.subheader("필터")
    q = st.text_input("검색어", placeholder="예: 쌀, 생선, 김치, 라면, 우유…")
    show_exempt = st.checkbox("면세 보기", value=True)
    show_taxable = st.checkbox("과세 보기", value=True)
    show_zero = st.checkbox("영세율 라벨 보이기", value=True)
    cat = st.selectbox("카테고리", CATEGORIES, index=0)
    proc = st.radio("가공여부", ["전체","미가공만","가공만"], horizontal=True)

# -----------------------------
# 필터링 + 정렬
# -----------------------------
filtered = []
for row in DATA:
    if not show_exempt and row["status"] == "면세":
        continue
    if not show_taxable and row["status"] == "과세":
        continue
    if not show_zero and row["status"] == "영세율":
        continue
    if cat != "전체" and row["category"] != cat:
        continue
    if proc == "가공만" and not row["processed"]:
        continue
    if proc == "미가공만" and row["processed"]:
        continue
    filtered.append({"row": row, "score": score_row(row, q or "")})

filtered.sort(key=lambda x: (-x["score"], x["row"]["name"]))
results = [x["row"] for x in filtered][:100]

# -----------------------------
# 결과 표시
# -----------------------------
if not results:
    st.info("검색 결과가 없습니다. 철자/동의어(예: 달걀→계란)를 시도해 보세요.")
else:
    for r in results:
        with st.container():
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"### {r['name']}", unsafe_allow_html=True)
                # 상태 뱃지
                tone = r["status"] if r["status"] in ["면세","과세","영세율"] else "기본"
                st.markdown(badge(r["status"], tone), unsafe_allow_html=True)
                # 메타 정보
                meta = f"{badge(r['category'], '기본')} · {'가공' if r['processed'] else '미가공'}"
                if r.get("keywords"):
                    k = ", ".join(r["keywords"][:4])
                    if len(r["keywords"]) > 4:
                        k += "…"
                    meta += f" · 키워드: {k}"
                st.markdown(meta, unsafe_allow_html=True)
                # 근거(메모)
                if r.get("basis"):
                    with st.expander("근거(메모)"):
                        st.write(r["basis"])
            with col2:
                st.write("")

# -----------------------------
# 안내 문구
# -----------------------------
st.divider()
st.caption(
    "※ 일반 원칙 예시: 미가공(현 상태) 식용 농·임·축·수산물은 통상 면세, "
    "가공(세척·절단·절임·가열·건조·정제·제분 등)되면 일반적으로 과세. "
    "영세율은 품목 고정이 아니라 **거래유형(수출 등)**에 따라 적용되는 별도 개념입니다.\n\n"
    "본 도구는 학습/내부 안내용 예시이며, 실제 과세 판단은 거래 형태·가공도·HS코드·개별 고시/예규 등에 따라 달라질 수 있으니 "
    "반드시 최신 법령과 국세청 유권해석을 확인하세요."
)




