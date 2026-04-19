import json 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu
# from chatbot import ChatBot
from chatbot_mocking import ChatBot
system_message = """
[지시사항] 
당신은 전문적인 청능 재활 전문 상담 챗봇입니다. 
사용자가 입력하거나 저장한 청력도 및 이명도 데이터를 기반으로 환자의 상태를 분석하고 적절한 상담을 제공합니다. 
환자가 질문을 입력하면, 저장된 데이터를 활용하여 맞춤형 상담을 진행합니다.

[제약사항] 
1. 응답은 반드시 저장된 청력도 및 이명도 데이터를 기반으로 제공해야 합니다.
2. 사용자가 입력한 증상과 저장된 청력도 및 이명도 데이터를 함께 분석하여 종합적인 결과를 제공해야 합니다.
3. 청력도의 주요 수치(예: 주파수별 청력 손실 정도)와 이명도 데이터를 활용해 환자 상태를 간단히 요약한 후, 구체적인 조언을 제공합니다.
4. 의료적 조언은 참고용으로 제공하며, 전문 의료진 상담이 필요하다는 점을 항상 명시해야 합니다.
5. 마지막으로 반드시 저장된 청력도 및 이명도 데이터와 https://scholar.google.co.kr/schhp?hl=ko 에서 가져온 청능 재활 관련 논문을 기반으로 정확한 정보를 신속하게 제공해야합니다.

[응답 형식 예시]
{
    "상태 요약": "사용자의 청력 손실은 오른쪽 귀에서 고주파 영역(4000Hz 이상)에서 심각한 수준입니다. 이명은 주파수 6000Hz에서 발생하며, 우측 귀에서 더 두드러집니다.",
    "권장 조치": "청력 손실 완화를 위해 보청기 착용을 고려할 수 있습니다. 추가로 이명 관리를 위한 백색소음 치료나 인지 행동 치료(CBT)를 추천드립니다.",
    "추천": "이비인후과 또는 청각 전문가를 방문하여 추가 검사를 받으시기 바랍니다."
}
"""

# 챗봇 생성
chatbot = ChatBot("gpt-4o", system_message)

# 페이지 설정
st.set_page_config(
    page_title="청능 재활 상담 챗봇",
    page_icon="👨‍⚕️",
    layout="wide"
)

# 기본 제목 설정
st.title("💬 청능 재활 상담 챗봇 서비스")
st.caption("👨‍⚕️ 언제 어디서나 만나는 인공지능 청능사 선생님")
st.markdown("---")

# 사이드바
st.sidebar.markdown("### 청능 재활 상담 챗봇")
st.sidebar.image("logo.webp")

with st.sidebar:
    menu = option_menu("", ["청력도 및 이명도","챗봇","자주 묻는 질문","문의하기"], 
    icons=["ear", "chat-dots","patch-question","telephone-forward"], default_index=0)

if menu == "청력도 및 이명도":
    st.subheader("📊 청력도 및 이명도")  

    # 기본 정보 입력
    st.markdown("### 기본 정보")
    with st.expander("기본 정보"):
        col1, col2 = st.columns(2)
        with col1:
            id_no = st.text_input("I.D. No.")
            name = st.text_input("성명")
            gender = st.radio("성별", ["남", "여"], horizontal=True)
        with col2:
            birthdate = st.date_input("생년월일")
            contact = st.text_input("연락처")
            examiner = st.text_input("검사자")
        address = st.text_area("주소")
        exam_date = st.date_input("검사일")
        guardian = st.text_input("보호자")

    if "basic_info" not in st.session_state:
        st.session_state["basic_info"] = {}
    
    st.session_state["basic_info"].update({
        "I.D. No.": id_no,
        "성명": name,
        "성별": gender,
        "생년월일": str(birthdate),
        "연락처": contact,
        "주소": address,
        "검사일": str(exam_date),
        "보호자": guardian,
        "검사자": examiner
    })

    # 청력도 초기 데이터 설정
    if "audiogram_data" not in st.session_state:
        st.session_state.audiogram_data = {
            "Frequency": ["Right Ear (dB HL)", "Left Ear (dB HL)"],
            "250": [0, 0],
            "500": [0, 0],
            "1000": [0, 0],
            "2000": [0, 0],
            "4000": [0, 0],
            "6000": [0, 0],
            "8000": [0, 0]
        }

    df = pd.DataFrame(st.session_state.audiogram_data).set_index("Frequency")

    # 데이터 입력받기
    st.subheader("청력도")
    edited_df = st.data_editor(
        df, 
        use_container_width=True
    )

    # 그래프 유지 및 생성 로직
    if "audiogram_graph" not in st.session_state:
        st.session_state.audiogram_graph = None

    if not edited_df.equals(pd.DataFrame(st.session_state.audiogram_data).set_index("Frequency")):
        st.session_state.audiogram_data = edited_df.reset_index().to_dict(orient="list")

        fig, ax = plt.subplots(figsize=(8, 6))

        frequencies = [250, 500, 1000, 2000, 4000, 6000, 8000]
        x_positions = [250 + i * (8000 - 250) / 6 for i in range(7)]
        ax.set_xticks(x_positions)  
        ax.set_xticklabels(map(str, frequencies))
        ax.set_xlim(min(x_positions), max(x_positions))

        ax.set_ylim(120, -10) 
        ax.set_yticks(range(-10, 130, 10))
        ax.set_yticklabels(map(str, range(-10, 130, 10)))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")

        ax.set_title("Pure Tone Audiometry", fontsize=14)
        ax.set_xlabel("Frequency (Hz)", fontsize=12)
        ax.set_ylabel("Hearing Level (dB HL)", fontsize=12)

        right_ear_values = edited_df.loc["Right Ear (dB HL)"].astype(float).values
        left_ear_values = edited_df.loc["Left Ear (dB HL)"].astype(float).values

        ax.plot(x_positions, right_ear_values,  
                label="Right Ear (dB HL)", marker="o", markersize=10, markeredgewidth=2,
                markerfacecolor="red", linewidth=2, color="red")
        ax.plot(x_positions, left_ear_values,  
                label="Left Ear (dB HL)", marker="x", markersize=10, markeredgewidth=2,
                markeredgecolor="blue", linewidth=2, color="blue")

        ax.legend(loc="lower right")
        st.session_state.audiogram_graph = fig

    if st.session_state.audiogram_graph:
        st.pyplot(st.session_state.audiogram_graph)

    # 이명도 검사 함수
    def render_tinnitogram():
        st.markdown("### 이명도 검사")

        tinnitogram_data = {
            "이명 방향": ["", ""],
            "소리 특징": ["", ""],
            "Pitch matching (Hz)": ["", "",],
            "Loudness matching (HL)": ["", ""],
            "MML (HL)": ["",""],
            "RI (O/X)": ["", ""]
        }

        tinnitogram_df = pd.DataFrame(tinnitogram_data, index=["R", "L"])

        edited_tinnitogram = st.data_editor(
            tinnitogram_df, 
            use_container_width=True
        )

        comments = st.text_area("코멘트", height=100)
        otoscopy = st.text_area("이경검사", height=100)

        return edited_tinnitogram, comments, otoscopy

    # 이명도 검사 호출 (그래프와 독립적으로 실행 가능)
    tinnitogram_data, comments, otoscopy = render_tinnitogram()

    # [수정된 코드 시작] 이명도 데이터를 session_state에 저장
    st.session_state["tinnitogram_data"] = tinnitogram_data.to_dict(orient="list")
    st.session_state["tinnitogram_comments"] = comments
    st.session_state["tinnitogram_otoscopy"] = otoscopy
    # [수정된 코드 끝]

    # 데이터 저장 버튼
    if st.button("전체 데이터 저장"):
        st.success("모든 데이터가 저장되었습니다.")
        st.markdown("### 저장된 데이터")

        # 기본 정보
        st.markdown("#### 기본 정보")
        st.write({
            "I.D. No.": id_no,
            "성명": name,
            "성별": gender,
            "생년월일": birthdate,
            "연락처": contact,
            "주소": address,
            "검사일": exam_date,
            "보호자": guardian,
            "검사자": examiner
        })

        # 청력도
        st.markdown("#### 청력도")
        st.write(pd.DataFrame(st.session_state.audiogram_data).set_index("Frequency"))

        # 이명도 검사
        st.markdown("#### 이명도 검사")
        st.write(tinnitogram_data)
        st.markdown(f"**코멘트:** {comments}")
        st.markdown(f"**이경검사:** {otoscopy}")


elif menu == "챗봇":
    st.subheader("😊💬 안녕하세요? AI 청능 재활 상담 챗봇입니다.")
    st.markdown("""                
정확한 상담을 위해 아래 사항을 입력해주세요.
- **증상 (자세히)**
- **발생 시기 및 지속 시간**
- **복용중인 약**
- **기타 특이 사항**
                
예시) *어제부터 오른쪽 귀에서 -삐 소리가 들리고, 잠들기 전에는 더 심해지는 증상이 있어요. 현재 복용중인 약은 없습니다.*
""")
    # 사용자 입력
    with st.form("my_form"): 
        user_input = st.text_area("증상을 입력하세요.")
        if st.form_submit_button("문의하기"):
            with st.spinner("AI 응답을 생성하고 있습니다..."):
                #  챗봇 호출 시 context에 데이터 전달
                #  st.session_state에서 basic_info를 가져옴
                context = {
                    "청력도": st.session_state.get("audiogram_data", {}),
                    "이명도": st.session_state.get("tinnitogram_data", {}),
                    "코멘트": st.session_state.get("tinnitogram_comments", ""),
                    "이경검사": st.session_state.get("tinnitogram_otoscopy", ""),
                    "기본 정보": st.session_state.get("basic_info", {})
                }
                # 

                # 챗봇 응답 생성
                response = chatbot.get_response(user_input, context)

            # 응답 처리 및 출력
            try:
                data = json.loads(response)  # JSON 형식으로 변환

                # 상태 요약
                if "상태 요약" in data:
                    st.markdown(f"### 🩺 상태 요약\n{data['상태 요약']}")

                # 권장 조치
                if "권장 조치" in data:
                    st.markdown(f"### 📝 권장 조치\n{data['권장 조치']}")

                # 추천
                if "추천" in data:
                    st.markdown(f"### 💡 추천\n{data['추천']}")

            except json.JSONDecodeError:
                st.error("챗봇의 응답을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.")
                st.error("챗봇의 응답을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.")

elif menu == "자주 묻는 질문":
    st.subheader("🔍 자주 묻는 질문")
    st.markdown("""
**Q1: 이 챗봇은 정확한 의료 진단을 제공하나요?**\n
**A1:** 아니요. 이 챗봇은 참고용이며, 정확한 진단은 전문 청능사를 통해 받아야 합니다.\n
---
**Q2: 개인정보는 안전하게 보호되나요?**\n
**A2:** 입력하신 정보는 안전하게 보호되며 다른 용도로 사용되지 않습니다.
""")

elif menu == "문의하기":
    st.subheader("📩 문의하기")
    st.markdown("""
서비스 사용 중 궁금한 사항이나 불편한 점 있으시면 아래 방법으로 연락주세요.\n
- **이메일**: support@medicalchatbot.com\n
- **전화**: 02-1234-5678\n
- **주고**: 서울특별시 해린구 해린로 123
""")

st.markdown("---")

st.write("❗이명 재활 상담 챗봇은 참고용이며, 정확한 진단은 전문 청능사와의 상담을 통해 이루어져야 합니다.")

