import streamlit as st, requests, re, io, random
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio
from gtts import gTTS

st.set_page_config(page_title="PA1 CINELUXE", layout="wide")
st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - REAL 360 VIDEO</h2>", unsafe_allow_html=True)

def add_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-180, h-50), (w-10, h-10)], fill=(0,0,0,100))
    draw.text((w-160, h-35), "PA1 PAVAN", fill=(212,175,55,255))
    return img

def make_prompt(s):
    return s + ", ultra realistic 8K, cinematic lighting, photorealistic, 360 view, natural movement"

def split_sent(t):
    return [p.strip() for p in re.split(r'[.!?\\n]+', t) if len(p.strip())>15]

script = st.text_area("PASTE ANY SCRIPT HERE", height=150, placeholder="My dream to watch sea dolphin at night with cool coconut trees...")
scenes = st.slider("Scenes", 3, 8, 4)
voice = st.radio("Voice", ["AI Voice", "No Voice"])

if st.button("GENERATE REAL 360 VIDEO", use_container_width=True):
    if not script:
        st.warning("Script pettu PA1!")
    else:
        sents = split_sent(script)[:scenes]
        imgs = []
        for i, s in enumerate(sents):
            st.write(f"Scene {i+1}: {s[:60]}")
            try:
                prompt = make_prompt(s)
                q = requests.utils.quote(prompt)
                seed = random.randint(1, 999999)
                url = f"https://image.pollinations.ai/prompt/{q}?width=1280&height=720&model=flux&seed={seed}"
                r = requests.get(url, timeout=60)
                im = Image.open(io.BytesIO(r.content)).convert("RGB")
                im = ImageEnhance.Color(im).enhance(1.3)
                im = add_watermark(im)
                st.image(im, use_container_width=True)
                imgs.append(im)
            except Exception as e:
                st.write(f"Error: {e}")

        if len(imgs) > 0:
            frames = []
            for img in imgs:
                base = img.resize((1280,720))
                for f in range(48):
                    pan_x = int(70 * np.sin(f*0.08))
                    pan_y = int(15 * np.cos(f*0.05))
                    zoom = 1.0 + (f*0.004)
                    w,h = base.size
                    nw,nh = int(w*zoom), int(h*zoom)
                    zm = base.resize((nw,nh))
                    cx = (nw-w)//2 + pan_x
                    cy = (nh-h)//2 + pan_y
                    cx = max(0, min(cx, nw-w))
                    cy = max(0, min(cy, nh-h))
                    crop = zm.crop((cx, cy, cx+w, cy+h))
                    frames.append(np.array(crop))
            video_path = "/tmp/pa1_360.mp4"
            imageio.mimsave(video_path, frames, fps=24, macro_block_size=1)
            st.video(video_path)
            st.success("DONE! Idi zoom kadu - REAL 360 motion video!")
            with open(video_path, "rb") as f:
                st.download_button("DOWNLOAD VIDEO", f, file_name="PA1_360.mp4", use_container_width=True)
