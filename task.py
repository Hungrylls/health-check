import streamlit as st

st.set_page_config(
    page_title="보건 체크",
    page_icon="🏥",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #f0f7ff; }
    .stButton > button {
        width: 100%;
        height: 70px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 16px;
        margin-bottom: 10px;
        border: none;
        background-color: #4A90D9;
        color: white;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #2c6fad;
        transform: scale(1.02);
    }
    .result-box {
        background-color: #ffffff;
        border-left: 6px solid #4A90D9;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 20px;
        font-size: 18px;
        color: #1a1a2e;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# 증상과 행동지침 데이터
symptoms = {
    "1️⃣ 1번 항목": "1번 항목입니다. 여기에 해당 증상의 행동지침을 입력하세요.",
    "2️⃣ 2번 항목": "2번 항목입니다. 여기에 해당 증상의 행동지침을 입력하세요.",
    "3️⃣ 3번 항목": "3번 항목입니다. 여기에 해당 증상의 행동지침을 입력하세요.",
    "4️⃣ 4번 항목": "4번 항목입니다. 여기에 해당 증상의 행동지침을 입력하세요.",
}

# 상태 초기화
if "selected" not in st.session_state:
    st.session_state.selected = None

# 제목
st.markdown("## 🏥 지금 몸 상태를 선택하세요")
st.markdown("해당하는 항목을 눌러주세요.")
st.markdown("---")

# 버튼 4개
for label in symptoms:
    if st.button(label):
        st.session_state.selected = label

# 결과 출력
if st.session_state.selected:
    st.markdown(f"""
        <div class="result-box">
            <b>📋 행동지침</b><br><br>
            {symptoms[st.session_state.selected]}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 다시 선택하기"):
        st.session_state.selected = None
        st.rerun()
