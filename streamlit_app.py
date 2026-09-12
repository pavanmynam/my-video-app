import streamlit as st, requests, re, io, time, os
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio
from gtts import gTTS
from pydub import AudioSegment

st.set_page_config(page_title="PA1 - Pavan Mynam | CINELUXE", layout="wide", page_icon="👑")

st.markdown("""
<style>
.stApp{background:#0a0a0a;color:#f5e6c8}
section[data-testid="stSidebar"]{background:#111;border-right:2px solid #d4af37;min-width:300px}
div.stButton>button{background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;font-weight:900;border-radius:12px;border:none;height:55px;width:100%;margin-bottom:8px}
textarea{background:#1e1e1e!important;color:#fff!important;border:1px solid #d4af37!important;border-radius:12px!important}
</style>
""", unsafe_allow_html=True)

if 'menu' not in st.session_state: st.session_state.menu="Text to Video"

def add_pa1_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-210, h-65), (w-10, h-10)], fill=(0,0,0,120))
    draw.text((w-190, h-55), "PA1", fill=(212,175,55,255))
    draw.text((w-190, h-30), "PAVAN MYNAM", fill=(255,255,255,200))
    return img

def telugu_to_prompt(s):
    mapping={"గ్రామం":"old Indian village mud houses","ఇల్లు":"traditional mud house","అమ్మాయి":"beautiful young Indian girl in saree","అబ్బాయి":"young Indian man","ఏడుపు":"crying emotional closeup","ప్రేమ":"romantic soft light","రాత్రి":"night moonlight cinematic","అడవి":"dense forest misty"}
    eng=s
    for k,v in mapping.items():
        if k in s: eng=v; break
    return f"{eng}, ultra realistic 8K, highly detailed, vibrant colors, sharp focus, cinematic lighting, photorealistic"

def split_sentences(t): return [p.strip() for p in re.split(r'[.!?।\n]+', t) if len(p.strip())>15]

with st.sidebar:
    st.markdown("<h1 style='color:#d4af37;text-align:center'>👑 CINELUXE</h1><p style='text-align:center;color:#d4af37;font-weight:900'>by PAVAN MYNAM<br>PA1</p>", unsafe_allow_html=True)
    if st.button("🏠 Home"): st.session_state.menu="Home"
    if st.button("📝 PA1 Text to Video"): st.session_state.menu="Text to Video"
    st.markdown("<div style='background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;padding:12px;border-radius:10px;text-align:center;font-weight:900;margin-top:20px'>PA1 PRO PLAN<br>Active</div>", unsafe_allow_html=True)

st.markdown("<h2 style='color:#d4af37;text-align:center'>👑 PA1 TEXT TO VIDEO STUDIO</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#fff'>by PAVAN MYNAM | Cinematic AI Video Generator</h4>", unsafe_allow_html=True)

script=st.text_area("INPUT — TELUGU SCRIPT", height=130, placeholder="పాత గ్రామం, మట్టి ఇల్లు...")

st.markdown("### 🎤 VOICE OVER - WITH UPLOAD")
voice_mode = st.radio("Voice:", ["🤖 AI Telugu Voice", "📁 Upload My Voice File", "🔇 No Voice"], horizontal=True)
uploaded_voice=None
if voice_mode=="📁 Upload My Voice File":
