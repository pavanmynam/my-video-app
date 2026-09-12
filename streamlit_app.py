import streamlit as st, requests, io, re
from PIL import Image
import numpy as np, imageio

st.set_page_config(page_title="CINELUXE UNIVERSAL", layout="wide")
st.markdown("<style>.stApp{background:#050505;color:white} h1{color:#d4af37!important; text-align:center}.stButton>button{height:60px}</style>", unsafe_allow_html=True)

# UNIVERSAL Telugu -> English Visual Dictionary
VISUAL_DICT = {
    "పర్వతం": "giant mountain", "వెండి": "pure shining silver", "బంగారం": "gold treasure",
    "గుర్రం": "horse", "అడవి": "dense forest", "దేశం": "ancient kingdom", "నాశనం": "ruined destroyed city",
    "నది": "river", "సముద్రం": "ocean", "యుద్ధం": "epic war battle", "రాజు": "ancient king",
    "ప్రజలు": "crowd of people", "కాయిన్": "silver coins", "డబ్బు": "treasure money", "చీకటి": "dark night",
    "వెలుగు": "bright light", "తుఫాను": "storm", "మంచు": "snow mountain", "ఎడారి": "desert"
}

def telugu_to_visual_prompt(telugu_sentence):
    prompt = telugu_sentence.lower()
    for te, en in VISUAL_DICT.items():
        if te in prompt:
            prompt = prompt.replace(te, en)
    # Clean and make cinematic
    prompt = re.sub(r'[^a-zA-Z0-9,]', ' ', prompt)
    prompt = prompt[:120] # cut
    return f"cinematic epic shot of {prompt}, 4k, dramatic lighting, movie scene, highly detailed"

st.markdown("<h1>✨ CINELUXE - UNIVERSAL TEXT TO VIDEO ✨</h1>")
st.caption("Em script past chesina - adhe visuals vastayi. Text kanipinchadu!")

script = st.text_area("👇 EM SCRIPT AINA PASTE CHEY (Telugu/English):",
"ఒక దేశం ఎలా నాశనం అవుతుంది అనడానికి ఇదొక పర్ఫెక్ట్ కేస్ స్టడీ. ఒక పెద్ద పర్వతం, ఆ పర్వతం లోపల అంతా స్వచ్ఛమైన వెండి తో నిండిపోయి ఉంది. ప్రపంచంలో ఉన్న వెండిలో 80 శాతం ఈ దేశం దగ్గరే ఉండేది. ఒక నల్లని గుర్రం అడవి లో పరిగెడుతుంది.", height=160)

col1, col2 = st.columns([3,1])
with col2:
    num_scenes = st.slider("Scenes", 2, 6, 4)
    fps = st.selectbox("Motion", ["Cinematic Slow Zoom", "Fast Pan"])

preview = st.empty()

if st.button("✨ GENERATE UNIVERSAL VIDEO ✨", type="primary", use_container_width=True):
    # Auto split script into scenes
    sentences = [s.strip() for s in re.split(r'[.!?।]+|\n', script) if len(s.strip())>10]
    if len(sentences) < num_scenes:
        # if less sentences, duplicate logic
        sentences = (sentences * 2)[:num_scenes]
    else:
        sentences = sentences[:num_scenes]

    writer = imageio.get_writer("universal.mp4", fps=24, macro_block_size=1)

    for i, sentence in enumerate(sentences):
        eng_prompt = telugu_to_visual_prompt(sentence)
        st.write(f"🎬 Scene {i+1}: `{sentence[:40]}...` -> `{eng_prompt[:60]}...`")

        # FREE AI IMAGE GENERATION (Flux model)
        url = f"https://image.pollinations.ai/prompt/{eng_prompt}?width=1280&height=720&nologo=true&model=flux&seed={i*17}"
        try:
            r = requests.get(url, timeout=40)
            img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720))
        except:
            img = Image.new('RGB', (1280,720), (15,15,15))

        arr = np.array(img)
        # VIDEO MOTION
        for f in range(72): # 3 sec per scene
            zoom = 1 + (f/72)*0.18
            h,w = arr.shape[0], arr.shape[1]
            nh, nw = int(h/zoom), int(w/zoom)
            y1 = (h-nh)//2; x1 = (w-nw)//2
            cropped = arr[y1:y1+nh, x1:x1+nw]
            frame = np.array(Image.fromarray(cropped).resize((1280,720)))
            writer.append_data(frame)

    writer.close()
    preview.video("universal.mp4")
    st.balloons()
    st.success(f"✅ {len(sentences)} SCENES REAL VIDEO READY! Em script ichina ide logic tho vastundi!")
    with open("universal.mp4","rb") as f:
        st.download_button("📥 DOWNLOAD UNIVERSAL MP4", f, "CineLuxe_Universal.mp4")

st.info("💡 Tip: Script lo 'parvatham, gurram, adavi, yuddham' lanti words unte - aa visuals ae vastayi. Text video lo undadu!")
