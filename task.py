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
    .drug-img-row {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        margin: 10px 0 4px 0;
    }
    .drug-img-card {
        text-align: center;
        font-size: 12px;
        color: #555;
    }
    .drug-img-card img {
        width: 90px;
        height: 90px;
        object-fit: contain;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background: #fafafa;
        display: block;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 증상 데이터
# ─────────────────────────────────────────────
GUIDE = {
    "1. 머리가 아파요 (두통)": """
• <b>환경 조성:</b> 빛과 소리에 예민해질 수 있으니 방을 어둡게 하고 조용한 곳에서 쉬세요.<br>
• <b>수분 섭취:</b> 탈수가 두통의 흔한 원인 중 하나입니다. 미지근한 물을 충분히 천천히 마셔주세요.<br>
• <b>디지털 디톡스:</b> 스마트폰·컴퓨터 화면은 눈의 피로를 높여 두통을 악화시킵니다. 화면 사용을 멈추고 눈을 감고 쉬세요.<br>
• <b>자세 점검 & 스트레칭:</b> 목과 어깨 근육이 뭉치면 긴장성 두통으로 이어지는 경우가 많습니다. 최근 오래 앉아 있었거나 고개를 숙이고 있었다면 자세를 교정해보세요. 목을 천천히 좌우로 기울이고, 어깨를 크게 으쓱했다가 내리는 스트레칭이 도움이 될 수 있습니다.<br>
• <b>스트레스 점검:</b> 스트레스와 수면 부족은 긴장성 두통의 대표적인 원인입니다. 최근 스트레스를 많이 받은 일이 있었는지 돌아보고, 복식호흡이나 잠깐의 명상으로 긴장을 풀어보세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 망치로 맞은 듯한 극심한 통증이 갑자기 시작되거나, 시야가 흐려지거나, 말이 어눌해지거나, 손발이 마비되는 느낌이 든다면 뇌졸중이나 뇌출혈의 가능성이 있으니 즉시 응급실로 가야 합니다.
""",

    "2. 배가 아파요 (복통/소화불량)": """
• <b>온찜질:</b> 따뜻한 수건이나 핫팩을 배에 대어 장 근육을 이완시켜 주세요. 단, 맹장 부위(오른쪽 아랫배)엔 온찜질을 피하세요.<br>
• <b>자세 조절:</b> 상체를 약간 높이거나 옆으로 눕는 것이 통증 완화에 도움이 될 수 있습니다.<br>
• <b>금식 & 식이 조절:</b> 속이 진정될 때까지는 맵고 기름진 음식, 탄산음료를 피하고 미음이나 죽처럼 자극 없는 음식을 드세요.<br>
• <b>스트레스 점검:</b> 스트레스는 장의 운동을 직접적으로 교란합니다. 만성적인 복통과 설사·변비가 반복된다면 '과민성 대장 증후군(IBS)'일 가능성이 있습니다. 최근 심리적 압박이 컸는지 생각해보고, 복식호흡·산책 등 긴장을 해소하는 것이 증상 완화에 도움이 됩니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 오른쪽 아랫배를 눌렀다 뗄 때 극심한 통증이 느껴지면 맹장염(충수염) 가능성이 있습니다. 혈변, 극심한 복통, 복부가 딱딱하게 굳는 증상이 나타나면 즉시 병원을 방문하세요.
""",

    "3. 열이 나고 몸이 떨려요 (발열/감기)": """
• <b>체온 조절:</b> 두꺼운 이불로 억지로 땀을 빼지 마세요. 얇은 이불을 덮고 체온이 자연스럽게 내려가도록 도와주세요.<br>
• <b>수분 및 전해질 보충:</b> 열로 땀이 많이 나면 탈수가 올 수 있습니다. 물, 이온음료를 조금씩 자주 마셔 주세요.<br>
• <b>미온수 마사지:</b> 38도 이상의 고열이 지속된다면 30~32°C의 미온수로 적신 수건으로 팔·다리·이마를 부드럽게 닦으면 체온 낮추기에 도움이 됩니다.<br>
• <b>동반 증상 주의:</b> 발열은 다양한 질환과 함께 나타날 수 있습니다.<br>
&nbsp;&nbsp;- <b>심한 인후통 + 열:</b> 세균성 편도염(연쇄상구균 감염)일 수 있어 항생제 치료가 필요할 수 있으니 병원을 방문하세요.<br>
&nbsp;&nbsp;- <b>피부 붉은 발진 + 열:</b> 홍역, 성홍열, 약물 알레르기 반응 등을 의심할 수 있습니다.<br>
&nbsp;&nbsp;- <b>소변 시 통증 + 열:</b> 요로감염 또는 신우신염의 가능성이 있으며 항생제 치료가 필요합니다.<br>
&nbsp;&nbsp;- <b>심한 기침 + 열 + 호흡 곤란:</b> 폐렴 가능성이 있으니 반드시 진료를 받으세요.<br>
&nbsp;&nbsp;- <b>구토 + 설사 + 열:</b> 장염이나 식중독의 가능성이 있습니다. 탈수에 각별히 주의하세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 39.5도 이상의 고열이 하루 이상 지속되거나, 열과 함께 목이 뻣뻣하고 피부에 출혈성 붉은 반점이 생긴다면 수막염을 의심할 수 있으니 즉시 응급실을 방문하세요.
""",
}

INJURY = {
    "찰과상 및 상처": """
• <b>지혈:</b> 깨끗한 천이나 거즈로 상처 부위를 5~10분간 직접 압박하여 출혈을 멈춥니다.<br>
• <b>세척:</b> 출혈이 멈추면 흐르는 깨끗한 물로 상처를 충분히 씻어 이물질과 세균을 제거하세요.<br>
• <b>드레싱:</b> 소독 후 항균 연고를 얇게 바르고 밴드나 거즈로 덮어 상처를 보호합니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 압박을 해도 출혈이 멈추지 않거나, 상처가 깊고 벌어져 있다면 봉합이 필요할 수 있으니 병원을 방문하세요.
""",
    "염좌 및 타박상": """
• <b>RICE 원칙:</b> 초기 48시간은 Rest(휴식), Ice(얼음찜질), Compression(압박 붕대), Elevation(다친 부위 높이기)을 기억하세요.<br>
• <b>얼음찜질:</b> 얼음을 수건에 싸서 한 번에 15~20분씩, 하루 여러 차례 대어주면 붓기와 통증 완화에 효과적입니다.<br>
• <b>온찜질 전환:</b> 부상 후 48~72시간이 지나 급성 붓기가 가라앉으면 온찜질로 전환하여 혈액순환을 도와 회복을 촉진하세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 해당 부위를 전혀 디딜 수 없거나, 뼈가 튀어나온 것처럼 보이거나, 극심한 변형이 관찰된다면 골절 가능성이 있으니 즉시 병원을 방문하세요.
""",
}

# ─────────────────────────────────────────────
# 약 이미지 (식약처 및 공개 이미지 URL 사용)
# ─────────────────────────────────────────────
MEDICINE_IMGS = {
    "1. 해열진통제 (타이레놀 계열)": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600022", "타이레놀정500mg"),
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600048", "타이레놀8시간이알"),
    ],
    "2. 소염진통제 (부루펜 계열)": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600034", "이지엔6애니"),
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600035", "이지엔6프로"),
    ],
    "3. 종합감기약": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600019", "판콜에이"),
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600020", "판피린티정"),
    ],
    "4. 소화제": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600031", "훼스탈골드정"),
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600032", "베아제정"),
    ],
}

# 약 이미지 표시 헬퍼 (이미지 로드 실패 시 조용히 처리)
def drug_imgs_html(key):
    imgs = MEDICINE_IMGS.get(key, [])
    if not imgs:
        return ""
    cards = ""
    for url, name in imgs:
        cards += f"""
        <div class="drug-img-card">
            <img src="{url}" alt="{name}" onerror="this.style.display='none'">
            <span>{name}</span>
        </div>"""
    return f'<div class="drug-img-row">{cards}</div>'

MEDICINE = {
    "1. 해열진통제 (타이레놀 계열)": """
• <b>대표 상품:</b> 타이레놀정 500mg, 타이레놀 8시간 이알 서방정 (성분: 아세트아미노펜)<br>
• <b>언제 먹나요:</b> 두통, 치통, 생리통, 발열, 근육통, 신경통<br>
• <b>복용 방법:</b> 1회 1~2정(500~1,000mg), 4~6시간 간격으로 복용. 빈속에 먹어도 비교적 안전<br>
• <b>최대 복용량:</b> 성인 기준 1일 최대 4,000mg(500mg 기준 8정). 이를 절대 넘기지 마세요.<br>
• <b>알레르기 주의:</b> 아세트아미노펜에 과민반응 경험이 있는 경우 복용 금지. 복용 후 두드러기, 피부 발진, 호흡 곤란이 나타나면 즉시 복용 중단 후 병원 방문<br>
• <span class='urgent'>⚠️ 주의사항:</span> 술(알코올)과 함께 복용 시 간에 심각한 손상을 줄 수 있습니다. 다른 감기약·종합감기약과 함께 복용 시 아세트아미노펜 중복 가능성이 있으니 성분을 반드시 확인하세요.
""",
    "2. 소염진통제 (부루펜 계열)": """
• <b>대표 상품:</b> 이지엔6 애니, 이지엔6 프로, 부루펜 (성분: 이부프로펜, 덱시부프로펜)<br>
• <b>언제 먹나요:</b> 근육통, 관절염, 목감기(인후염), 심한 생리통, 타박상 통증<br>
• <b>복용 방법:</b> 반드시 식사 후에 복용 (위장 보호 필수)<br>
• <b>최대 복용량:</b> 이부프로펜 기준 성인 1일 최대 1,200mg(일반의약품), 덱시부프로펜 기준 1일 최대 900mg. 의사 처방 없이 이를 초과하지 마세요.<br>
• <b>알레르기 주의:</b> 아스피린 등 NSAIDs(비스테로이드성 소염제)에 의해 과거 천식 발작, 두드러기를 경험한 사람은 복용 금지. 아스피린 과민 천식 환자는 같은 계열 약물에 교차 반응이 생길 수 있습니다.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 빈속에 먹으면 속 쓰림·위염 유발 가능. 평소 위장이 약하거나, 신장 또는 심혈관 질환이 있는 사람은 복용 전 약사·의사와 상담하세요.
""",
    "3. 종합감기약": """
• <b>대표 상품:</b> 판콜에이, 판피린티정, 테라플루<br>
• <b>언제 먹나요:</b> 콧물, 코막힘, 기침, 몸살 기운이 동시에 있을 때<br>
• <b>복용 방법:</b> 초기 감기 증상 완화용. 식후 복용 권장<br>
• <b>최대 복용량:</b> 제품별 권장 용법을 반드시 지키세요. 대부분 성분에 아세트아미노펜이 포함되어 있어, 타이레놀 등과 중복 복용 시 하루 최대량(4,000mg)을 초과하기 쉽습니다.<br>
• <b>알레르기 주의:</b> 종합감기약에는 항히스타민제, 진통제, 충혈제거제 등 여러 성분이 혼합되어 있어 알레르기 반응이 나타날 경우 원인 성분을 파악하기 어렵습니다. 과거 특정 성분에 반응한 경험이 있다면 성분 목록을 꼼꼼히 확인하세요.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 강한 졸음을 유발하므로 운전·공부 전에 주의. 다른 진통제(타이레놀 등)와 절대 중복 복용 금지.
""",
    "4. 소화제": """
• <b>대표 상품:</b> 훼스탈 골드정(고체), 베아제정(고체), 까스베아제액(액체)<br>
• <b>언제 먹나요:</b> 과식 후 더부룩함, 소화가 잘 안 될 때, 명치가 답답할 때<br>
• <b>복용 방법:</b> 식후 바로 복용하는 것이 가장 효과적<br>
• <b>고체 vs 액체 소화제 차이:</b><br>
&nbsp;&nbsp;- <b>고체(정제·캡슐):</b> 훼스탈, 베아제 등. 소화 효소가 위장 전반에 걸쳐 천천히 작용해 과식이나 만성 소화 불량에 적합합니다.<br>
&nbsp;&nbsp;- <b>액체(시럽·드링크):</b> 까스베아제액 등. 이미 액체 상태라 체내 흡수가 상대적으로 빠르고, 속이 더부룩하거나 메스꺼울 때 삼키기 쉽습니다. 급성 불편감이나 고체 복용이 어려운 경우에 유리합니다.<br>
• <b>최대 복용량:</b> 소화제는 소화 효소 제제로, 권장 용량을 초과해도 효과가 비례해 커지지 않습니다. 제품별 1일 권장 용법(보통 1일 3회 식후)을 지키면 충분합니다.<br>
• <b>알레르기 주의:</b> 소화제 자체의 알레르기 반응은 드물지만, 첨가제(유당, 옥수수 전분 등)에 민감한 경우 발진·소화 이상이 생길 수 있습니다.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 복통이 심하거나 며칠째 지속된다면 소화제로 해결하려 하지 말고 병원을 방문하세요.
""",
}

# ─────────────────────────────────────────────
# 편의점 약 데이터
# ─────────────────────────────────────────────
CONVENIENCE_IMGS = {
    "💊 해열진통제": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600022", "타이레놀정500mg"),
    ],
    "🤢 소화제": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600031", "훼스탈"),
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600032", "베아제"),
    ],
    "🤧 감기약": [
        ("https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148604377754600019", "판콜에이"),
    ],
    "🩹 외용 상처약": [],
    "🏃 파스 (근육통)": [],
}

CONVENIENCE = {
    "💊 해열진통제": """
• <b>살 수 있는 약:</b> 타이레놀정 500mg (아세트아미노펜 500mg)<br>
• <b>언제 사나요:</b> 두통, 발열, 몸살이 갑자기 생겼을 때<br>
• <b>최대 복용량:</b> 성인 기준 1회 1~2정, 1일 최대 8정(4,000mg) 초과 금지<br>
• <b>알레르기 주의:</b> 복용 후 두드러기·발진·호흡 곤란이 나타나면 즉시 중단<br>
• <span class='urgent'>⚠️ 주의:</span> 편의점 약은 1~2회 응급용입니다. 증상이 지속되면 약국에서 구매하거나 병원을 방문하세요.
""",
    "🤢 소화제": """
• <b>살 수 있는 약:</b> 훼스탈 플러스정, 베아제정<br>
• <b>언제 사나요:</b> 과식 후 더부룩하거나 소화가 안 될 때<br>
• <b>복용 방법:</b> 식후 바로 복용<br>
• <b>최대 복용량:</b> 제품 권장 용법(1일 3회)을 초과하지 마세요<br>
• <span class='urgent'>⚠️ 주의:</span> 복통이 심하다면 병원 방문을 우선하세요.
""",
    "🤧 감기약": """
• <b>살 수 있는 약:</b> 판콜에이 내복액, 화이투벤 등<br>
• <b>언제 사나요:</b> 콧물, 코막힘, 가벼운 몸살 기운이 있을 때<br>
• <b>복용 방법:</b> 식후 복용, 졸음 유발 주의<br>
• <b>최대 복용량:</b> 제품별 1일 복용 횟수 준수. 아세트아미노펜 포함 제품이 많으므로 하루 4,000mg 초과 주의<br>
• <b>알레르기 주의:</b> 복용 후 발진, 호흡 곤란 등 이상 반응이 나타나면 즉시 중단<br>
• <span class='urgent'>⚠️ 주의:</span> 다른 진통제(타이레놀 등)와 절대 함께 먹으면 안 돼요.
""",
    "🩹 외용 상처약": """
• <b>살 수 있는 약:</b> 대일밴드, 후시딘 연고, 마데카솔 연고<br>
• <b>언제 사나요:</b> 가벼운 찰과상, 작은 상처가 났을 때<br>
• <b>사용 방법:</b> 상처를 물로 씻은 후 연고 바르고 밴드로 덮기<br>
• <b>알레르기 주의:</b> 항생제 성분(후시딘=퓨시딘산)에 알레르기가 있거나, 연고 사용 후 발진·가려움이 심해지면 사용 중단<br>
• <span class='urgent'>⚠️ 주의:</span> 상처가 깊거나 출혈이 심하면 병원에 가세요.
""",
    "🏃 파스 (근육통)": """
• <b>살 수 있는 약:</b> 제일파스, 신신파스에이, 쿨파스<br>
• <b>언제 사나요:</b> 근육통, 어깨 결림, 타박상 초기<br>
• <b>사용 방법:</b> 아픈 부위에 붙이고 4~8시간 후 제거. 같은 부위에 장시간 반복 부착 자제<br>
• <b>알레르기 주의:</b> 파스의 살리실산염 성분에 알레르기(특히 아스피린 과민 반응)가 있는 경우 주의. 피부에 발진·가려움이 생기면 즉시 제거<br>
• <span class='urgent'>⚠️ 주의:</span> 상처가 난 피부나 습진이 있는 부위에는 절대 붙이지 마세요.
""",
}

# ─────────────────────────────────────────────
# 지도 HTML (folium → Leaflet.js + OpenStreetMap)
# ─────────────────────────────────────────────
PHARMACY_MAP_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body { margin: 0; padding: 0; font-family: sans-serif; }
  #map { width: 100%; height: 560px; }
  .custom-popup .leaflet-popup-content-wrapper {
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  }
  .popup-name { font-size: 15px; font-weight: bold; color: #1a3a6b; margin-bottom: 6px; }
  .popup-row { font-size: 13px; color: #333; margin-top: 4px; line-height: 1.6; }
</style>
</head>
<body>
<div id="map"></div>
<script>
  var map = L.map('map').setView([37.6588, 127.1543], 15);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19
  }).addTo(map);

  var redIcon = L.divIcon({
    className: '',
    html: '<div style="background:#EA4335;width:14px;height:14px;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.4);"></div>',
    iconSize: [14, 14],
    iconAnchor: [7, 7],
    popupAnchor: [0, -10]
  });

  var pharmacies = [
    { name: "1. 하나로약국",      lat: 37.6601, lng: 127.1530, phone: "📞 031-571-7579", hours: "🕐 월~금 09:00~18:00 / 토 09:00~16:00 / 일 휴무" },
    { name: "2. 용한약국",        lat: 37.6595, lng: 127.1528, phone: "📞 031-527-1188", hours: "🕐 월~금 09:00~22:00 / 토 09:00~21:00 / 공휴일 10:00~22:00 / 일 휴무" },
    { name: "3. 소중한약국",      lat: 37.6589, lng: 127.1527, phone: "📞 031-571-7233", hours: "🕐 월~금 09:00~19:00 / 일 09:00~15:00 / 토·공휴일 휴무" },
    { name: "4. 세민약국",        lat: 37.6582, lng: 127.1529, phone: "📞 031-571-6734", hours: "🕐 월~금 09:00~20:00 / 토 09:00~21:00 / 공휴일 09:00~18:00 / 일 휴무" },
    { name: "5. 임약국",          lat: 37.6578, lng: 127.1561, phone: "📞 031-574-8484", hours: "🕐 월~목 09:00~20:00 / 금 09:00~18:00 / 토 09:00~15:00 / 일 09:00~18:00" },
    { name: "6. 참조은약국",      lat: 37.6574, lng: 127.1531, phone: "📞 031-574-1251", hours: "🕐 월~금 09:00~18:00 / 토 09:00~13:00 / 일 휴무" },
    { name: "7. 비젼약국",        lat: 37.6570, lng: 127.1558, phone: "📞 031-574-1008", hours: "🕐 월~금 09:00~18:30 / 토 09:00~14:00 / 일 휴무" },
    { name: "8. 참사랑약국",      lat: 37.6568, lng: 127.1572, phone: "📞 031-528-5767", hours: "🕐 월~금 09:00~20:00 / 토 09:00~21:00 / 일 휴무" },
    { name: "9. 문온누리약국",    lat: 37.6561, lng: 127.1530, phone: "📞 031-572-0409", hours: "🕐 월·수·금 08:00~21:00 / 화·목 08:00~19:00 / 토·일 08:00~16:00" },
    { name: "10. 굿모닝약국",     lat: 37.6556, lng: 127.1558, phone: "📞 031-572-7749", hours: "🕐 월~금 09:00~13:00 / 토 09:00~16:00 / 일 휴무" },
    { name: "11. 미엘약국",       lat: 37.6547, lng: 127.1530, phone: "📞 031-571-2147", hours: "🕐 월~금 09:00~21:00 / 토·일·공휴일 09:00~18:00" },
    { name: "12. 정안약국",       lat: 37.6534, lng: 127.1530, phone: "📞 031-571-9574", hours: "🕐 월~금 09:00~20:30 / 토 09:00~17:00 / 일 휴무" }
  ];

  pharmacies.forEach(function(p) {
    var popupContent =
      '<div class="popup-name">🏥 ' + p.name + '</div>' +
      '<div class="popup-row">' + p.phone + '</div>' +
      '<div class="popup-row">' + p.hours + '</div>';
    L.marker([p.lat, p.lng], { icon: redIcon })
      .bindPopup(popupContent, { className: 'custom-popup', maxWidth: 280 })
      .addTo(map);
  });
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────
# 상태 초기화 함수
# ─────────────────────────────────────────────
def reset():
    st.session_state.menu = None
    st.session_state.symptom = None
    st.session_state.injury = None
    st.session_state.medicine = None
    st.session_state.convenience = None

def go_back_menu():
    st.session_state.menu = None
    st.session_state.symptom = None
    st.session_state.injury = None
    st.session_state.medicine = None
    st.session_state.convenience = None

def go_back_symptom():
    st.session_state.symptom = None
    st.session_state.injury = None

def go_back_injury():
    st.session_state.injury = None

def go_back_medicine():
    st.session_state.medicine = None

def go_back_convenience():
    st.session_state.convenience = None

for key in ["menu", "symptom", "injury", "medicine", "convenience"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ─────────────────────────────────────────────
# UI 렌더링
# ─────────────────────────────────────────────
st.markdown("## 🏥 보건 도우미")
st.markdown("---")

# ── 메인 메뉴 ─────────────────────────────────
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

# ── 증상 가이드 ───────────────────────────────
elif st.session_state.menu == "guide":
    if st.session_state.symptom is None:
        st.markdown("### 💊 증상별 대처 가이드")
        st.markdown("해당하는 증상을 선택하세요.")
        for label in list(GUIDE.keys()) + ["4. 다쳤어요 (근육통/외상)"]:
            if st.button(label):
                st.session_state.symptom = label
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 페이지"):
                go_back_menu()
                st.rerun()
        with col2:
            if st.button("🔄 처음으로 돌아가기", key="reset_guide_list"):
                reset()
                st.rerun()

    elif st.session_state.symptom == "4. 다쳤어요 (근육통/외상)":
        if st.session_state.injury is None:
            st.markdown("### 🩹 어떻게 다쳤나요?")
            for label in INJURY.keys():
                if st.button(label):
                    st.session_state.injury = label
                    st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ 이전 페이지"):
                    go_back_symptom()
                    st.rerun()
            with col2:
                if st.button("🔄 처음으로 돌아가기", key="reset_injury_list"):
                    reset()
                    st.rerun()
        else:
            st.markdown(f"### 🩹 {st.session_state.injury}")
            st.markdown(f"<div class='result-box'>{INJURY[st.session_state.injury]}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ 이전 페이지"):
                    go_back_injury()
                    st.rerun()
            with col2:
                if st.button("🔄 처음으로 돌아가기", key="reset_injury_detail"):
                    reset()
                    st.rerun()
    else:
        st.markdown(f"### {st.session_state.symptom}")
        st.markdown(f"<div class='result-box'>{GUIDE[st.session_state.symptom]}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 페이지"):
                go_back_symptom()
                st.rerun()
        with col2:
            if st.button("🔄 처음으로 돌아가기", key="reset_symptom_detail"):
                reset()
                st.rerun()

# ── 상비약 백과 ───────────────────────────────
elif st.session_state.menu == "medicine":
    if st.session_state.medicine is None:
        st.markdown("### 🏠 우리 집 상비약 백과")
        st.markdown("알고 싶은 약을 선택하세요.")
        for label in MEDICINE.keys():
            if st.button(label):
                st.session_state.medicine = label
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 페이지"):
                go_back_menu()
                st.rerun()
        with col2:
            if st.button("🔄 처음으로 돌아가기", key="reset_med_list"):
                reset()
                st.rerun()
    else:
        st.markdown(f"### {st.session_state.medicine}")
        imgs_html = drug_imgs_html(st.session_state.medicine)
        st.markdown(
            f"<div class='result-box'>{imgs_html}{MEDICINE[st.session_state.medicine]}</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 페이지"):
                go_back_medicine()
                st.rerun()
        with col2:
            if st.button("🔄 처음으로 돌아가기", key="reset_med_detail"):
                reset()
                st.rerun()

# ── 주변 약국 ─────────────────────────────────
elif st.session_state.menu == "pharmacy":
    st.markdown("### 🗺️ 주변 약국 찾기")
    st.markdown("📍 지도의 빨간 마커를 클릭하면 약국 이름·전화번호·운영시간이 표시됩니다.")
    components.html(PHARMACY_MAP_HTML, height=580, scrolling=False)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전 페이지"):
            go_back_menu()
            st.rerun()
    with col2:
        if st.button("🔄 처음으로 돌아가기", key="reset_pharmacy"):
            reset()
            st.rerun()

# ── 편의점 상비약 ─────────────────────────────
elif st.session_state.menu == "convenience":
    if st.session_state.convenience is None:
        st.markdown("### 🏪 편의점 상비약 안내")
        st.markdown("알고 싶은 약 종류를 선택하세요.")
        for label in CONVENIENCE.keys():
            if st.button(label):
                st.session_state.convenience = label
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 페이지"):
                go_back_menu()
                st.rerun()
        with col2:
            if st.button("🔄 처음으로 돌아가기", key="reset_conv_list"):
                reset()
                st.rerun()
    else:
        st.markdown(f"### {st.session_state.convenience}")
        imgs_html = ""
        imgs = CONVENIENCE_IMGS.get(st.session_state.convenience, [])
        if imgs:
            cards = "".join(
                f'<div class="drug-img-card"><img src="{u}" alt="{n}" onerror="this.style.display=\'none\'"><span>{n}</span></div>'
                for u, n in imgs
            )
            imgs_html = f'<div class="drug-img-row">{cards}</div>'
        st.markdown(
            f"<div class='result-box'>{imgs_html}{CONVENIENCE[st.session_state.convenience]}</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 페이지"):
                go_back_convenience()
                st.rerun()
        with col2:
            if st.button("🔄 처음으로 돌아가기", key="reset_conv_detail"):
                reset()
                st.rerun()
