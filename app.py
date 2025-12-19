import streamlit as st
import requests
import json
from datetime import datetime

# --- 1. 基础配置与 GitHub 路径 ---
# 请确保下面的 URL 中 'willbazinga' 是你的正确 ID
GITHUB_RAW_URL = "https://raw.githubusercontent.com/willbazinga/ByteStep-App/main/data/lessons.json"

st.set_page_config(page_title="ByteStep AI", page_icon="🚀")

# --- 2. 增强型移动端样式 ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
    .main-card {
        background: white; padding: 25px; border-radius: 24px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        border-bottom: 6px solid #0052cc; margin-top: 10px;
    }
    .tag { color: #0052cc; font-size: 12px; font-weight: 700; text-transform: uppercase; }
    .word { font-size: 32px; font-weight: 800; color: #1E293B; margin: 8px 0; }
    .def { font-size: 16px; color: #475569; line-height: 1.5; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- 3. 动态数据抓取逻辑 ---
@st.cache_data(ttl=3600) # 每小时自动刷新一次缓存
def load_data():
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    # 彻底无法联网时的保底内容
    return [{
        "word": "Real-time Communication",
        "tag": "BytePlus RTC",
        "def": "A technology that allows for instantaneous exchange of information.",
        "example": "BytePlus RTC powers global video conferencing with ultra-low latency.",
        "quiz": "What does RTC stand for?"
    }]

# --- 4. 页面渲染 ---
data = load_data()
# 根据日期自动轮换课程
today_idx = datetime.now().day % len(data)
item = data[today_idx]

st.write(f"👋 **Hello, willbazinga!**")
st.caption(f"Today is {datetime.now().strftime('%Y-%m-%d')}")

st.markdown(f"""
<div class="main-card">
    <div class="tag">● {item.get('tag', 'BytePlus Tech')}</div>
    <div class="word">{item['word']}</div>
    <p class="def">{item['def']}</p>
    <div style="background:#F1F5F9; padding:12px; border-radius:10px; font-style:italic; color:#64748B;">
        "{item['example']}"
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # 间距

col1, col2 = st.columns(2)
with col1:
    if st.button("🔈 Pronunciation"):
        st.info("Seed Speech API Active")
with col2:
    if st.button("💡 Show Answer"):
        st.success(f"Key: {item['word']}")

st.subheader("Interactive Practice")
user_input = st.text_input("Quick Check: Type the key term below")
if user_input.lower().strip() == item['word'].lower().strip():
    st.balloons()
    st.write("✅ Excellent! You've mastered this term.")
