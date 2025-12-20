import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. 配置与基础设置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
# 增加时间戳参数防止 GitHub Raw 缓存旧数据
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.0", page_icon="🚀", layout="centered")

# --- 2. 样式美化 ---
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-title { font-size: 22px; font-weight: 800; color: #1E293B; }
    .tech-title { color: #0052cc; font-size: 24px; font-weight: 800; }
    /* 遮罩样式：用于记忆挑战 */
    .blur-text { filter: blur(5px); transition: filter 0.3s; cursor: pointer; background: #f1f5f9; border-radius: 4px; }
    .blur-text:active { filter: blur(0); }
    </style>
""", unsafe_allow_html=True)

# --- 3. 数据加载逻辑 ---
@st.cache_data(ttl=60)
def load_data():
    try:
        # 强制请求最新 JSON
        r = requests.get(RAW_URL, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.error(f"Sync Error: {e}")
    return None

data_list = load_data()

# --- 4. 页面主体渲染 ---
if data_list:
    today_data = data_list[-1]
    st.title("🚀 ByteStep Pro 2.0")
    st.caption(f"Willbazinga's Tech Lab | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 功能选项卡
    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        st.subheader("5 Daily Terms")
        # 记忆挑战开关
        quiz_mode = st.toggle("Memory Challenge (Blur Definitions)", value=False)
        
        for i, v in enumerate(today_data['vocabulary']):
            col1, col2 = st.columns([0.82, 0.18])
            
            with col1:
                # 如果开启挑战模式，给定义加上模糊滤镜
                display_def = f'<span class="blur-text">{v["def"]}</span>' if quiz_mode else v["def"]
                st.markdown(f"""
                    <div class="section-card">
                        <div class="word-title">{v['word']}</div>
                        <div style="color:#475569; margin-top:8px; font-size:16px;">{display_def}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # 修复版语音逻辑：将 JS 打包发送，穿透沙箱
                if st.button(f"🔊", key=f"speak_{i}"):
                    clean_word = v['word'].replace("'", "\\'")
                    clean_def = v['def'].replace("'", "\\'")
                    js_code = f"""
                        <script>
                        var msg = new SpeechSynthesisUtterance('{clean_word}. Definition: {clean_def}');
                        msg.lang = 'en-US';
                        msg.rate = 0.9; // 稍微放慢语速
                        window.speechSynthesis.speak(msg);
                        </script>
                    """
                    st.components.v1.html(js_code, height=0)

    with tab2:
        st.subheader("2 Grammar Points")
        for g in today_data['grammar']:
            st.markdown(f"""<div class="section-card">
                <div style="font-weight:bold; color:#0052cc; font-size:18px;">{g['rule']}</div>
                <div style="margin-top:8px; line-height:1.5;">{g['note']}</div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.subheader("Tech Spotlight")
        t = today_data['tech_spotlight']
        st.markdown(f"""<div class="section-card" style="border-left-color:#f97316;">
            <div class="tech-title">{t['title']}</div>
            <p style="margin-top:10px; line-height:1.6; font-size:16px;">{t['detail']}</p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("Complete Today's Intake"):
            st.balloons()
            st.success("Great job! See you tomorrow.")

else:
    st.info("Waiting for today's data deployment...")
