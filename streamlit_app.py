import streamlit as st, requests, re, io, time
from PIL import Image, ImageEnhance
import numpy as np, imageio

st.set_page_config(page_title="CINELUXE PRO", layout="wide", page_icon="👑")

# --- PREMIUM UI - NEE SCREENSHOT LAAGANE ---
st.markdown("""
<style>
.stApp{background:#0a0a0a;color:#f5e6c8}
section[data-testid="stSidebar"]{background:#111111;border-right:2px solid #d4af37;min-width:280px}
div.stButton>button{background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;font-weight:900;border-radius:12px;border:none;height:58px;font-size:16px}
textarea{background:#1e1e1e!important;color:#fff!important;border:1px solid #d4af37!important;border-radius:12px!important}
.stSelectbox div[data-baseweb="select"]{background:#1e1e1e;border:1px solid #333}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color:#d4af37;text-align:center;letter-spacing:2px'>👑 CINELUXE</h1>", unsafe_allow_html=True)
    st.markdown("**CREATION**")
    st.button("🏠 Home", use_container_width=True)
    st.button("📁 Projects", use_container_width=True)
    st.button("📄 Templates", use_container_width=True)
    st.button("📝 Text to Video", use_container_width=True)
    st.markdown("---")
    st.markdown("**AI TOOLS**")
    st.button("🎤 AI Voice", use_container_width=True)
    st.button("🎵 BGM Library", use_container_width=True)
    st.markdown("---")
    st.button("📤 Exports", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)
    st.markdown("<div style='background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;padding:14px;border-radius:12px;margin-top:20px;text-align:center;font-weight:900'>PRO PLAN<br><small>Active - Renews Nov 24</small></div>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#d4af37'>PREVIEW — CINEMATIC (16:9) · 4K HDR</h3>")
st.markdown("<div style='height:320px;background:linear-gradient(180deg,#2a2a2a,#000);border-radius:16px;display:flex;align-items:center;justify-content:center;border:1px solid #333'><span style='font-size:70px'>▶️</span></div>", unsafe_allow_html=True)
st.slider("00:12 — 01:30", 0, 100, 12, disabled=True)

st.markdown("### INPUT — TELUGU SCRIPT")
script = st.text_area("", height=130, placeholder="శిక్ష: నా సినిమా కథ - ఒక ప్రయాణం ప్రారంభం. పాత గ్రామం, మట్టి ఇల్లు...")

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox("🎤 VOICE SELECTION", ["తెలుగు - శ్రీ (ప్రశాంతం) | Tone: Calm - Speed: 1.0x", "తెలుగు - లక్ష్మి (ఎమోషనల్)", "English - Deep Male"])
with col2:
    bgm = st.selectbox("🎵 BGM SELECTION", ["BGM: సినిమాటిక్ - సింఫనీ | Mood: Epic - Vol: 65%", "BGM: Emotional Piano", "BGM: Suspense Thriller"])
    max_scenes = st.slider("Max Scenes", 3, 15, 10)

def split_sentences(text):
    parts = [p.strip() for p in re.split(r'[.!?।\n]+', text) if len(p.strip()) > 15]
    return parts

if st.button("✨ GENERATE VIDEO ✨", use_container_width=True):
    if not script:
        st.warning("Bro script pettu mundu!")
    else:
        start = time.time()
        sents = split_sentences(script)[:max_scenes]
        
        prog = st.progress(0)
        status = st.empty()
        timer_info = st.empty()
        
        st.success(f"📜 {len(sents)} sentences found! | Expected Video: {len(sents)*1.2:.1f} sec")
        
        imgs = []
        for i, s in enumerate(sents):
            elapsed = time.time() - start
            eta = (elapsed / (i+1)) * (len(sents) - (i+1)) if i>0 else 0
            
            prog.progress((i+1)/len(sents))
            status.markdown(f"### 🎬 Scene {i+1}/{len(sents)}")
            timer_info.markdown(f"⏱️ **Elapsed:** {int(elapsed)}s | **Remaining:** {int(eta)}s | **Final Video Length:** {len(sents)*1.2:.1f}s")
            
            try:
                enhanced_prompt = f"{s}, ultra realistic cinematic movie scene, 8K HDR, sharp focus, highly detailed, vibrant full colors, professional color grading, dramatic lighting, skin texture detailed, no blur, no black and white"
                url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(enhanced_prompt)}?width=1920&height=1080&model=flux&enhance=true&nologo=true&seed={i*17}"
                r = requests.get(url, timeout=90)
                im = Image.open(io.BytesIO(r.content)).convert("RGB")
                # ULTRA CLARITY BOOST
                im = ImageEnhance.Sharpness(im).enhance(1.8)
                im = ImageEnhance.Color(im).enhance(1.35)
                im = ImageEnhance.Contrast(im).enhance(1.15)
                st.image(im, caption=f"Scene {i+1}: {s[:70]}...", use_container_width=True)
                imgs.append(im)
            except Exception as e:
                st.error(f"Scene {i+1} error - retry")
        
        if imgs:
            total_gen_time = int(time.time() - start)
            st.markdown(f"## ✅ DONE! Generation Time: {total_gen_time}s")
            
            # KEN BURNS - ZOOM MOVEMENT EFFECT
            with st.spinner("🎥 Adding cinematic movement..."):
                frames = []
                for img in imgs:
                    base = img.resize((1280,720))
                    for z in range(12): # 12 frames per image = smooth zoom
                        zoom = 1 + (z * 0.012)
                        w,h = base.size
                        nw, nh = int(w*zoom), int(h*zoom)
                        zoomed = base.resize((nw,nh)).crop(((nw-w)//2, (nh-h)//2, (nw-w)//2+w, (nh-h)//2+h))
                        frames.append(np.array(zoomed))
                
                out_path = "/tmp/cineluxe_final.mp4"
                imageio.mimsave(out_path, frames, fps=12, macro_block_size=1)
                
                final_duration = len(frames)/12
                st.success(f"🎬 Final Video: {final_duration:.1f} seconds | {len(imgs)} scenes with movement")
                st.video(out_path)
                st.download_button("⬇️ DOWNLOAD 4K VIDEO", open(out_path,"rb"), file_name="cineluxe_4k.mp4", use_container_width=True)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a: st.button("🔖 SAVE DRAFT", use_container_width=True)
        with col_b: st.markdown("<div style='text-align:center;padding:10px;color:#d4af37'>🛡️ 4K Export Ready | 🤖 AI Powered</div>", unsafe_allow_html=True)
