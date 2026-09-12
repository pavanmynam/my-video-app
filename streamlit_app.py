import streamlit as st, requests, re, io
from PIL import Image
import numpy as np, imageio

st.set_page_config(page_title="CINELUXE UNIVERSAL", layout="wide", page_icon="👑")

st.markdown("""
<style>
.stApp{background:#080808;color:#f5e6c8}
section[data-testid="stSidebar"]{background:#111;border-right:1.5px solid #d4af37}
h1,h2{color:#d4af37!important}
div.stButton>button{background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;font-weight:900;height:60px;border-radius:12px;border:none;font-size:18px}
textarea{background:#1a1a1a!important;color:#fff!important;border:1px solid #d4af37!important;border-radius:14px!important}
.preview{background:#111;border:1px solid #d4af37;border-radius:20px;padding:15px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='text-align:center'>👑 CINELUXE</h1>", unsafe_allow_html=True)
    st.markdown("Universal - Em script aina work avtundi!")

st.markdown("<h1 style='text-align:center'>✨ UNIVERSAL TEXT TO VIDEO ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:0.7'>Em script paste chesina - prathi sentence ki video vastundi. Malli code avasaram ledu!</p>", unsafe_allow_html=True)

def split_sentences(text):
    parts = re.split(r'[.!?।\n]+', text)
    return [p.strip() for p in parts if len(p.strip()) > 15]

# --- UNIVERSAL - NO KEYWORDS! ---
def get_visual(sentence, idx):
    # Nee sentence ne direct prompt - em language aina
    return f"{sentence}, cinematic movie scene, ultra realistic, 8k hdr, dramatic light, no text, no watermark"

left, right = st.columns([1,1.4])
with left:
    script = st.text_area("INPUT — TELUGU SCRIPT", height=300, placeholder="Ne script ikkada paste chey... Oka desham ela nasanam avutundi... dollars dachadam... parvatham... edi aina...")
    scenes = st.slider("Max Scenes", 3, 12, 10)
    gen = st.button("✨ GENERATE VIDEO ✨", use_container_width=True)

with right:
    st.markdown('<div class="preview">', unsafe_allow_html=True)
    if gen and script:
        sentences = split_sentences(script)
        st.success(f"📜 {len(sentences)} sentences found - anni visuals ga vastayi!")
        
        images = []
        for i, sent in enumerate(sentences[:scenes]):
            st.markdown(f"**Scene {i+1}:** {sent}")
            prompt = get_visual(sent, i)
            try:
                url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1280&height=720&nologo=true&model=flux&seed={i*13}"
                r = requests.get(url, timeout=90)
                im = Image.open(io.BytesIO(r.content))
                st.image(im, use_container_width=True)
                images.append(im)
            except Exception as e:
                st.error(f"Scene {i+1} loading...")
        
        if len(images) >= 2:
            st.markdown("---")
            st.markdown("### 🎬 FINAL VIDEO")
            try:
                frames = [np.array(img.resize((1280,720)).convert("RGB")) for img in images]
                out = "/tmp/universal.mp4"
                imageio.mimsave(out, frames, fps=0.9, macro_block_size=1)
                st.video(out)
                with open(out,"rb") as f:
                    st.download_button("⬇️ DOWNLOAD VIDEO", f, file_name="cineluxe_universal.mp4", mime="video/mp4", use_container_width=True)
            except Exception as e:
                st.error("Video stitch lo time padutundi - images download chesko!")
    else:
        st.info("Script paste chesi GENERATE nokku bro - em script aina vastundi!")
    st.markdown('</div>', unsafe_allow_html=True)
