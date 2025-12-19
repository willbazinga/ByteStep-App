import streamlit as st

# 设置页面适配
st.set_page_config(page_title="ByteStep", layout="centered")

# 简单的移动端 UI 样式
st.markdown("""
    <style>
    .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-left: 10px solid #0052cc; }
    .stButton>button { border-radius: 25px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 ByteStep AI")
st.caption("Daily Tech English powered by BytePlus Content")

# 模拟每日内容内容库
lesson = {
    "term": "Low Latency",
    "def": "A minimal delay in processing network data.",
    "quote": "BytePlus RTC ensures low latency for real-time interaction."
}

st.markdown(f"""
<div class="card">
    <h2 style='color:#0052cc;'>{lesson['term']}</h2>
    <p><b>Definition:</b> {lesson['def']}</p>
    <hr>
    <p style='color:#555;'><i>"{lesson['quote']}"</i></p>
</div>
""", unsafe_allow_html=True)

if st.button("🔈 Listen to Pronunciation"):
    st.info("Synthesizing audio via BytePlus TTS...")

st.text_input("Try writing your own sentence using this term:")
