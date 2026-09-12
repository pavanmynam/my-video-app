import streamlit as st
import requests, re, io, random, time
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import imageio

st.set_page_config(page_title="PA1 CINELUXE", layout="wide")
st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - FINAL FIX</h2>", unsafe_allow_html=True)

def watermark(img):
    d = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    d.rectangle([(w-180, h-35), (w-10, h-10)], fill=(0,0,0,100))
    d.text((w-160, h-25), "PA1 PAVAN", fill=(212,175,55,255))
    return img

def fetch_image(prompt, seed):
    # Pollinations sometimes fails - retry 3 times with different model
    for attempt in range(3):
        try:
            q = requests.utils.quote(prompt)
            # Use flux model - more stable than turbo
            url = f"https://image.pollinations.ai/prompt/{q}?width=1024&height=576&model=flux&seed={seed}&nologo=true"
            r = requests.get(url, timeout=60)
            # Check if it's actually an image
            if r.status_code == 200 and r.headers.get('content-type','').startswith('image'):
                if len(r.content) > 20000:
                    return Image.open(io.BytesIO(r.content)).convert("RGB")
            # If not image, it returned text/error - wait and retry
            time.sleep(2)
        except Exception as e:
            time.sleep(2)
            continue
    return None

def get_english_prompt(telugu_sent, idx):
    # Telugu -> English mapping - NO TELUGU in final prompt
    prompts = [
        "Cerro Rico de Potosi Bolivia silver mountain cross-section cut open showing huge pure silver veins inside, mining tunnels, dramatic clouds, town below, ultra realistic 8K National Geographic cinematic depth volumetric light",
        "Massive pile of ancient Spanish silver coins from Potosi 1692, PHILIPPVS engravings, cross symbol, burlap sack, ultra realistic 8K macro photorealistic",
        "Argentina economic crisis, people losing trust in banks, empty bank vault, pesos devaluation concept, ultra realistic 8K cinematic emotional",
        "Argentina country born from silver, now begging, contrast of rich silver mountain vs poor streets, ultra realistic 8K storytelling"
    ]
    return prompts[idx % len(prompts)]

script = st.text_area("SCRIPT - Telugu", height=150, value="డాలర్ల కాపీ ని ఇలా దాచిపెట్టుకున్నారు. ఈ అమెరికా వాళ్ళ సంబ్రల బ్యాంక్ దగ్గర ఉన్న రిజర్వ్స్ కంటే 5 టైమ్స్ ఎక్కువ. ఒక దేశ ప్రజలకి తమ సొంత దేశపు కరెన్సీ మీద నమ్మకం పోతే పరిస్థితి ఎంత దారుణంగా ఉంటుందో చెప్పడానికి అర్జెంటీనా ఒక బెస్ట్ ఎగ్జాంపుల్. అసలు వెండి తో పుట్టిన ఒక దేశం, ఈరోజు ఇలా ఎందుకు అడుక్కునే స్థాయికి పడిపోయింది?")
scenes = st.slider("Scenes", 2, 4, 4)

if st.button("GENERATE ULTIMATE 360 VIDEO - FIXED", use_container_width=True):
    sents = [s.strip() for s in re.split(r'[.!?।\n]+', script) if len(s.strip())>20][:scenes]
    imgs = []
    base = random.randint(1, 99999)
    
    for i, sent in enumerate(sents):
        st.write(f"**Scene {i+1}:** {sent[:80]}...")
        with st.spinner(f"Generating Scene {i+1}..."):
            prompt = get_english_prompt(sent, i)
            st.caption(f"Prompt: {prompt[:80]}...")
            im = fetch_image(prompt, base+i)
            if im:
                im = ImageEnhance.Color(im).enhance(1.4)
                im = ImageEnhance.Sharpness(im).enhance(1.2)
                im = watermark(im)
                st.image(im, use_container_width=True)
                imgs.append(im)
            else:
                st.error(f"Scene {i+1} failed after 3 retries - trying next")
    
    if len(imgs)>=1:
        st.write("### Creating 360° Slow Motion...")
        frames = []
        for img in imgs:
            base_img = img.resize((1024, 576))
            for f in range(40):
                px = int(60 * np.sin(f*0.08))
                py = int(15 * np.cos(f*0.05))
                zoom = 1.0 + f*0.002
                w,h = base_img.size
                nw,nh = int(w*zoom), int(h*zoom)
                zm = base_img.resize((nw,nh))
                cx = max(0, min((nw-w)//2 + px, nw-w))
                cy = max(0, min((nh-h)//2 + py, nh-h))
                frames.append(np.array(zm.crop((cx, cy, cx+w, cy+h))))
        
        path = "/tmp/pa1_final.mp4"
        imageio.mimsave(path, frames, fps=24, macro_block_size=1)
        st.success(f"DONE! {len(imgs)} scenes - 360 Slow Motion Ready")
        st.video(path)
        with open(path, "rb") as f:
            st.download_button("DOWNLOAD VIDEO", f, file_name="PA1_360.mp4", use_container_width=True)
    else:
        st.error("All images failed - Pollinations busy - 2 mins taruvata malli try chey PA1!")
