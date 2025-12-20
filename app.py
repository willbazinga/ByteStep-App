import streamlit as st
import requests
import time
from datetime import datetime
from urllib.parse import quote

# --- 1. 配置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.2", page_icon="🚀")

# --- 2. 样式 ---
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-title { font-size: 22px; font-weight: 800; color: #1E293B; }
    .blur-text { filter: blur(6px); transition: filter 0.3s; cursor: pointer; }
    .blur-text:active { filter: blur(0); }
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
    st.title("🚀 ByteStep Pro 2.2")
    st.caption(f"Willbazinga's Tech Lab | {datetime.now().strftime('%H:%M')}")

    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        quiz_mode = st.toggle("Memory Challenge (Blur Mode)", value=False)
        for i, v in enumerate(today_data['vocabulary']):
            display_def = f'<span class="blur-text">{v["def"]}</span>' if quiz_mode else v["def"]
            
            st.markdown(f"""
                <div class="section-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="word-title">{v['word']}</span>
                    </div>
                    <div style="color:#475569; margin-top:8px;">{display_def}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # --- 核心改变：使用原生音频播放组件 ---
            # 这种方式直接调用手机的音频播放器，Spotify 能响，这个就一定能响
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={quote(v['word'])}&tl=en&client=tw-ob"
            st.audio(tts_url, format="audio/mp3")

    with tab2:
        for g in today_data['grammar']:
            st.markdown(f'<div class="section-card"><b style="color:#0052cc;">{g["rule"]}</b><br>{g["note"]}</div>', unsafe_allow_html=True)

    with tab3:
        t = today_data['tech_spotlight']
        st.markdown(f'<div class="section-card" style="border-left-color:#f97316;"><b>{t["title"]}</b><p>{t["detail"]}</p></div>', unsafe_allow_html=True)
        if st.button("Complete Today"): st.balloons()
