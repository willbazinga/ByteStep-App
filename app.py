import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. 配置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.0", page_icon="🚀")

# --- 2. 核心语音 JS 逻辑 ---
# 将 speak 函数直接挂载到 window 对象，确保全局可调
st.markdown("""
    <script>
    window.speakText = function(text) {
        window.speechSynthesis.cancel(); // 先停止之前的朗读
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'en-US';
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
    };
    </script>
""", unsafe_allow_html=True)

# 样式
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: relative; }
    .word-title { font-size: 22px; font-weight: 800; color: #1E293B; }
    .blur-text { filter: blur(6px); transition: filter 0.3s; cursor: pointer; }
    .blur-text:active { filter: blur(0); }
    /* 自定义原生 HTML 按钮样式 */
    .audio-icon-btn {
        background: #f1f5f9; border: none; border-radius: 50%; width: 40px; height: 40px;
        cursor: pointer; font-size: 20px; display: flex; align-items: center; justify-content: center;
    }
    .audio-icon-btn:active { background: #e2e8f0; }
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
    st.caption(f"Willbazinga's Tech Lab | 北京时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        quiz_mode = st.toggle("Memory Challenge (Blur Mode)", value=False)
        for i, v in enumerate(today_data['vocabulary']):
            # 准备要朗读的内容，处理掉可能的单引号
            safe_text = f"{v['word']}. {v['def']}".replace("'", "\\'")
            
            # 渲染卡片：这里我们直接用 HTML 画按钮，并绑定 onclick 事件
            # 这种“原生 HTML 触发”是破解移动端禁音的最佳手段
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

    with tab2:
        for g in today_data['grammar']:
            st.markdown(f'<div class="section-card"><b style="color:#0052cc;">{g["rule"]}</b><br>{g["note"]}</div>', unsafe_allow_html=True)

    with tab3:
        t = today_data['tech_spotlight']
        st.markdown(f'<div class="section-card" style="border-left-color:#f97316;"><b style="font-size:20px;">{t["title"]}</b><p>{t["detail"]}</p></div>', unsafe_allow_html=True)
        if st.button("Complete Today"): st.balloons()
