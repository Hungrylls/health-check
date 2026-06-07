import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보건 체크", page_icon="🏥", layout="centered")

st.markdown("""
<style>
.main { background-color: #f0f7ff; }
.stButton > button {
    width:100%; height:60px; font-size:17px; font-weight:bold;
    border-radius:14px; margin-bottom:8px; border:none;
    background-color:#4A90D9; color:white; transition:0.2s;
}
.stButton > button:hover { background-color:#2c6fad; transform:scale(1.02); }
.result-box {
    background-color:#ffffff; border-left:6px solid #4A90D9;
    border-radius:12px; padding:20px 24px; margin-top:10px;
    font-size:16px; color:#1a1a2e;
    box-shadow:0 2px 12px rgba(0,0,0,0.08); line-height:2;
}
.urgent { color:#cc0000; font-weight:bold; }
.drug-img-row { display:flex; gap:16px; flex-wrap:wrap; margin:10px 0 8px 0; }
.drug-card {
    text-align:center; font-size:12px; color:#555;
    background:#f4f8ff; border:1px solid #d0e4f7;
    border-radius:12px; padding:10px 12px; min-width:100px;
}
.drug-card svg { display:block; margin:0 auto 6px auto; }
.drug-name { font-weight:600; color:#1a3a6b; font-size:13px; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 약 아이콘 SVG (인라인, 외부 URL 없음 → 항상 표시)
# ─────────────────────────────────────────────────────────────
SVG = {
    "pill_white": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="40" cy="40" rx="34" ry="22" fill="#f0f0f0" stroke="#bbb" stroke-width="2"/>
  <line x1="6" y1="40" x2="74" y2="40" stroke="#bbb" stroke-width="2"/>
  <ellipse cx="40" cy="40" rx="34" ry="22" fill="none" stroke="#999" stroke-width="1.5"/>
  <text x="40" y="46" text-anchor="middle" font-size="11" fill="#555" font-family="sans-serif">정제</text>
</svg>""",
    "pill_red": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="40" cy="40" rx="34" ry="22" fill="#ffe0e0" stroke="#e07070" stroke-width="2"/>
  <ellipse cx="22" cy="40" rx="16" ry="22" fill="#ffb3b3" stroke="#e07070" stroke-width="1.5"/>
  <text x="40" y="46" text-anchor="middle" font-size="10" fill="#c00" font-family="sans-serif">해열</text>
</svg>""",
    "pill_orange": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="40" cy="40" rx="34" ry="22" fill="#ffe8cc" stroke="#e09040" stroke-width="2"/>
  <ellipse cx="22" cy="40" rx="16" ry="22" fill="#ffc080" stroke="#e09040" stroke-width="1.5"/>
  <text x="40" y="46" text-anchor="middle" font-size="10" fill="#a05000" font-family="sans-serif">소염</text>
</svg>""",
    "pill_blue": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="28" width="60" height="24" rx="12" fill="#cce0ff" stroke="#5080c0" stroke-width="2"/>
  <rect x="10" y="28" width="30" height="24" rx="12" fill="#90b8f0" stroke="#5080c0" stroke-width="1.5"/>
  <text x="40" y="44" text-anchor="middle" font-size="10" fill="#1a3a8c" font-family="sans-serif">감기약</text>
</svg>""",
    "digestive": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <circle cx="40" cy="40" r="28" fill="#e8f5e9" stroke="#60b060" stroke-width="2"/>
  <text x="40" y="36" text-anchor="middle" font-size="11" fill="#2e7d32" font-family="sans-serif">소화</text>
  <text x="40" y="50" text-anchor="middle" font-size="11" fill="#2e7d32" font-family="sans-serif">효소</text>
</svg>""",
    "liquid": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="28" y="18" width="24" height="44" rx="6" fill="#e0f0ff" stroke="#4090d0" stroke-width="2"/>
  <rect x="33" y="12" width="14" height="8" rx="3" fill="#b0d4f0" stroke="#4090d0" stroke-width="1.5"/>
  <rect x="28" y="42" width="24" height="20" rx="0 0 6 6" fill="#90c8f0"/>
  <text x="40" y="62" text-anchor="middle" font-size="9" fill="#1a5080" font-family="sans-serif">액체</text>
</svg>""",
    "bandage": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="30" width="64" height="20" rx="10" fill="#fce8c8" stroke="#d4943a" stroke-width="2"/>
  <rect x="26" y="30" width="28" height="20" fill="#fff5e0" stroke="#d4943a" stroke-width="1"/>
  <circle cx="32" cy="36" r="2" fill="#d4943a"/><circle cx="32" cy="44" r="2" fill="#d4943a"/>
  <circle cx="48" cy="36" r="2" fill="#d4943a"/><circle cx="48" cy="44" r="2" fill="#d4943a"/>
  <text x="40" y="62" text-anchor="middle" font-size="10" fill="#8a5000" font-family="sans-serif">밴드</text>
</svg>""",
    "ointment": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="35" width="40" height="28" rx="5" fill="#d0f0d0" stroke="#40a040" stroke-width="2"/>
  <rect x="28" y="25" width="24" height="12" rx="4" fill="#a0d8a0" stroke="#40a040" stroke-width="1.5"/>
  <text x="40" y="56" text-anchor="middle" font-size="9" fill="#1a6020" font-family="sans-serif">연고</text>
</svg>""",
    "patch": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="20" width="52" height="40" rx="8" fill="#fff0cc" stroke="#c0903a" stroke-width="2"/>
  <line x1="14" y1="35" x2="66" y2="35" stroke="#c0903a" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="14" y1="50" x2="66" y2="50" stroke="#c0903a" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="40" y="44" text-anchor="middle" font-size="11" fill="#7a5000" font-family="sans-serif">파스</text>
</svg>""",
    "tablet_box": """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="22" width="56" height="36" rx="6" fill="#e8eeff" stroke="#7080d0" stroke-width="2"/>
  <circle cx="30" cy="40" r="8" fill="#b0bef0" stroke="#7080d0" stroke-width="1.5"/>
  <circle cx="50" cy="40" r="8" fill="#b0bef0" stroke="#7080d0" stroke-width="1.5"/>
  <text x="40" y="70" text-anchor="middle" font-size="10" fill="#3040a0" font-family="sans-serif">정제</text>
</svg>""",
}

DRUG_ICONS = {
    "1. 해열진통제 (타이레놀 계열)": [
        (SVG["pill_red"],    "타이레놀정 500mg",    "아세트아미노펜"),
        (SVG["tablet_box"],  "타이레놀 8시간이알",   "서방정"),
    ],
    "2. 소염진통제 (부루펜 계열)": [
        (SVG["pill_orange"], "이지엔6 애니",         "덱시부프로펜"),
        (SVG["pill_orange"], "이지엔6 프로",         "이부프로펜"),
    ],
    "3. 종합감기약": [
        (SVG["pill_blue"],   "판콜에이",             "복합성분"),
        (SVG["pill_blue"],   "판피린티정",           "복합성분"),
    ],
    "4. 소화제": [
        (SVG["digestive"],   "훼스탈 골드정",        "고체 소화효소"),
        (SVG["liquid"],      "까스베아제액",         "액체 소화효소"),
    ],
    "💊 해열진통제": [
        (SVG["pill_red"],    "타이레놀정 500mg",    "아세트아미노펜"),
    ],
    "🤢 소화제": [
        (SVG["digestive"],   "훼스탈 플러스정",      "소화효소"),
    ],
    "🤧 감기약": [
        (SVG["pill_blue"],   "판콜에이",             "복합성분"),
    ],
    "🩹 외용 상처약": [
        (SVG["bandage"],     "대일밴드",             "상처보호"),
        (SVG["ointment"],    "후시딘/마데카솔",      "항균연고"),
    ],
    "🏃 파스 (근육통)": [
        (SVG["patch"],       "신신파스에이",         "살리실산"),
        (SVG["patch"],       "제일파스",             "쿨파스"),
    ],
}

def render_icons(key):
    items = DRUG_ICONS.get(key, [])
    if not items:
        return ""
    cards = ""
    for svg, name, sub in items:
        cards += f'''<div class="drug-card">{svg}
          <div class="drug-name">{name}</div>
          <div style="font-size:11px;color:#888;">{sub}</div>
        </div>'''
    return f'<div class="drug-img-row">{cards}</div>'

# ─────────────────────────────────────────────────────────────
# 증상 / 부상 / 약 데이터
# ─────────────────────────────────────────────────────────────
GUIDE = {
    "1. 머리가 아파요 (두통)": """
• <b>환경 조성:</b> 빛과 소리에 예민해질 수 있으니 방을 어둡게 하고 조용한 곳에서 쉬세요.<br>
• <b>수분 섭취:</b> 탈수가 두통의 흔한 원인 중 하나입니다. 미지근한 물을 충분히 마셔주세요.<br>
• <b>디지털 디톡스:</b> 스마트폰·컴퓨터 화면은 눈의 피로를 높여 두통을 악화시킵니다. 화면 사용을 멈추고 눈을 감고 쉬세요.<br>
• <b>자세 점검 &amp; 스트레칭:</b> 목과 어깨 근육이 뭉치면 긴장성 두통으로 이어지는 경우가 많습니다. 목을 천천히 좌우로 기울이고, 어깨를 크게 으쓱했다가 내리는 스트레칭을 해보세요.<br>
• <b>스트레스 점검:</b> 스트레스와 수면 부족은 긴장성 두통의 대표적인 원인입니다. 최근 스트레스를 많이 받은 일이 있었는지 돌아보고, 복식호흡이나 잠깐의 명상으로 긴장을 풀어보세요.<br>
• <span class='urgent'>⚠️ 긴급:</span> 망치로 맞은 듯한 극심한 통증이 갑자기 시작되거나, 시야가 흐려지거나, 말이 어눌해지거나, 손발 마비 느낌이 든다면 즉시 응급실로 가야 합니다.
""",
    "2. 배가 아파요 (복통/소화불량)": """
• <b>온찜질:</b> 따뜻한 수건이나 핫팩을 배에 대어 장 근육을 이완시켜 주세요. 오른쪽 아랫배 통증 시엔 온찜질을 피하세요.<br>
• <b>자세 조절:</b> 상체를 약간 높이거나 옆으로 눕는 것이 통증 완화에 도움이 됩니다.<br>
• <b>금식 &amp; 식이 조절:</b> 속이 진정될 때까지는 자극적인 음식과 탄산음료를 피하고 미음이나 죽을 드세요.<br>
• <b>스트레스 점검:</b> 스트레스는 장 운동을 직접 교란합니다. 만성적인 복통과 설사·변비가 반복된다면 <b>과민성 대장 증후군(IBS)</b> 가능성이 있습니다. 복식호흡·산책 등 긴장 해소가 증상 완화에 도움이 됩니다.<br>
• <span class='urgent'>⚠️ 긴급:</span> 오른쪽 아랫배를 눌렀다 뗄 때 극심한 통증이 느껴지면 맹장염 가능성이 있습니다. 혈변, 극심한 복통, 배가 딱딱해지는 증상이 나타나면 즉시 병원을 방문하세요.
""",
    "3. 열이 나고 몸이 떨려요 (발열/감기)": """
• <b>체온 조절:</b> 두꺼운 이불로 억지로 땀을 빼지 마세요. 얇은 이불을 덮고 체온이 자연스럽게 내려가도록 도와주세요.<br>
• <b>수분 및 전해질 보충:</b> 열로 땀이 많이 나면 탈수가 올 수 있습니다. 물, 이온음료를 조금씩 자주 마셔 주세요.<br>
• <b>미온수 마사지:</b> 38도 이상 고열 지속 시 30~32°C 미온수 수건으로 팔·다리·이마를 부드럽게 닦으면 체온 낮추기에 도움이 됩니다.<br>
• <b>동반 증상 주의:</b><br>
&nbsp;&nbsp;- <b>심한 인후통 + 열:</b> 세균성 편도염 가능성, 항생제 치료 필요할 수 있으니 병원 방문<br>
&nbsp;&nbsp;- <b>피부 붉은 발진 + 열:</b> 홍역, 성홍열, 약물 알레르기 의심<br>
&nbsp;&nbsp;- <b>소변 시 통증 + 열:</b> 요로감염 또는 신우신염 가능성<br>
&nbsp;&nbsp;- <b>심한 기침 + 열 + 호흡 곤란:</b> 폐렴 가능성, 즉시 진료 필요<br>
&nbsp;&nbsp;- <b>구토 + 설사 + 열:</b> 장염·식중독 가능성, 탈수 주의<br>
• <span class='urgent'>⚠️ 긴급:</span> 39.5도 이상 고열이 하루 이상 지속되거나, 열과 함께 목이 뻣뻣하고 출혈성 반점이 생기면 즉시 응급실을 방문하세요.
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

MEDICINE = {
    "1. 해열진통제 (타이레놀 계열)": """
• <b>대표 상품:</b> 타이레놀정 500mg, 타이레놀 8시간 이알 서방정 (성분: 아세트아미노펜)<br>
• <b>언제 먹나요:</b> 두통, 치통, 생리통, 발열, 근육통, 신경통<br>
• <b>복용 방법:</b> 1회 1~2정(500~1,000mg), 4~6시간 간격. 빈속에 먹어도 비교적 안전<br>
• <b>최대 복용량:</b> 성인 기준 1일 최대 4,000mg(500mg 기준 하루 8정). 절대 초과 금지<br>
• <b>알레르기 주의:</b> 복용 후 두드러기·피부 발진·호흡 곤란이 나타나면 즉시 중단 후 병원 방문<br>
• <span class='urgent'>⚠️ 주의사항:</span> 음주자는 간 손상 위험이 크게 증가합니다. 다른 감기약과 중복 복용 시 아세트아미노펜 과다 복용 위험 — 성분을 반드시 확인하세요.
""",
    "2. 소염진통제 (부루펜 계열)": """
• <b>대표 상품:</b> 이지엔6 애니, 이지엔6 프로, 부루펜 (성분: 이부프로펜, 덱시부프로펜)<br>
• <b>언제 먹나요:</b> 근육통, 관절염, 목감기(인후염), 심한 생리통, 타박상 통증<br>
• <b>복용 방법:</b> 반드시 식사 후에 복용 (위장 보호 필수)<br>
• <b>최대 복용량:</b> 이부프로펜 성인 1일 최대 1,200mg, 덱시부프로펜 1일 최대 900mg<br>
• <b>알레르기 주의:</b> 아스피린 등 NSAIDs에 의해 과거 천식 발작·두드러기를 경험한 사람은 복용 금지<br>
• <span class='urgent'>⚠️ 주의사항:</span> 빈속 복용 시 속 쓰림·위염 유발 가능. 신장·심혈관 질환자는 복용 전 의사·약사와 상담하세요.
""",
    "3. 종합감기약": """
• <b>대표 상품:</b> 판콜에이, 판피린티정, 테라플루<br>
• <b>언제 먹나요:</b> 콧물, 코막힘, 기침, 몸살 기운이 동시에 있을 때<br>
• <b>복용 방법:</b> 초기 감기 증상 완화용. 식후 복용 권장<br>
• <b>최대 복용량:</b> 제품별 1일 권장 용법 준수. 대부분 아세트아미노펜 포함 → 타이레놀 등과 중복 복용 시 1일 4,000mg 초과 위험<br>
• <b>알레르기 주의:</b> 여러 성분이 혼합되어 있어, 과거 특정 성분에 반응 경험이 있다면 성분 목록을 꼼꼼히 확인하세요.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 강한 졸음 유발 — 운전·공부 전 주의. 다른 진통제(타이레놀 등)와 절대 중복 복용 금지.
""",
    "4. 소화제": """
• <b>대표 상품:</b> 훼스탈 골드정(고체), 베아제정(고체), 까스베아제액(액체)<br>
• <b>언제 먹나요:</b> 과식 후 더부룩함, 소화가 잘 안 될 때, 명치가 답답할 때<br>
• <b>복용 방법:</b> 식후 바로 복용이 가장 효과적<br>
• <b>고체 vs 액체 소화제:</b><br>
&nbsp;&nbsp;- <b>고체(정제·캡슐):</b> 소화 효소가 위장 전반에 천천히 작용해 과식·만성 소화 불량에 적합<br>
&nbsp;&nbsp;- <b>액체(드링크):</b> 흡수가 상대적으로 빠르고 삼키기 쉬워 급성 불편감·고체 복용 어려울 때 유리<br>
• <b>최대 복용량:</b> 1일 3회 식후 기준을 지키면 충분. 초과해도 효과가 비례해 증가하지 않음<br>
• <b>알레르기 주의:</b> 첨가제(유당, 옥수수 전분 등)에 민감한 경우 발진·소화 이상이 생길 수 있습니다.<br>
• <span class='urgent'>⚠️ 주의사항:</span> 복통이 심하거나 며칠째 지속된다면 소화제 대신 병원을 방문하세요.
""",
}

CONVENIENCE = {
    "💊 해열진통제": """
• <b>살 수 있는 약:</b> 타이레놀정 500mg (아세트아미노펜 500mg)<br>
• <b>언제 사나요:</b> 두통, 발열, 몸살이 갑자기 생겼을 때<br>
• <b>최대 복용량:</b> 성인 기준 1회 1~2정, 1일 최대 8정(4,000mg) 초과 금지<br>
• <b>알레르기 주의:</b> 복용 후 두드러기·발진·호흡 곤란이 나타나면 즉시 중단<br>
• <span class='urgent'>⚠️ 주의:</span> 편의점 약은 1~2회 응급용입니다. 증상이 지속되면 약국 또는 병원을 방문하세요.
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
• <b>알레르기 주의:</b> 복용 후 발진·호흡 곤란 등 이상 반응이 나타나면 즉시 중단<br>
• <span class='urgent'>⚠️ 주의:</span> 다른 진통제(타이레놀 등)와 절대 함께 먹으면 안 돼요.
""",
    "🩹 외용 상처약": """
• <b>살 수 있는 약:</b> 대일밴드, 후시딘 연고, 마데카솔 연고<br>
• <b>언제 사나요:</b> 가벼운 찰과상, 작은 상처가 났을 때<br>
• <b>사용 방법:</b> 상처를 물로 씻은 후 연고 바르고 밴드로 덮기<br>
• <b>알레르기 주의:</b> 항생제 성분(후시딘=퓨시딘산)에 알레르기가 있거나, 사용 후 발진·가려움이 심해지면 즉시 중단<br>
• <span class='urgent'>⚠️ 주의:</span> 상처가 깊거나 출혈이 심하면 병원에 가세요.
""",
    "🏃 파스 (근육통)": """
• <b>살 수 있는 약:</b> 제일파스, 신신파스에이, 쿨파스<br>
• <b>언제 사나요:</b> 근육통, 어깨 결림, 타박상 초기<br>
• <b>사용 방법:</b> 아픈 부위에 붙이고 4~8시간 후 제거. 같은 부위 장시간 반복 부착 자제<br>
• <b>알레르기 주의:</b> 살리실산염 성분에 알레르기(아스피린 과민 반응)가 있는 경우 주의. 피부에 발진·가려움이 생기면 즉시 제거<br>
• <span class='urgent'>⚠️ 주의:</span> 상처가 난 피부나 습진 부위에는 절대 붙이지 마세요.
""",
}

# ─────────────────────────────────────────────────────────────
# 지도 (실제 Google Places 좌표)
# ─────────────────────────────────────────────────────────────
PHARMACY_MAP_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
body{margin:0;padding:0;font-family:sans-serif;}
#map{width:100%;height:560px;}
.pname{font-size:15px;font-weight:bold;color:#1a3a6b;margin-bottom:6px;}
.prow{font-size:13px;color:#333;margin-top:4px;line-height:1.6;}
.leaflet-popup-content-wrapper{border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,.18);}
</style>
</head>
<body>
<div id="map"></div>
<script>
var map = L.map('map').setView([37.6530, 127.1430], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
  attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom:19
}).addTo(map);

function mkIcon(n){
  return L.divIcon({className:'',
    html:'<div style="background:#EA4335;color:#fff;width:28px;height:28px;border-radius:50%;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;line-height:1;">'+n+'</div>',
    iconSize:[28,28],iconAnchor:[14,14],popupAnchor:[0,-16]
  });
}

// ★ Google Places API로 확인한 실제 좌표
//   비젼·문온누리·미엘·정안은 전화번호 기반 인접 추정
var data=[
  {n:"1. 하나로약국",   lat:37.6566,lng:127.1436,ph:"📞 031-571-7579",hr:"🕐 월~금 09:00~18:00 / 토 09:00~16:00 / 일 휴무"},
  {n:"2. 용한약국",     lat:37.6552,lng:127.1440,ph:"📞 031-527-1188",hr:"🕐 월~금 09:00~22:00 / 토 09:00~21:00 / 공휴일 10:00~22:00 / 일 휴무"},
  {n:"3. 소중한약국",   lat:37.6524,lng:127.1428,ph:"📞 031-571-7233",hr:"🕐 월~금 09:00~19:00 / 일 09:00~15:00 / 토·공휴일 휴무"},
  {n:"4. 세민약국",     lat:37.6514,lng:127.1418,ph:"📞 031-571-6734",hr:"🕐 월~금 09:00~20:00 / 토 09:00~21:00 / 공휴일 09:00~18:00 / 일 휴무"},
  {n:"5. 임약국",       lat:37.6512,lng:127.1424,ph:"📞 031-574-8484",hr:"🕐 월~목 09:00~20:00 / 금 09:00~18:00 / 토 09:00~15:00 / 일 09:00~18:00"},
  {n:"6. 참조은약국",   lat:37.6509,lng:127.1421,ph:"📞 031-574-1251",hr:"🕐 월~금 09:00~18:00 / 토 09:00~13:00 / 일 휴무"},
  {n:"7. 비젼약국",     lat:37.6505,lng:127.1420,ph:"📞 031-574-1008",hr:"🕐 월~금 09:00~18:30 / 토 09:00~14:00 / 일 휴무"},
  {n:"8. 참사랑약국",   lat:37.6505,lng:127.1419,ph:"📞 031-528-5767",hr:"🕐 월~금 09:00~20:00 / 토 09:00~21:00 / 일 휴무"},
  {n:"9. 문온누리약국", lat:37.6499,lng:127.1417,ph:"📞 031-572-0409",hr:"🕐 월·수·금 08:00~21:00 / 화·목 08:00~19:00 / 토·일 08:00~16:00"},
  {n:"10. 굿모닝약국",  lat:37.6493,lng:127.1412,ph:"📞 031-572-7749",hr:"🕐 월~금 09:00~13:00 / 토 09:00~16:00 / 일 휴무"},
  {n:"11. 미엘약국",    lat:37.6487,lng:127.1412,ph:"📞 031-571-2147",hr:"🕐 월~금 09:00~21:00 / 토·일·공휴일 09:00~18:00"},
  {n:"12. 정안약국",    lat:37.6479,lng:127.1413,ph:"📞 031-571-9574",hr:"🕐 월~금 09:00~20:30 / 토 09:00~17:00 / 일 휴무"}
];

data.forEach(function(p,i){
  var pop='<div class="pname">🏥 '+p.n+'</div>'
         +'<div class="prow">'+p.ph+'</div>'
         +'<div class="prow">'+p.hr+'</div>';
  L.marker([p.lat,p.lng],{icon:mkIcon(i+1)})
   .bindPopup(pop,{maxWidth:300}).addTo(map);
});
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────
# 상태 초기화
# ─────────────────────────────────────────────────────────────
for k in ["menu","symptom","injury","medicine","convenience"]:
    if k not in st.session_state:
        st.session_state[k] = None

def reset():
    for k in ["menu","symptom","injury","medicine","convenience"]:
        st.session_state[k] = None

def ss(**kw):
    for k,v in kw.items():
        st.session_state[k] = v

def nav(back_fn, bk, rs):
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ 이전 페이지", key=bk):
            back_fn(); st.rerun()
    with c2:
        if st.button("🔄 처음으로 돌아가기", key=rs):
            reset(); st.rerun()

# ─────────────────────────────────────────────────────────────
# UI 렌더링
# ─────────────────────────────────────────────────────────────
st.markdown("## 🏥 보건 도우미")
st.markdown("---")

if st.session_state.menu is None:
    st.markdown("### 원하는 항목을 선택하세요")
    if st.button("💊 [1] 증상별 대처 가이드"):   ss(menu="guide");       st.rerun()
    if st.button("🏠 [2] 우리 집 상비약 백과"):  ss(menu="medicine");     st.rerun()
    if st.button("🗺️ [3] 주변 약국 찾기"):       ss(menu="pharmacy");     st.rerun()
    if st.button("🏪 [4] 편의점 상비약 안내"):   ss(menu="convenience");  st.rerun()

elif st.session_state.menu == "guide":
    if st.session_state.symptom is None:
        st.markdown("### 💊 증상별 대처 가이드")
        for label in list(GUIDE.keys()) + ["4. 다쳤어요 (근육통/외상)"]:
            if st.button(label): ss(symptom=label); st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        nav(lambda: ss(menu=None), "bk_g0","rs_g0")
    elif st.session_state.symptom == "4. 다쳤어요 (근육통/외상)":
        if st.session_state.injury is None:
            st.markdown("### 🩹 어떻게 다쳤나요?")
            for label in INJURY.keys():
                if st.button(label): ss(injury=label); st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            nav(lambda: ss(symptom=None), "bk_g1","rs_g1")
        else:
            st.markdown(f"### 🩹 {st.session_state.injury}")
            st.markdown(f"<div class='result-box'>{INJURY[st.session_state.injury]}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            nav(lambda: ss(injury=None), "bk_g2","rs_g2")
    else:
        st.markdown(f"### {st.session_state.symptom}")
        st.markdown(f"<div class='result-box'>{GUIDE[st.session_state.symptom]}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        nav(lambda: ss(symptom=None), "bk_g3","rs_g3")

elif st.session_state.menu == "medicine":
    if st.session_state.medicine is None:
        st.markdown("### 🏠 우리 집 상비약 백과")
        for label in MEDICINE.keys():
            if st.button(label): ss(medicine=label); st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        nav(lambda: ss(menu=None), "bk_m0","rs_m0")
    else:
        st.markdown(f"### {st.session_state.medicine}")
        st.markdown(
            f"<div class='result-box'>{render_icons(st.session_state.medicine)}{MEDICINE[st.session_state.medicine]}</div>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        nav(lambda: ss(medicine=None), "bk_m1","rs_m1")

elif st.session_state.menu == "pharmacy":
    st.markdown("### 🗺️ 주변 약국 찾기")
    st.markdown("📍 번호 마커를 클릭하면 약국 정보가 표시됩니다.")
    components.html(PHARMACY_MAP_HTML, height=580, scrolling=False)
    st.markdown("<br>", unsafe_allow_html=True)
    nav(lambda: ss(menu=None), "bk_p0","rs_p0")

elif st.session_state.menu == "convenience":
    if st.session_state.convenience is None:
        st.markdown("### 🏪 편의점 상비약 안내")
        for label in CONVENIENCE.keys():
            if st.button(label): ss(convenience=label); st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        nav(lambda: ss(menu=None), "bk_c0","rs_c0")
    else:
        st.markdown(f"### {st.session_state.convenience}")
        st.markdown(
            f"<div class='result-box'>{render_icons(st.session_state.convenience)}{CONVENIENCE[st.session_state.convenience]}</div>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        nav(lambda: ss(convenience=None), "bk_c1","rs_c1")
