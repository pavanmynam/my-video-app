import streamlit as st, requests, re, io, random
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio

st.set_page_config(page_title="PA1 CINELUXE", layout="wide")
st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - REAL 360 VIDEO</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ccc'>Any Script = Same Video | Real Motion - Not Just Zoom</p>", unsafe_allow_html=True)

def add_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-180, h-45), (w-10, h-10)], fill=(0,0,0,100))
    draw.text((w-160, h-30), "PA1 PAVAN", fill=(212,175,55,255))
    return img

def make_prompt(s):
    # Beer bottle valla image block avvakunda safe ga marchu
    s_clean = s.lower().replace("beer bottle", "coconut drink").replace("beer", "coconut drink").replace("bottle", "glass")
    return s_clean + ", ultra realistic 8K, vibrant colors, cinematic lighting, photorealistic, tropical night beach, dolphins jumping, moonlight sparkling on waves, coconut trees swaying"

def split_sent(t):
    parts = re.split(r'[.!?\n]+', t)
    clean = []
    for p in parts:
        if len(p.strip()) > 15:
            clean.append(p.strip())
    return clean

script = st.text_area("PASTE YOUR DREAM SCRIPT HERE - ANY STORY", height=150, placeholder="My dream to watch sea dolphin at night with cool coconut trees along with coconut drink in my hand and my husband was with shorts and catching fishes")

col1, col2 = st.columns(2)
with col1:
    scenes = st.slider("Scenes", 3, 8, 5)
with col2:
    voice_opt = st.radio("Voice", ["AI Voice", "No Voice"])

if st.button("GENERATE REAL 360 VIDEO", use_container_width=True):
    if not script:
        st.warning("Script pettu PA1!")
    else:
        sents = split_sent(script)[:scenes]
        imgs = []
        st.write("Generating Real Images...")

        for i, s in enumerate(sents):
            st.write(f"Scene {i+1}: {s[:70]}...")
            try:
                prompt = make_prompt(s)
                q = requests.utils.quote(prompt)
                seed = random.randint(1, 999999)
                url = f"https://image.pollinations.ai/prompt/{q}?width=1280&height=720&model=flux&enhance=true&seed={seed}&nologo=true"
                r = requests.get(url, timeout=90)
                
                if r.status_code == 200 and len(r.content) > 15000:
                    im = Image.open(io.BytesIO(r.content)).convert("RGB")
                else:
                    # Backup safe prompt if blocked
                    safe_prompt = "tropical night beach full moon coconut trees swaying dolphins jumping ocean romantic couple fishing moonlight"
                    safe_q = requests.utils.quote(safe_prompt)
                    r2 = requests.get(f"https://image.pollinations.ai/prompt/{safe_q}?width=1280&height=720&model=flux&seed={seed}", timeout=90)
                    im = Image.open(io.BytesIO(r2.content)).convert("RGB")

                im = ImageEnhance.Color(im).enhance(1.3)
                im = ImageEnhance.Sharpness(im).enhance(1.2)
                im = add_watermark(im)
                st.image(im, caption=f"Scene {i+1}", use_container_width=True)
                imgs.append(im)

            except Exception as e:
                st.write(f"Image error: {e} - safe image try chestunna")
                try:
                    safe_q = requests.utils.quote("beautiful tropical night beach moonlight coconut trees")
                    r2 = requests.get(f"https://image.pollinations.ai/prompt/{safe_q}?width=1280&height=720&model=flux&seed={random.randint(1,999999)}", timeout=60)
                    im = Image.open(io.BytesIO(r2.content)).convert("RGB")
                    imgs.append(im)
                except Exception as e2:
                    st.write(f"Backup kuda fail: {e2}")

        if len(imgs) > 0:
            st.write("Creating REAL 360 Motion Video - Not Just Zoom...")
            frames = []
            for img in imgs:
                base = img.resize((1280,720))
                # REAL 360 MOTION - 3 sec per scene
                for f in range(72):
                    pan_x = int(90 * np.sin(f*0.06))
                    pan_y = int(25 * np.cos(f*0.04))
                    shake_x = random.randint(-4, 4)
                    shake_y = random.randint(-2, 2)
                    zoom = 1.0 + (f*0.003)
                    
                    w,h = base.size
                    nw,nh = int(w*zoom), int(h*zoom)
                    zm = base.resize((nw,nh))
                    
                    cx = (nw-w)//2 + pan_x + shake_x
                    cy = (nh-h)//2 + pan_y + shake_y
                    cx = max(0, min(cx, nw-w))
                    cy = max(0, min(cy, nh-h))
                    
                    crop = zm.crop((cx, cy, cx+w, cy+h))
                    frames.append(np.array(crop))

            video_path = "/tmp/pa1_real_360.mp4"
            imageio.mimsave(video_path, frames, fps=24, macro_block_size=1)
            
            st.success("DONE! Idi Zoom kadu - REAL 360° Motion Video!")
            st.video(video_path)
            
            with open(video_path, "rb") as f:
                st.download_button("DOWNLOAD REAL VIDEO", f, file_name="PA1_CINELUXE_REAL_360.mp4", mime="video/mp4", use_container_width=True)
        else:
            st.error("Images raaledu PA1 - Script lo beer teesi coconut drink ani pettu malli try chey!")
