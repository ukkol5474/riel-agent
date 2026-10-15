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
    st.header("🔑 API 설정")
    dart_key_input = st.text_input("DART API Key", type="password", placeholder="다트 오픈API 키 입력")
    openai_key_input = st.text_input("OpenAI API Key", type="password", placeholder="OpenAI API 키 입력")
    
    st.markdown("---")
    st.markdown("### 📌 관심종목 및 포트폴리오 설정")
    all_stocks = ["삼성전자", "유진테크", "SK하이닉스", "헥토이노베이션", "세아홀딩스", "더블유게임즈"]
    selected_watchlist = st.multiselect("관심종목 선택", all_stocks, default=["삼성전자", "유진테크", "SK하이닉스"])
    
    st.markdown("---")
    st.markdown("### 🚨 리스크 알람 조건 설정")
    alert_threshold = st.slider("손실률 알람 기준 (%)", min_value=-20, max_value=0, value=-10)
    st.info(f"현재 설정된 알람 기준: 수익률 {alert_threshold}% 이하 시 긴급 경고 활성화")

# API 키 미입력 시 안내
if not openai_key_input:
    st.warning("⚠️ 사이드바에 OpenAI API Key를 입력해주셔야 AI 심층 분석 및 대화 기능이 정상 작동합니다.")

# 3. 포트폴리오 및 밸류에이션 요약 데이터프레임 (관심종목 연동)
watchlist_data = {
    "종목명": selected_watchlist if selected_watchlist else ["삼성전자"],
    "현재가(원)": [65000, 39000, 195000, 42000, 150000, 45000][:len(selected_watchlist or ["삼성전자"])],
    "수익률(%)": [-7.1, -13.3, +8.3, -2.1, +5.0, -11.5][:len(selected_watchlist or ["삼성전자"])],
    "PER": [14.2, 18.5, 22.1, 12.4, 8.9, 15.0][:len(selected_watchlist or ["삼성전자"])],
    "PBR": [1.3, 1.8, 2.5, 1.1, 0.7, 1.2][:len(selected_watchlist or ["삼성전자"])],
    "ROE(%)": [9.5, 11.2, 14.8, 10.2, 12.0, 8.5][:len(selected_watchlist or ["삼성전자"])],
}
df_portfolio = pd.DataFrame(watchlist_data)

# 4. 실시간 알람 체크 기능
triggered_alerts = df_portfolio[df_portfolio["수익률(%)"] <= alert_threshold]
if not triggered_alerts.empty:
    for idx, row in triggered_alerts.iterrows():
        st.error(f"🚨 **[긴급 알람]** 관심종목 **{row['종목명']}**의 수익률이 {row['수익률(%)']}%로 설정된 알람 기준({alert_threshold}%)을 이탈했습니다! 리스크 관리가 필요합니다.")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📊 내 관심종목 및 밸류에이션 요약")
    st.dataframe(df_portfolio, use_container_width=True)

    st.markdown("---")
    st.subheader("🚨 AI 실시간 처분(매도) 1순위 진단")
    
    st.error("⚠️
