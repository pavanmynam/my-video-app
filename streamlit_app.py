import streamlit as st
import requests, io, random
from PIL import Image

st.set_page_config(page_title="PA1 CINELUXE")
st.title("PA1 CINELUXE - WORKING")
st.write("App is LIVE! Now paste script below")

script = st.text_area("SCRIPT", height=150, placeholder="దేశం ఎలా నాశనం అవుతుంది... పెద్ద పర్వతం లోపల వెండి...")

if st.button("GENERATE"):
    if not script:
        st.warning("Script pettu")
    else:
        # Simple prompt - Argentina story ki
        if "parvatham" in script or "silver" in script:
            prompt = "Cerro Rico Potosi silver mountain cross-section showing silver veins inside, cinematic 8k"
        else:
            prompt = script[:100] + ", cinematic 8k"

        q = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{q}?width=1024&height=576&model=turbo&seed={random.randint(1,99999)}"
        r = requests.get(url, timeout=60)
        im = Image.open(io.BytesIO(r.content))
        st.image(im, use_container_width=True)
        st.success("Image generated! App working!")
