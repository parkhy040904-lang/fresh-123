import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Scan Eat!", page_icon="🌿", layout="wide")

st.markdown("""
<style>
#MainMenu, header, footer { visibility: hidden; }
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
.main, body { background: #d9f0db !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#d9f0db;display:flex;justify-content:center;align-items:flex-start;min-height:100vh;font-family:'Nunito',sans-serif;padding:24px 0;}

.phone{width:390px;height:844px;background:#f7faf7;border-radius:50px;
  box-shadow:0 30px 80px rgba(0,0,0,0.22),inset 0 0 0 2px #ccc;
  overflow:hidden;display:flex;flex-direction:column;position:relative;}

.sbar{background:#111;color:#fff;padding:14px 28px 8px;display:flex;
  justify-content:space-between;align-items:center;font-size:12px;font-weight:700;
  flex-shrink:0;position:relative;}
.notch{width:110px;height:26px;background:#111;border-radius:0 0 18px 18px;
  position:absolute;top:0;left:50%;transform:translateX(-50%);}

.hdr{background:linear-gradient(135deg,#1b5e20,#388e3c,#66bb6a);
  padding:20px 24px 24px;flex-shrink:0;position:relative;overflow:hidden;}
.hdr::before{content:'';position:absolute;width:180px;height:180px;
  background:rgba(255,255,255,0.07);border-radius:50%;top:-50px;right:-30px;}
.hdr-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.logo{font-size:26px;font-weight:900;color:#fff;}
.logo em{color:#b9f6ca;font-style:normal;}
.ava{width:36px;height:36px;background:rgba(255,255,255,0.2);border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:18px;
  border:2px solid rgba(255,255,255,0.35);}
.hdr-sub{color:rgba(255,255,255,0.8);font-size:13px;font-weight:600;}
.hdr-main{color:#fff;font-size:16px;font-weight:800;margin-top:2px;}

.scroll{flex:1;overflow-y:auto;padding:0 0 24px;}
.scroll::-webkit-scrollbar{display:none;}

.sec{padding:20px 18px 0;}
.sec-title{font-size:14px;font-weight:800;color:#1a1a1a;margin-bottom:12px;display:flex;align-items:center;gap:6px;}

.cam-box{background:linear-gradient(145deg,#1a1a2e,#0f3460);border-radius:22px;
  height:210px;position:relative;overflow:hidden;
  box-shadow:0 8px 24px rgba(15,52,96,0.4);}
.corner{position:absolute;width:26px;height:26px;border-color:#4caf50;border-style:solid;border-width:0;}
.corner.tl{top:14px;left:14px;border-top-width:3px;border-left-width:3px;border-radius:4px 0 0 0;}
.corner.tr{top:14px;right:14px;border-top-width:3px;border-right-width:3px;border-radius:0 4px 0 0;}
.corner.bl{bottom:14px;left:14px;border-bottom-width:3px;border-left-width:3px;border-radius:0 0 0 4px;}
.corner.br{bottom:14px;right:14px;border-bottom-width:3px;border-right-width:3px;border-radius:0 0 4px 0;}
.sline{position:absolute;width:70%;height:2px;left:15%;
  background:linear-gradient(90deg,transparent,#4caf50,transparent);
  box-shadow:0 0 8px #4caf50;animation:sm 2s ease-in-out infinite;}
@keyframes sm{0%{top:18px;opacity:0;}15%{opacity:1;}85%{opacity:1;}100%{top:185px;opacity:0;}}
#camVideo{width:100%;height:100%;object-fit:cover;display:none;}
.cam-placeholder{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:pointer;}
.cam-placeholder .big-icon{font-size:44px;margin-bottom:8px;}
.cam-placeholder .lbl{color:#fff;font-size:14px;font-weight:700;}
.cam-placeholder .sub{color:rgba(255,255,255,0.45);font-size:11px;margin-top:3px;}
#camBtns{position:absolute;bottom:12px;left:0;right:0;
  display:none;justify-content:center;gap:10px;z-index:10;}
.cbtn{padding:8px 16px;border-radius:20px;border:none;cursor:pointer;
  font-family:'Nunito',sans-serif;font-size:12px;font-weight:800;}
.cbtn.shoot{background:#4caf50;color:#fff;}
.cbtn.stop{background:rgba(255,255,255,0.15);color:#fff;}
.cbtn.flip{background:rgba(255,255,255,0.25);color:#fff;}

#camResult{display:none;margin-top:12px;}
#camResult img{width:100%;border-radius:18px;max-height:180px;object-fit:cover;
  border:2px solid #a5d6a7;display:block;}

.up-label{margin-top:12px;background:#fff;border:2px dashed #a5d6a7;border-radius:18px;
  padding:15px 16px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:all 0.2s;}
.up-label:hover{background:#f1f8f1;border-color:#4caf50;}
.up-label:active{transform:scale(0.98);}
.up-icon{width:44px;height:44px;background:linear-gradient(135deg,#e8f5e9,#c8e6c9);
  border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;}
.up-t{font-size:14px;font-weight:800;color:#2d7a3a;}
.up-s{font-size:11px;color:#999;margin-top:2px;font-weight:600;}
#fileInput{display:none;}

#uploadResult{display:none;margin-top:12px;}
#uploadResult img{width:100%;border-radius:18px;max-height:180px;object-fit:cover;
  border:2px solid #a5d6a7;display:block;}

.abtn{width:100%;margin-top:10px;padding:13px;
  background:linear-gradient(135deg,#2d7a3a,#4caf50);
  border:none;border-radius:16px;color:#fff;
  font-size:15px;font-weight:800;font-family:'Nunito',sans-serif;
  cursor:pointer;box-shadow:0 4px 14px rgba(76,175,80,0.35);transition:transform 0.15s;}
.abtn:active{transform:scale(0.97);}

.rbox{background:#fff;border-radius:20px;padding:18px;
  box-shadow:0 4px 16px rgba(0,0,0,0.07);margin-top:14px;display:none;}
.rhead{display:flex;align-items:center;gap:12px;margin-bottom:10px;}
.rbig{font-size:46px;}
.rname{font-size:17px;font-weight:900;color:#111;}
.rscore{font-size:13px;color:#888;font-weight:600;margin-top:2px;}
.bwrap{background:#eee;border-radius:10px;height:10px;overflow:hidden;margin:8px 0 10px;}
.bfill{height:100%;border-radius:10px;transition:width 0.9s ease;}
.tags{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;}
.tag{padding:5px 12px;border-radius:20px;font-size:11px;font-weight:800;}
.tag.g{background:#e8f5e9;color:#2e7d32;}
.tag.y{background:#fff8e1;color:#e65100;}
.tag.o{background:#fff3e0;color:#bf360c;}
.tag.r{background:#fce4ec;color:#b71c1c;}
.tip{background:#f5fbf5;border-radius:12px;padding:10px 12px;
  font-size:12px;color:#444;font-weight:600;line-height:1.65;}

.score-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin:10px 0 6px;}
.score-item{background:#f7f7f7;border-radius:12px;padding:9px 6px;text-align:center;}
.score-label{font-size:9px;color:#aaa;font-weight:700;letter-spacing:0.02em;}
.score-val{font-size:20px;font-weight:900;margin-top:2px;}
.recipe-btn{width:100%;margin-top:10px;padding:11px;
  background:linear-gradient(135deg,#2d7a3a,#4caf50);
  border:none;border-radius:14px;color:#fff;
  font-size:14px;font-weight:800;font-family:'Nunito',sans-serif;
  cursor:pointer;box-shadow:0 4px 14px rgba(76,175,80,0.35);transition:transform 0.15s;display:none;}
.recipe-btn:active{transform:scale(0.97);}
.rbox2{background:#fff;border-radius:20px;padding:18px;
  box-shadow:0 4px 16px rgba(0,0,0,0.07);margin-top:10px;display:none;}
.recipe-name{font-size:15px;font-weight:900;color:#111;}
.recipe-time{font-size:11px;color:#aaa;font-weight:600;margin-top:2px;}
.recipe-sec{font-size:11px;font-weight:800;color:#e65100;margin-top:12px;margin-bottom:5px;}
.recipe-body{font-size:12px;color:#444;font-weight:600;line-height:1.75;}

.ggrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.gc{background:#fff;border-radius:18px;padding:16px;
  box-shadow:0 2px 10px rgba(0,0,0,0.06);cursor:pointer;transition:transform 0.15s;}
.gc:active{transform:scale(0.97);}
.gemo{font-size:30px;margin-bottom:5px;}
.gname{font-size:13px;font-weight:800;color:#111;}
.gsub{font-size:10px;color:#aaa;margin-top:1px;font-weight:600;}
.gdetail{display:none;margin-top:10px;padding-top:10px;border-top:1px solid #f0f0f0;
  font-size:11px;color:#444;font-weight:600;line-height:1.75;}
.gdetail .ok{color:#2d7a3a;font-weight:800;}
.gdetail .no{color:#c62828;font-weight:800;}
.gc.open .gdetail{display:block;}
</style>
</head>
<body>
<div class="phone">

  <div class="sbar">
    <div class="notch"></div>
    <span style="padding-left:6px" id="clock">9:41</span>
    <span>●●● WiFi 🔋</span>
  </div>

  <div class="hdr">
    <div class="hdr-top">
      <div class="logo">Scan Eat<em>!</em></div>
      <div class="ava">🌿</div>
    </div>
    <div class="hdr-sub">안녕하세요 👋</div>
    <div class="hdr-main">오늘의 신선도를 확인해볼까요?</div>
  </div>

  <div class="scroll">

    <div class="sec">
      <div class="sec-title">📷 카메라 스캔</div>
      <div class="cam-box">
        <div class="corner tl"></div><div class="corner tr"></div>
        <div class="corner bl"></div><div class="corner br"></div>
        <div class="sline" id="sline"></div>
        <video id="camVideo" autoplay playsinline></video>
        <div class="cam-placeholder" id="camPH" onclick="startCam()">
          <div class="big-icon">📸</div>
          <div class="lbl">카메라로 스캔하기</div>
          <div class="sub">탭하여 카메라 시작</div>
        </div>
        <div id="camBtns">
          <button class="cbtn stop" onclick="stopCam(event)">✕ 취소</button>
          <button class="cbtn flip" onclick="flipCam(event)">🔄 전환</button>
          <button class="cbtn shoot" onclick="shoot(event)">📸 촬영</button>
        </div>
      </div>
      <canvas id="cvs" style="display:none"></canvas>
      <div id="camResult">
        <img id="camImg" src="">
        <button class="abtn" onclick="analyze('cam')">🔍 신선도 분석하기</button>
      </div>
    </div>

    <div class="sec">
      <div class="sec-title">🖼️ 사진 업로드</div>
      <label class="up-label" for="fileInput">
        <div class="up-icon">📁</div>
        <div>
          <div class="up-t">갤러리에서 선택</div>
          <div class="up-s">JPG · PNG 이미지 업로드</div>
        </div>
        <span style="color:#ccc;font-size:20px;margin-left:auto">›</span>
      </label>
      <input type="file" id="fileInput" accept="image/*" onchange="loadFile(event)">
      <div id="uploadResult">
        <img id="uploadImg" src="">
        <button class="abtn" onclick="analyze('upload')">🔍 신선도 분석하기</button>
      </div>
    </div>

    <div class="sec">
      <div class="rbox" id="rbox">
        <div class="rhead">
          <div class="rbig" id="remo">🥦</div>
          <div>
            <div class="rname" id="rname">분석 결과</div>
            <div class="rscore" id="rscore">—</div>
          </div>
        </div>
        <div class="bwrap"><div class="bfill" id="bfill" style="width:0%"></div></div>
        <div class="score-grid" id="scoreGrid"></div>
        <div class="tags" id="rtags"></div>
        <div class="tip" id="rtip"></div>
        <button class="recipe-btn" id="recipeBtn" onclick="fetchRecipe()">🍳 이 재료로 만드는 레시피 보기</button>
      </div>
      <div class="rbox2" id="rbox2"></div>
    </div>

    <div class="sec" style="padding-bottom:24px">
      <div class="sec-title">📗 농작물 고르는 가이드</div>
      <div class="ggrid">

        <div class="gc" onclick="this.classList.toggle('open')">
          <div class="gemo">🍉</div><div class="gname">수박</div>
          <div class="gsub">탭해서 보기</div>
          <div class="gdetail">
            <span class="ok">✔ 좋은 것</span><br>
            두드렸을 때 탁한 소리<br>줄무늬 선명하고 윤기<br>배꼽 작고 건조<br>묵직한 무게<br><br>
            <span class="no">✘ 피할 것</span><br>
            두드렸을 때 맑은 소리<br>꼭지 없거나 시든 것
          </div>
        </div>

        <div class="gc" onclick="this.classList.toggle('open')">
          <div class="gemo">🍎</div><div class="gname">사과</div>
          <div class="gsub">탭해서 보기</div>
          <div class="gdetail">
            <span class="ok">✔ 좋은 것</span><br>
            껍질 팽팽·광택 있음<br>꼭지 싱싱·단단<br>달콤한 향<br><br>
            <span class="no">✘ 피할 것</span><br>
            물렁·주름진 것<br>검은 반점·곰팡이
          </div>
        </div>

        <div class="gc" onclick="this.classList.toggle('open')">
          <div class="gemo">🍓</div><div class="gname">딸기</div>
          <div class="gsub">탭해서 보기</div>
          <div class="gdetail">
            <span class="ok">✔ 좋은 것</span><br>
            전체 선명한 빨간색<br>꼭지 초록 싱싱<br>향 진하고 통통함<br><br>
            <span class="no">✘ 피할 것</span><br>
            흰 부분 남은 미숙한 것<br>물컹하거나 즙 새는 것
          </div>
        </div>

        <div class="gc" onclick="this.classList.toggle('open')">
          <div class="gemo">🥬</div><div class="gname">배추</div>
          <div class="gsub">탭해서 보기</div>
          <div class="gdetail">
            <span class="ok">✔ 좋은 것</span><br>
            잎 빳빳하고 선명한 초록<br>속 꽉 차고 묵직함<br>밑동 하얗고 단단<br><br>
            <span class="no">✘ 피할 것</span><br>
            잎 시들고 노란 것<br>속 비어 가벼운 것
          </div>
        </div>

        <div class="gc" onclick="this.classList.toggle('open')">
          <div class="gemo">🧅</div><div class="gname">양파</div>
          <div class="gsub">탭해서 보기</div>
          <div class="gdetail">
            <span class="ok">✔ 좋은 것</span><br>
            껍질 얇고 광택·건조<br>단단하고 묵직함<br>목 부분 건조<br><br>
            <span class="no">✘ 피할 것</span><br>
            싹이 난 것<br>물렁하거나 냄새 심한 것
          </div>
        </div>

        <div class="gc" onclick="this.classList.toggle('open')">
          <div class="gemo">🫜</div><div class="gname">무</div>
          <div class="gsub">탭해서 보기</div>
          <div class="gdetail">
            <span class="ok">✔ 좋은 것</span><br>
            묵직하고 단단함<br>껍질 매끄럽고 흰색<br>잎 초록 싱싱<br><br>
            <span class="no">✘ 피할 것</span><br>
            바람 들어 속이 빈 것<br>갈라지거나 물렁한 것
          </div>
        </div>

      </div>
    </div>

    <div style="text-align:center;color:#aaa;font-size:0.78rem;padding:1.5rem 0;">Scan Eat! © 2026</div>

  </div>
</div>

<script>
const GROQ_API_KEY = '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';
let stream = null;
let facingMode = 'environment';

function updateClock() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2, '0');
  const m = String(now.getMinutes()).padStart(2, '0');
  document.getElementById('clock').textContent = h + ':' + m;
}
updateClock();
setInterval(updateClock, 1000);

async function startCam(mode) {
  if (mode) facingMode = mode;
  try {
    if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
    stream = await navigator.mediaDevices.getUserMedia({video:{facingMode},audio:false});
    const v = document.getElementById('camVideo');
    v.srcObject = stream;
    v.style.display = 'block';
    document.getElementById('camPH').style.display = 'none';
    document.getElementById('sline').style.display = 'none';
    document.getElementById('camBtns').style.display = 'flex';
  } catch(e) {
    alert('카메라 권한을 허용해주세요.\\n(HTTPS 또는 localhost 환경 필요)');
  }
}

function flipCam(e) {
  e.stopPropagation();
  startCam(facingMode === 'environment' ? 'user' : 'environment');
}

function stopCam(e) {
  if(e) e.stopPropagation();
  if(stream){ stream.getTracks().forEach(t=>t.stop()); stream=null; }
  document.getElementById('camVideo').style.display = 'none';
  document.getElementById('camPH').style.display = 'flex';
  document.getElementById('sline').style.display = 'block';
  document.getElementById('camBtns').style.display = 'none';
}

function shoot(e) {
  e.stopPropagation();
  const v = document.getElementById('camVideo');
  const c = document.getElementById('cvs');
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext('2d').drawImage(v,0,0);
  const url = c.toDataURL('image/jpeg');
  stopCam(null);
  document.getElementById('camImg').src = url;
  document.getElementById('camResult').style.display = 'block';
  document.getElementById('rbox').style.display = 'none';
}

function loadFile(e) {
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    document.getElementById('uploadImg').src = ev.target.result;
    document.getElementById('uploadResult').style.display = 'block';
    document.getElementById('rbox').style.display = 'none';
  };
  reader.readAsDataURL(file);
}

function imgToBase64(imgEl) {
  const c = document.createElement('canvas');
  c.width = imgEl.naturalWidth;
  c.height = imgEl.naturalHeight;
  c.getContext('2d').drawImage(imgEl, 0, 0);
  return c.toDataURL('image/jpeg').split(',')[1];
}

function scoreColor(s) {
  const n = parseFloat(s);
  return n >= 8 ? '#43a047' : n >= 5 ? '#fb8c00' : n >= 3 ? '#ff6f00' : '#e53935';
}

function showLoading() {
  const rbox = document.getElementById('rbox');
  rbox.style.display = 'block';
  document.getElementById('remo').textContent = '⏳';
  document.getElementById('rname').textContent = 'AI 분석 중...';
  document.getElementById('rscore').textContent = '잠시만 기다려주세요';
  document.getElementById('bfill').style.width = '0%';
  document.getElementById('scoreGrid').innerHTML = '';
  document.getElementById('rtags').innerHTML = '';
  document.getElementById('rtip').textContent = 'AI가 사진을 분석하고 있어요 🤖';
  document.getElementById('recipeBtn').style.display = 'none';
  document.getElementById('rbox2').style.display = 'none';
  rbox.scrollIntoView({behavior:'smooth', block:'nearest'});
}

function showResult(produce, score, colorScore, textureScore, status, desc, storage, shelf) {
  const scorePct = Math.min(parseFloat(score) * 10, 100);
  let tagCls, emoji, color, statusLabel;
  const s = parseFloat(score);
  if (s >= 8) {
    tagCls = 'g'; emoji = '🏆'; color = '#43a047'; statusLabel = '신선';
  } else if (s >= 5) {
    tagCls = 'y'; emoji = '👍'; color = '#fb8c00'; statusLabel = '보통';
  } else if (s >= 3) {
    tagCls = 'o'; emoji = '⚠️'; color = '#ff6f00'; statusLabel = '주의';
  } else {
    tagCls = 'r'; emoji = '🚨'; color = '#e53935'; statusLabel = '경고';
  }
  document.getElementById('remo').textContent = emoji;
  document.getElementById('rname').textContent = produce;
  document.getElementById('rscore').textContent = '종합 신선도 ' + score + '/10';
  const bar = document.getElementById('bfill');
  bar.style.width = '0%';
  bar.style.background = 'linear-gradient(90deg,' + color + '88,' + color + ')';
  setTimeout(() => { bar.style.width = scorePct + '%'; }, 50);
  document.getElementById('scoreGrid').innerHTML =
    '<div class="score-item"><div class="score-label">🎨 색상</div><div class="score-val" style="color:' + scoreColor(colorScore) + '">' + colorScore + '</div></div>' +
    '<div class="score-item"><div class="score-label">👁 외관</div><div class="score-val" style="color:' + scoreColor(textureScore) + '">' + textureScore + '</div></div>' +
    '<div class="score-item"><div class="score-label">⭐ 종합</div><div class="score-val" style="color:' + color + '">' + score + '</div></div>';
  document.getElementById('rtags').innerHTML =
    '<span class="tag ' + tagCls + '">' + statusLabel + '</span>' +
    '<span class="tag" style="background:#f3f3f3;color:#666">AI 분석</span>' +
    '<span class="tag" style="background:#f3f3f3;color:#666">' + score + '/10점</span>';
  document.getElementById('rtip').innerHTML =
    '💡 ' + (desc || '분석이 완료됐어요!') + '<br><br>' +
    '🏪 <b>보관법:</b> ' + (storage || '—') + '<br>' +
    '⏰ <b>남은 기한:</b> ' + (shelf || '—');
  document.getElementById('recipeBtn').style.display = 'block';
  document.getElementById('rbox').scrollIntoView({behavior:'smooth', block:'nearest'});
}

async function analyze(src) {
  const imgEl = document.getElementById(src === 'cam' ? 'camImg' : 'uploadImg');
  if (!imgEl.src || imgEl.src === '') { alert('이미지가 없어요!'); return; }
  const run = async () => {
    showLoading();
    try {
      const base64 = imgToBase64(imgEl);
      const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + GROQ_API_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'meta-llama/llama-4-scout-17b-16e-instruct',
          messages: [{
            role: 'user',
            content: [
              {type: 'image_url', image_url: {url: 'data:image/jpeg;base64,' + base64}},
              {type: 'text', text: '사진 속 농산물을 분석합니다. 아래 순서대로 생각한 뒤 결론만 형식에 맞게 출력하세요.\\n\\n[관찰 체크리스트 - 내부 사고용]\\n① 전체 색상이 고른가? 갈변·변색 있는가?\\n② 표면에 곰팡이·검은 반점·흰 가루가 있는가?\\n③ 형태가 물러지거나 쪼그라들었는가?\\n④ 이물질·상처·균열이 있는가?\\n\\n[채점 기준 - 반드시 준수]\\n9~10: 결점 없이 완벽히 신선\\n7~8: 소량 흠집, 전반적으로 신선\\n5~6: 변색·흠집 있으나 섭취 가능\\n3~4: 곰팡이·반점·물러짐 일부 확인\\n1~2: 광범위한 부패, 섭취 불가\\n→ 곰팡이·부패 흔적이 조금이라도 보이면 무조건 4점 이하\\n\\n[출력 형식 - 이것만 출력, 다른 말 금지]\\n농산물 종류: (이름)\\n색상 점수: (0.0~10.0)\\n외관 점수: (0.0~10.0)\\n종합 신선도 점수: (0.0~10.0)\\n상태: (신선/보통/주의/부패 중 하나)\\n상태 설명: (관찰한 특징 포함해서 두 문장)\\n보관 방법: (구체적 온도·방법)\\n예상 남은 기한: (기간)'}
            ]
          }]
        })
      });
      if (!res.ok) throw new Error('API 오류: ' + res.status);
      const json = await res.json();
      const raw = json.choices[0].message.content
        .replace(/\*+/g, '').replace(/#+/g, '').replace(/\$/g, '')
        .replace(/`+/g, '').replace(/_{2,}/g, '').replace(/\\\\[a-zA-Z]+/g, '')
        .trim();
      const sectionKeys = [
        {key:'농산물 종류', kws:['농산물','종류','채소','작물','식품']},
        {key:'색상 점수',   kws:['색상']},
        {key:'외관 점수',   kws:['외관','질감']},
        {key:'종합 신선도 점수', kws:['종합','신선도 점수']},
        {key:'상태 설명',   kws:['상태 설명','설명']},
        {key:'상태',        kws:['상태']},
        {key:'보관 방법',   kws:['보관','저장']},
        {key:'예상 남은 기한', kws:['기한','유통','남은']},
      ];
      const sections = {}; let curSec = null;
      for (const line of raw.split('\\n')) {
        const ci = line.indexOf(':');
        const k  = ci > -1 ? line.slice(0, ci).trim() : '';
        const v  = ci > -1 ? line.slice(ci + 1).trim() : line.trim();
        const matched = sectionKeys.find(s => s.kws.some(kw => k.includes(kw)) && k.length < 20);
        if (matched) { curSec = matched.key; sections[curSec] = v; }
        else if (curSec && line.trim()) sections[curSec] += ' ' + line.trim();
      }
      const parseScore = r => { const m = (r||'').match(/([\\d.]+)/); return m ? parseFloat(m[1]).toFixed(1) : '5.0'; };
      const produce      = sections['농산물 종류'] || '농산물';
      const colorScore   = parseScore(sections['색상 점수']);
      const textureScore = parseScore(sections['외관 점수']);
      const score        = parseScore(sections['종합 신선도 점수']);
      const status       = sections['상태'] || '보통';
      const desc         = sections['상태 설명'] || '';
      const storage      = sections['보관 방법'] || '';
      const shelf        = sections['예상 남은 기한'] || '';
      showResult(produce, score, colorScore, textureScore, status, desc, storage, shelf);
    } catch(err) {
      document.getElementById('remo').textContent = '❌';
      document.getElementById('rname').textContent = '분석 실패';
      document.getElementById('rscore').textContent = err.message;
      document.getElementById('rtip').textContent = '다시 시도해주세요.';
    }
  };
  if (imgEl.complete && imgEl.naturalWidth > 0) run();
  else { imgEl.onload = run; }
}

async function fetchRecipe() {
  const produce = document.getElementById('rname').textContent;
  const rbox2 = document.getElementById('rbox2');
  rbox2.style.display = 'block';
  rbox2.innerHTML = '<div style="text-align:center;padding:24px;color:#aaa;font-size:13px;font-weight:700;">🍳 레시피 불러오는 중...</div>';
  rbox2.scrollIntoView({behavior:'smooth', block:'nearest'});
  try {
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + GROQ_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'meta-llama/llama-4-scout-17b-16e-instruct',
        messages: [{
          role: 'user',
          content: produce + '를 주재료로 한 간단한 레시피를 아래 형식 그대로 답하세요. 다른 말은 절대 하지 마세요.\\n요리이름: 여기에 요리 이름\\n조리시간: 여기에 시간\\n재료: 재료명 양(예: 오이 1개, 소금 1작은술, 참기름 1큰술)\\n조리법: 각 단계를 번호와 함께 상세하게(온도, 시간, 방법 포함). 예) 1. 오이를 0.3cm 두께로 얇게 썬다. 2. 소금 1작은술을 뿌려 10분간 절인다.'
        }]
      })
    });
    if (!res.ok) throw new Error('API ' + res.status);
    const json = await res.json();
    const raw = json.choices[0].message.content
      .replace(/\*+/g, '').replace(/#+/g, '').replace(/\$/g, '')
      .replace(/`+/g, '').replace(/_{2,}/g, '')
      .trim();
    const topKeys = ['요리이름','레시피명','조리시간','조리 시간','재료','조리법'];
    const sections = {};
    let curKey = null;
    raw.split('\\n').forEach(line => {
      const ci = line.indexOf(':');
      const maybeKey = ci > -1 ? line.slice(0, ci).trim() : '';
      const matched = topKeys.find(k => maybeKey === k);
      if (matched) {
        curKey = matched;
        sections[curKey] = line.slice(ci + 1).trim();
      } else if (curKey && line.trim()) {
        sections[curKey] += '\\n' + line.trim();
      }
    });
    const name  = sections['요리이름'] || sections['레시피명'] || produce + ' 레시피';
    const time  = sections['조리시간'] || sections['조리 시간'] || '—';
    const ingr  = sections['재료'] || '';
    const steps = sections['조리법'] || '';
    const ingrHtml  = ingr.split(/[,\\n]/).map(s => s.trim()).filter(Boolean).map(s => '• ' + s).join('<br>');
    const stepsHtml = steps.split('\\n').map(s => s.trim()).filter(Boolean).join('<br>');
    rbox2.innerHTML =
      '<div style="background:linear-gradient(135deg,#e8f5e9,#c8e6c9);border-radius:14px;padding:14px;margin-bottom:14px;">' +
        '<div style="font-size:11px;color:#2d7a3a;font-weight:800;margin-bottom:4px;">🍳 추천 레시피</div>' +
        '<div style="font-size:17px;font-weight:900;color:#1b5e20;">' + name + '</div>' +
        '<div style="font-size:11px;color:#888;font-weight:600;margin-top:3px;">⏱ ' + time + '</div>' +
      '</div>' +
      '<div class="recipe-sec">🛒 재료</div>' +
      '<div class="recipe-body">' + ingrHtml + '</div>' +
      '<div class="recipe-sec">🍽️ 조리법</div>' +
      '<div class="recipe-body">' + stepsHtml + '</div>' +
      '<button onclick="fetchRecipe()" style="width:100%;margin-top:14px;padding:10px;background:#f0f4f0;border:none;border-radius:12px;font-size:13px;font-weight:800;color:#2d7a3a;cursor:pointer;font-family:Nunito,sans-serif;">🔄 다른 레시피 보기</button>';
  } catch(err) {
    rbox2.innerHTML = '<div style="text-align:center;padding:20px;color:#e53935;font-size:13px;font-weight:700;">오류: ' + err.message + '</div>';
  }
}
</script>
</body>
</html>"""

components.html(html, height=920, scrolling=False)
