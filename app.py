import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. 配置 ---
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro 2.4", page_icon="🚀")

# --- 2. 样式美化 ---
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-title { font-size: 20px; font-weight: 800; color: #1E293B; }
    .blur-text { filter: blur(6px); transition: filter 0.3s; cursor: pointer; }
    .blur-text:active { filter: blur(0); }
    .scenario-box { background: #f8fafc; padding: 15px; border-radius: 10px; border: 1px dashed #cbd5e1; font-family: monospace; }
    .speaker { color: #0052cc; font-weight: bold; }
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
    st.title("🚀 ByteStep Pro 2.4")
    st.caption(f"Willbazinga's Tech Lab | {datetime.now().strftime('%m-%d %H:%M')}")

    # 修改后的三个 Tab
    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💬 Scenario"])

    with tab1:
        quiz_mode = st.toggle("Memory Challenge (Blur Mode)", value=False)
        for v in today_data['vocabulary']:
            display_def = f'<span class="blur-text">{v["def"]}</span>' if quiz_mode else v["def"]
            st.markdown(f"""
                <div class="section-card">
                    <div class="word-title">{v['word']}</div>
                    <div style="color:#475569; margin-top:8px;">{display_def}</div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        for g in today_data['grammar']:
            st.markdown(f'<div class="section-card"><b style="color:#0052cc;">{g["rule"]}</b><br>{g["note"]}</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("💻 Today's Tech Dialogue")
        # 模拟真实的职场对话场景，将当天的词汇串联起来
        # 注意：未来的版本我们可以让爬虫自动生成这段 JSON 内容
        words = [v['word'] for v in today_data['vocabulary']]
        
        st.info("看看今天学习的词汇如何应用在【架构评审会议】中：")
        
        st.markdown(f"""
        <div class="scenario-box">
            <p><span class="speaker">Senior Architect:</span> "We need to ensure the <b>{words[0]}</b> of our new service. If the <b>{words[1]}</b> is too high, users will complain."</p>
            <p><span class="speaker">Willbazinga:</span> "I agree. We should also monitor the <b>{words[2]}</b> to make sure we can handle 10k requests per second."</p>
            <p><span class="speaker">Senior Architect:</span> "Good point. What about <b>{words[3]}</b>?"</p>
            <p><span class="speaker">Willbazinga:</span> "We'll use multi-region deployment to keep it at 99.99%."</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Complete & Celebrate"):
            st.balloons()

else:
    st.info("Syncing data from GitHub...")
