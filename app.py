import streamlit as st
import requests
import time
from datetime import datetime

# 配置与路径
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.0", page_icon="🚀")

# 引入 JavaScript 实现语音朗读功能
st.markdown("""
    <script>
    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        window.speechSynthesis.speak(utterance);
    }
    </script>
""", unsafe_allow_html=True)

# 样式美化
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-header { display: flex; justify-content: space-between; align-items: center; }
    .word-title { font-size: 20px; font-weight: 800; color: #1E293B; }
    .audio-btn { cursor: pointer; font-size: 20px; background: none; border: none; }
    .tech-title { color: #0052cc; font-size: 24px; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    try:
        r = requests.get(RAW_URL, timeout=5)
        if r.status_code == 200: return r.json()
    except: pass
    return None

data_list = load_data()

if data_list:
    today_data = data_list[-1]
    st.title("🚀 ByteStep Pro 2.0")
    st.caption(f"Willbazinga's Tech Lab | {datetime.now().strftime('%Y-%m-%d')}")

    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        st.subheader("5 Daily Terms")
        for i, v in enumerate(today_data['vocabulary']):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"""<div class="section-card">
                    <div class="word-header">
                        <span class="word-title">{v['word']}</span>
                    </div>
                    <div style="color:#475569; margin-top:5px;">{v['def']}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                # 语音朗读按钮
                if st.button(f"🔊", key=f"btn_{i}"):
                    st.components.v1.html(f"<script>window.parent.speak('{v['word']}. Definition: {v['def']}')</script>", height=0)

    with tab2:
        st.subheader("2 Grammar Points")
        for g in today_data['grammar']:
            st.markdown(f"""<div class="section-card">
                <div style="font-weight:bold; color:#0052cc;">{g['rule']}</div>
                <div style="margin-top:5px;">{g['note']}</div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.subheader("Tech Spotlight")
        t = today_data['tech_spotlight']
        st.markdown(f"""<div class="section-card" style="border-left-color:#f97316;">
            <div class="tech-title">{t['title']}</div>
            <p style="margin-top:10px; line-height:1.6;">{t['detail']}</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Mark as Read"):
            st.balloons()
else:
    st.error("Data Syncing...")
