import streamlit as st
import requests, re, io, time
from PIL import Image
import numpy as np
import imageio

st.set_page_config(page_title="CINELUXE", layout="wide", page_icon="👑")

# --- LUXURY BLACK+GOLD CSS (Nee Screenshot Design) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');
.stApp { background: #080808; color: #f5e6c8; }
section[data-testid="stSidebar"] { background: #111; border-right: 1.5px solid #d4af37; }
h1,h2,h3 { font-family: 'Cinzel', serif; color: #d4af37 !important; }
div.stButton > button { background: linear-gradient(90deg, #d4af37, #f9e27a); color: #000; font-weight: 900; border-radius: 12px; height: 60px; font-size: 19px; border: none; }
div.stButton > button:hover { transform: scale(1.02); }
textarea { background: #1a1a1a !important; color: #fff !important; border: 1px solid #d4af37 !important; border-radius: 14px !important; }
.preview-box { background: #111; border: 1px solid #d4af37; border-radius: 20px; padding: 18px; }
.gold-card { background: #151515; border: 1px solid #d4af37; border-radius: 14px; padding: 16px; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center'>👑 CINELUXE</h1>", unsafe_allow_html=True)
    st.markdown("**CREATION**")
    st.button("◆ Home", use_container_width=True)
    st.button("◈ Projects", use_container_width=True)
    st.button("📄 Text to Video", use_container_width=True)
    st.markdown("---")
    st.markdown("**AI TOOLS**")
    st.button("🎙️ AI Voice", use_container_width=True)
    st.button("🎵 BGM Library", use_container_width=True)
    st.markdown("<div style='background:linear-gradient(90deg,#d4af37,#f9e27a); color:#000; padding:12px; border-radius:10px; text-align:center; font-weight:800;'>PRO PLAN<br><small>Active — Renews Nov 24</small></div>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>CINELUXE — CINEMATIC (16:9) · 4K HDR</h1>", unsafe_allow_html=True)

# --- LOGIC: EVERY SENTENCE VISIBLE ---
def split_sentences(text):
    parts = re.split(r'[.!?।\n]+', text)
    return [p.strip() for p in parts if len(p.strip()) > 12]

def visual_prompt(sent):
    s = sent.lower()
    if "parvatham" in s or "konda" in s: return "giant silver mountain full of pure silver, glowing mine inside, cinematic epic 4k"
    if "vendi" in s: return "pure silver shining inside dark mountain cave, treasure, 80 percent world silver"
    if "gurram" in s: return "black horse running fast in dark misty forest, cinematic slow motion"
    if "adavi" in s: return "dense dark mysterious forest at golden sunset, foggy drone shot"
    if "gramam" in s: return "ancient old Indian village, mist, cinematic"
    if "nasana" in s or "yuddh" in s: return "epic destruction, country collapse, dark storm clouds cinematic"
    return f"{sent[:80]}, cinematic ultra realistic 4k hdr, no text, no words"

left, right = st.columns([1, 1.3])
with left:
    st.markdown("### INPUT — TELUGU SCRIPT")
    script = st.text_area("", height=220, placeholder="Oka desham ela nasanam avutundi... Oka pedda parvatham, aa parvatham lopala antha swachhamaina vendi to nindipoyi undi...", label_visibility="collapsed")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**VOICE SELECTION**")
        st.selectbox("", ["స్వరం: తెలుగు — స్త్రీ (ప్రశాంతం)", "Telugu Male", "English"], label_visibility="collapsed")
        st.caption("Tone: Calm • Style: Natural • Speed: 1.0x")
    with col_b:
        st.markdown("**BGM SELECTION**")
        st.selectbox("", ["BGM: సినిమాటిక్ • సింఫొనీ", "Epic", "Sad"], label_visibility="collapsed")
        st.caption("Mood: Epic • Volume: 65%")
    
    gen = st.button("✨ GENERATE VIDEO ✨", use_container_width=True)
    st.button("🔖 SAVE DRAFT", use_container_width=True)

with right:
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    if gen and script:
        sents = split_sentences(script)
        st.info(f"📜 {len(sents)} sentences found — prathi sentence ki video frame vastundi!")
        imgs = []
        for i, sentence in enumerate(sents):
            prompt = visual_prompt(sentence)
            st.markdown(f"**Scene {i+1}:** {sentence}")
            try:
                url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1280&height=720&nologo=true&model=flux&seed={i*7}"
                r = requests.get(url, timeout=90)
                im = Image.open(io.BytesIO(r.content))
                st.image(im, use_container_width=True)
                imgs.append(im)
            except Exception as e:
                st.error(f"Scene {i+1} error: {e}")
        
        if len(imgs) > 1:
            st.success(f"✅ {len(imgs)} frames generated - ippudu video avutundi!")
            try:
                frames = [np.array(img.resize((1280,720)).convert("RGB")) for img in imgs]
                out_path = "/tmp/cineluxe_final.mp4"
                imageio.mimsave(out_path, frames, fps=1, macro_block_size=1)
                st.video(out_path)
                with open(out_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD FULL VIDEO", f, file_name="cineluxe.mp4", mime="video/mp4")
            except Exception as e:
                st.error(f"Video stitch error: {e}")
    else:
        st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200", use_container_width=True)
        st.markdown("00:12 ———●———— 01:30 &nbsp;&nbsp; 4K Export Ready • AI Powered")
    st.markdown('</div>', unsafe_allow_html=True)
