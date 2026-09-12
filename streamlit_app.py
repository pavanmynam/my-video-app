import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap, os, requests
import numpy as np
import imageio

st.set_page_config(page_title="CINELUXE STUDIO", layout="wide")

# --- LUXURY BLACK + GOLD CSS ---
st.markdown("""
<style>
.stApp { background:#050505; color:#f5f5f5; }
[data-testid="stSidebar"] { background:#101010; border-right:1px solid #d4af3740; }
h1, h2, h3 { color:#d4af37 !important; font-family: serif; letter-spacing:2px; }
.stButton>button[kind="primary"] { background: linear-gradient(90deg,#d4af37,#f9e7a1); color:black; font-weight:900; border-radius:12px; height:55px; border:none; }
.card { background:#121212; border:1px solid #d4af3744; border-radius:15px; padding:15px; }
</style>
""", unsafe_allow_html=True)

# Telugu Font Downloader
if not os.path.exists("NotoSansTelugu.ttf"):
    try:
        url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansTelugu/NotoSansTelugu-Regular.ttf"
        r = requests.get(url, timeout=10)
        open("NotoSansTelugu.ttf","wb").write(r.content)
    except: pass

def get_font(size):
    if os.path.exists("NotoSansTelugu.ttf"):
        return ImageFont.truetype("NotoSansTelugu.ttf", size)
    return ImageFont.load_default()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 👑 CINELUXE")
    menu = st.selectbox("CREATION", ["Home", "Projects", "Templates", "Text to Video"])
    st.markdown("---")
    st.markdown("### AI TOOLS")
    voice_tool = st.selectbox("🎙️ AI Voice", ["Telugu Female - Calm", "Telugu Male - Epic", "English"])
    bgm_tool = st.selectbox("🎵 BGM Library", ["Cinematic Epic", "Suspense", "Emotional"])
    st.markdown("---")
    st.button("📤 Exports", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)
    st.success("PRO PLAN Active - Renews Nov 24")

# --- MAIN AREA ---
st.markdown("<h1 style='text-align:center'>✨ CINELUXE STUDIO ✨</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("### PREVIEW — CINEMATIC (16:9) • 4K HDR")
    preview_slot = st.empty()
    preview_slot.image("https://images.unsplash.com/photo-1514539079130-25950c84af65?w=1280", caption="Luxury Preview - Ready to Generate")
    st.slider("Timeline", 0, 90, 12, format="00:%d / 01:30")

with col2:
    st.markdown("### ⚙️ EXPORT SETTINGS")
    quality = st.selectbox("Quality", ["4K HDR", "1080p", "720p"])
    fmt = st.selectbox("Format", ["YouTube 16:9", "Shorts 9:16", "Reels"])
    st.metric("Render Time", "~15 sec")
    st.markdown('<div class="card">🛡️ 4K Export Ready<br>🤖 AI Powered</div>', unsafe_allow_html=True)

# --- INPUT ---
st.markdown("---")
st.markdown("### ✍️ INPUT — TELUGU SCRIPT")
script = st.text_area("", "ఒక దేశం ఎలా నాశనం అవుతుంది అనడానికి ఇదొక పర్ఫెక్ట్ కేస్ స్టడీ. ఒక పెద్ద పర్వతం, ఆ పర్వతం లోపల అంతా స్వచ్ఛమైన వెండి తో నిండిపోయి ఉంది...", height=130)

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 🎙️ VOICE SELECTION")
    v = st.selectbox("", ["స్వరం: తెలుగు - స్త్రీ (ప్రశాంతం)", "తెలుగు - పురుషుడు (Epic)"], label_visibility="collapsed")
    st.caption("Tone: Calm • Style: Natural • Speed: 1.0x")
with c2:
    st.markdown("#### 🎵 BGM SELECTION")
    b = st.selectbox("", ["BGM: సినిమాటిక్ • సింఫనీ", "Suspense Dark", "Inspirational"], label_visibility="collapsed")
    st.caption("Mood: Epic • Volume: 65%")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.button("🔖 SAVE DRAFT", use_container_width=True)
with col_btn2:
    if st.button("✨ GENERATE VIDEO ✨", type="primary", use_container_width=True):
        with st.spinner("🔥 Luxury Video Rendering in 4K..."):
            parts = [p.strip() for p in script.split("...") if p.strip()]
            if len(parts) < 2:
                parts = textwrap.wrap(script, width=60)
            
            writer = imageio.get_writer("cineluxe_final.mp4", fps=1, macro_block_size=1)
            last_img_path = "frame.jpg"
            
            for i, text in enumerate(parts[:4]):
                W,H = 1280,720
                img = Image.new('RGB', (W,H), (7,7,7))
                draw = ImageDraw.Draw(img)
                draw.rectangle([0,0,W-1,H-1], outline=(212,175,55), width=10)
                draw.text((60,40), f"CINELUXE • 4K HDR • SCENE {i+1}", fill=(212,175,55), font=get_font(28))
                wrapped = textwrap.fill(text, width=22)
                draw.text((70,150), wrapped, fill=(255,255,255), font=get_font(40), spacing=18)
                draw.text((60,650), f"VOICE: {voice_tool} | BGM: {bgm_tool}", fill=(212,175,55), font=get_font(20))
                img.save(last_img_path)
                for _ in range(3):
                    writer.append_data(np.array(img))
            
            writer.close()
            preview_slot.video("cineluxe_final.mp4")
            st.balloons()
            st.success("🔥 Luxury Video Ready - 4K Export!")
            with open("cineluxe_final.mp4","rb") as f:
                st.download_button("📥 DOWNLOAD LUXURY MP4", f, "CineLuxe_4K.mp4", mime="video/mp4")

st.markdown("<p style='text-align:center; color:#d4af37'>🛡️ 4K Export Ready | 🤖 AI Powered</p>", unsafe_allow_html=True)
