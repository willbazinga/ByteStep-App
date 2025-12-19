import streamlit as st
import requests
import time
from datetime import datetime

# 配置与路径
GITHUB_ID = "willbazinga"
REPO_NAME = "ByteStep-App"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep Pro", page_icon="🚀")

# 移动端精致样式
st.markdown("""
    <style>
    .section-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #0052cc; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .word-title { font-size: 20px; font-weight: 800; color: #1E293B; }
    .tech-title { color: #0052cc; font-size: 24px; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_enhanced_data():
    try:
        r = requests.get(RAW_URL, timeout=5)
        if r.status_code == 200: return r.json()
    except: pass
    return None # 这里可以加一个更复杂的保底逻辑

data_list = load_enhanced_data()

if data_list:
    # 始终取最新的一组内容
    today_data = data_list[-1] 
    
    st.title("🚀 ByteStep Pro")
    st.caption(f"Willbazinga's Daily Tech Intake | {datetime.now().strftime('%Y-%m-%d')}")

    # 使用 Tabs 标签页适配手机底部或顶部切换
    tab1, tab2, tab3 = st.tabs(["🔤 Vocabulary", "📝 Grammar", "💻 Tech"])

    with tab1:
        st.subheader("5 Daily Terms")
        for v in today_data['vocabulary']:
            st.markdown(f"""<div class="section-card">
                <div class="word-title">{v['word']}</div>
                <div style="color:#475569;">{v['def']}</div>
            </div>""", unsafe_allow_html=True)

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
        if st.button("✅ Mark as Read"):
            st.balloons()
            st.success("Great job today!")
else:
    st.error("Data sync in progress... Please check GitHub Actions.")
