import streamlit as st
from PIL import Image
import base64
import re
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Scan Eat!", page_icon="🌿", layout="centered")

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False
if "show_upload" not in st.session_state:
    st.session_state.show_upload = False
if "selected_guide" not in st.session_state:
    st.session_state.selected_guide = None
if "result_html" not in st.session_state:
    st.session_state.result_html = ""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
* { font-family: 'Nunito', sans-serif; box-sizing: border-box; }
body, .main, .block-container { background: #d9f0db !important; padding: 0 !important; }
#MainMenu, header, footer { visibility: hidden; }
.block-container { max-width: 420px !important; margin: 0 auto !important; padding: 0 0 2rem 0 !important; }

.sbar {
    background: #111; color: #fff;
    padding: 14px 28px 8px;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 12px; font-weight: 700;
}
.hdr {
    background: linear-gradient(135deg, #1b5e20, #388e3c, #66bb6a);
    padding: 20px 24px 24px; color: white; position: relative; overflow: hidden;
}
.hdr::before {
    content: ''; position: absolute; width: 180px; height: 180px;
    background: rgba(255,255,255,0.07); border-radius: 50%; top: -50px; right: -30px;
}
.hdr-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.logo { font-size: 26px; font-weight: 900; color: #fff; }
.logo em { color: #b9f6ca; font-style: normal; }
.ava { width: 36px; height: 36px; background: rgba(255,255,255,0.2); border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
    border: 2px solid rgba(255,255,255,0.35); }
.hdr-sub { color: rgba(255,255,255,0.8); font-size: 13px; font-weight: 600; }
.hdr-main { color: #fff; font-size: 16px; font-weight: 800; margin-top: 2px; }

.scroll-body { background: #f7faf7; padding-bottom: 24px; }
.sec { padding: 20px 18px 0; }
.sec-title { font-size: 14px; font-weight: 800; color: #1a1a1a; margin-bottom: 12px;
    display: flex; align-items: center; gap: 6px; }

/* 카메라 박스 */
.cam-box {
    background: linear-gradient(145deg, #1a1a2e, #0f3460);
    border-radius: 22px; height: 180px; position: relative; overflow: hidden;
    box-shadow: 0 8px 24px rgba(15,52,96,0.4); margin-bottom: 10px;
}
.corner { position: absolute; width: 26px; height: 26px; border-color: #4caf50; border-style: solid; border-width: 0; }
.corner.tl { top:14px; left:14px; border-top-width:3px; border-left-width:3px; border-radius:4px 0 0 0; }
.corner.tr { top:14px; right:14px; border-top-width:3px; border-right-width:3px; border-radius:0 4px 0 0; }
.corner.bl { bottom:14px; left:14px; border-bottom-width:3px; border-left-width:3px; border-radius:0 0 0 4px; }
.corner.br { bottom:14px; right:14px; border-bottom-width:3px; border-right-width:3px; border-radius:0 0 4px 0; }
.sline {
    position: absolute; width: 70%; height: 2px; left: 15%;
    background: linear-gradient(90deg, transparent, #4caf50, transparent);
    box-shadow: 0 0 8px #4caf50; animation: sm 2s ease-in-out infinite;
}
@keyframes sm { 0%{top:18px;opacity:0;} 15%{opacity:1;} 85%{opacity:1;} 100%{top:162px;opacity:0;} }
.cam-inner { position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; }
.cam-inner .big-icon { font-size: 44px; margin-bottom: 8px; }
.cam-inner .lbl { color: #fff; font-size: 14px; font-weight: 700; }
.cam-inner .sub { color: rgba(255,255,255,0.45); font-size: 11px; margin-top: 3px; }

/* 업로드 카드 */
.up-card {
    background: #fff; border: 2px dashed #a5d6a7; border-radius: 18px;
    padding: 15px 16px; display: flex; align-items: center; gap: 12px; margin-bottom: 10px;
}
.up-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    border-radius: 13px; display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0; }
.up-t { font-size: 14px; font-weight: 800; color: #2d7a3a; }
.up-s { font-size: 11px; color: #999; margin-top: 2px; font-weight: 600; }

/* 결과 박스 */
.rbox { background: #fff; border-radius: 20px; padding: 18px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.07); margin-top: 14px; }
.rhead { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.rbig { font-size: 46px; }
.rname { font-size: 17px; font-weight: 900; color: #111; }
.rscore { font-size: 13px; color: #888; font-weight: 600; margin-top: 2px; }
.bwrap { background: #eee; border-radius: 10px; height: 10px; overflow: hidden; margin: 8px 0 10px; }
.bfill { height: 100%; border-radius: 10px; }
.tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.tag { padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; }
.tag.g { background: #e8f5e9; color: #2e7d32; }
.tag.y { background: #fff8e1; color: #e65100; }
.tag.r { background: #fce4ec; color: #b71c1c; }
.tip { background: #f5fbf5; border-radius: 12px; padding: 10px 12px;
    font-size: 12px; color: #444; font-weight: 600; line-height: 1.65; }

/* 가이드 카드 */
.gc { background: #fff; border-radius: 18px; padding: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
.gemo { font-size: 30px; margin-bottom: 5px; }
.gname { font-size: 13px; font-weight: 800; color: #111; }
.gsub { font-size: 10px; color: #aaa; margin-top: 1px; font-weight: 600; }
.gdetail { font-size: 11px; color: #444; font-weight: 600; line-height: 1.75;
    margin-top: 10px; padding-top: 10px; border-top: 1px solid #f0f0f0; }
.gdetail .ok { color: #2d7a3a; font-weight: 800; display: block; margin-bottom: 2px; }
.gdetail .no { color: #c62828; font-weight: 800; display: block; margin-top: 8px; margin-bottom: 2px; }

/* 카메라 버튼 */
div:has(.camera-btn-wrap) + div button {
    background: linear-gradient(145deg, #1a1a2e, #0f3460) !important;
    color: white !important; border-radius: 14px !important; border: none !important;
    padding: 0.8rem !important; font-size: 0.95rem !important; font-weight: 700 !important;
    width: 100% !important; min-height: unset !important; box-shadow: none !important;
}
/* 업로드 버튼 */
div:has(.upload-btn-wrap) + div button {
    background: white !important; color: #2d7a3a !important;
    border: 2px dashed #a5d6a7 !important; border-radius: 18px !important;
    padding: 0.8rem !important; font-size: 0.95rem !important; font-weight: 800 !important;
    width: 100% !important; min-height: unset !important; box-shadow: none !important;
}
/* 분석 버튼 */
div:has(.analyze-btn-wrap) + div button {
    background: linear-gradient(135deg, #2d7a3a, #4caf50) !important;
    color: white !important; border-radius: 16px !important; border: none !important;
    padding: 0.85rem !important; font-size: 1rem !important; font-weight: 800 !important;
    width: 100% !important; min-height: unset !important;
    box-shadow: 0 4px 14px rgba(76,175,80,0.35) !important;
}
/* 가이드 토글 버튼 */
.stButton > button {
    background: #f0f4f0 !important; color: #555 !important;
    border: none !important; border-radius: 8px !important;
    padding: 5px 10px !important; font-size: 0.75rem !important; font-weight: 700 !important;
    width: 100% !important; min-height: unset !important;
    box-shadow: none !important; margin-top: 4px !important;
}
.stButton > button:hover { background: #e0ece0 !important; color: #2d7a3a !important; }
</style>
""", unsafe_allow_html=True)

# ── 상태바 ──
st.markdown("""
<div class="sbar">
  <span style="padding-left:6px">9:41</span>
  <span>●●● WiFi 🔋</span>
</div>
""", unsafe_allow_html=True)

# ── 헤더 ──
st.markdown("""
<div class="hdr">
  <div class="hdr-top">
    <div class="logo">Scan Eat<em>!</em></div>
    <div class="ava">🌿</div>
  </div>
  <div class="hdr-sub">안녕하세요 👋</div>
  <div class="hdr-main">오늘의 신선도를 확인해볼까요?</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="scroll-body">', unsafe_allow_html=True)

# ── 카메라 섹션 ──
st.markdown("""
<div class="sec">
  <div class="sec-title">📷 카메라 스캔</div>
  <div class="cam-box">
    <div class="corner tl"></div><div class="corner tr"></div>
    <div class="corner bl"></div><div class="corner br"></div>
    <div class="sline"></div>
    <div class="cam-inner">
      <div class="big-icon">📸</div>
      <div class="lbl">카메라로 스캔하기</div>
      <div class="sub">아래 버튼을 눌러 카메라 시작</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="padding:0 18px 0;">', unsafe_allow_html=True)
st.markdown('<div class="camera-btn-wrap"></div>', unsafe_allow_html=True)
if st.button("📷  카메라 열기", key="cam_btn", use_container_width=True):
    st.session_state.show_camera = not st.session_state.show_camera
    st.session_state.show_upload = False
st.markdown('</div>', unsafe_allow_html=True)

camera_photo = None
if st.session_state.show_camera:
    camera_photo = st.camera_input("촬영", label_visibility="collapsed")

# ── 업로드 섹션 ──
st.markdown("""
<div class="sec">
  <div class="sec-title">🖼️ 사진 업로드</div>
  <div class="up-card">
    <div class="up-icon">📁</div>
    <div>
      <div class="up-t">갤러리에서 선택</div>
      <div class="up-s">JPG · PNG 이미지 업로드</div>
    </div>
    <span style="color:#ccc;font-size:20px;margin-left:auto">›</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="padding:0 18px 0;">', unsafe_allow_html=True)
st.markdown('<div class="upload-btn-wrap"></div>', unsafe_allow_html=True)
if st.button("📁  갤러리 열기", key="upload_btn", use_container_width=True):
    st.session_state.show_upload = not st.session_state.show_upload
    st.session_state.show_camera = False
st.markdown('</div>', unsafe_allow_html=True)

uploaded_file = None
if st.session_state.show_upload:
    uploaded_file = st.file_uploader("이미지 선택", type=["jpg","jpeg","png"], label_visibility="collapsed")

# ── 이미지 표시 ──
image = None
image_bytes = None
if camera_photo:
    image = Image.open(camera_photo)
    image_bytes = camera_photo.getvalue()
elif uploaded_file:
    image = Image.open(uploaded_file)
    image_bytes = uploaded_file.getvalue()

if image:
    st.markdown('<div style="padding:10px 18px 0;">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 분석 버튼 ──
st.markdown('<div style="padding:10px 18px 0;">', unsafe_allow_html=True)
st.markdown('<div class="analyze-btn-wrap"></div>', unsafe_allow_html=True)
analyze = st.button("🔍 신선도 분석하기", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── 분석 결과 ──
if analyze:
    if not image:
        st.warning("사진을 먼저 업로드하거나 촬영해주세요!")
    else:
        with st.spinner("AI가 분석 중이에요..."):
            image_data = base64.b64encode(image_bytes).decode("utf-8")
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                    {"type": "text", "text": "이 농산물 사진을 보고 아래 항목을 분석해주세요. 반드시 아래 형식으로만 답하세요:\n\n농산물 종류:\n신선도 점수: (숫자/10)\n상태: (신선/보통/주의/부패 중 하나)\n상태 설명:\n보관 방법:\n예상 남은 기한: "}
                ]}]
            )
            result = response.choices[0].message.content

            # 결과 파싱
            data = {}
            for line in result.strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    data[k.strip()] = v.strip()

            produce   = data.get('농산물 종류', '농산물')
            score_raw = data.get('신선도 점수', '5')
            status    = data.get('상태', '보통')
            desc      = data.get('상태 설명', '')
            storage   = data.get('보관 방법', '')
            shelf     = data.get('예상 남은 기한', '')

            m = re.search(r'(\d+)', score_raw)
            score = int(m.group(1)) if m else 5
            score_pct = min(score * 10, 100)

            if '신선' in status:
                color, tag_cls, emoji = '#43a047', 'g', '🥬'
            elif '보통' in status:
                color, tag_cls, emoji = '#fb8c00', 'y', '⚠️'
            else:
                color, tag_cls, emoji = '#e53935', 'r', '🚨'

            tip = desc if desc else '분석이 완료됐어요!'

            st.session_state.result_html = f"""
            <div class="sec">
              <div class="rbox">
                <div class="rhead">
                  <div class="rbig">{emoji}</div>
                  <div>
                    <div class="rname">{produce}</div>
                    <div class="rscore">신선도 {score}/10점</div>
                  </div>
                </div>
                <div class="bwrap">
                  <div class="bfill" style="width:{score_pct}%;background:linear-gradient(90deg,{color}88,{color})"></div>
                </div>
                <div class="tags">
                  <span class="tag {tag_cls}">{status}</span>
                  <span class="tag" style="background:#f3f3f3;color:#666">AI 분석</span>
                  <span class="tag" style="background:#f3f3f3;color:#666">{score}/10점</span>
                </div>
                <div class="tip">
                  💡 {tip}<br><br>
                  🏪 <b>보관법:</b> {storage}<br>
                  ⏰ <b>남은 기한:</b> {shelf}
                </div>
              </div>
            </div>
            """

if st.session_state.result_html:
    st.markdown(st.session_state.result_html, unsafe_allow_html=True)

# ── 가이드 섹션 ──
st.markdown("""
<div class="sec" style="padding-bottom:8px;">
  <div class="sec-title">📗 농작물 고르는 가이드</div>
</div>
""", unsafe_allow_html=True)

guides = [
    ("🍉", "수박",  ["두드렸을 때 탁한 소리", "줄무늬 선명하고 윤기", "배꼽 작고 건조", "묵직한 무게"], ["두드렸을 때 맑은 소리", "꼭지 없거나 시든 것"]),
    ("🍎", "사과",  ["껍질 팽팽·광택 있음", "꼭지 싱싱·단단", "달콤한 향"], ["물렁·주름진 것", "검은 반점·곰팡이"]),
    ("🍓", "딸기",  ["전체 선명한 빨간색", "꼭지 초록 싱싱", "향 진하고 통통함"], ["흰 부분 남은 미숙한 것", "물컹하거나 즙 새는 것"]),
    ("🥬", "배추",  ["잎 빳빳하고 선명한 초록", "속 꽉 차고 묵직함", "밑동 하얗고 단단"], ["잎 시들고 노란 것", "속 비어 가벼운 것"]),
    ("🧅", "양파",  ["껍질 얇고 광택·건조", "단단하고 묵직함", "목 부분 건조"], ["싹이 난 것", "물렁하거나 냄새 심한 것"]),
    ("🫜", "무",    ["묵직하고 단단함", "껍질 매끄럽고 흰색", "잎 초록 싱싱"], ["바람 들어 속이 빈 것", "갈라지거나 물렁한 것"]),
]

st.markdown('<div style="padding:0 18px;">', unsafe_allow_html=True)
for i in range(0, len(guides), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= len(guides):
            continue
        g_emoji, name, good, bad = guides[idx]
        is_open = st.session_state.selected_guide == idx
        detail = ""
        if is_open:
            good_str = "<br>".join(good)
            bad_str  = "<br>".join(bad)
            detail = f"""
            <div class="gdetail">
              <span class="ok">✔ 좋은 것</span>{good_str}
              <span class="no">✘ 피할 것</span>{bad_str}
            </div>
            """
        with col:
            st.markdown(f"""
            <div class="gc">
              <div class="gemo">{g_emoji}</div>
              <div class="gname">{name}</div>
              <div class="gsub">탭해서 보기</div>
              {detail}
            </div>
            """, unsafe_allow_html=True)
            if st.button("▲ 닫기" if is_open else "▼ 보기", key=f"guide_{idx}", use_container_width=True):
                st.session_state.selected_guide = None if is_open else idx
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#aaa;font-size:0.78rem;padding:1.5rem 0;">Scan Eat! © 2024</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
