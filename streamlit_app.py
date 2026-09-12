import streamlit as st
import requests, re, io, random
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import imageio

st.set_page_config(page_title="PA1 CINELUXE", layout="wide")
st.markdown("<h2 style='color:#d4af37;text-align:center'>PA1 CINELUXE - ULTIMATE 360</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Depth | 360 Slow Motion | Script Matching</p>", unsafe_allow_html=True)

def watermark(img):
    draw = ImageDraw.Draw(img, "RGBA")
    w,h = img.size
    draw.rectangle([(w-180, h-35), (w-10, h-10)], fill=(0,0,0,100))
    draw.text((w-160, h-25), "PA1 PAVAN", fill=(212,175,55,255))
    return img

def get_smart_prompt(sentence):
    s = sentence.lower()
    
    # TELUGU + ENGLISH KEYWORDS - UNDERSTANDING
    if any(x in s for x in ["parvatham", "vendi", "silver", "potosi", "cerro", "dollar", "reserve", "బ్యాంక్", "వెండి"]):
        if "coin" in s or "koyin" in s or "డాలర్" in s or "dollar" in s:
            return "Ancient Spanish silver coins from Potosi Bolivia, POTOSI 1692 engravings, massive pile of silver coins, 250 years history, ultra realistic 8K macro photorealistic"
        else:
            return "Cerro Rico de Potosi silver mountain in Bolivia cross-section cut open showing massive pure silver veins inside, mining tunnels, dramatic storm clouds, small town below, ultra realistic 8K National Geographic cinematic depth"
    
    elif any(x in s for x in ["argentina", "argentum", "దేశం", "నాశనం"]):
        return "Argentina country origin story, map of Argentina, silver mountain Potosi background, Argentum silver text glowing, economic collapse concept, ultra realistic 8K cinematic"

    elif any(x in s for x in ["palace", "bhavanam", "europe", "రాజ"]):
        return "Grand Spanish royal palace Escorial built from Potosi silver wealth, ornate baroque, ultra realistic 8K"

    else:
        clean = sentence.replace("beer", "coconut drink").replace("బీర్", "కొబ్బరి")
        return f"{clean[:120]}, tropical night beach full moon dolphins, ultra realistic 8K cinematic"

def split_sent(t):
    return [p.strip() for p in re.split(r'[.!?।\n]+', t) if len(p.strip()) > 25]

script = st.text_area("PASTE FULL SCRIPT - Telugu ok", height=180, value="డాలర్ల కాపీ ని ఇలా దాచిపెట్టుకున్నారు. ఈ అమెరికా వాళ్ళ సంబ్రల బ్యాంక్ దగ్గర ఉన్న రిజర్వ్స్ కంటే 5 టైమ్స్ ఎక్కువ. ఒక దేశ ప్రజలకి తమ సొంత దేశపు కరెన్సీ మీద, బ్యాంకుల మీద నమ్మకం పోతే పరిస్థితి ఎంత దారుణంగా ఉంటుందో చెప్పడానికి అర్జెంటీనా ఒక బెస్ట్ ఎగ్జాంపుల్. అసలు వెండి తో పుట్టిన ఒక దేశం, ఈరోజు ఇలా ఎందుకు అడుక్కునే స్థాయికి పడిపోయింది?")
character = st.text_input("Character (optional)", value="Bolivian miner")
scenes = st.slider("Scenes", 2, 4, 3)
motion = st.selectbox("Motion", ["360 SLOW MOTION", "DEPTH PARALLAX"])

if st.button("GENERATE ULTIMATE 360 VIDEO", use_container_width=True):
    sents = split_sent(script)[:scenes]
    imgs = []
    base_seed = random.randint(1, 99999)
    
    for i, sent in enumerate(sents):
        st.write(f"**Scene {i+1}:** {sent[:100]}...")
        try:
            prompt = get_smart_prompt(sent)
            if character:
                prompt += f", {character}"
            q = requests.utils.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{q}?width=1024&height=576&model=turbo&enhance=true&seed={base_seed+i}&nologo=true"
            r = requests.get(url, timeout=90)
            im = Image.open(io.BytesIO(r.content)).convert("RGB")
            im = ImageEnhance.Color(im).enhance(1.4)
            im = ImageEnhance.Sharpness(im).enhance(1.3)
            im = watermark(im)
            st.image(im, caption=f"Scene {i+1} - Depth", use_container_width=True)
            imgs.append(im)
        except Exception as e:
            st.write(f"Error: {e}")

    if len(imgs) >= 1:
        st.write("### Creating 360° Slow Motion Video...")
        frames = []
        for img in imgs:
            base = img.resize((1024, 576))
            for f in range(40):  # 40 frames per scene - stable
                px = int(70 * np.sin(f*0.08)) if motion == "360 SLOW MOTION" else int(40 * np.sin(f*0.06))
                py = int(20 * np.cos(f*0.05))
                zoom = 1.0 + f*0.002
                w,h = base.size
                nw,nh = int(w*zoom), int(h*zoom)
                zm = base.resize((nw,nh))
                cx = max(0, min((nw-w)//2 + px, nw-w))
                cy = max(0, min((nh-h)//2 + py, nh-h))
                crop = zm.crop((cx, cy, cx+w, cy+h))
                frames.append(np.array(crop))
        
        path = "/tmp/pa1_final.mp4"
        imageio.mimsave(path, frames, fps=24, macro_block_size=1)
        st.success(f"ULTIMATE DONE! {len(frames)} frames | 360 Slow Motion | Depth Clear")
        st.video(path)
        with open(path, "rb") as f:
            st.download_button("DOWNLOAD 360 VIDEO", f, file_name="PA1_ULTIMATE_360.mp4", mime="video/mp4", use_container_width=True)
