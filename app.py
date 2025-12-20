import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. 配置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.3", page_icon="🚀")

# --- 2. 极其精简且强健的 JS 逻辑 ---
st.markdown("""
    <script>
    window.playWord = function(word, definition) {
        // 核心：每次点击都重新获取合成器实例，确保激活
        const synth = window.speechSynthesis;
        synth.cancel(); 
        const text = word + ". " + definition;
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = 'en-US';
        utter.rate = 0.85;
        synth.speak(utter);
    };
    </script>
""", unsafe_allow_html=True)

# 样式美化
st.markdown("""
    <style>
    .section-card { 
        background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; 
        border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
        cursor: pointer; transition: transform 0.1s;
    }
    .section-card:active { transform: scale(0.98); background: #f8fafc; }
    .word-title { font-size: 22px; font-weight: 800; color: #1E293B; }
    .blur-text { filter: blur(6px); transition: filter 0.3s; }
    .hint-text { font-size: 12px; color: #94a3b8; margin-top: 5px; }
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
    st.title("🚀 ByteStep Pro 2.3")
    
    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        st.info("💡 提示：点击下方的单词卡片，即可听到发音！")
        quiz_mode = st.toggle("Memory Challenge (Blur Mode)", value=False)
        
        for i, v in enumerate(today_data['vocabulary']):
            safe_word = v['word'].replace("'", "\\'")
            safe_def = v['def'].replace("'", "\\'")
            display_def = f'<span class="blur-text">{v["def"]}</span>' if quiz_mode else v["def"]
            
            # 直接将 onclick 绑定到整个卡片上，用户体验最丝滑
            st.markdown(f"""
                <div class="section-card" onclick="window.playWord('{safe_word}', '{safe_def}')">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="word-title">{v['word']}</span>
                        <span style="font-size: 20px;">🔊</span>
                    </div>
                    <div style="color:#475569; margin-top:8px;">{display_def}</div>
                    <div class="hint-text">Click to listen</div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        for g in today_data['grammar']:
            st.markdown(f'<div class="section-card"><b style="color:#0052cc;">{g["rule"]}</b><br>{g["note"]}</div>', unsafe_allow_html=True)

    with tab3:
        t = today_data['tech_spotlight']
        st.markdown(f'<div class="section-card" style="border-left-color:#f97316;"><b>{t["title"]}</b><p>{t["detail"]}</p></div>', unsafe_allow_html=True)
        if st.button("Complete Today"): st.balloons()
