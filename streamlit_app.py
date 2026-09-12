import streamlit as st, requests, re, io, os, random, time
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio
from gtts import gTTS

st.set_page_config(page_title="PA1 CINELUXE", layout="wide")

st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - REAL MOTION</h2>", unsafe_allow_html=True)

def add_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-210, h-65), (w-10, h-10)], fill=(0,0,0,120))
    draw.text((w-190, h-55), "PA1", fill=(212,175,55,255))
    return img

def telugu_to_prompt(s):
    return s + ", ultra realistic 8K, vibrant colors, cinematic lighting, photorealistic, detailed"

def split_sentences(t):
    return [p.strip() for p in re.split(r'[.!?]+', t) if len(p.strip())>15]

script = st.text_area("PASTE ANY SCRIPT", height=150)
max_scenes = st.slider("Scenes", 3, 10, 5)
voice_mode = st.radio("Voice", ["AI Telugu Voice", "Upload My Voice", "No Voice"])

uploaded_voice = None
if voice_mode == "Upload My Voice":
    uploaded_voice = st.file_uploader("Upload MP3/WAV", type=["mp3","wav","m4a"])

if st.button("GENERATE VIDEO", use_container_width=True):
    if not script:
        st.warning("Script pettu!")
    else:
        sents = split_sentences(script)[:max_scenes]
        imgs = []
        audio_files = []

        for i, s in enumerate(sents):
            st.write(f"Scene {i+1}: {s[:50]}")
            try:
                prompt = telugu_to_prompt(s)
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
                st.write(f"Image error: {e}")

            if voice_mode == "AI Telugu Voice":
                try:
                    tts = gTTS(text=s, lang='te')
                    vp = f"/tmp/voice_{i}.mp3"
                    tts.save(vp)
                    audio_files.append(vp)
                except Exception as e:
                    st.write(f"Voice error: {e}")

        if voice_mode == "Upload My Voice" and uploaded_voice is not None:
            with open("/tmp/my_voice.mp3", "wb") as f:
                f.write(uploaded_voice.getbuffer())
            final_audio_path = "/tmp/my_voice.mp3"
        elif len(audio_files) > 0:
            final_audio_path = audio_files[0]
        else:
            final_audio_path = None

        if len(imgs) > 0:
            frames = []
            for img in imgs:
                base = img.resize((1280,720))
                for f in range(48):
                    pan_x = int(60 * np.sin(f*0.08))
                    zoom = 1.0 + (f*0.004)
                    w,h = base.size
                    nw,nh = int(w*zoom), int(h*zoom)
                    zm = base.resize((nw,nh))
                    cx = (nw-w)//2 + pan_x
                    cy = (nh-h)//2
                    cx = max(0, min(cx, nw-w))
                    crop = zm.crop((cx, cy, cx+w, cy+h))
                    frames.append(np.array(crop))

            video_path = "/tmp/final.mp4"
            imageio.mimsave(video_path, frames, fps=24, macro_block_size=1)
            st.video(video_path)
            st.success("Video Ready! Eme script aina ide vastundi - beach de kadu!")
            st.download_button("DOWNLOAD", open(video_path,"rb"), file_name="PA1.mp4")
