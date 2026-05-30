import streamlit as st
import streamlit.components.v1 as components

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
    .result-box {
        background-color: #ffffff;
        border-left: 6px solid #4A90D9;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 20px;
        font-size: 16px;
        color: #1a1a2e;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        line-height: 2;
    }
    .urgent { color: #cc0000; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

KAKAO_API_KEY = "2a3d252c9366dd5397faac80ddca611f"

GUIDE = {
    "1. 머리가 아파요 (두통)": """
• <b>환경 조성:</b> 빛과 소리에 예민해질 수 있으니 방을 어둡게 하고 조용한 상태에서 쉬세요.<br>
• <b>수분 섭취:</b> 탈수가 원인일 수 있으므로 미지근한 물을 충분히 마십니다.<br>
• <b>디지털 디톡스:</b> 화면을 보는 것은 눈의 피로를 높여 통증을 악화시키니 스마트폰 사용을 멈추세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 망치로 맞은 듯한 극심한 통증, 시야 흐림, 말이 어눌해지는 증상이 있다면 즉시 응급실로 가야 합니다.
""",
    "2. 배가 아파요 (복통/소화불량)": """
• <b>온찜질:</b> 따뜻한 수건이나 핫팩을 배에 대어 근육을 이완시켜 주세요.<br>
• <b>자세 조절:</b> 상체를 약간 높이거나, 옆으로 눕는 것이 통증 완화에 도움이 될 수 있습니다.<br>
• <b>금식:</b> 속이 진정될 때까지는 자극적인 음식(매운 것, 탄산)을 피하고 미음이나 죽을 드세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 오른쪽 아랫배를 눌렀다 뗄 때 비명이 나올 정도로 아프다면 맹장염 가능성이 있으니 병원을 방문하세요.
""",
    "3. 열이 나고 몸이 떨려요 (발열/감기)": """
• <b>체온 조절:</b> 두꺼운 이불로 억지로 땀을 빼려 하지 마세요. 오히려 얇은 이불을 덮고 체온이 자연스럽게 내려가도록 도와주세요.<br>
• <b>수분 및 전해질 보충:</b> 열로 인해 땀이 많이 나면 탈수가 올 수 있으니 물이나 이온음료를 조금씩 자주 마십니다.<br>
• <b>미온수 마사지:</b> 38도 이상의 고열이 지속된다면 미온수(30~32°C)로 적신 수건으로 팔, 다리, 이마를 부드럽게 닦아주면 체온을 낮추는 데 도움이 됩니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 39.5도 이상의 고열이 하루 이상 지속되거나, 열과 함께 목이 뻣뻣하고 피부에 붉은 반점이 생긴다면 즉시 응급실을 방문하세요.
""",
}

INJURY = {
    "찰과상 및 상처": """
• <b>지혈:</b> 깨끗한 천이나 거즈로 상처 부위를 5~10분간 직접 압박하여 출혈을 멈춥니다.<br>
• <b>세척:</b> 출혈이 멈추면 흐르는 깨끗한 물로 상처를 충분히 씻어내어 이물질과 세균을 제거하세요.<br>
• <b>드레싱:</b> 소독 후 항균 연고를 얇게 바르고 밴드나 거즈로 덮어 상처를 보호합니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 압박을 해도 출혈이 멈추지 않거나, 상처가 깊고 벌어져 있다면 봉합이 필요할 수 있으니 병원을 방문하세요.
""",
    "염좌 및 타박상": """
• <b>RICE 원칙:</b> 초기 48시간은 Rest(휴식), Ice(얼음찜질), Compression(압박 붕대), Elevation(다친 부위 높이기)을 기억하세요.<br>
• <b>얼음찜질:</b> 얼음을 수건에 싸서 한 번에 15~20분씩, 하루 여러 차례 대어주면 붓기와 통증을 줄이는 데 효과적입니다.<br>
• <b>온찜질 전환:</b> 부상 후 48~72시간이 지나 급성 붓기가 가라앉으면 온찜질로 전환하여 혈액순환을 도와 회복을 촉진하세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 해당 부위를 전혀 디딜 수 없거나, 뼈가 튀어나온 것처럼 보이거나, 극심한 변형이 관찰된다면 골절 가능성이 있으니 즉시 병원을 방문하세요.
""",
}

MEDICINE = {
    "1. 해열진통제 (타이레놀 계열)": """
• <b>대표 상품:</b> 타이레놀 (성분: 아세트아미노펜)<br>
• <b>언제 먹나요:</b> 두통, 치통, 생리통, 갑작스러운 발열<br>
• <b>복용 방법:</b> 빈속에 먹어도 비교적 안전함<br>
• <span class='urgent'>⚠️ 주의사항:</span> 술(알코올)과 함께 먹으면 간에 심각한 손상을 줄 수 있음. 하루 최대 복용량을 절대 넘기지 말 것.
""",
    "2. 소염진통제 (부루펜 계열)": """
• <b>대표 상품:</b> 이지엔6, 부루펜 (성분: 이부프로펜, 덱시부프로펜)<br>
• <b>언제 먹나요:</b> 근육통, 관절염, 목감기(인후염), 심한 생리통<br>
• <b>복용 방법:</b> 반드시 식사 후에 복용 (위장 보호)<br>
• <span class='urgent'>⚠️ 주의사항:</span> 빈속에 먹으면 속 쓰림이나 위염을 유발할 수 있음. 평소 위장이 약한 사람은 주의 필요.
""",
    "3. 종합감기약": """
• <b>대표 상품:</b> 판콜, 판피린, 테라플루<br>
• <b>언제 먹나요:</b> 콧물, 코막힘, 기침, 몸살 기운이 동시에 있을 때<br>
• <b>복용 방법:</b> 초기 감기 증상 완화용<br>
• <span class='urgent'>⚠️ 주의사항:</span> 강한 졸음을 유발하므로 하교 길이나 운전, 공부 전에 주의. 다른 진통제와 중복해서 먹지 마세요.
""",
    "4. 소화제": """
• <b>대표 상품:</b> 훼스탈, 베아제, 닥터베아제<br>
• <b>언제 먹나요:</b> 과식 후 더부룩함, 소화가 잘 안 될 때, 명치가 답답할 때<br>
• <b>복용 방법:</b> 식후 바로 복용하는 것이 가장 효과적입니다<br>
• <span class='urgent'>⚠️ 주의사항:</span> 복통이 심하거나 며칠째 지속된다면 병원을 방문하세요.
""",
}

CONVENIENCE = {
    "💊 해열진통제": """
• <b>살 수 있는 약:</b> 타이레놀 (아세트아미노펜 500mg)<br>
• <b>편의점 브랜드:</b> 타이레놀 이알, 게보린 소프트 등<br>
• <b>언제 사나요:</b> 두통, 발열, 몸살이 갑자기 생겼을 때<br>
• <span class='urgent'>⚠️ 주의:</span> 편의점 약은 1~2회 응급용입니다. 증상이 지속되면 약국에서 구매하세요.
""",
    "🤢 소화제": """
• <b>살 수 있는 약:</b> 훼스탈 플러스, 베아제<br>
• <b>언제 사나요:</b> 과식 후 더부룩하거나 소화가 안 될 때<br>
• <b>복용 방법:</b> 식후 바로 복용<br>
• <span class='urgent'>⚠️ 주의:</span> 복통이 심하다면 병원 방문을 우선하세요.
""",
    "🤧 감기약": """
• <b>살 수 있는 약:</b> 판콜에이, 화이투벤 등<br>
• <b>언제 사나요:</b> 콧물, 코막힘, 가벼운 몸살 기운이 있을 때<br>
• <b>복용 방법:</b> 식후 복용, 졸음 유발 주의<br>
• <span class='urgent'>⚠️ 주의:</span> 다른 진통제(타이레놀 등)와 함께 먹으면 안 돼요.
""",
    "🩹 외용 상처약": """
• <b>살 수 있는 약:</b> 대일밴드, 후시딘, 마데카솔<br>
• <b>언제 사나요:</b> 가벼운 찰과상, 작은 상처가 났을 때<br>
• <b>사용 방법:</b> 상처를 물로 씻은 후 연고 바르고 밴드로 덮기<br>
• <span class='urgent'>⚠️ 주의:</span> 상처가 깊거나 출혈이 심하면 병원에 가세요.
""",
    "🏃 파스 (근육통)": """
• <b>살 수 있는 약:</b> 제일파스, 신신파스, 쿨파스<br>
• <b>언제 사나요:</b> 근육통, 어깨 결림, 타박상 초기<br>
• <b>사용 방법:</b> 아픈 부위에 붙이고 4~8시간 후 제거<br>
• <span class='urgent'>⚠️ 주의:</span> 상처가 난 피부에는 붙이지 마세요.
""",
}

# 약국 데이터 (주소로 geocoding해서 지도에 표시)
PHARMACIES = [
    {"name": "하나로약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 117", "phone": "031-571-7579", "hours": "월~금 09:00~18:00 / 토 09:00~16:00 / 일 휴무"},
    {"name": "용한약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 93", "phone": "031-527-1188", "hours": "월~금 09:00~22:00 / 토 09:00~21:00 / 공휴일 10:00~22:00 / 일 휴무"},
    {"name": "소중한약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 70", "phone": "031-571-7233", "hours": "월~금 09:00~19:00 / 일 09:00~15:00 / 토·공휴일 휴무"},
    {"name": "세민약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 51", "phone": "031-571-6734", "hours": "월~금 09:00~20:00 / 토 09:00~21:00 / 공휴일 09:00~18:00 / 일 휴무"},
    {"name": "임약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 52", "phone": "031-574-8484", "hours": "월~목 09:00~20:00 / 금 09:00~18:00 / 토 09:00~15:00 / 일 09:00~18:00"},
    {"name": "참조은약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 48", "phone": "031-574-1251", "hours": "월~금 09:00~18:00 / 토 09:00~13:00 / 일 휴무"},
    {"name": "비젼약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 46-1", "phone": "031-574-1008", "hours": "월~금 09:00~18:30 / 토 09:00~14:00 / 일 휴무"},
    {"name": "참사랑약국", "address": "경기 남양주시 퇴계원읍 퇴계원로46번길 1", "phone": "031-528-5767", "hours": "월~금 09:00~20:00 / 토 09:00~21:00 / 일 휴무"},
    {"name": "문온누리약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 29", "phone": "031-572-0409", "hours": "월·수·금 08:00~21:00 / 화·목 08:00~19:00 / 토·일 08:00~16:00"},
    {"name": "굿모닝약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 30", "phone": "031-572-7749", "hours": "월~금 09:00~13:00 / 토 09:00~16:00 / 일 휴무"},
    {"name": "미엘약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 20", "phone": "031-571-2147", "hours": "월~금 09:00~21:00 / 토·일·공휴일 09:00~18:00"},
    {"name": "정안약국", "address": "경기 남양주시 퇴계원읍 퇴계원로 16", "phone": "031-571-9574", "hours": "월~금 09:00~20:30 / 토 09:00~17:00 / 일 휴무"},
]

def pharmacy_map_html(pharmacies, api_key):
    import json
    pharmacies_json = json.dumps(pharmacies, ensure_ascii=False)
    return f"""
    <div style="font-family: sans-serif;">
      <div id="map" style="width:100%; height:450px; border-radius:12px; border:1px solid #ddd;"></div>
      <p style="font-size:13px; color:#666; margin-top:8px;">📍 약국 마커를 클릭하면 상세 정보가 나와요!</p>
    </div>
    <script type="text/javascript"
      src="//dapi.kakao.com/v2/maps/sdk.js?appkey={api_key}&libraries=services">
    </script>
    <script>
      var pharmacies = {pharmacies_json};

      var mapContainer = document.getElementById('map');
      var mapOption = {{
        center: new kakao.maps.LatLng(37.6528, 127.1300),
        level: 4
      }};
      var map = new kakao.maps.Map(mapContainer, mapOption);
      var geocoder = new kakao.maps.services.Geocoder();
      var bounds = new kakao.maps.LatLngBounds();

      pharmacies.forEach(function(p) {{
        geocoder.addressSearch(p.address, function(result, status) {{
          if (status === kakao.maps.services.Status.OK) {{
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
            bounds.extend(coords);

            var marker = new kakao.maps.Marker({{
              map: map,
              position: coords,
              title: p.name
            }});

            var content =
              '<div style="padding:12px;min-width:220px;font-size:13px;line-height:2;box-shadow:0 2px 8px rgba(0,0,0,0.15);border-radius:8px;background:#fff;">' +
              '<b style="font-size:15px;">🏥 ' + p.name + '</b><br>' +
              '📍 ' + p.address + '<br>' +
              '📞 ' + p.phone + '<br>' +
              '🕐 ' + p.hours +
              '</div>';

            var infowindow = new kakao.maps.InfoWindow({{ content: content, removable: true }});

            kakao.maps.event.addListener(marker, 'click', function() {{
              infowindow.open(map, marker);
            }});

            map.setBounds(bounds);
          }}
        }});
      }});
    </script>
    """

def reset():
    st.session_state.menu = None
    st.session_state.symptom = None
    st.session_state.injury = None
    st.session_state.medicine = None
    st.session_state.convenience = None

for key in ["menu", "symptom", "injury", "medicine", "convenience"]:
    if key not in st.session_state:
        st.session_state[key] = None

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

elif st.session_state.menu == "guide":
    if st.session_state.symptom is None:
        st.markdown("### 💊 증상별 대처 가이드")
        st.markdown("해당하는 증상을 선택하세요.")
        for label in list(GUIDE.keys()) + ["4. 다쳤어요 (근육통/외상)"]:
            if st.button(label):
                st.session_state.symptom = label
                st.rerun()
    elif st.session_state.symptom == "4. 다쳤어요 (근육통/외상)":
        if st.session_state.injury is None:
            st.markdown("### 🩹 어떻게 다쳤나요?")
            for label in INJURY.keys():
                if st.button(label):
                    st.session_state.injury = label
                    st.rerun()
        else:
            st.markdown(f"### 🩹 {st.session_state.injury}")
            st.markdown(f"<div class='result-box'>{INJURY[st.session_state.injury]}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {st.session_state.symptom}")
        st.markdown(f"<div class='result-box'>{GUIDE[st.session_state.symptom]}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 처음으로 돌아가기"):
        reset()
        st.rerun()

elif st.session_state.menu == "medicine":
    if st.session_state.medicine is None:
        st.markdown("### 🏠 우리 집 상비약 백과")
        st.markdown("알고 싶은 약을 선택하세요.")
        for label in MEDICINE.keys():
            if st.button(label):
                st.session_state.medicine = label
                st.rerun()
    else:
        st.markdown(f"### {st.session_state.medicine}")
        st.markdown(f"<div class='result-box'>{MEDICINE[st.session_state.medicine]}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 처음으로 돌아가기"):
        reset()
        st.rerun()

elif st.session_state.menu == "pharmacy":
    st.markdown("### 🗺️ 주변 약국 찾기")
    st.markdown("마커를 클릭하면 약국 정보가 나와요! 📍")
    components.html(pharmacy_map_html(PHARMACIES, KAKAO_API_KEY), height=520, scrolling=False)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 처음으로 돌아가기"):
        reset()
        st.rerun()

elif st.session_state.menu == "convenience":
    if st.session_state.convenience is None:
        st.markdown("### 🏪 편의점 상비약 안내")
        st.markdown("알고 싶은 약 종류를 선택하세요.")
        for label in CONVENIENCE.keys():
            if st.button(label):
                st.session_state.convenience = label
                st.rerun()
    else:
        st.markdown(f"### {st.session_state.convenience}")
        st.markdown(f"<div class='result-box'>{CONVENIENCE[st.session_state.convenience]}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 처음으로 돌아가기"):
        reset()
        st.rerun()
