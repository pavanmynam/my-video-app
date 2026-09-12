import streamlit as st
st.set_page_config(page_title="CineLuxe", layout="wide")

st.markdown("""
<style>
.stApp {background:#050505;}
[data-testid="stSidebar"]{background:#111111; border-right:1px solid #d4af37;}
h1,h2,h3{color:#e6c67a !important;}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#d4af37,#f9e7a1); color:black; font-weight:900; border-radius:12px; height:55px;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 👑 CINELUXE")
    st.button("◆ Home", type="primary", use_container_width=True)
    st.button("◈ Projects", use_container_width=True)
    st.button("☰ Templates", use_container_width=True)
    st.button("🎙️ AI Voice", use_container_width=True)
    st.button("🎵 BGM Library", use_container_width=True)
    st.button("📤 Exports", use_container_width=True)
    st.info("PRO PLAN Active")

st.markdown("### PREVIEW — CINEMATIC • 4K HDR")
st.video("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")
st.slider("",0,90,12,format="00:%d — 01:30",label_visibility="collapsed")

st.markdown("#### ✍️ INPUT — TELUGU SCRIPT")
script=st.text_area("", "ఒక దేశం ఎలా నాశనం అవుతుంది... ఒక పెద్ద పర్వతం వెండి తో నిండిపోయి ఉంది...",height=120,label_visibility="collapsed")

c1,c2=st.columns(2)
with c1:
    st.selectbox("Voice",["తెలుగు - స్త్రీ (ప్రశాంతం)","Telugu Male Epic"])
with c2:
    st.selectbox("BGM",["Cinematic Epic","Suspense"])

b1,b2=st.columns(2)
with b1:
    st.button("🔖 SAVE DRAFT",use_container_width=True)
with b2:
    if st.button("GENERATE VIDEO ✨",type="primary",use_container_width=True):
        st.balloons()
        st.success("Video Ready! 4K Export ✅")
