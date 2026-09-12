import streamlit as st, requests, re, io, time, os
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np, imageio
from gtts import gTTS

st.set_page_config(page_title="PA1 - Pavan Mynam | CINELUXE", layout="wide", page_icon="👑")

st.markdown("""
<style>
.stApp{background:#0a0a0a;color:#f5e6c8}
section[data-testid="stSidebar"]{background:#111;border-right:2px solid #d4af37}
div.stButton>button{background:linear-gradient(90deg,#d4af37,#f9e27a);color:#000;font-weight:900;border-radius:12px;border:none;height:55px;width:100%;margin-bottom:8px}
textarea{background:#1e1e1e!important;color:#fff!important;border:1px solid #d4af37!important;border-radius:12px!important}
</style>
""", unsafe_allow_html=True)

if 'menu' not in st.session_state:
    st.session_state.menu="Text to Video"

def add_pa1_watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-210, h-65), (w-10, h-10)], fill=(0,0,0,120))
    draw.text((w-190, h-55), "PA1", fill=(212,175,55,255))
    draw.text((w-190, h-30), "PAVAN MYNAM", fill=(255,255,255,200))
    return img

def telugu_to_prompt(s):
    mapping={"గ్రామం":"old Indian village mud houses","ఇల్లు":"traditional mud house","అమ్మాయి":"beautiful young Indian girl in saree","అబ్బాయి":"young Indian man","ఏడుపు":"crying emotional closeup","ప్రేమ":"romantic soft light","రాత్రి":"night moonlight cinematic"}
    eng=s
    for k,v in mapping.items():
        if k in s:
            eng=v
            break
    return eng + ", ultra realistic 8K, vibrant colors, sharp focus, cinematic lighting"

def split_sentences(t):
    return [p.strip() for p in re.split(r'[.!?।\n]+', t) if len(p.strip())>15]

with st.sidebar:
    st.markdown("<h1 style='color:#d4af37;text-align:center'>CINELUXE</h1><p style='text-align:center;color:#d4af37;font-weight:900'>by PAVAN MYNAM<br>PA1</p>", unsafe_allow_html=True)
    if st.button("Home"):
        st.session_state.menu="Home"
    if st.button("PA1 Text to Video"):
        st.session_state.menu="Text to Video"

st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 TEXT TO VIDEO STUDIO</h2>", unsafe_allow_html=True)

script=st.text_area("INPUT - TELUGU SCRIPT", height=130, placeholder="పాత గ్రామం, మట్టి ఇల్లు...")

st.markdown("### VOICE OVER")
voice_mode = st.radio("Voice:", ["AI Telugu Voice", "Upload My Voice File", "No Voice"], horizontal=True)
uploaded_voice=None
if voice_mode == "Upload My Voice File":
    uploaded_voice=st.file_uploader("Upload MP3/WAV", type=["mp3","wav","m4a","ogg"])
    if uploaded_voice:
        st.audio(uploaded_voice)

max_scenes=st.slider("Max Scenes", 3, 10, 5)

if st.button("GENERATE PA1 VIDEO", use_container_width=True):
    if not script:
        st.warning("Script pettu PA1!")
    else:
        start=time.time()
        sents=split_sentences(script)[:max_scenes]
        prog=st.progress(0)
        status=st.empty()
        timer=st.empty()
        imgs=[]
        audio_files=[]
        for i,s in enumerate(sents):
            elapsed=time.time()-start
            eta=(elapsed/(i+1))*(len(sents)-(i+1)) if i>0 else 0
            prog.progress((i+1)/len(sents))
            status.markdown(f"Scene {i+1}/{len(sents)}")
            timer.markdown(f"Elapsed {int(elapsed)}s | Remain {int(eta)}s")
            try:
                prompt=telugu_to_prompt(s)
                q=requests.utils.quote(prompt)
                url="https://image.pollinations.ai/prompt/"+q+"?width=1280&height=720&model=flux&enhance=true&nologo=true&seed="+str(i*101)
                r=requests.get(url, timeout=90)
                im=Image.open(io.BytesIO(r.content)).convert("RGB")
                im=ImageEnhance.Sharpness(im).enhance(2.2)
                im=ImageEnhance.Color(im).enhance(1.4)
                im=add_pa1_watermark(im)
                st.image(im, caption=f"Scene {i+1}", use_container_width=True)
                imgs.append(im)
            except Exception as e:
                st.write(f"Img err {e}")
            if voice_mode == "AI Telugu Voice":
                try:
                    tts=gTTS(text=s, lang='te')
                    vp=f"/tmp/voice_{i}.mp3"
                    tts.save(vp)
                    audio_files.append(vp)
                except:
                    pass
        final_audio_path=None
        if voice_mode == "Upload My Voice File" and uploaded_voice:
            with open("/tmp/my_voice.mp3","wb") as f:
                f.write(uploaded_voice.getbuffer())
            final_audio_path="/tmp/my_voice.mp3"
        elif audio_files:
            try:
                from moviepy.editor import AudioFileClip, concatenate_audioclips
                clips=[AudioFileClip(af) for af in audio_files]
                final_audio=concatenate_audioclips(clips)
                final_audio_path="/tmp/final_audio.mp3"
                final_audio.write_audiofile(final_audio_path)
                st.audio(final_audio_path)
            except:
                final_audio_path=audio_files[0] if audio_files else None
        if imgs:
            frames=[]
            for img in imgs:
                base=img.resize((1280,720))
                for z in range(24):
                    zoom=1+z*0.008
                    w,h=base.size
                    nw,nh=int(w*zoom),int(h*zoom)
                    zm=base.resize((nw,nh)).crop(((nw-w)//2,(nh-h)//2,(nw-w)//2+w,(nh-h)//2+h))
                    zm=add_pa1_watermark(zm)
                    frames.append(np.array(zm))
            video_path="/tmp/final_no_audio.mp4"
            imageio.mimsave(video_path, frames, fps=12, macro_block_size=1)
            try:
                from moviepy.editor import VideoFileClip, AudioFileClip
                vclip=VideoFileClip(video_path)
                if final_audio_path and os.path.exists(final_audio_path):
                    aclip=AudioFileClip(final_audio_path)
                    if aclip.duration > vclip.duration:
                        vclip=vclip.loop(duration=aclip.duration)
                    final=vclip.set_audio(aclip)
                    out_path="/tmp/PA1_Final.mp4"
                    final.write_videofile(out_path, codec='libx264', audio_codec='aac')
                    st.video(out_path)
                    st.download_button("DOWNLOAD PA1 VIDEO", open(out_path,"rb"), file_name="PA1_PavanMynam_Official.mp4", use_container_width=True)
                else:
                    st.video(video_path)
                    st.download_button("DOWNLOAD VIDEO", open(video_path,"rb"), file_name="PA1_PavanMynam.mp4")
            except Exception as e:
                st.video(video_path)
                if final_audio_path:
                    st.audio(final_audio_path)
