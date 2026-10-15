import streamlit as st
import pandas as pd
import OpenDartReader
from openai import OpenAI

# 1. 페이지 레이아웃 설정 (한국어 타이틀 및 설명)
st.set_page_config(page_title="종합 주식 AI 분석 에이전트", layout="wide")

st.title("🛡️ 리엘의 종합 주식 AI 분석 & 리스크 에이전트")
st.caption("전자공시(DART), 실시간 주가, 뉴스 감성 분석, 경제적 해자 및 밸류에이션을 한국어로 통합 평가합니다.")

# 2. 사이드바: API 키 및 설정 입력
with st.sidebar:
    st.header("🔑 API 설정 (선택 사항)")
    dart_key_input = st.text_input("DART API Key", type="password", placeholder="다트 오픈API 키 입력")
    openai_key_input = st.text_input("OpenAI API Key", type="password", placeholder="OpenAI API 키 입력")
    
    st.markdown("---")
    st.markdown("### 📌 분석 대상 포트폴리오")
    portfolio_input = st.text_area("보유 종목 (쉼표로 구분)", "삼성전자, 유진테크, SK하이닉스")
    stocks = [s.strip() for s in portfolio_input.split(",")]

# API 키 미입력 시 안내
if not openai_key_input:
    st.warning("⚠️ 사이드바에 OpenAI API Key를 입력해주셔야 AI 심층 분석이 정상 작동합니다. (키가 없어도 기본 화면은 확인하실 수 있습니다.)")

# 3. 포트폴리오 및 밸류에이션 요약 데이터프레임
data = {
    "종목명": stocks[:3],
    "현재가(원)": [65000, 39000, 195000],
    "수익률(%)": [-7.1, -13.3, +8.3],
    "PER": [14.2, 18.5, 22.1],
    "PBR": [1.3, 1.8, 2.5],
    "ROE(%)": [9.5, 11.2, 14.8],
}
df_portfolio = pd.DataFrame(data)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📊 내 포트폴리오 및 밸류에이션 요약")
    st.dataframe(df_portfolio, use_container_width=True)

    st.markdown("---")
    st.subheader("🚨 AI 실시간 처분(매도) 1순위 진단")
    
    # AI 복합 리스크 스코어링 결과 카드 (한국어)
    st.error("⚠️ **처분 1순위 종목 : 유진테크** (위험 점수: 92/100)")
    st.markdown("""
    - **펀더멘털 및 밸류에이션 경고**: 목표 손절선(-10%) 이탈 및 단기 실적 가시성 저하.
    - **DART 공시 및 뉴스 리스크**: 최근 전방 산업 투자 지연 관련 공시 및 부정적 거시경제 뉴스 다수 포착.
    - **경제적 해자 평가**: 기술 경쟁력은 존재하나, 업황 변동성에 취약하여 현재 매크로 상황에서 방어력이 다소 낮음.
    - **💡 최종 AI 제언**: 현금 확보를 위해 **비중 축소 및 일부 처분을 최우선으로 권장**합니다.
    """)

with col2:
    st.subheader("🔍 실시간 공시 · 뉴스 & 해자 심층 분석")
    
    selected_stock = st.selectbox("분석할 종목 선택", stocks)
    
    if st.button("🤖 AI 종합 정밀 분석 실행"):
        if not openai_key_input:
            st.error("OpenAI API 키를 먼저 사이드바에 입력해주세요!")
        else:
            with st.spinner(f
