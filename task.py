import streamlit as st
from streamlit_folium import st_folium
import folium

# 1. 페이지 설정
st.set_page_config(
    page_title="보건 체크",
    page_icon="🏥",
    layout="centered"
)

# 2. CSS 스타일 정의 (상단 배치 및 정돈)
st.markdown("""
    <style>
    .main { background-color: #f0f7ff; }
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 17px;
        font-weight: bold;
        border-radius: 14px;
        margin-bottom: 8px;
        border: none;
        background-color: #4A90D9;
        color: white;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #2c6fad;
        transform: scale(1.02);
    }
    .nav-box { 
        display: flex; 
        gap: 10px; 
        margin-top: 20px; 
    }
    .result-box {
        background-color: #ffffff;
        border-left: 6px solid #4A90D9;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-size: 16px;
        color: #1a1a2e;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        line-height: 2;
    }
    .urgent { color: #cc0000; font-weight: bold; }
    .highlight { color: #2c6fad; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터베이스 (의학 정보 팩트 체크 및 항목 반영)
GUIDE = {
    "1. 머리가 아파요 (두통)": """
• <span class='highlight'>자세 및 스트레칭:</span> 두통은 목, 어깨 근육이 뭉치는 긴장성 두통인 경우가 많습니다. 허리를 펴고 목을 천천히 돌리며 승모근을 스트레칭해 보세요.<br>
• <span class='highlight'>스트레스 점검:</span> 스트레스는 혈관을 수축시켜 두통을 유발하는 가장 큰 원인입니다. 최근 나를 신경 쓰이게 한 일이 있는지 돌아보고 짚어보며 심호흡을 하세요.<br>
• <b>환경 조성:</b> 빛과 소리에 예민해질 수 있으니 방을 어둡게 하고 조용한 상태에서 쉬세요.<br>
• <b>수분 섭취:</b> 탈수가 원인일 수 있으므로 미지근한 물을 충분히 마십니다.<br>
• <b>디지털 디톡스:</b> 화면을 보는 것은 눈의 피로를 높여 통증을 악화시키니 스마트폰 사용을 멈추세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 망치로 맞은 듯한 극심한 통증, 시야 흐림, 말이 어눌해지거나 마비 증상이 있다면 즉시 응급실로 가야 합니다.
""",
    "2. 배가 아파요 (복통/소화불량)": """
• <span class='highlight'>스트레스와 과민성 대장:</span> 위와 장은 신경계와 긴밀히 연결되어 있어 스트레스를 받으면 위산 분비가 불균형해지고 장이 과도하게 수축합니다. 반복적인 복통과 가스, 설사/변비는 <span class='highlight'>과민성 대장 증후군</span>이나 신경성 위염일 수 있으니 마음을 편안히 다스려야 합니다.<br>
• <b>온찜질:</b> 따뜻한 수건이나 핫팩을 배에 대어 장기 근육을 이완시켜 주세요.<br>
• <b>자세 조절:</b> 상체를 약간 높이거나, 왼쪽으로 눕는 것이 위산 역류와 통증 완화에 도움이 됩니다.<br>
• <b>금식 및 식단:</b> 속이 진정될 때까지는 자극적인 음식(매운 것, 탄산, 밀가루)을 피하고 미음이나 죽을 드세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 오른쪽 아랫배를 눌렀다 뗄 때 찌르는 듯한 통증이 심하다면 충수염(맹장염) 가능성이 있으니 즉시 병원을 방문하세요.
""",
    "3. 열이 나고 몸이 떨려요 (발열/감기)": """
• <span class='highlight'>타 증상 연계 가이드:</span> 단순 감기 외에도, 독감(인플루엔자)은 급격한 고열과 심한 근육통을 동반하며, 코로나19는 인후통 및 후각/미각 상실이 잦습니다. 만약 열과 함께 오한이 나면서 옆구리나 등(요통)이 끊어질 듯 아프다면 <span class='highlight'>급성 신우신염(신장 감염)</span>일 수 있으니 동반 증상을 잘 관찰해야 합니다.<br>
• <b>체온 조절:</b> 오한이 들 때는 얇은 이불을 덮고, 열이 오르기 시작하면 두꺼운 이불로 땀을 억지로 빼지 마세요. 내부 체온이 더 올라 위험할 수 있습니다.<br>
• <b>수분 및 전해질 보충:</b> 열로 인해 탈수가 오기 쉬우므로 미지근한 물이나 이온음료를 자주 마십니다.<br>
• <b>미온수 마사지:</b> 고열이 지속된다면 미온수(30~32°C) 수건으로 목, 겨드랑이, 사타구니를 닦아내어 열을 교환해 줍니다. <b>(얼음물/알코올 금지)</b><br>
• <span class='urgent'>⚠️ 긴급:</span> 39.5도 이상의 고열이 하루 이상 지속되거나, 목이 뻣뻣해 숙여지지 않고 피부에 붉은 반점이 생긴다면(뇌수막염 의심) 즉시 응급실로 가십시오.
""",
}

INJURY = {
    "찰과상 및 상처": """
• <b>지혈:</b> 깨끗한 천이나 거즈로 상처 부위를 5~10분간 직접 압박하여 출혈을 멈춥니다.<br>
• <b>세척:</b> 흐르는 깨끗한 물이나 생리식염수로 상처를 충분히 씻어내어 흙이나 이물질을 완벽히 제거하세요. (침을 바르는 것은 세균 감염을 높입니다.)<br>
• <b>드레싱:</b> 소독 후 항균 연고를 바르고 습윤 밴드나 거즈로 덮어 상처 버호합니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 지혈 후에도 출혈이 멈추지 않거나 상처가 깊게 벌어져 지방층이 보인다면 봉합이 필요하므로 즉시 병원으로 이동하세요.
""",
    "염좌 및 타박상": """
• <b>RICE 원칙:</b> 초기 48시간은 Rest(휴식), Ice(얼음찜질), Compression(압박 붕대), Elevation(다친 부위 심장보다 높이기)을 철저히 지킵니다.<br>
• <b>얼음찜질:</b> 부상 직후에는 얼음을 수건에 싸서 한 번에 15~20분씩 대어주어 내부 출혈과 부종을 억제합니다.<br>
• <b>온찜질 전환 시기:</b> 부상 후 48~72시간이 지나 붉은 기와 붓기가 가라앉으면 온찜질로 바꾸어 혈액순환과 조직 회복을 돕습니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 다친 부위에 체중을 실어 디딜 수 없거나 모양이 변형되었다면 골절 및 인대 파열 가능성이 매우 높으니 방치하지 말고 정형외과로 가세요.
""",
}

MEDICINE = {
    "1. 해열진통제 (타이레놀 계열)": {
        "text": """
• <b>대표 성분:</b> 아세트아미노펜 (타이레놀, 타세놀 등)<br>
• <b>적응증:</b> 두통, 치통, 생리통, 감기로 인한 발열 등<br>
• <b>복용 방법:</b> 위장 장애가 적어 식사 여부와 상관없이 빈속에도 복용 가능합니다.<br>
• <span class='highlight'>⚖️ 최대 복용량:</span> 성인 기준 <b>하루 최대 4,000mg</b> (500mg 기준 하루 최대 8알)입니다. 초과 시 심각한 간 손상을 유발합니다.<br>
• <span class='urgent'>🚨 알레르기 주의:</span> 복용 후 피부에 붉은 반점, 두드러기, 가려움증이 생기거나 호흡 곤란이 오면 즉시 복용을 중단해야 합니다.<br>
• <span class='urgent'>⚠️ 필수 주의사항:</span> <b>술(알코올)을 마신 전후에는 절대로 복용해서는 안 됩니다.</b> 간 독성이 극대화됩니다.
""",
        "img": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&auto=format&fit=crop&q=60"
    },
    "2. 소염진통제 (부루펜 계열)": {
        "text": """
• <b>대표 성분:</b> 이부프로펜, 덱시부프로펜, 나프록센 (이지엔6, 부루펜, 탁센 등)<br>
• <b>적응증:</b> 관절염, 근육통, 목감기(인후염), 치통, 염증을 동반한 통증<br>
• <b>복용 방법:</b> 위점막을 자극할 수 있으므로 <b>반드시 식후에 충분한 물과 함께 복용</b>하세요.<br>
• <span class='highlight'>⚖️ 최대 복용량:</span> 이부프로펜 기준 일반적인 <b>하루 최대 복용량은 3,200mg</b>입니다.<br>
• <span class='urgent'>🚨 알레르기 주의:</span> 과거 소염진통제를 먹고 눈이나 입술이 붓거나 천식 발작(쌕쌕거림), 두드러기가 났던 경험(NSAIDs 과민반응)이 있다면 이 계열의 약물 복용을 금해야 합니다.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 평소 위궤양이 있거나 신장 기능이 떨어진 분들은 장기 복용을 피하세요.
""",
        "img": "https://images.unsplash.com/photo-1626716493137-b67fe9501e76?w=500&auto=format&fit=crop&q=60"
    },
    "3. 종합감기약": {
        "text": """
• <b>대표 상품:</b> 판콜, 판피린, 테라플루 등<br>
• <b>적응증:</b> 기침, 콧물, 코막힘, 몸살, 발열 등 여러 감기 증상이 복합적으로 나타날 때<br>
• <span class='highlight'>⚖️ 최대 복용량:</span> 제품 뒷면의 정해진 용법(예: 하루 3회, 1회 1병/1포)을 엄격히 따라야 합니다.<br>
• <span class='urgent'>🚨 알레르기 및 성분 중복 주의:</span> 종합감기약 안에는 이미 아세트아미노펜이 들어있는 경우가 많으므로 타이레놀을 추가로 복용 시 <b>간 독성 위험</b>이 커집니다.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 콧물을 멈추는 항히스타민제 성분 때문에 <b>심한 졸음</b>을 유발합니다. 운전 전에는 복용을 삼가세요.
""",
        "img": "https://images.unsplash.com/photo-1550572017-edd951b55104?w=500&auto=format&fit=crop&q=60"
    },
    "4. 소화제": {
        "text": """
• <b>대표 상품:</b> 훼스탈, 베아제, 가스활명수, 속청 등<br>
• <span class='highlight'>🧪 고체(알약) vs 액상(드링크) 소화제 차이점:</span><br>
  - <b>액상 소화제 (생약 성분):</b> 고추, 육계 등 생약이 들어있어 위장의 운동을 촉진하고 가스를 빠르게 배출합니다.<br>
  - <b>고체 소화제 (소화효소제):</b> 판크레아틴 등 탄수화물, 단백질, 지방을 직접 분해하는 효소가 들어있어 음식물을 부숩니다.<br>
  - <i>속이 꽉 막혔을 때는 알약을, 가스가 차고 더부룩할 때는 액상제를 선택하는 것이 좋습니다.</i><br>
• <span class='highlight'>⚖️ 최대 복용량:</span> 소화효소제는 보통 1회 1~2정씩 하루 3회 식후에 복용하며, 매일 장기 복용 시 자체 소화 능력이 떨어질 수 있습니다.<br>
• <span class='urgent'>🚨 알레르기 주의:</span> 알약 소화제에는 '돼지 췌장(판크레아틴)' 유래 성분이 많으므로, 돼지 관련 심한 알레르기 환자는 주의해야 합니다.
""",
        "img": "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=500&auto=format&fit=crop&q=60"
    },
}

CONVENIENCE = {
    "💊 해열진통제": {
        "text": """
• <b>편의점 판매 약:</b> 타이레놀정 500mg (8정) 등<br>
• <span class='highlight'>⚖️ 최대 복용량:</span> 성인 기준 최대 4,000mg. 편의점용 한 팩이 딱 하루 최대치 분량입니다.<br>
• <span class='urgent'>🚨 알레르기 및 주의:</span> 복용 후 가려움, 호흡 곤란이 발생하면 즉시 중단하십시오. 음주 후 복용 절대 금지.
""",
        "img": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&auto=format&fit=crop&q=60"
    },
    "🤢 소화제": {
        "text": """
• <b>편의점 판매 약:</b> 훼스탈 플러스, 베아제정, 가스활명수-에이 등<br>
• <span class='highlight'>🧪 형태별 차이:</span> 훼스탈/베아제는 '소화효소제(알약)'이며, 가스활명수-에이는 위장 운동을 돕는 '생약 드링크(액상)'입니다.<br>
• <span class='urgent'>🚨 알레르기 주의:</span> 알약 소화제에는 돼지 췌장 추출물이 포함되어 있으므로 관련 알레르기 유병자는 주의가 필요합니다.
""",
        "img": "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=500&auto=format&fit=crop&q=60"
    },
    "🤧 감기약": {
        "text": """
• <b>편의점 판매 약:</b> 판콜에이 내복액, 판피린티 정 등<br>
• <span class='urgent'>🚨 중복 및 알레르기 주의:</span> 아세트아미노펜이 다량 포함되어 있습니다. <b>타이레놀과 동시에 교차 복용 시 간 독성 위험</b>이 커집니다.<br>
• <b>주의사항:</b> 졸음을 유발하므로 운전이나 기계 조작 전에는 피하십시오.
""",
        "img": "https://images.unsplash.com/photo-1550572017-edd951b55104?w=500&auto=format&fit=crop&q=60"
    },
}

PHARMACY_DATA = [
    {"name": "1. 하나로약국", "phone": "031-571-7579", "hours": "월~금 09:00~18:00 / 토 09:00~16:00 / 일 휴무", "lat": 37.6495, "lon": 127.1855},
    {"name": "2. 용한약국", "phone": "031-527-1188", "hours": "월~금 09:00~22:00 / 토 09:00~21:00 / 일 휴무", "lat": 37.6488, "lon": 127.1856},
    {"name": "3. 소중한약국", "phone": "031-571-7233", "hours": "월~금 09:00~19:00 / 일 09:00~15:00", "lat": 37.6480, "lon": 127.1854},
    {"name": "4. 세민약국", "phone": "031-571-6734", "hours": "월~금 09:00~20:00 / 토 09:00~21:00 / 일 휴무", "lat": 37.6472, "lon": 127.1853},
    {"name": "5. 임약국", "phone": "031-574-8484", "hours": "월~목 09:00~20:00 / 일 09:00~18:00", "lat": 37.6468, "lon": 127.1882},
    {"name": "6. 참조은약국", "phone": "031-574-1251", "hours": "월~금 09:00~18:00 / 토 09:00~13:00 / 일 휴무", "lat": 37.6455, "lon": 127.1852},
    {"name": "7. 비젼약국", "phone": "031-574-1008", "hours": "월~금 09:00~18:30 / 토 09:00~14:00 / 일 휴무", "lat": 37.6453, "lon": 127.1883},
    {"name": "8. 참사랑약국", "phone": "031-528-5767", "hours": "월~금 09:00~20:00 / 토 09:00~21:00 / 일 휴무", "lat": 37.6452, "lon": 127.1895},
    {"name": "9. 문온누리약국", "phone": "031-572-0409", "hours": "월~금 08:00~21:00 / 토·일 08:00~16:00", "lat": 37.6442, "lon": 127.1851},
    {"name": "10. 굿모닝약국", "phone": "031-572-7749", "hours": "월~금 09:00~13:00 / 토 09:00~16:00 / 일 휴무", "lat": 37.6440, "lon": 127.1884},
    {"name": "11. 미엘약국", "phone": "031-571-2147", "hours": "월~금 09:00~21:00 / 토·일 09:00~18:00", "lat": 37.6430, "lon": 127.1850},
    {"name": "12. 정안약국", "phone": "031-571-9574", "hours": "월~금 09:00~20:30 / 토 09:00~17:00 / 일 휴무", "lat": 37.6415, "lon": 127.1848}
]

# 4. 세션 초기화 기능
def reset():
    st.session_state.menu = None
    st.session_state.symptom = None
    st.session_state.injury = None
    st.session_state.medicine = None
    st.session_state.convenience = None

for key in ["menu", "symptom", "injury", "medicine", "convenience"]:
    if key not in st.session_state:
        st.session_state[key] = None

# 5. 하단 공통 네비게이션 버튼 바 함수
def show_navigation_buttons(prev_level):
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전으로"):
            if prev_level == "menu":
                st.session_state.menu = None
            elif prev_level == "symptom":
                st.session_state.symptom = None
            elif prev_level == "injury":
                st.session_state.injury = None
            elif prev_level == "medicine":
                st.session_state.medicine = None
            elif prev_level == "convenience":
                st.session_state.convenience = None
            st.rerun()
    with col2:
        if st.button("🔄 처음으로 돌아가기"):
            reset()
            st.rerun()

# 6. 메인 화면 출력 및 라우팅 구조
st.markdown("## 🏥 보건 도우미")
st.markdown("---")

if st.session_state.menu is None:
    st.markdown("### 원하는 항목을 선택하세요")
    if st.button("💊 [1] 증상별 대처 가이드"):
        st.session_state.menu = "guide"
        st.rerun()
    if st.button("🏠 [2] 우리 집 상비약 백과"):
        st.session_state.menu = "medicine"
        st.rerun()
    if st.button("🗺️ [3] 주변 약국 찾기"):
        st.session_state.menu = "pharmacy"
        st.rerun()
    if st.button("🏪 [4] 편의점 상비약 안내"):
        st.session_state.menu = "convenience"
        st.rerun()

# [1] 가이드 메뉴 진입
elif st.session_state.menu == "guide":
    if st.session_state.symptom is None:
        st.markdown("### 💊 증상별 대처 가이드")
        st.markdown("해당하는 증상을 선택하세요.")
        for label in list(GUIDE.keys()) + ["4. 다쳤어요 (근육통/외상)"]:
            if st.button(label):
                st.session_state.symptom = label
                st.rerun()
        show_navigation_buttons("menu")
        
    elif st.session_state.symptom == "4. 다쳤어요 (근육통/외상)":
        if st.session_state.injury is None:
            st.markdown("### 🩹 어떻게 다쳤나요?")
            for label in INJURY.keys():
                if st.button(label):
                    st.session_state.injury = label
                    st.rerun()
            show_navigation_buttons("symptom")
        else:
            st.markdown(f"### 🩹 {st.session_state.injury}")
            st.markdown(f"<div class='result-box'>{INJURY[st.session_state.injury]}</div>", unsafe_allow_html=True)
            show_navigation_buttons("injury")
    else:
        st.markdown(f"### {st.session_state.symptom}")
        st.markdown(f"<div class='result-box'>{GUIDE[st.session_state.symptom]}</div>", unsafe_allow_html=True)
        show_navigation_buttons("symptom")

# [2] 상비약 백과 진입
elif st.session_state.menu == "medicine":
    if st.session_state.medicine is None:
        st.markdown("### 🏠 우리 집 상비약 백과")
        st.markdown("알고 싶은 약을 선택하세요.")
        for label in MEDICINE.keys():
            if st.button(label):
                st.session_state.medicine = label
                st.rerun()
        show_navigation_buttons("menu")
    else:
        st.markdown(f"### {st.session_state.medicine}")
        st.image(MEDICINE[st.session_state.medicine]["img"], width=250)
        st.markdown(f"<div class='result-box'>{MEDICINE[st.session_state.medicine]['text']}</div>", unsafe_allow_html=True)
        show_navigation_buttons("medicine")

# [3] 주변 약국 찾기 지도 진입
elif st.session_state.menu == "pharmacy":
    st.markdown("### 🗺️ 주변 약국 찾기")
    st.markdown("📍 지도상의 마커를 클릭하시면 상세 약국 정보를 확인하실 수 있습니다.")
    
    m = folium.Map(location=[37.6455, 127.1865], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([37.6510, 127.1830], popup="퇴계원고등학교", icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
    folium.Marker([37.6465, 127.1810], popup="퇴계원중학교", icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
    
    for p in PHARMACY_DATA:
        popup_html = f"<b>🏥 {p['name']}</b><br>📞 {p['phone']}<br>🕐 {p['hours']}"
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red", icon="plus")
        ).add_to(m)
        
    st_folium(m, width=700, height=500, returned_objects=[])
    show_navigation_buttons("menu")

# [4] 편의점 안내 진입
elif st.session_state.menu == "convenience":
    if st.session_state.convenience is None:
        st.markdown("### 🏪 편의점 상비약 안내")
        st.markdown("알고 싶은 약 종류를 선택하세요.")
        for label in CONVENIENCE.keys():
            if st.button(label):
                st.session_state.convenience = label
                st.rerun()
        show_navigation_buttons("menu")
    else:
        st.markdown(f"### {st.session_state.convenience}")
        st.image(CONVENIENCE[st.session_state.convenience]["img"], width=250)
        st.markdown(f"<div class='result-box'>{CONVENIENCE[st.session_state.convenience]['text']}</div>", unsafe_allow_html=True)
        show_navigation_buttons("convenience")
