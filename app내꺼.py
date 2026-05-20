import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Scan It!", page_icon="🌿", layout="wide")

groq_key = st.secrets["GROQ_API_KEY"]

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

PRODUCE_DATA = [
    ('사과','🍎'),('딸기','🍓'),('토마토','🍅'),('배추','🥬'),
    ('감자','🥔'),('당근','🥕'),('오이','🥒'),('양파','🧅'),
    ('무','🫜'),('수박','🍉'),('포도','🍇'),('바나나','🍌'),
]
PREP_PRODUCE_DATA = [
    ('수박','🍉'),('사과','🍎'),('딸기','🍓'),
    ('배추','🥬'),('양파','🧅'),('무','🫜'),
]
def make_produce_list(t, data=None):
    if data is None:
        data = PRODUCE_DATA
    badge = '레시피 3개' if t=='recipe' else '세척·손질·보관'
    bc = ' blue' if t=='prep' else ''
    rows=[]
    for i,(name,emoji) in enumerate(data):
        rows.append(
            f'<div class="pitem-wrap" id="{t}Wrap{i}">'
            f'<div class="pitem" onclick="toggleProduceItem(\'{t}\',{i},\'{name}\',\'{emoji}\')">'
            f'<span class="pitem-emo">{emoji}</span>'
            f'<div class="pitem-info"><div class="pitem-name">{name}</div>'
            f'<span class="pitem-badge{bc}">{badge}</span></div>'
            f'<span class="pitem-arrow">&#x203A;</span></div>'
            f'<div class="pitem-detail" id="{t}Detail{i}"></div></div>'
        )
    return ''.join(rows)

recipe_list_html = make_produce_list('recipe')
prep_list_html   = make_produce_list('prep', PREP_PRODUCE_DATA)

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
.btn-row{display:none;gap:8px;margin-top:10px;}
.recipe-btn{flex:1;padding:11px;
  background:linear-gradient(135deg,#2d7a3a,#4caf50);
  border:none;border-radius:14px;color:#fff;
  font-size:13px;font-weight:800;font-family:'Nunito',sans-serif;
  cursor:pointer;box-shadow:0 4px 14px rgba(76,175,80,0.35);transition:transform 0.15s;}
.recipe-btn:active{transform:scale(0.97);}
.compare-btn{flex:1;padding:11px;
  background:linear-gradient(135deg,#0277bd,#0288d1);
  border:none;border-radius:14px;color:#fff;
  font-size:13px;font-weight:800;font-family:'Nunito',sans-serif;
  cursor:pointer;box-shadow:0 4px 14px rgba(2,136,209,0.3);transition:transform 0.15s;}
.compare-btn:active{transform:scale(0.97);}
.cbox{background:#fff;border-radius:20px;padding:18px;
  box-shadow:0 4px 16px rgba(0,0,0,0.07);margin-top:10px;display:none;}
.cmp-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;}
.cmp-card{background:#f7f9f7;border-radius:14px;padding:12px;text-align:center;position:relative;}
.cmp-card.winner{background:#e8f5e9;border:2px solid #4caf50;}
.cmp-label{font-size:10px;font-weight:800;color:#aaa;margin-bottom:4px;}
.cmp-name{font-size:13px;font-weight:900;color:#111;}
.cmp-score{font-size:26px;font-weight:900;margin:4px 0;}
.cmp-badge{position:absolute;top:-8px;right:-8px;background:#4caf50;color:#fff;
  font-size:10px;font-weight:800;padding:3px 8px;border-radius:10px;}
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

.pages{flex:1;position:relative;overflow:hidden;}
.page{position:absolute;inset:0;display:none;flex-direction:column;}
.page.active{display:flex;}
.bnav{background:#fff;border-top:1px solid #ebebeb;display:flex;flex-shrink:0;height:58px;}
.bnav-btn{flex:1;border:none;background:transparent;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:2px;cursor:pointer;
  font-family:'Nunito',sans-serif;color:#bbb;font-size:10px;font-weight:800;}
.bnav-btn.active{color:#2d7a3a;}
.bnav-ico{font-size:20px;line-height:1;}
.tab-hdr{padding:16px 20px;flex-shrink:0;background:linear-gradient(135deg,#1b5e20,#388e3c);}
.tab-hdr-title{font-size:20px;font-weight:900;color:#fff;}
.tab-hdr-sub{color:rgba(255,255,255,0.75);font-size:12px;font-weight:600;margin-top:3px;}
.plist{padding:12px 14px;display:flex;flex-direction:column;gap:8px;}
.pitem-wrap{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05);flex-shrink:0;}
.pitem{display:flex;align-items:center;gap:12px;padding:14px 16px;cursor:pointer;transition:background 0.15s;}
.pitem:active{background:#f5f5f5;}
.pitem-emo{font-size:36px;flex-shrink:0;}
.pitem-info{flex:1;}
.pitem-name{font-size:14px;font-weight:800;color:#111;}
.pitem-badge{display:inline-block;background:#43a047;color:#fff;font-size:11px;font-weight:800;padding:4px 10px;border-radius:20px;margin-top:6px;letter-spacing:0.02em;}
.pitem-badge.blue{background:#c8e6c9;color:#2d7a3a;}
.pitem-arrow{color:#ccc;font-size:20px;font-weight:700;transition:transform 0.2s;flex-shrink:0;}
.pitem-wrap.open .pitem-arrow{transform:rotate(90deg);}
.pitem-detail{display:none;padding:12px;border-top:1px solid #f0f0f0;background:#f2f4f0;}
.rcipe-hdr{background:#3d6b3d;border-radius:12px;padding:14px 16px;color:#fff;display:flex;align-items:center;gap:12px;margin-bottom:10px;}
.rcipe-hdr .rhemo{font-size:42px;flex-shrink:0;}
.rcipe-hdr h3{font-size:15px;font-weight:800;margin:0;}
.rcipe-hdr p{font-size:12px;opacity:.8;margin-top:3px;}
.rcipe-card{background:#fff;border-radius:12px;padding:14px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,.07);}
.rctit{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:800;color:#111;margin-bottom:8px;flex-wrap:wrap;}
.rctag{font-size:11px;background:#eaf4ea;color:#3d6b3d;border-radius:20px;padding:2px 8px;font-weight:700;}
.rctag.o{background:#fff3e0;color:#e07b00;}
.rcchips{display:flex;gap:6px;margin-bottom:10px;}
.rcchip{background:#f5f5f5;border-radius:8px;padding:6px 8px;display:flex;flex-direction:column;align-items:center;gap:1px;flex:1;}
.chlbl{font-size:10px;color:#aaa;}
.chval{font-weight:700;color:#222;font-size:11px;text-align:center;}
.rcingr{background:#f9fbf9;border-radius:10px;padding:10px;margin-bottom:10px;}
.ilbl{font-size:11px;font-weight:800;color:#3d6b3d;margin-bottom:6px;}
.rcingr-chips{display:flex;flex-wrap:wrap;gap:5px;}
.rcingr-chips span{background:#fff;border:1px solid #dce8dc;border-radius:20px;padding:3px 9px;font-size:11px;color:#333;}
.rcsteps{list-style:none;margin:0;padding:0;}
.rcsteps li{display:flex;gap:8px;margin-bottom:7px;font-size:12px;color:#333;line-height:1.55;}
.rcstep-n{min-width:20px;height:20px;background:#3d6b3d;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;flex-shrink:0;margin-top:1px;}
.rctip{background:#fffbea;border-left:3px solid #f0c040;border-radius:0 8px 8px 0;padding:8px 12px;font-size:11px;color:#555;margin-top:8px;line-height:1.6;}
.rctip strong{color:#b08800;}
.psection{background:#fff;border-radius:12px;padding:14px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,.07);}
.pstitle{font-size:13px;font-weight:800;color:#3d6b3d;margin-bottom:10px;display:flex;align-items:center;gap:6px;}
.pstep-list{list-style:none;margin:0;padding:0;}
.pstep-list li{display:flex;gap:8px;margin-bottom:8px;font-size:12px;color:#333;line-height:1.55;padding-bottom:8px;border-bottom:1px solid #f5f5f5;}
.pstep-list li:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0;}
.pstep-n{min-width:22px;height:22px;background:#eaf4ea;color:#3d6b3d;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;flex-shrink:0;margin-top:1px;}
.pcaution{background:#fdecea;border-radius:12px;padding:14px;margin-bottom:8px;}
.pcaution-t{font-size:13px;font-weight:800;color:#c0392b;margin-bottom:8px;}
.pcaution ul{list-style:none;padding:0;}
.pcaution ul li{font-size:12px;color:#555;line-height:1.7;padding-left:12px;position:relative;margin-bottom:3px;}
.pcaution ul li::before{content:'•';position:absolute;left:0;color:#c0392b;}
.pstorage{background:#fff;border-radius:12px;padding:14px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,.07);}
.psrow{display:flex;gap:8px;margin-bottom:10px;}
.pschip{flex:1;background:#f5f5f5;border-radius:10px;padding:10px;text-align:center;}
.psico{font-size:20px;margin-bottom:4px;}
.psname{font-size:11px;color:#888;margin-bottom:2px;}
.psdays{font-size:13px;font-weight:800;color:#3d6b3d;}

.fav-btn{width:100%;margin-top:8px;padding:11px;background:#fff;border:2px solid #4caf50;border-radius:16px;color:#2d7a3a;font-size:14px;font-weight:800;font-family:'Nunito',sans-serif;cursor:pointer;transition:all 0.2s;}
.fav-btn.saved{background:#e8f5e9;border-color:#2e7d32;color:#1b5e20;}
.fav-btn:active{transform:scale(0.97);}
.hist-empty{text-align:center;padding:48px 20px;color:#aaa;}
.hist-empty-ico{font-size:48px;margin-bottom:12px;}
.hist-empty-t{font-size:14px;font-weight:800;color:#bbb;}
.hist-empty-s{font-size:12px;margin-top:6px;font-weight:600;}
.hist-tabbar{display:flex;background:#fff;border-bottom:1px solid #ebebeb;flex-shrink:0;}
.hist-tabbtn{flex:1;border:none;background:transparent;padding:11px 4px;font-size:11px;font-weight:800;color:#bbb;cursor:pointer;font-family:'Nunito',sans-serif;border-bottom:2px solid transparent;transition:all 0.15s;}
.hist-tabbtn.active{color:#2d7a3a;border-bottom-color:#2d7a3a;}
.hist-alert{background:linear-gradient(135deg,#2d7a3a,#43a047);border-radius:16px;padding:14px 16px;display:flex;align-items:center;gap:12px;margin-bottom:12px;cursor:default;}
.hist-alert-t{font-size:13px;font-weight:900;color:#fff;}
.hist-alert-s{font-size:11px;color:rgba(255,255,255,0.82);margin-top:3px;font-weight:600;}
.hcmp-card{background:#fff;border-radius:16px;padding:14px;margin-bottom:10px;box-shadow:0 2px 8px rgba(0,0,0,0.06);}
.hcmp-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;}
.hcmp-name{font-size:13px;font-weight:900;color:#111;}
.hbadge{font-size:10px;font-weight:800;padding:3px 9px;border-radius:10px;}
.hbadge.dn{background:#fdecea;color:#e53935;}
.hbadge.up{background:#e8f5e9;color:#2d7a3a;}
.hbar-row{display:flex;align-items:center;gap:8px;margin-bottom:7px;}
.hbar-date{font-size:10px;color:#aaa;font-weight:700;min-width:36px;text-align:right;}
.hbar-track{flex:1;background:#f0f0f0;border-radius:6px;height:9px;overflow:hidden;}
.hbar-fill{height:100%;border-radius:6px;}
.hbar-score{font-size:12px;font-weight:900;min-width:26px;}
.hlist-item{background:#fff;border-radius:16px;padding:13px 14px;margin-bottom:8px;box-shadow:0 2px 8px rgba(0,0,0,0.05);display:flex;align-items:center;gap:10px;flex-shrink:0;}
.hlist-ico{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:26px;flex-shrink:0;}
.hlist-info{flex:1;min-width:0;}
.hlist-name{font-size:14px;font-weight:900;color:#111;}
.hlist-meta{font-size:11px;color:#aaa;font-weight:600;margin-top:2px;}
.hlist-right{text-align:right;flex-shrink:0;}
.hlist-score{font-size:22px;font-weight:900;line-height:1;}
.hlist-change{font-size:10px;font-weight:700;margin-top:3px;}
.hlist-right{text-align:right;flex-shrink:0;}
.hsec-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
.hsec-t{font-size:14px;font-weight:900;color:#1a1a1a;}
.hsec-cnt{font-size:11px;font-weight:700;color:#aaa;}
.rescan-overlay{position:absolute;inset:0;background:rgba(0,0,0,0.55);z-index:50;display:none;flex-direction:column;border-radius:50px;overflow:hidden;}
.rescan-overlay.open{display:flex;}
.rescan-sheet{background:#f7faf7;border-radius:28px 28px 0 0;margin-top:auto;padding:20px 18px 28px;max-height:88%;overflow-y:auto;}
.rescan-sheet::-webkit-scrollbar{display:none;}
.htimeline{display:flex;align-items:flex-start;gap:0;margin:12px 0 14px;}
.htl-node{flex:0;text-align:center;min-width:64px;}
.htl-circle{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:900;margin:0 auto;}
.htl-label{font-size:10px;font-weight:700;color:#aaa;margin-top:5px;}
.htl-line{flex:1;height:3px;background:#eee;margin-top:24px;}
.hstats-row{display:flex;gap:8px;margin-bottom:8px;}
.hstat{flex:1;background:#f7f7f7;border-radius:12px;padding:10px;text-align:center;}
.hstat-label{font-size:10px;color:#aaa;font-weight:700;}
.hstat-val{font-size:15px;font-weight:900;color:#222;margin-top:3px;}
.hai-comment{background:#fffbea;border-left:3px solid #f0c040;border-radius:0 10px 10px 0;padding:10px 12px;font-size:12px;color:#555;line-height:1.65;margin-top:8px;}
.crop-grid{display:flex;flex-direction:column;gap:12px;}
.crop-card{background:#fff;border-radius:18px;padding:16px;box-shadow:0 2px 10px rgba(0,0,0,0.07);}
.crop-card__header{display:flex;align-items:center;gap:12px;margin-bottom:14px;}
.crop-card__emoji{font-size:36px;flex-shrink:0;}
.crop-card__title{font-size:15px;font-weight:900;color:#111;}
.crop-card__sub{font-size:11px;color:#aaa;font-weight:600;margin-top:2px;}
.crop-card__steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px;margin-bottom:12px;}
.crop-card__step{display:flex;gap:8px;align-items:flex-start;font-size:12px;color:#333;line-height:1.55;}
.crop-card__num{min-width:22px;height:22px;background:#e8f5e9;color:#2d7a3a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;flex-shrink:0;margin-top:1px;}
.crop-card__step-text{flex:1;padding-top:3px;}
.crop-card__tip{background:#fffbea;border-left:3px solid #f0c040;border-radius:0 8px 8px 0;padding:8px 12px;font-size:11px;color:#555;line-height:1.6;}
.crop-card__yt{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;padding:10px 14px;background:#2d7a3a;border-radius:12px;color:#fff;font-size:12px;font-weight:800;text-decoration:none;}
.recipe-grid{display:flex;flex-direction:column;gap:14px;}
.recipe-sec{background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.07);}
.recipe-sec__hdr{background:linear-gradient(135deg,#1b5e20,#388e3c);padding:14px 16px;display:flex;align-items:center;gap:10px;}
.recipe-sec__emoji{font-size:28px;}
.recipe-sec__name{font-size:15px;font-weight:900;color:#fff;}
.recipe-item{padding:14px 16px;border-bottom:1px solid #f0f0f0;}
.recipe-item:last-child{border-bottom:none;}
.recipe-item__hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;gap:8px;}
.recipe-item__title{font-size:13px;font-weight:900;color:#111;flex:1;}
.recipe-item__yt{display:flex;align-items:center;gap:5px;padding:6px 10px;background:#2d7a3a;border-radius:10px;color:#fff;font-size:11px;font-weight:800;text-decoration:none;flex-shrink:0;}
.recipe-item__ingr{background:#f7f9f7;border-radius:10px;padding:9px 12px;margin-bottom:10px;font-size:11px;color:#444;line-height:1.7;font-weight:600;}
.recipe-item__ingr-lbl{font-size:11px;font-weight:800;color:#2d7a3a;display:block;margin-bottom:4px;}
.recipe-item__steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px;}
.recipe-item__step{display:flex;gap:8px;align-items:flex-start;font-size:12px;color:#333;line-height:1.55;}
.recipe-item__num{min-width:20px;height:20px;background:#e8f5e9;color:#2d7a3a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;flex-shrink:0;margin-top:1px;}
</style>
</head>
<body>
<div class="phone">

  <div class="sbar">
    <div class="notch"></div>
    <span style="padding-left:6px" id="clock">9:41</span>
    <span>●●● WiFi 🔋</span>
  </div>

  <div class="pages">
  <div id="pageHome" class="page active">
  <div class="hdr">
    <div class="hdr-top">
      <div class="logo">Scan It<em>!</em></div>
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
        <div class="btn-row" id="btnRow">
          <button class="compare-btn" onclick="startCompare()">📊 비교하기</button>
        </div>
        <button class="fav-btn" id="favBtn" onclick="toggleFav()">⭐ 찜하기</button>
      </div>
      <div class="rbox2" id="rbox2"></div>
      <div class="cbox" id="cbox">
        <div style="font-size:13px;font-weight:800;color:#111;margin-bottom:10px;">📊 비교할 사진 추가</div>
        <div style="display:flex;gap:8px;margin-bottom:12px;">
          <button id="cmpTabCam" onclick="switchCmpTab('cam')" style="flex:1;padding:8px;border-radius:10px;border:none;background:#e3f2fd;color:#1565c0;font-size:12px;font-weight:800;font-family:'Nunito',sans-serif;cursor:pointer;">📷 카메라</button>
          <button id="cmpTabFile" onclick="switchCmpTab('file')" style="flex:1;padding:8px;border-radius:10px;border:none;background:#f0f0f0;color:#888;font-size:12px;font-weight:800;font-family:'Nunito',sans-serif;cursor:pointer;">🖼️ 갤러리</button>
        </div>
        <div id="cmpCamSection">
          <div style="background:linear-gradient(145deg,#1a1a2e,#0f3460);border-radius:16px;height:160px;position:relative;overflow:hidden;">
            <video id="compareCamVideo" autoplay playsinline style="width:100%;height:100%;object-fit:cover;display:none;"></video>
            <div id="compareCamPH" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;" onclick="startCompareCam()">
              <div style="font-size:36px;margin-bottom:6px;">📸</div>
              <div style="color:#fff;font-size:13px;font-weight:700;">탭하여 카메라 시작</div>
            </div>
            <div id="compareCamBtns" style="position:absolute;bottom:10px;left:0;right:0;display:none;justify-content:center;gap:8px;">
              <button class="cbtn stop" onclick="stopCompareCam(event)">✕ 취소</button>
              <button class="cbtn flip" onclick="flipCompareCam(event)">🔄 전환</button>
              <button class="cbtn shoot" onclick="shootCompare(event)">📸 촬영</button>
            </div>
          </div>
        </div>
        <div id="cmpFileSection" style="display:none;">
          <label style="background:#f7f9f7;border:2px dashed #90caf9;border-radius:14px;padding:14px;display:flex;align-items:center;gap:10px;cursor:pointer;" for="compareInput">
            <div style="width:38px;height:38px;background:linear-gradient(135deg,#e3f2fd,#bbdefb);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">📁</div>
            <div>
              <div style="font-size:13px;font-weight:800;color:#1565c0;">사진 선택</div>
              <div style="font-size:11px;color:#999;margin-top:1px;font-weight:600;">JPG · PNG 업로드</div>
            </div>
          </label>
          <input type="file" id="compareInput" accept="image/*" style="display:none" onchange="loadCompareFile(event)">
        </div>
        <canvas id="compareCvs" style="display:none"></canvas>
        <div id="comparePreview" style="display:none;margin-top:10px;">
          <img id="compareImg" src="" style="width:100%;border-radius:14px;max-height:160px;object-fit:cover;border:2px solid #90caf9;display:block;">
          <button class="abtn" style="background:linear-gradient(135deg,#0277bd,#0288d1);box-shadow:0 4px 14px rgba(2,136,209,0.3);" onclick="analyzeCompare()">📊 비교 분석하기</button>
        </div>
        <div id="compareResult" style="display:none;margin-top:12px;"></div>
      </div>
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

    <div style="text-align:center;color:#aaa;font-size:0.78rem;padding:1.5rem 0;">Scan It! © 2026</div>

  </div>
  </div><div id="pageRecipe" class="page">
    <div class="tab-hdr">
      <div class="tab-hdr-title">🍳 레시피</div>
      <div class="tab-hdr-sub">농산물별 레시피 모음</div>
    </div>
    <div class="scroll" style="padding:12px 14px 24px;">
      <div class="recipe-grid" id="recipeGrid"></div>
    </div>
  </div>

  <div id="pagePrep" class="page">
    <div class="tab-hdr">
      <div class="tab-hdr-title">🔪 손질법</div>
      <div class="tab-hdr-sub">신선한 농산물 손질 가이드</div>
    </div>
    <div class="scroll" style="padding:12px 14px 24px;">
      <div class="crop-grid" id="cropGrid"></div>
    </div>
  </div>

  <div id="pageHistory" class="page">
    <div class="tab-hdr">
      <div class="tab-hdr-title">📋 히스토리</div>
      <div class="tab-hdr-sub">내 농산물 분석 기록</div>
    </div>
    <div class="hist-tabbar">
      <button class="hist-tabbtn active" id="htab0" onclick="switchHistTab(0)">📋 전체 기록</button>
      <button class="hist-tabbtn" id="htab1" onclick="switchHistTab(1)">⭐ 찜한 항목</button>
      <button class="hist-tabbtn" id="htab2" onclick="switchHistTab(2)">📊 비교 분석</button>
    </div>
    <div class="scroll" id="histContent" style="padding:12px 14px 24px;"></div>
  </div>

  </div><div class="bnav">
    <button class="bnav-btn active" id="btnHome" onclick="showPage('home')">
      <span class="bnav-ico">🏠</span><span>홈</span>
    </button>
    <button class="bnav-btn" id="btnRecipe" onclick="showPage('recipe')">
      <span class="bnav-ico">🍳</span><span>레시피</span>
    </button>
    <button class="bnav-btn" id="btnPrep" onclick="showPage('prep')">
      <span class="bnav-ico">🔪</span><span>손질법</span>
    </button>
    <button class="bnav-btn" id="btnHistory" onclick="showPage('history')">
      <span class="bnav-ico">📋</span><span>히스토리</span>
    </button>
  </div>

  <div class="rescan-overlay" id="rescanOverlay">
    <div class="rescan-sheet">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
        <div style="font-size:16px;font-weight:900;color:#111;">🔄 재스캔하기</div>
        <button onclick="closeRescan()" style="background:#f0f0f0;border:none;border-radius:10px;padding:6px 14px;font-size:12px;font-weight:800;cursor:pointer;color:#555;font-family:'Nunito',sans-serif;">✕ 닫기</button>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:14px;">
        <button id="rescanTabCam" onclick="switchRescanTab('cam')" style="flex:1;padding:8px;border-radius:10px;border:none;background:#e8f5e9;color:#2d7a3a;font-size:12px;font-weight:800;font-family:'Nunito',sans-serif;cursor:pointer;">📷 카메라</button>
        <button id="rescanTabFile" onclick="switchRescanTab('file')" style="flex:1;padding:8px;border-radius:10px;border:none;background:#f0f0f0;color:#888;font-size:12px;font-weight:800;font-family:'Nunito',sans-serif;cursor:pointer;">🖼️ 갤러리</button>
      </div>
      <div id="rescanCamSection">
        <div style="background:linear-gradient(145deg,#1a1a2e,#0f3460);border-radius:16px;height:150px;position:relative;overflow:hidden;">
          <video id="rescanCamVideo" autoplay playsinline style="width:100%;height:100%;object-fit:cover;display:none;"></video>
          <div id="rescanCamPH" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;" onclick="startRescanCam()">
            <div style="font-size:34px;margin-bottom:6px;">📸</div>
            <div style="color:#fff;font-size:13px;font-weight:700;">탭하여 카메라 시작</div>
          </div>
          <div id="rescanCamBtns" style="position:absolute;bottom:10px;left:0;right:0;display:none;justify-content:center;gap:8px;">
            <button class="cbtn stop" onclick="stopRescanCam(event)">✕ 취소</button>
            <button class="cbtn flip" onclick="flipRescanCam(event)">🔄 전환</button>
            <button class="cbtn shoot" onclick="shootRescan(event)">📸 촬영</button>
          </div>
        </div>
        <div id="rescanCamResult" style="display:none;margin-top:10px;">
          <img id="rescanCamImg" src="" style="width:100%;border-radius:14px;max-height:130px;object-fit:cover;border:2px solid #a5d6a7;display:block;">
          <button class="abtn" onclick="doRescan('cam')" style="margin-top:8px;">🔍 변화 분석하기</button>
        </div>
      </div>
      <div id="rescanFileSection" style="display:none;">
        <label style="background:#f7f9f7;border:2px dashed #a5d6a7;border-radius:14px;padding:14px;display:flex;align-items:center;gap:10px;cursor:pointer;" for="rescanFileInput">
          <div style="width:38px;height:38px;background:linear-gradient(135deg,#e8f5e9,#c8e6c9);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">📁</div>
          <div><div style="font-size:13px;font-weight:800;color:#2d7a3a;">사진 선택</div><div style="font-size:11px;color:#999;margin-top:1px;font-weight:600;">JPG · PNG 업로드</div></div>
        </label>
        <input type="file" id="rescanFileInput" accept="image/*" style="display:none" onchange="loadRescanFile(event)">
        <div id="rescanFileResult" style="display:none;margin-top:10px;">
          <img id="rescanFileImg" src="" style="width:100%;border-radius:14px;max-height:130px;object-fit:cover;border:2px solid #a5d6a7;display:block;">
          <button class="abtn" onclick="doRescan('file')" style="margin-top:8px;">🔍 변화 분석하기</button>
        </div>
      </div>
      <canvas id="rescanCvs" style="display:none"></canvas>
      <div id="rescanCompareResult" style="display:none;margin-top:12px;"></div>
    </div>
  </div>
</div>

<script>
const GROQ_API_KEY = '__GROQ_KEY__';
let stream = null;
let facingMode = 'environment';
let shownRecipes = [];
let lastResult = null;
let compareStream = null;
let compareFacingMode = 'environment';
let compareCachedHTML = null;

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
  return n >= 8 ? '#43a047' : n >= 6 ? '#7cb342' : n >= 4 ? '#fb8c00' : n >= 2 ? '#e64a19' : '#e53935';
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
  document.getElementById('btnRow').style.display = 'none';
  document.getElementById('rbox2').style.display = 'none';
  rbox.scrollIntoView({behavior:'smooth', block:'nearest'});
}

function showResult(produce, score, colorScore, textureScore, status, desc, storage, shelf) {
  const scorePct = Math.min(parseFloat(score) * 10, 100);
  let tagCls, emoji, color, statusLabel;
  const s = parseFloat(score);
  if (s >= 8) {
    tagCls = 'g'; emoji = '🏆'; color = '#43a047'; statusLabel = '신선';
  } else if (s >= 6) {
    tagCls = 'g'; emoji = '👍'; color = '#7cb342'; statusLabel = '양호';
  } else if (s >= 4) {
    tagCls = 'y'; emoji = '⚠️'; color = '#fb8000'; statusLabel = '주의';
  } else if (s >= 2) {
    tagCls = 'o'; emoji = '🚨'; color = '#e64a19'; statusLabel = '위험';
  } else {
    tagCls = 'r'; emoji = '🚫'; color = '#e53935'; statusLabel = '폐기';
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
  document.getElementById('btnRow').style.display = 'flex';
  shownRecipes = [];
  lastResult = {produce, score, colorScore, textureScore, desc};
  compareCachedHTML = null;
  if (compareStream) stopCompareCam(null);
  document.getElementById('cbox').style.display = 'none';
  document.getElementById('comparePreview').style.display = 'none';
  document.getElementById('compareResult').style.display = 'none';
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
          temperature: 0,
          messages: [{
            role: 'user',
            content: [
              {type: 'image_url', image_url: {url: 'data:image/jpeg;base64,' + base64}},
              {type: 'text', text: '사진 속 농산물의 신선도를 아래 규칙에 따라 엄격하게 채점하세요.\\n\\n[필수 관찰 항목]\\n① 검은 반점·갈색 부패 부위가 있는가?\\n② 곰팡이(흰색/회색/검은색 가루·솜털)가 있는가?\\n③ 껍질이 주름지거나 물러진 부위가 있는가?\\n④ 표면이 균열되거나 즙이 새는가?\\n\\n[채점 규칙 - 절대 준수]\\n• ①~④ 중 하나라도 해당하면 → 종합 점수 4점 이하\\n• 검은 반점이나 곰팡이가 명확히 보이면 → 종합 점수 2점 이하\\n• 곰팡이가 광범위하거나 악취 등 심각한 부패면 → 종합 점수 1점 이하\\n• 사진에 신선한 것과 상한 것이 섞여 있으면 → 가장 상한 것 기준으로 채점\\n• 전체가 완벽히 신선할 때만 8점 이상 가능\\n\\n[점수 기준]\\n8~10: 흠집 전혀 없이 완벽히 신선, 바로 섭취 가능\\n6~7: 아주 작은 흠집, 2~3일 내 섭취 권장\\n4~5: 변색·이상 있으나 오늘~내일 섭취 가능\\n2~3: 부패 일부, 섭취 위험\\n0~1: 곰팡이·광범위 부패, 즉시 폐기\\n\\n[중요] 모든 점수는 반드시 소수점 첫째 자리까지 작성 (예: 8.0 금지, 7.5 또는 8.3처럼)\\n\\n[출력 형식 - 이것만 출력, 다른 말 금지]\\n농산물 종류: (이름)\\n색상 점수: (0.0~10.0, 소수점 필수)\\n외관 점수: (0.0~10.0, 소수점 필수)\\n종합 신선도 점수: (0.0~10.0, 소수점 필수)\\n상태: (신선/보통/주의/부패 중 하나)\\n상태 설명: (관찰한 특징 포함해서 두 문장)\\n보관 방법: (구체적 온도·방법)\\n예상 남은 기한: (기간)'}
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
      const status       = sections['상태'] || '보통';
      const desc         = sections['상태 설명'] || '';
      const storage      = sections['보관 방법'] || '';
      const shelf        = sections['예상 남은 기한'] || '';
      let s  = parseFloat(parseScore(sections['종합 신선도 점수']));
      let cs = parseFloat(colorScore);
      let ts = parseFloat(textureScore);
      const combined = desc + ' ' + status;
      const negWords  = ['없','않','전혀','아닌','안 '];
      const sentences = combined.split(/[.!?\\n。]/);
      const hasBad = (words) => sentences.some(sent =>
        words.some(w => sent.includes(w)) && !negWords.some(neg => sent.includes(neg))
      );
      const moldWords = ['곰팡이','악취'];
      const rotWords  = ['부패','썩','검은 반점','검은반점','흑변'];
      const warnWords = ['물러','주름','변색','균열','상함','상해'];
      if (hasBad(moldWords)) {
        s  = Math.min(s,  1.9);
        cs = Math.min(cs, 2.0);
        ts = Math.min(ts, 2.0);
      } else if (hasBad(rotWords) || status === '부패') {
        s  = Math.min(s,  2.9);
        cs = Math.min(cs, 3.0);
        ts = Math.min(ts, 3.0);
      } else if (status === '주의' || hasBad(warnWords)) {
        s  = Math.min(s,  4.9);
        cs = Math.min(cs, 5.0);
        ts = Math.min(ts, 5.0);
      }
      const score = s.toFixed(1);
      const colorScoreFinal   = cs.toFixed(1);
      const textureScoreFinal = ts.toFixed(1);
      let shelfFinal;
      if (s < 2) shelfFinal = '즉시 버리세요 (섭취 불가)';
      else if (s < 4) shelfFinal = '오늘 안에 폐기하거나 상한 부분 완전히 제거 후 확인';
      else if (s < 6) shelfFinal = shelf || '오늘~내일 사용 권장';
      else shelfFinal = shelf;
      showResult(produce, score, colorScoreFinal, textureScoreFinal, status, desc, storage, shelfFinal);
      autoSaveEntry(src);
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

function startCompare() {
  const cbox = document.getElementById('cbox');
  cbox.style.display = 'block';
  document.getElementById('rbox2').style.display = 'none';
  switchCmpTab('cam');
  cbox.scrollIntoView({behavior:'smooth', block:'nearest'});
}

function switchCmpTab(tab) {
  const isCam = tab === 'cam';
  document.getElementById('cmpCamSection').style.display = isCam ? 'block' : 'none';
  document.getElementById('cmpFileSection').style.display = isCam ? 'none' : 'block';
  document.getElementById('cmpTabCam').style.background = isCam ? '#e3f2fd' : '#f0f0f0';
  document.getElementById('cmpTabCam').style.color = isCam ? '#1565c0' : '#888';
  document.getElementById('cmpTabFile').style.background = isCam ? '#f0f0f0' : '#e3f2fd';
  document.getElementById('cmpTabFile').style.color = isCam ? '#888' : '#1565c0';
  if (!isCam) stopCompareCam(null);
}

async function startCompareCam(mode) {
  if (mode) compareFacingMode = mode;
  try {
    if (compareStream) { compareStream.getTracks().forEach(t => t.stop()); compareStream = null; }
    compareStream = await navigator.mediaDevices.getUserMedia({video:{facingMode: compareFacingMode}, audio:false});
    const v = document.getElementById('compareCamVideo');
    v.srcObject = compareStream;
    v.style.display = 'block';
    document.getElementById('compareCamPH').style.display = 'none';
    document.getElementById('compareCamBtns').style.display = 'flex';
  } catch(e) {
    alert('카메라 권한을 허용해주세요.\\n(HTTPS 또는 localhost 환경 필요)');
  }
}

function flipCompareCam(e) {
  e.stopPropagation();
  startCompareCam(compareFacingMode === 'environment' ? 'user' : 'environment');
}

function stopCompareCam(e) {
  if (e) e.stopPropagation();
  if (compareStream) { compareStream.getTracks().forEach(t => t.stop()); compareStream = null; }
  document.getElementById('compareCamVideo').style.display = 'none';
  document.getElementById('compareCamPH').style.display = 'flex';
  document.getElementById('compareCamBtns').style.display = 'none';
}

function shootCompare(e) {
  e.stopPropagation();
  const v = document.getElementById('compareCamVideo');
  const c = document.getElementById('compareCvs');
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext('2d').drawImage(v, 0, 0);
  const url = c.toDataURL('image/jpeg');
  stopCompareCam(null);
  document.getElementById('compareImg').src = url;
  document.getElementById('comparePreview').style.display = 'block';
  document.getElementById('compareResult').style.display = 'none';
  compareCachedHTML = null;
}

function loadCompareFile(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    document.getElementById('compareImg').src = ev.target.result;
    document.getElementById('comparePreview').style.display = 'block';
    document.getElementById('compareResult').style.display = 'none';
    compareCachedHTML = null;
  };
  reader.readAsDataURL(file);
}

async function analyzeCompare() {
  const imgEl = document.getElementById('compareImg');
  if (!imgEl.src || imgEl.src === '') { alert('사진을 먼저 선택해주세요!'); return; }
  const resultEl = document.getElementById('compareResult');
  if (compareCachedHTML) {
    resultEl.style.display = 'block';
    resultEl.innerHTML = compareCachedHTML;
    resultEl.scrollIntoView({behavior:'smooth', block:'nearest'});
    return;
  }
  resultEl.style.display = 'block';
  resultEl.innerHTML = '<div style="text-align:center;padding:16px;color:#aaa;font-size:13px;font-weight:700;">⏳ 분석 중...</div>';
  try {
    const base64 = imgToBase64(imgEl);
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {'Authorization': 'Bearer ' + GROQ_API_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify({
        model: 'meta-llama/llama-4-scout-17b-16e-instruct',
        temperature: 0,
        messages: [{
          role: 'user',
          content: [
            {type: 'image_url', image_url: {url: 'data:image/jpeg;base64,' + base64}},
            {type: 'text', text: '사진 속 농산물의 신선도를 아래 규칙에 따라 엄격하게 채점하세요.\\n\\n[필수 관찰 항목]\\n① 검은 반점·갈색 부패 부위가 있는가?\\n② 곰팡이(흰색/회색/검은색 가루·솜털)가 있는가?\\n③ 껍질이 주름지거나 물러진 부위가 있는가?\\n④ 표면이 균열되거나 즙이 새는가?\\n\\n[채점 규칙 - 절대 준수]\\n• ①~④ 중 하나라도 해당하면 → 종합 점수 4점 이하\\n• 검은 반점이나 곰팡이가 명확히 보이면 → 종합 점수 2점 이하\\n• 곰팡이가 광범위하거나 악취 등 심각한 부패면 → 종합 점수 1점 이하\\n• 사진에 신선한 것과 상한 것이 섞여 있으면 → 가장 상한 것 기준으로 채점\\n• 전체가 완벽히 신선할 때만 8점 이상 가능\\n\\n[점수 기준]\\n8~10: 완벽히 신선\\n6~7: 아주 작은 흠집\\n4~5: 변색·이상 있음\\n2~3: 부패 일부\\n0~1: 곰팡이·광범위 부패\\n\\n[중요] 점수는 반드시 소수점 첫째 자리까지 작성 (예: 7.5, 8.3)\\n\\n[출력 형식 - 이것만 출력]\\n농산물 종류: (이름)\\n종합 신선도 점수: (0.0~10.0, 소수점 필수)\\n상태 설명: (부패·이상 여부 포함 한 문장)'}
          ]
        }]
      })
    });
    if (!res.ok) throw new Error('API 오류: ' + res.status);
    const json = await res.json();
    const raw = json.choices[0].message.content.replace(/\\*+/g,'').replace(/#+/g,'').trim();
    const sectionKeys = [
      {key:'농산물 종류', kws:['농산물','종류','채소','작물','식품']},
      {key:'종합 신선도 점수', kws:['종합','신선도 점수']},
      {key:'상태 설명', kws:['상태 설명','설명']},
    ];
    const sections = {}; let curSec = null;
    for (const line of raw.split('\\n')) {
      const ci = line.indexOf(':');
      const k = ci > -1 ? line.slice(0, ci).trim() : '';
      const v = ci > -1 ? line.slice(ci + 1).trim() : line.trim();
      const matched = sectionKeys.find(s => s.kws.some(kw => k.includes(kw)) && k.length < 20);
      if (matched) { curSec = matched.key; sections[curSec] = v; }
      else if (curSec && line.trim()) sections[curSec] += ' ' + line.trim();
    }
    const parseScore = r => { const m = (r||'').match(/([\\d.]+)/); return m ? parseFloat(m[1]).toFixed(1) : '5.0'; };
    const bProduce = sections['농산물 종류'] || '농산물';
    const bDesc    = sections['상태 설명'] || '';
    let bs = parseFloat(parseScore(sections['종합 신선도 점수']));
    const bNegWords = ['없','않','전혀','아닌','안 '];
    const bSents = bDesc.split(/[.!?\\n。]/);
    const bHasBad = (words) => bSents.some(sent =>
      words.some(w => sent.includes(w)) && !bNegWords.some(neg => sent.includes(neg))
    );
    if (bHasBad(['곰팡이','악취'])) bs = Math.min(bs, 1.9);
    else if (bHasBad(['부패','썩','검은 반점','검은반점','흑변'])) bs = Math.min(bs, 2.9);
    else if (bHasBad(['물러','주름','변색','균열','상함','상해'])) bs = Math.min(bs, 4.9);
    const bScore = bs;
    const aProduce = lastResult.produce;
    if (!aProduce.includes(bProduce) && !bProduce.includes(aProduce)) {
      resultEl.innerHTML =
        '<div style="background:#fff3e0;border-radius:14px;padding:14px 16px;text-align:center;">' +
          '<div style="font-size:28px;margin-bottom:6px;">🚫</div>' +
          '<div style="font-size:13px;font-weight:800;color:#e65100;">다른 종류라 비교할 수 없어요</div>' +
          '<div style="font-size:11px;color:#888;font-weight:600;margin-top:6px;">A: ' + aProduce + ' &nbsp;|&nbsp; B: ' + bProduce + '</div>' +
          '<div style="font-size:11px;color:#aaa;font-weight:600;margin-top:4px;">같은 종류의 농산물을 비교해주세요</div>' +
        '</div>';
      return;
    }
    const aScore   = parseFloat(lastResult.score);
    const diff     = Math.abs(aScore - bScore).toFixed(1);
    const aWins    = aScore > bScore;
    const tie      = diff < 0.5;
    const summary  = tie ? '두 개의 신선도가 거의 비슷합니다.' : (aWins ? 'A가 ' + diff + '점 더 신선합니다. A를 선택하세요! 👈' : 'B가 ' + diff + '점 더 신선합니다. B를 선택하세요! 👉');
    resultEl.innerHTML =
      '<div class="cmp-grid">' +
        '<div class="cmp-card' + (aWins || tie ? ' winner' : '') + '">' +
          (aWins && !tie ? '<div class="cmp-badge">✅ 추천</div>' : '') +
          '<div class="cmp-label">A (처음 것)</div>' +
          '<div class="cmp-name">' + lastResult.produce + '</div>' +
          '<div class="cmp-score" style="color:' + scoreColor(lastResult.score) + '">' + lastResult.score + '</div>' +
        '</div>' +
        '<div class="cmp-card' + (!aWins || tie ? ' winner' : '') + '">' +
          (!aWins && !tie ? '<div class="cmp-badge">✅ 추천</div>' : '') +
          '<div class="cmp-label">B (비교 것)</div>' +
          '<div class="cmp-name">' + bProduce + '</div>' +
          '<div class="cmp-score" style="color:' + scoreColor(bScore.toFixed(1)) + '">' + bScore.toFixed(1) + '</div>' +
        '</div>' +
      '</div>' +
      '<div style="background:#f5f5f5;border-radius:12px;padding:10px 12px;margin-top:10px;font-size:12px;font-weight:700;color:#333;text-align:center;">' + summary + '</div>';
    compareCachedHTML = resultEl.innerHTML;
    resultEl.scrollIntoView({behavior:'smooth', block:'nearest'});
  } catch(err) {
    resultEl.innerHTML = '<div style="text-align:center;padding:16px;color:#e53935;font-size:13px;font-weight:700;">오류: ' + err.message + '</div>';
  }
}

const RECIPE_DATA = [
  {
    emoji: '🥬', name: '배추',
    recipes: [
      {
        title: '김치',
        ytLink: 'https://youtu.be/K55CPyYTUJI?si=ya-HyUUSH9e2x1_T',
        ingredients: '절인배추 12kg, 굴 1kg, 물(찹쌀풀용) 1.5L, 찹쌀가루 100g, 소고기 다시다 2큰술(20g), MSG 2큰술(20g), 굵은고춧가루 750g, 다진마늘 500g, 새우젓 350g, 다진생강 25g, 멸치액젓 500g, 꽃소금 75g, 설탕 200g, 무 1.5kg, 쪽파 700g, 홍갓 500g, 청갓 700g, 알타리무청 6줄기, 당근 1/3개(80g), 미나리 200g',
        steps: [
          '물에 찹쌀가루를 넣어 풀어준다',
          '찹쌀물을 냄비에 붓고 중불에서 바닥을 긁어가며 끓인다',
          '찹쌀 풀에 소고기 다시다 2큰술을 넣어 섞어준다',
          '농도가 잡히면 고춧가루, MSG를 넣어 섞어준다',
          '무는 채칼을 이용하여 썰어준다',
          '채 썬 무에 꽃소금, 멸치액젓, 새우젓을 넣어 절여준다',
          '갓은 뿌리를 제거하고 줄기 3cm, 이파리 2cm 길이로 자른다',
          '무청, 쪽파는 3cm 길이로 잘라 준비한다',
          '당근은 채칼을 이용하여 썰어준다',
          '손질한 채소에 절인 무, 불린 고춧가루, 간 마늘, 간 생강, 황설탕을 넣어 섞어준다',
          '절인 배추에 김칫소를 한 장 한 장 얇게 발라준다',
          '골고루 양념이 묻으면 큰 이파리로 감싸 모양을 잡는다',
          '김치통에 담은 후 꾹꾹 눌러 틈이 생기지 않게 한다',
          '김치통이 채워지면 남은 배추 이파리로 덮어 보관한다'
        ]
      },
      {
        title: '배추전',
        ytLink: 'https://youtu.be/jN6rB-bUQXM?si=jVpN6990zIlrGPdZ',
        ingredients: '[배추전] 배추, 부침가루, 정수물, 식용유 / [양념장] 청양고추, 대파, 진간장, 식초',
        steps: [
          '배추는 세척 후 밑동 1cm 위쪽을 잘라 낱장으로 떨어지게 한다',
          '줄기 부분을 칼 옆면으로 두드려 편다',
          '물기 있는 상태로 부침가루를 뿌려 골고루 묻힌다',
          '부침가루와 물을 1:1 비율로 섞어 물반죽을 만든다',
          '프라이팬을 강불에 올려 예열 후 식용유를 넉넉히 두른다',
          '배추에 물반죽을 얇게 입혀 중불에서 앞뒤로 노릇하게 구워낸다',
          '[양념장] 대파·청양고추를 0.3cm로 썰고 간장과 식초를 1:2로 섞어 곁들인다'
        ]
      }
    ]
  },
  {
    emoji: '🧅', name: '양파',
    recipes: [
      {
        title: '양파볶음',
        ytLink: 'https://youtu.be/xuO5Gvb83jk?si=d3qhhz1XhkcoG3Bk',
        ingredients: '양파 2개, 마늘 반 큰 술, 쪽파(고명) 약간, 식용유 2큰술 / [양념] 간장 2큰술, 설탕 반큰술, 들기름 1큰술, 통깨 약간, 후추 약간',
        steps: [
          '양파를 깨끗이 씻어 두툼하게 썰어준다',
          '뭉쳐있는 양파를 하나하나 떼어준다',
          '중불 팬에 식용유 2큰술을 두르고 마늘 반 큰술을 볶는다',
          '마늘향이 올라오면 양파를 넣어 볶는다',
          '양파가 노릇해지면 간장 2큰술, 설탕 반큰술을 넣고 강불에서 볶는다',
          '수분이 줄면 통깨와 후추를 뿌리고 약불에서 20초 볶는다',
          '약불을 유지하고 들기름 1큰술을 두른다'
        ]
      },
      {
        title: '어니언 스프',
        ytLink: 'https://youtu.be/1O3kG9DQt0s?si=psH1HFpFp-i22VG3',
        ingredients: '양파 1kg, 그뤼에르 치즈 100-200g, 버터 40g, 와인 100ml, 마늘 15g, 바게트, 소금, 후추, 설탕, 육수(치킨·비프·야채 중 택1) 1000ml',
        steps: [
          '양파를 2-3mm 두께로 썰어준다',
          '마늘을 적당히 다져준다',
          '두꺼운 냄비에 버터를 녹이고 양파를 갈색빛이 날 때까지 충분히 볶는다',
          '다진마늘을 넣어 2-3분 볶는다',
          '육수를 넣고 소금간을 한다',
          '뚜껑을 닫고 약불에서 20분 끓여 맛을 우려낸다',
          '어니언 스프용 용기에 스프를 담고 미리 구워둔 바게트를 올린다',
          '치즈를 올려 230-250도 오븐에 5-10분 굽는다',
          '취향에 따라 후추와 타임, 오일을 올려 완성한다'
        ]
      }
    ]
  },
  {
    emoji: '🫜', name: '무',
    recipes: [
      {
        title: '무 생채',
        ytLink: 'https://youtu.be/dXN1dlsYdJI?si=6EujJRSSDkgaQTED',
        ingredients: '무 1/2개(700g), 고운고춧가루 1/4컵(20g), 황설탕 2큰술(20g), 간마늘 1큰술(20g), 식초 1/4컵(40g), 꽃소금 2큰술(20g), 대파 1컵(80g), 깨소금 1큰술(5g)',
        steps: [
          '무는 깨끗이 세척하여 껍질을 제거한다',
          '채칼로 일정한 두께로 썰어 준비한다',
          '대파는 송송 썬다',
          '채 썬 무에 꽃소금, 황설탕, 고운 고춧가루, 간 마늘, 식초, 대파를 넣고 잘 버무린다',
          '깨소금을 넣어 섞은 후 마무리한다'
        ]
      },
      {
        title: '소고기 무국',
        ytLink: 'https://youtu.be/vG07DHeNH9c?si=eSr_AK8134_bqNve',
        ingredients: '무 1과1/2컵(230g), 소양지 1컵(150g), 양파 1/4개(50g), 참기름 1큰술(8g), 식용유 1큰술(8g), 대파 1/3컵(30g), 간마늘 1큰술(15g), 국간장 2큰술(20g), 멸치액젓 2큰술(20g), 꽃소금 1/2큰술(5g), 후춧가루 적당량, 물 1.5L',
        steps: [
          '무는 사방 3cm 정도로 편 썰기 하여 준비한다',
          '소고기는 핏기를 제거하여 준비한다',
          '대파는 송송·어슷 썰고 양파는 채 썰어 준비한다',
          '냄비에 참기름, 식용유를 두르고 소고기를 넣어 볶는다',
          '고기 겉면이 익으면 무를 넣어 볶는다',
          '물, 간마늘, 국간장, 멸치액젓을 넣고 중불에서 20분 끓인다',
          '소고기가 부드러워지면 양파를 넣어 끓인다',
          '소금으로 간을 맞추고 대파, 후추를 넣어 마무리한다'
        ]
      }
    ]
  },
  {
    emoji: '🍉', name: '수박',
    recipes: [
      {
        title: '수박 화채',
        ytLink: 'https://youtu.be/wAktJuv7REY?si=O4zOTvsWzrrgFo51',
        ingredients: '수박(속 부분) 1/4통(800g), 후르츠칵테일 1/2캔(270g), 흰우유 1/5컵(400ml), 사이다 1캔(250ml), 황설탕 4큰술(48g), 얼음 적당량',
        steps: [
          '수박은 사방 2cm 주사위 모양으로 썬다 (칼과 도마는 미리 깨끗이 씻어주세요)',
          '후르츠칵테일은 원액과 함께 준비한다',
          '넓은 볼에 흰 우유, 사이다, 황설탕을 넣고 섞는다',
          '썰어 둔 수박과 후르츠칵테일을 우유에 넣고 섞는다',
          '얼음을 띄워 완성한다'
        ]
      },
      {
        title: '수박 오이 냉국',
        ytLink: 'https://youtu.be/qI1LRerUWXQ?si=fJoyUukgCfgQNbS',
        ingredients: '수박(속 부분) 1/8통(400g), 오이 약 1/2개(100g), 정수 물 2와1/2컵(450ml), 황설탕 4와1/2큰술(54g), 환만식초 4와1/2큰술(36g), 진간장 1과1/2큰술(15g), 꽃소금 약간, 얼음 적당량',
        steps: [
          '수박은 사방 2cm 깍둑 썰기 한다',
          '오이는 반 갈라 얇게 편 썬다',
          '넓은 볼에 물, 황설탕, 진간장, 환만식초, 꽃소금을 넣고 섞어 냉국 육수를 만든다',
          '썰어놓은 수박과 오이를 육수에 넣고 섞는다',
          '얼음을 띄워 완성한다'
        ]
      }
    ]
  },
  {
    emoji: '🍎', name: '사과',
    recipes: [
      {
        title: '사과 파이',
        ytLink: 'https://youtu.be/jVH2k4yNi4o?si=u7ur2inGZ1ye-bSK',
        ingredients: '사과조림 1컵(180g), 중력분 1과1/2컵(150g), 황설탕 1/2컵(80g), 달걀 1개(60g), 우유 1/3컵(65g), 꽃소금 1/2큰술(2g), 베이킹파우더 1큰술(8g), 스틱버터 1/2개(40g), 스틱버터(코팅용) 적당량',
        steps: [
          '버터를 전자레인지에 1분 돌려 녹인 후 식힌다',
          '큰 볼에 달걀, 황설탕을 설탕이 녹을 때까지 거품기로 섞는다',
          '우유를 넣고 섞은 후 꽃소금, 버터를 조금씩 넣어가며 섞는다',
          '중력분, 베이킹파우더를 넣고 뭉치지 않도록 섞는다',
          '사과조림을 넣고 섞어준다',
          '오븐 용기 안쪽에 버터를 얇게 바른다',
          '반죽을 용기에 넣고 바닥을 쳐 공기를 제거한다',
          '에어프라이어 150도에서 10분 예열 후 30분 굽는다',
          '파이가 구워지면 용기에서 분리해 먹기 좋은 크기로 자른다',
          '바닐라 아이스크림, 시나몬 가루를 곁들여 완성한다'
        ]
      },
      {
        title: '사과 고르곤졸라',
        ytLink: 'https://youtu.be/jVH2k4yNi4o?si=u7ur2inGZ1ye-bSK',
        ingredients: '또띠아(20cm) 1장(45g), 사과조림 1컵(180g), 모짜렐라치즈 1컵(110g), 물 2큰술(10g), 고르곤졸라치즈 적당량, 파슬리 가루 적당량',
        steps: [
          '프라이팬을 약불에서 예열한다',
          '또띠아에 사과조림을 넓게 펼친다',
          '모짜렐라치즈를 사과조림 위에 골고루 뿌린다',
          '고르곤졸라 치즈를 잘게 잘라 모짜렐라 위에 올린다',
          '예열된 프라이팬에 물 2큰술을 넣는다',
          '토핑한 피자를 프라이팬에 넣는다',
          '가장 약불에서 뚜껑을 덮고 치즈가 녹을 때까지 굽는다',
          '완성 접시에 꺼내 파슬리가루를 뿌려 완성한다'
        ]
      }
    ]
  },
  {
    emoji: '🍓', name: '딸기',
    recipes: [
      {
        title: '딸기잼',
        ytLink: 'https://youtu.be/fUAl5Z2zjvE?si=LZBYK9zyAIWUrFCo',
        ingredients: '딸기 1kg, 황설탕 2컵(320g), 소금 1/2스푼',
        steps: [
          '딸기를 얇게 슬라이스하고 누름도구로 으깨준다',
          '황설탕 2컵과 소금 1/2스푼을 넣고 저어준다',
          '30분동안 끓여준다 (색이 예쁘려면 거품을 걷어낸다)'
        ]
      },
      {
        title: '딸기 티라미수',
        ytLink: 'https://youtu.be/WtCaqeozjH4?si=Z-TaR7hl6zZU7uMF',
        ingredients: '생크림 75g, 크림치즈 150g, 연유 두큰술, 황설탕 50g, 레몬즙 5큰술, 딸기 500g, 애플민트',
        steps: [
          '딸기를 다양한 모양으로 썰어준다',
          '자른 딸기에 설탕, 레몬즙을 넣어 한 시간 절여준다',
          '생크림, 설탕을 핸드믹서로 잘 섞어준다',
          '크림치즈, 연유를 넣어 섞어준다',
          '준비한 용기에 절인 딸기를 넣고 크림을 올린다',
          '다시 한 번 반복해 넣어준다',
          '애플민트를 올려 완성한다'
        ]
      }
    ]
  }
];

function renderRecipes(data, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = data.map(crop => {
    const items = crop.recipes.map(r => {
      const stepsHtml = r.steps.map((s, i) =>
        '<li class="recipe-item__step"><span class="recipe-item__num">' + (i + 1) + '</span><span>' + s + '</span></li>'
      ).join('');
      return '<div class="recipe-item">' +
        '<div class="recipe-item__hdr">' +
          '<span class="recipe-item__title">' + r.title + '</span>' +
          '<a class="recipe-item__yt" href="' + r.ytLink + '" target="_blank">▶ 동영상</a>' +
        '</div>' +
        '<div class="recipe-item__ingr"><span class="recipe-item__ingr-lbl">🛒 재료</span>' + r.ingredients + '</div>' +
        '<ol class="recipe-item__steps">' + stepsHtml + '</ol>' +
        '</div>';
    }).join('');
    return '<div class="recipe-sec">' +
      '<div class="recipe-sec__hdr">' +
        '<span class="recipe-sec__emoji">' + crop.emoji + '</span>' +
        '<span class="recipe-sec__name">' + crop.name + '</span>' +
      '</div>' + items + '</div>';
  }).join('');
}

renderRecipes(RECIPE_DATA, 'recipeGrid');

const CROPS = [
  {
    id: 'watermelon', emoji: '🍉', name: '수박', sub: 'Watermelon',
    ytLink: 'https://www.youtube.com/shorts/KUeeubKP-uc',
    steps: [
      '수박을 흐르는 물에 깨끗이 씻는다',
      '수박을 반으로 자른다',
      '자른 수박을 두 번 더 반으로 잘라 삼각뿔 모양으로 만든다',
      '각 모서리 부분에 칼을 넣어 과육만 분리한다',
      '원하는 크기로 조각으로 자른다'
    ],
    tip: '자르기 전 냉장 보관하면 더 시원하게 즐길 수 있어요'
  },
  {
    id: 'apple', emoji: '🍎', name: '사과', sub: 'Apple',
    steps: [
      '흐르는 물에 껍질을 손으로 문질러 깨끗이 씻는다',
      '꼭지 부분을 제거한다',
      '4등분하여 씨방과 씨를 V자로 도려낸다',
      '껍질을 벗기거나 그대로 용도에 맞게 썬다'
    ],
    tip: '갈변 방지를 위해 자른 후 소금물이나 레몬물에 잠깐 담가두세요'
  },
  {
    id: 'strawberry', emoji: '🍓', name: '딸기', sub: 'Strawberry',
    steps: [
      '흐르는 물에 가볍게 헹군다 (세게 문지르지 않는다)',
      '물기를 키친타월로 조심스럽게 제거한다',
      '꼭지를 손으로 비틀거나 칼로 잘라 제거한다'
    ],
    tip: '씻기 전 꼭지를 제거하면 물이 들어가 맛이 떨어지므로 반드시 나중에 제거하세요'
  },
  {
    id: 'cabbage', emoji: '🥬', name: '배추', sub: 'Napa Cabbage',
    steps: [
      '겉잎을 2~3장 떼어낸다 (손상되거나 오염된 잎 제거)',
      '밑동을 칼로 평평하게 잘라낸다',
      '밑동에 칼집을 넣고 손으로 찢어 반으로 가른다 (아삭함 유지)',
      '잎을 한 장씩 분리해 흐르는 물에 씻는다',
      '용도에 맞게 먹기 좋은 크기로 썬다'
    ],
    tip: '김치용이라면 소금에 절이기 전, 요리용이라면 씻은 후 바로 사용하세요'
  },
  {
    id: 'onion', emoji: '🧅', name: '양파', sub: 'Onion',
    steps: [
      '겉의 마른 껍질을 손으로 벗겨낸다',
      '위 꼭지 부분과 뿌리 부분을 칼로 잘라낸다',
      '반으로 잘라 흐르는 물에 헹군다',
      '용도에 따라 채썰기, 깍둑썰기, 링 모양으로 썬다'
    ],
    tip: '아린 맛을 줄이고 싶다면, 세로로 써세요'
  },
  {
    id: 'radish', emoji: '🫜', name: '무', sub: 'Radish (Daikon)',
    ytLink: 'https://www.youtube.com/shorts/qnVyhXTte4g?si=_65NYMplLsmEm4sR',
    steps: [
      '흐르는 물에 흙을 꼼꼼히 씻어낸다',
      '무청을 잘라낸다 (육수 활용 가능)',
      '필러로 껍질을 깎아낸다',
      '원하는 크기나 모양으로 썬다'
    ],
    tip: '무 윗부분은 달고 아래로 갈수록 매운 맛이 강해요. 용도에 맞게 부위를 선택하세요'
  }
];

function renderCrops(crops, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = crops.map(crop => {
    const stepsHtml = crop.steps.map((step, i) =>
      '<li class="crop-card__step"><span class="crop-card__num">' + (i + 1) + '</span><span class="crop-card__step-text">' + step + '</span></li>'
    ).join('');
    const ytBtn = crop.ytLink
      ? '<a class="crop-card__yt" href="' + crop.ytLink + '" target="_blank">▶ 동영상으로 보기</a>'
      : '';
    return '<div class="crop-card crop-card--' + crop.id + '">' +
      '<div class="crop-card__header">' +
      '<span class="crop-card__emoji">' + crop.emoji + '</span>' +
      '<div><p class="crop-card__title">' + crop.name + '</p><p class="crop-card__sub">' + crop.sub + '</p></div>' +
      '</div>' +
      '<ol class="crop-card__steps">' + stepsHtml + '</ol>' +
      '<div class="crop-card__tip">💡 ' + crop.tip + '</div>' +
      ytBtn + '</div>';
  }).join('');
}

renderCrops(CROPS, 'cropGrid');

function showPage(page) {
  const map = {home:'pageHome', recipe:'pageRecipe', prep:'pagePrep', history:'pageHistory'};
  const btnMap = {home:'btnHome', recipe:'btnRecipe', prep:'btnPrep', history:'btnHistory'};
  Object.values(map).forEach(id => document.getElementById(id).classList.remove('active'));
  Object.values(btnMap).forEach(id => document.getElementById(id).classList.remove('active'));
  document.getElementById(map[page]).classList.add('active');
  document.getElementById(btnMap[page]).classList.add('active');
  if (page === 'history') renderHistContent();
}

// ---- HISTORY FEATURE ----
const PRODUCE_EMOJI_MAP = {'사과':'🍎','딸기':'🍓','토마토':'🍅','배추':'🥬','감자':'🥔','당근':'🥕','오이':'🥒','양파':'🧅','무':'🫜','수박':'🍉','포도':'🍇','바나나':'🍌'};
function getProduceEmoji(name) {
  for (const [k,v] of Object.entries(PRODUCE_EMOJI_MAP)) { if (name.includes(k)) return v; }
  return '🥬';
}
function getEmojiBg(e) {
  const m={'🍎':'#fce4e4','🍓':'#fce4e4','🍅':'#fce4e4','🥬':'#e4f0e4','🥔':'#fdf5e4','🥕':'#fdecea','🥒':'#e4f0e4','🧅':'#fdf5e4','🫜':'#f5f5f5','🍉':'#fce4e4','🍇':'#f0e4fc','🍌':'#fdf5e4'};
  return m[e]||'#f0f0f0';
}
function getScoreCol(s){const n=parseFloat(s);return n>=8?'#43a047':n>=6?'#7cb342':n>=4?'#fb8c00':'#e53935';}

function loadHistory() {
  try { return JSON.parse(localStorage.getItem('scanHistory') || '[]'); } catch(e) { return []; }
}
function saveHistory(arr) {
  try { localStorage.setItem('scanHistory', JSON.stringify(arr)); } catch(e) {}
}

let lastEntryId = null;
let currentHistTab = 0;

function autoSaveEntry(method) {
  if (!lastResult) return;
  const now = new Date();
  const dateStr = now.getFullYear() + '.' + String(now.getMonth()+1).padStart(2,'0') + '.' + String(now.getDate()).padStart(2,'0');
  const entry = {
    id: Date.now(), produce: lastResult.produce,
    emoji: getProduceEmoji(lastResult.produce),
    score: lastResult.score, date: dateStr, dateMs: Date.now(),
    method: method, starred: false, desc: lastResult.desc || ''
  };
  const hist = loadHistory(); hist.unshift(entry); saveHistory(hist);
  lastEntryId = entry.id;
  const btn = document.getElementById('favBtn');
  if (btn) { btn.textContent = '⭐ 찜하기'; btn.classList.remove('saved'); btn.disabled = false; }
}

function toggleFav() {
  if (!lastEntryId) return;
  const hist = loadHistory();
  const entry = hist.find(h => h.id === lastEntryId);
  if (!entry) return;
  entry.starred = !entry.starred;
  saveHistory(hist);
  const btn = document.getElementById('favBtn');
  if (entry.starred) { btn.textContent = '⭐ 찜됨'; btn.classList.add('saved'); }
  else { btn.textContent = '⭐ 찜하기'; btn.classList.remove('saved'); }
}

function switchHistTab(tab) {
  currentHistTab = tab;
  [0,1,2].forEach(i => document.getElementById('htab'+i).classList.toggle('active', i===tab));
  renderHistContent();
}

function renderHistList() { renderHistContent(); }

function renderHistContent() {
  const content = document.getElementById('histContent');
  if (!content) return;
  const hist = loadHistory();
  if (currentHistTab === 0) renderAllRecords(content, hist, false);
  else if (currentHistTab === 1) renderAllRecords(content, hist.filter(h=>h.starred), true);
  else renderCompareTab(content, hist);
}

function renderAllRecords(content, hist, isStarred) {
  if (!hist.length) {
    const msg = isStarred ? '찜한 항목이 없어요' : '분석 기록이 없어요';
    const sub = isStarred ? '기록 목록에서 ⭐를 눌러 찜하세요!' : '홈에서 농산물을 분석하면 자동으로 저장돼요!';
    const ico = isStarred ? '⭐' : '📋';
    content.innerHTML = '<div class="hist-empty"><div class="hist-empty-ico">'+ico+'</div><div class="hist-empty-t">'+msg+'</div><div class="hist-empty-s">'+sub+'</div></div>';
    return;
  }
  const allHist = loadHistory();
  const byProduce = {};
  allHist.forEach(h => { if(!byProduce[h.produce]) byProduce[h.produce]=[]; byProduce[h.produce].push(h); });
  const items = hist.map(h => {
    const col = getScoreCol(h.score);
    const bg = getEmojiBg(h.emoji||'🥬');
    const methodLabel = h.method==='cam'?'카메라 스캔':h.method==='upload'?'갤러리 업로드':'분석';
    const group = byProduce[h.produce]||[];
    const idx = group.findIndex(g=>g.id===h.id);
    const prev = group[idx+1];
    let changeHtml = '<span style="color:#bbb;font-weight:700;font-size:10px;">✨ 첫 분석</span>';
    if (prev) {
      const raw = parseFloat(h.score) - parseFloat(prev.score);
      const days = Math.max(1, Math.round((h.dateMs - prev.dateMs)/86400000));
      const arrow = raw>=0?'▲':'▼'; const cc = raw>=0?'#2d7a3a':'#e53935';
      changeHtml = '<span style="color:'+cc+';font-weight:800;font-size:10px;">'+arrow+Math.abs(raw).toFixed(1)+'점 ('+days+'일 전 대비)</span>';
    }
    const starTxt = h.starred ? '⭐' : '☆';
    return '<div class="hlist-item">' +
      '<div class="hlist-ico" style="background:'+bg+'">'+(h.emoji||'🥬')+'</div>' +
      '<div class="hlist-info"><div class="hlist-name">'+h.produce+'</div><div class="hlist-meta">'+h.date+' · '+methodLabel+'</div></div>' +
      '<div class="hlist-right"><div class="hlist-score" style="color:'+col+'">'+h.score+'점</div><div class="hlist-change">'+changeHtml+'</div></div>' +
      '<span style="font-size:18px;cursor:pointer;flex-shrink:0;user-select:none;" onclick="toggleItemStar('+h.id+',this)">'+starTxt+'</span>' +
      '<button onclick="openRescan('+h.id+')" style="background:none;border:none;font-size:16px;cursor:pointer;flex-shrink:0;padding:2px 1px;" title="재스캔">🔄</button>' +
      '<button onclick="deleteHist('+h.id+')" style="background:none;border:none;color:#ccc;font-size:20px;cursor:pointer;flex-shrink:0;padding:2px 1px;line-height:1;">×</button>' +
    '</div>';
  }).join('');
  content.innerHTML = '<div class="hsec-hdr"><span class="hsec-t">전체 분석 기록</span><span class="hsec-cnt">총 '+hist.length+'건</span></div>' + items;
}

function toggleItemStar(id, el) {
  const hist = loadHistory();
  const entry = hist.find(h=>h.id===id);
  if (!entry) return;
  entry.starred = !entry.starred;
  saveHistory(hist);
  el.textContent = entry.starred ? '⭐' : '☆';
  if (id === lastEntryId) {
    const btn = document.getElementById('favBtn');
    if (btn) { btn.textContent=entry.starred?'⭐ 찜됨':'⭐ 찜하기'; if(entry.starred)btn.classList.add('saved');else btn.classList.remove('saved'); }
  }
}

function renderCompareTab(content, hist) {
  if (hist.length < 2) {
    content.innerHTML = '<div class="hist-empty"><div class="hist-empty-ico">📊</div><div class="hist-empty-t">비교할 데이터가 부족해요</div><div class="hist-empty-s">같은 농산물을 2번 이상 분석하면 비교할 수 있어요!</div></div>';
    return;
  }
  const groups = {};
  hist.forEach(h => { if(!groups[h.produce]) groups[h.produce]=[]; groups[h.produce].push(h); });
  const multiGroups = Object.entries(groups).filter(([,v])=>v.length>=2);
  if (!multiGroups.length) {
    content.innerHTML = '<div class="hist-empty"><div class="hist-empty-ico">📊</div><div class="hist-empty-t">비교할 데이터가 부족해요</div><div class="hist-empty-s">같은 농산물을 2번 이상 분석해보세요!</div></div>';
    return;
  }
  let alertHtml = '';
  multiGroups.forEach(([name, entries]) => {
    const sorted = [...entries].sort((a,b)=>a.dateMs-b.dateMs);
    const last=sorted[sorted.length-1], prev=sorted[sorted.length-2];
    const diff = parseFloat(last.score)-parseFloat(prev.score);
    if (diff < -0.5 && !alertHtml) {
      const emoji = sorted[0].emoji||'🥬';
      alertHtml = '<div class="hist-alert"><span style="font-size:26px;flex-shrink:0;">📉</span><div><div class="hist-alert-t">'+emoji+' '+name+' 신선도가 떨어지고 있어요!</div><div class="hist-alert-s">지난 '+sorted.length+'번의 분석 결과를 확인해보세요</div></div></div>';
    }
  });
  const cards = multiGroups.map(([name, entries]) => {
    const sorted = [...entries].sort((a,b)=>a.dateMs-b.dateMs);
    const emoji = sorted[0].emoji||'🥬';
    const totalDiff = parseFloat(sorted[sorted.length-1].score)-parseFloat(sorted[0].score);
    const badge = '<span class="hbadge '+(totalDiff>=0?'up':'dn')+'">'+(totalDiff>=0?'▲':'▼')+Math.abs(totalDiff).toFixed(1)+'점</span>';
    const rows = sorted.slice(-4).map((e,i,arr) => {
      const isLast = i===arr.length-1;
      const lbl = isLast ? '오늘' : e.date.slice(5).replace('.','/');
      const col = getScoreCol(e.score);
      const pct = Math.min(100, parseFloat(e.score)*10);
      return '<div class="hbar-row"><span class="hbar-date">'+lbl+'</span><div class="hbar-track"><div class="hbar-fill" style="width:'+pct+'%;background:'+col+'"></div></div><span class="hbar-score" style="color:'+col+'">'+e.score+'</span></div>';
    }).join('');
    return '<div class="hcmp-card"><div class="hcmp-hdr"><span class="hcmp-name">'+emoji+' '+name+'</span>'+badge+'</div>'+rows+'</div>';
  }).join('');
  content.innerHTML = alertHtml + '<div class="hsec-hdr" style="margin-bottom:10px;"><span class="hsec-t">📊 최근 분석 비교</span></div>' + cards;
}

function deleteHist(id) {
  saveHistory(loadHistory().filter(h => h.id !== id));
  renderHistContent();
}

let currentRescanId = null;
let rescanStream = null;
let rescanFacingMode = 'environment';

function openRescan(id) {
  currentRescanId = id;
  document.getElementById('rescanOverlay').classList.add('open');
  document.getElementById('rescanCamResult').style.display = 'none';
  document.getElementById('rescanFileResult').style.display = 'none';
  document.getElementById('rescanCompareResult').style.display = 'none';
  document.getElementById('rescanCamImg').src = '';
  document.getElementById('rescanFileImg').src = '';
  switchRescanTab('cam');
}

function closeRescan() {
  document.getElementById('rescanOverlay').classList.remove('open');
  stopRescanCam(null);
  currentRescanId = null;
}

function switchRescanTab(tab) {
  const isCam = tab === 'cam';
  document.getElementById('rescanCamSection').style.display = isCam ? 'block' : 'none';
  document.getElementById('rescanFileSection').style.display = isCam ? 'none' : 'block';
  document.getElementById('rescanTabCam').style.background = isCam ? '#e8f5e9' : '#f0f0f0';
  document.getElementById('rescanTabCam').style.color = isCam ? '#2d7a3a' : '#888';
  document.getElementById('rescanTabFile').style.background = isCam ? '#f0f0f0' : '#e8f5e9';
  document.getElementById('rescanTabFile').style.color = isCam ? '#888' : '#2d7a3a';
  if (!isCam) stopRescanCam(null);
}

async function startRescanCam(mode) {
  if (mode) rescanFacingMode = mode;
  try {
    if (rescanStream) { rescanStream.getTracks().forEach(t => t.stop()); rescanStream = null; }
    rescanStream = await navigator.mediaDevices.getUserMedia({video:{facingMode: rescanFacingMode}, audio:false});
    const v = document.getElementById('rescanCamVideo');
    v.srcObject = rescanStream; v.style.display = 'block';
    document.getElementById('rescanCamPH').style.display = 'none';
    document.getElementById('rescanCamBtns').style.display = 'flex';
  } catch(e) { alert('카메라 권한을 허용해주세요.'); }
}

function flipRescanCam(e) { e.stopPropagation(); startRescanCam(rescanFacingMode === 'environment' ? 'user' : 'environment'); }

function stopRescanCam(e) {
  if (e) e.stopPropagation();
  if (rescanStream) { rescanStream.getTracks().forEach(t => t.stop()); rescanStream = null; }
  const v = document.getElementById('rescanCamVideo'); if(v) v.style.display = 'none';
  const ph = document.getElementById('rescanCamPH'); if(ph) ph.style.display = 'flex';
  const bt = document.getElementById('rescanCamBtns'); if(bt) bt.style.display = 'none';
}

function shootRescan(e) {
  e.stopPropagation();
  const v = document.getElementById('rescanCamVideo');
  const c = document.getElementById('rescanCvs');
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext('2d').drawImage(v, 0, 0);
  stopRescanCam(null);
  document.getElementById('rescanCamImg').src = c.toDataURL('image/jpeg');
  document.getElementById('rescanCamResult').style.display = 'block';
  document.getElementById('rescanCompareResult').style.display = 'none';
}

function loadRescanFile(e) {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    document.getElementById('rescanFileImg').src = ev.target.result;
    document.getElementById('rescanFileResult').style.display = 'block';
    document.getElementById('rescanCompareResult').style.display = 'none';
  };
  reader.readAsDataURL(file);
}

async function doRescan(src) {
  if (!currentRescanId) return;
  const hist = loadHistory();
  const entry = hist.find(h => h.id === currentRescanId);
  if (!entry) return;
  const imgEl = document.getElementById(src === 'cam' ? 'rescanCamImg' : 'rescanFileImg');
  if (!imgEl.src || imgEl.src === window.location.href) { alert('사진을 먼저 준비해주세요!'); return; }
  const resultEl = document.getElementById('rescanCompareResult');
  resultEl.style.display = 'block';
  resultEl.innerHTML = '<div style="text-align:center;padding:20px;color:#aaa;font-size:13px;font-weight:700;">⏳ AI 분석 중...</div>';
  resultEl.scrollIntoView({behavior:'smooth', block:'nearest'});
  try {
    const base64 = imgToBase64(imgEl);
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {'Authorization': 'Bearer ' + GROQ_API_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify({
        model: 'meta-llama/llama-4-scout-17b-16e-instruct', temperature: 0,
        messages: [{role:'user', content:[
          {type:'image_url', image_url:{url:'data:image/jpeg;base64,' + base64}},
          {type:'text', text:'사진 속 ' + entry.produce + '의 신선도를 엄격하게 채점하세요.\\n[채점 규칙]\\n• 곰팡이·악취 → 2점 이하\\n• 부패·변색·물러짐 → 4점 이하\\n• 완벽히 신선 → 8점 이상\\n• 점수는 소수점 첫째 자리까지\\n[출력 형식]\\n종합 신선도 점수: (0.0~10.0)\\n상태 설명: (한 문장)'}
        ]}]
      })
    });
    if (!res.ok) throw new Error('API 오류: ' + res.status);
    const json = await res.json();
    const raw = json.choices[0].message.content.replace(/\\*+/g,'').replace(/#+/g,'').trim();
    const parseScore = r => { const m = (r||'').match(/([\\d.]+)/); return m ? parseFloat(m[1]) : 5.0; };
    let newScore = 5.0; let newDesc = '';
    raw.split('\\n').forEach(line => {
      if (line.includes('신선도 점수') || line.includes('종합')) newScore = parseScore(line);
      else if (line.includes('상태 설명') || line.includes('설명')) newDesc = line.slice(line.indexOf(':')+1).trim();
    });
    newScore = Math.max(0, Math.min(10, newScore));

    let aiComment = '';
    try {
      const aiRes = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {'Authorization': 'Bearer ' + GROQ_API_KEY, 'Content-Type': 'application/json'},
        body: JSON.stringify({
          model: 'meta-llama/llama-4-scout-17b-16e-instruct',
          messages: [{role:'user', content: entry.produce + '을(를) ' + entry.date + '에 신선도 ' + entry.score + '점으로 저장했고, 오늘 재스캔 결과 ' + newScore.toFixed(1) + '점입니다. 변화를 친근하게 한국어 두 문장으로 설명해주세요. 다른 말은 쓰지 마세요.'}]
        })
      });
      if (aiRes.ok) {
        const aiJson = await aiRes.json();
        aiComment = aiJson.choices[0].message.content.replace(/\\*+/g,'').replace(/#+/g,'').trim();
      }
    } catch(e) {}

    const origScore = parseFloat(entry.score);
    const diff = newScore - origScore;
    const diffStr = (diff >= 0 ? '+' : '') + diff.toFixed(1);
    const diffColor = diff < -0.3 ? '#e53935' : diff > 0.3 ? '#43a047' : '#888';
    const daysElapsed = Math.max(0, Math.round((Date.now() - entry.dateMs) / 86400000));
    const origCol = origScore >= 8 ? '#43a047' : origScore >= 6 ? '#7cb342' : origScore >= 4 ? '#fb8c00' : '#e53935';
    const newCol  = newScore  >= 8 ? '#43a047' : newScore  >= 6 ? '#7cb342' : newScore  >= 4 ? '#fb8c00' : '#e53935';
    resultEl.innerHTML =
      '<div style="font-size:13px;font-weight:900;color:#111;margin-bottom:10px;">📊 재스캔 결과</div>' +
      '<div class="htimeline">' +
        '<div class="htl-node">' +
          '<div class="htl-circle" style="background:' + origCol + '22;color:' + origCol + '">' + entry.score + '</div>' +
          '<div class="htl-label">처음<br>' + entry.date + '</div>' +
        '</div>' +
        '<div class="htl-line"></div>' +
        '<div class="htl-node">' +
          '<div class="htl-circle" style="background:' + newCol + '22;color:' + newCol + '">' + newScore.toFixed(1) + '</div>' +
          '<div class="htl-label">지금<br>오늘</div>' +
        '</div>' +
      '</div>' +
      '<div class="hstats-row">' +
        '<div class="hstat"><div class="hstat-label">경과 일수</div><div class="hstat-val">' + daysElapsed + '일</div></div>' +
        '<div class="hstat"><div class="hstat-label">신선도 변화</div><div class="hstat-val" style="color:' + diffColor + '">' + diffStr + '점</div></div>' +
        '<div class="hstat"><div class="hstat-label">현재 상태</div><div class="hstat-val" style="color:' + newCol + '">' + newScore.toFixed(1) + '점</div></div>' +
      '</div>' +
      (aiComment ? '<div class="hai-comment">🤖 ' + aiComment + '</div>' : '') +
      (newDesc ? '<div style="background:#f7f9f7;border-radius:10px;padding:8px 12px;font-size:11px;color:#555;margin-top:8px;line-height:1.6;">' + newDesc + '</div>' : '');
  } catch(err) {
    resultEl.innerHTML = '<div style="text-align:center;padding:16px;color:#e53935;font-size:13px;font-weight:700;">오류: ' + err.message + '</div>';
  }
}

</script>
</body>
</html>"""

html = html.replace('__GROQ_KEY__', groq_key)
components.html(html, height=920, scrolling=False)
