import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. 配置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.0", page_icon="🚀")

# --- 2. 核心语音 JS 逻辑（带解锁功能） ---
st.markdown("""
    <script>
    // 全局语音函数
    window.speakText = function(text) {
        window.speechSynthesis.cancel(); 
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'en-US';
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
    };

    // 音频锁激活函数
    window.unlockAudio = function() {
        const msg = new SpeechSynthesisUtterance('Voice active');
        msg.volume = 0; // 静音播放一次用于解锁
        window.speechSynthesis.speak(msg);
        alert('Voice Lab Unlocked! Now you can click the speaker icons.');
    };
    </script>
""", unsafe_allow_html=True)

# 样式美化
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-title { font-size: 22px; font-weight: 800; color: #1E293B; }
    .blur-text { filter: blur(6px); transition: filter 0.3s; cursor: pointer; }
    .blur-text:active { filter: blur(0); }
    .audio-icon-btn {
        background: #f1f5f9; border: none; border-radius: 50%; width: 42px; height: 42px;
        cursor: pointer; font-size: 22px; display: flex; align-items: center; justify-content: center;
    }
    .unlock-btn {
        background: #0052cc; color: white; border: none; padding: 10px 20px;
        border-radius: 10px; font-weight: bold; width: 100%; margin-bottom: 20px;
    }
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
    
    # --- 新增：手动解锁音频按钮 ---
    # 第一次进入页面必须点击这个
    st.markdown('<button class="unlock-btn" onclick="window.unlockAudio()">点击解锁语音功能 (Unlock Voice)</button>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        quiz_mode = st.toggle("Memory Challenge (Blur Mode)", value=False)
        for i, v in enumerate(today_data['vocabulary']):
            safe_text = f"{v['word']}. {v['def']}".replace("'", "\\'")
            display_def = f'<span class="blur-text">{v["def"]}</span>' if quiz_mode else v["def"]
            
            st.markdown(f"""
                <div class="section-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="word-title">{v['word']}</span>
                        <button class="audio-icon-btn" onclick="window.speakText('{safe_text}')">🔊</button>
                    </div>
                    <div style="color:#475569; margin-top:8px;">{display_def}</div>
                </div>
            """, unsafe_allow_html=True)

    # ... 后续卡片逻辑保持不变
