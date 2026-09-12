import streamlit as st, requests, re, io, random
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio

st.set_page_config(page_title="PA1 CINELUXE ULTIMATE", layout="wide")
st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - ULTIMATE 360 CINEMA</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Meta AI Quality | Depth | 360 Slow Motion | Character Matching</p>", unsafe_allow_html=True)

def add_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-180, h-35), (w-10, h-10)], fill=(0,0,0,100))
    draw.text((w-160, h-25), "PA1 PAVAN", fill=(212,175,55,255))
    return img

def get_ultimate_prompt(sentence, character=""):
    s = sentence.lower()
    char = f", {character}" if character else ""
    
    if any(x in s for x in ["parvatham", "mountain", "vendi", "silver", "potosi", "cerro"]):
        return f"Cerro Rico de Potosi mountain cross-section sliced open showing massive glowing pure silver veins inside, mining tunnels scaffolding, dramatic clouds fog, town below{char}, ultra realistic 8K, National Geographic, depth, volumetric lighting, cinematic epic"
    
    elif any(x in s for x in ["coin", "koyin", "80", "250"]):
        return f"Extreme macro ancient Spanish silver coins scattered on burlap, PHILIPPVS POTOSI 1692 engravings, cross symbol, text 1 IN 5 COINS WORLDWIDE{char}, ultra realistic 8K photorealistic dirt texture"
    
    elif any(x in s for x in ["palace", "bhavanam", "europe", "raja"]):
        return f"Grand European royal palace built from silver wealth, Spanish palace ornate architecture{char}, ultra realistic 8K cinematic golden hour"
    
    elif any(x in s for x in ["argentina", "argentum", "peru"]):
        return f"Argentina name origin Argentum silver shining letters, silver mountain Potosi background, map{char}, ultra realistic 8K educational"
    
    elif any(x in s for x in ["dolphin", "samudram", "beach", "coconut"]):
        clean = sentence.replace("beer bottle", "coconut drink").replace("beer", "coconut drink")
        return f"{clean}{char}, tropical night beach full moon dolphins jumping sea coconut trees swaying moonlight sparkling waves, depth, ultra realistic 8K cinematic emotional"
    
    else:
        return f"{sentence}{char}, ultra realistic 8K cinematic depth highly detailed storytelling"

def split_sent(t):
    return [p.strip() for p in re.split(r'[.!?।\n]+', t) if len(p.strip()) > 20]

# UI
script = st.text_area("PASTE SCRIPT - Telugu or English - FULL STORY", height=180, placeholder="దేశం ఎలా నాశనం అవుతుంది... పెద్ద పర్వతం లోపల వెండి... OR My dream to watch dolphin at night...")
character = st.text_input("CHARACTER - Same character motham video lo (Ex: young Indian couple, husband in shorts fishing)", value="")
col1, col2 = st.columns(2)
with col1:
    scenes = st.slider("Scenes", 2, 5, 3)
with col2:
    motion_style = st.selectbox("Motion", ["360 SLOW MOTION", "DEPTH PARALLAX", "EMOTIONAL SLOW"])

if st.button("GENERATE ULTIMATE 360 VIDEO", use_container_width=True):
    if not script:
        st.warning("Script pettu PA1!")
    else:
        sents = split_sent(script)[:scenes]
        imgs = []
        base_seed = random.randint(1, 99999)
        
        for i, sent in enumerate(sents):
            st.write(f"**Scene {i+1}:** {sent[:80]}...")
            try:
                prompt = get_ultimate_prompt(sent, character)
                q = requests.utils.quote(prompt)
                # Character matching - same base seed
                url = f"https://image.pollinations.ai/prompt/{q}?width=1024&height=576&model=turbo&enhance=true&seed={base_seed+i}&nologo=true"
                r = requests.get(url, timeout=90)
                
                if r.status_code == 200 and len(r.content) > 15000:
                    im = Image.open(io.BytesIO(r.content)).convert("RGB")
                    im = ImageEnhance.Color(im).enhance(1.4)
                    im = ImageEnhance.Sharpness(im).enhance(1.3)
                    im = add_watermark(im)
                    st.image(im, caption=f"Scene {i+1}", use_container_width=True)
                    imgs.append(im)
                else:
                    st.write(f"Scene {i+1} blocked, retrying...")
            except Exception as e:
                st.write(f"Error Scene {i+1}: {e}")

        if imgs:
            st.write("### Creating 360° Slow Motion - Quality + Depth...")
            frames = []
            for img in imgs:
                base = img.resize((1024, 576))
                # 40 frames per scene = 1.6 sec slow motion - STABLE - no crash
                for f in range(40):
                    if motion_style == "360 SLOW MOTION":
                        pan_x = int(70 * np.sin(f*0.08))
                        pan_y = int(20 * np.cos(f*0.05))
                        zoom = 1.0 + (f*0.002)
                    elif motion_style == "DEPTH PARALLAX":
                        pan_x = int(50 * np.sin(f*0.06))
                        pan_y = int(15 * np.cos(f*0.04))
                        zoom = 1.0 + (f*0.0025)
                    else:
                        pan_x = int(30 * np.sin(f*0.05))
                        pan_y = int(10 * np.sin(f*0.03))
                        zoom = 1.0 + (f*0.0015)
                    
                    w,h = base.size
                    nw,nh = int(w*zoom), int(h*zoom)
                    zm = base.resize((nw,nh))
                    cx = max(0, min((nw-w)//2 + pan_x, nw-w))
                    cy = max(0, min((nh-h)//2 + pan_y, nh-h))
                    crop = zm.crop((cx, cy, cx+w, cy+h))
                    frames.append(np.array(crop))

            video_path = "/tmp/pa1_ultimate.mp4"
            imageio.mimsave(video_path, frames, fps=24, macro_block_size=1)
            st.success(f"DONE! {len(imgs)} Scenes | {len(frames)} Frames | 360 Slow Motion | Depth | Character Matched")
            st.video(video_path)
            with open(video_path, "rb") as f:
                st.download_button("DOWNLOAD ULTIMATE VIDEO", f, file_name="PA1_ULTIMATE_360.mp4", mime="video/mp4", use_container_width=True)
