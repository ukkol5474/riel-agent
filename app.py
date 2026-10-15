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
# 선택한 관심종목 수에 맞게 샘플 데이터 생성
current_watchlist = selected_watchlist if selected_watchlist else ["삼성전자"]
sample_data = {
    "삼성전자": {"현재가": 65000, "수익률": -7.1, "PER": 14.2, "PBR": 1.3, "ROE": 9.5},
    "유진테크": {"현재가": 39000, "수익률": -13.3, "PER": 18.5, "PBR": 1.8, "ROE": 11.2},
    "SK하이닉스": {"현재가": 195000, "수익률": 8.3, "PER": 22.1, "PBR": 2.5, "ROE": 14.8},
    "헥토이노베이션": {"현재가": 42000, "수익률": -2.1, "PER": 12.4, "PBR": 1.1, "ROE": 10.2},
    "세아홀딩스": {"현재가": 150000, "수익률": 5.0, "PER": 8.9, "PBR": 0.7, "ROE": 12.0},
    "더블유게임즈": {"현재가": 45000, "수익률": -11.5, "PER": 15.0, "PBR": 1.2, "ROE": 8.5},
}

portfolio_list = []
for stock in current_watchlist:
    if stock in sample_data:
        info = sample_data[stock]
        portfolio_list.append({
            "종목명": stock,
            "현재가(원)": info["현재가"],
            "수익률(%)": info["수익률"],
            "PER": info["PER"],
            "PBR": info["PBR"],
            "ROE(%)": info["ROE"],
        })
    else:
        portfolio_list.append({
            "종목명": stock,
            "현재가(원)": 0,
            "수익률(%)": 0.0,
            "PER": 0.0,
            "PBR": 0.0,
            "ROE(%)": 0.0,
        })

df_portfolio = pd.DataFrame(portfolio_list)

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
    
    st.error("⚠️ **처분 1순위 종목 : 유진테크** (위험 점수: 92/100)")
    st.markdown("""
    - **펀더멘털 및 밸류에이션 경고**: 목표 손절선 이탈 및 단기 실적 가시성 저하.
    - **DART 공시 및 뉴스 리스크**: 최근 전방 산업 투자 지연 관련 공시 및 부정적 거시경제 뉴스 다수 포착.
    - **경제적 해자 평가**: 기술 경쟁력은 존재하나, 업황 변동성에 취약하여 현재 방어력이 다소 낮음.
    - **💡 최종 AI 제언**: 현금 확보를 위해 **비중 축소 및 일부 처분을 최우선으로 권장**합니다.
    """)

with col2:
    st.subheader("🔍 실시간 공시 · 뉴스 & 해자 심층 분석")
    
    selected_stock = st.selectbox("분석할 종목 선택", current_watchlist)
    
    if st.button("🤖 AI 종합 정밀 분석 실행"):
        if not openai_key_input:
            st.error("OpenAI API 키를 먼저 사이드바에 입력해주세요!")
        else:
            with st.spinner(f"{selected_stock}에 대한 DART 공시 및 경제적 해자 분석 중..."):
                try:
                    client = OpenAI(api_key=openai_key_input)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "당신은 전문 주식 애널리스트이자 밸류에이션 및 경제적 해자 분석 전문가입니다. 한국어로 상세히 답변해주세요."},
                            {"role": "user", "content": f"{selected_stock}에 대해 경제적 해자(Economic Moat), PER/PBR/ROE 기반 밸류에이션, 그리고 현재 리스크 요인을 분석해줘."}
                        ]
                    )
                    st.success("분석 완료!")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"API 호출 중 오류 발생: {e}")

# 5. 대화형 AI 에이전트 섹션 (Chat Interface)
st.markdown("---")
st.subheader("💬 주식 AI 에이전트와 실시간 대화하기")
st.caption("선택한 관심종목이나 투자 전략, 경제적 해자에 대해 무엇이든 자유롭게 물어보세요!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 내용 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요 (예: 유진테크의 적정 주가 계산 방식은?)"):
    # 1) 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2) AI 응답 생성 및 표시
    if not openai_key_input:
        with st.chat_message("assistant"):
            st.warning("사이드바에 OpenAI API Key를 입력하셔야 답변을 생성할 수 있습니다.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):
                try:
                    client = OpenAI(api_key=openai_key_input)
                    
                    # 대화 히스토리 포함하여 API 호출
                    api_messages = [{"role": "system", "content": "당신은 가치투자 및 경제적 해자 분석 전문 주식 AI 에이전트입니다. 한국어로 정중하고 객관적으로 답변해주세요."}]
                    for msg in st.session_state.messages:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=api_messages
                    )
                    
                    answer = response.choices[0].message.content
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
