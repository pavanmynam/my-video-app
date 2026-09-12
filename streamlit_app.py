import streamlit as st, requests, re, io, time, os, random
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio
from gtts import gTTS

st.set_page_config(page_title="PA1 CINELUXE", layout="wide", page_icon="👑")

st.markdown("""
<style>
.stApp{background:#0a0a0a;color:#f5e6c8}
div.stButton>button{background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;font-weight:900;border-radius:12px;border:none;height:60px;width:100%}
textarea{background:#1e1e1e!important;color:#fff!important;border:1px solid #d4af37!important;border-radius:12px!important}
</style>
""", unsafe_allow_html=True)

def add_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-210, h-65), (w-10, h-10)], fill=(0,0,0,120))
    draw.text((w-190, h-55), "PA1", fill=(212,175,55,255))
    draw.text((w-190, h-30), "PAVAN MYNAM", fill=(255,255,255,200))
    return img

def telugu_to_prompt(s):
    return s + ", ultra realistic 8K, vibrant colors, sharp focus, cinematic lighting, photorealistic, detailed, natural movement, 360 degree view"

def split_sentences(t):
    parts = re.split(r'[.!?।\n]+', t)
    clean = []
    for p in parts:
        if len(p.strip()) > 15:
            clean.append(p.strip())
    return clean

st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - REAL MOTION STUDIO</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#fff'>Any Script = Same Video | No More Fake Zoom</p>", unsafe_allow_html=True)

script = st.text_area("PASTE YOUR SCRIPT HERE - ANY STORY", height=150, placeholder="Ex: My dream to watch sea dolphin at night with coconut trees... OR Argentina silver story... OR Village love story...")

col1, col2 = st.columns(2)
with col1:
    voice_mode = st.radio("Voice:", ["AI Telugu Voice", "Upload My Voice", "No Voice"])
with col2:
    max_scenes = st.slider("Scenes", 3, 10, 5)

uploaded_voice = None
if voice_mode == "Upload My Voice":
    uploaded_voice = st.file_uploader("Upload MP3/WAV", type=["mp3","wav","m4a","ogg"])
    if uploaded_voice:
        st.audio(uploaded_voice)

if st.button("GENERATE REAL MOTION VIDEO", use_container_width=True):
    if not script:
        st.warning("Script pettu PA1!")
    else:
        start = time.time()
        sents = split_sentences(script)[:max_scenes]
        prog = st.progress(0)
        status = st.empty()
        imgs = []
        audio_files = []
        
        for i,s in enumerate(sents):
            prog.progress((i+1)/len(sents))
            status.markdown(f"Generating Scene {i+1}/{len(sents)}: {s[:60]}...")
            try:
                prompt = telugu_to_prompt(s)
                q = requests.utils.quote(prompt)
                seed = random.randint(1, 999999)
                url = "https://image.pollinations.ai/prompt/" + q + "?width=1280&height=720&model=flux&enhance=true&nologo=true&seed=" + str(seed)
                r = requests.get(url, timeout=90)
