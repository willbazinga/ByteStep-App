import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. 配置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.1", page_icon="🚀")

# --- 2. 核心语音逻辑（极简直连版） ---
st.markdown("""
    <script>
    // 只有一个函数，负责激活并播放
    window.quickSpeak = function(text) {
        // 1. 立即停止任何正在进行的朗读
        window.speechSynthesis.cancel();
        
        // 2. 创建朗读对象
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        
        // 3. 核心技巧：iOS 有时需要一个微小的延迟来处理音频队列
        setTimeout(() => {
            window.speechSynthesis.speak(utterance);
        }, 10);
    };
    </script>
""", unsafe_allow_html=True)

# 样式
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-title { font-size: 22px; font-weight: 800; color: #1E293B; }
    .blur-text { filter: blur(6px); transition: filter 0.3s; cursor: pointer; }
    .blur-text:active { filter: blur(0); }
    .audio-btn {
        background: #0052cc; color: white; border: none; border-radius: 10px; 
        padding: 5px 12px; font-size: 18px; cursor: pointer;
    }
    .audio-btn:active { background: #003d99; transform: scale(0.95); }
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
    st.title("🚀 ByteStep Pro 2.1")
    st.caption(f"Willbazinga's Tech Lab | 北京时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        quiz_mode = st.toggle("Memory Challenge (Blur Mode)", value=False)
        for i, v in enumerate(today_data['vocabulary']):
            safe_text = f"{v['word']}. {v['def']}".replace("'", "\\'")
            display_def = f'<span class="blur-text">{v["def"]}</span>' if quiz_mode else v["def"]
            
            st.markdown(f"""
                <div class="section-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span class="word-title">{v['word']}</span>
                        <button class="audio-btn" onclick="window.quickSpeak('{safe_text}')">🔊 朗读 (Speak)</button>
                    </div>
                    <div style="color:#475569;">{display_def}</div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        for g in today_data['grammar']:
            st.markdown(f'<div class="section-card"><b style="color:#0052cc;">{g["rule"]}</b><br>{g["note"]}</div>', unsafe_allow_html=True)

    with tab3:
        t = today_data['tech_spotlight']
        st.markdown(f'<div class="section-card" style="border-left-color:#f97316;"><b style="font-size:20px;">{t["title"]}</b><p>{t["detail"]}</p></div>', unsafe_allow_html=True)
        if st.button("Complete Today"): st.balloons()
