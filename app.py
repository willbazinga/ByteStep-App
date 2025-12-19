import streamlit as st
import requests
import json
import time
from datetime import datetime

# --- 核心修改：增加时间戳防止缓存 ---
# 请手动确认这个 URL 在浏览器能打开并看到 JSON 内容
GITHUB_ID = "willbazinga" # 如果你的 ID 不对，请在这里修改
REPO_NAME = "ByteStep-App" # 如果仓库名不对，请在这里修改

RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_ID}/{REPO_NAME}/main/data/lessons.json?t={int(time.time())}"

st.set_page_config(page_title="ByteStep AI", page_icon="🚀")

@st.cache_data(ttl=60) # 将缓存缩短到 1 分钟
def load_data():
    try:
        # 打印一下正在尝试访问的 URL 到控制台，方便排查
        response = requests.get(RAW_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Sync Error: {e}")
    return [{"word": "Syncing...", "tag": "System", "def": "Waiting for GitHub data...", "example": "Please wait.", "quiz": ""}]

# --- 以下 UI 逻辑保持不变 ---
data = load_data()
today_idx = datetime.now().day % len(data)
item = data[today_idx]

st.markdown(f"""
<div style="background: white; padding: 25px; border-radius: 20px; border-bottom: 6px solid #0052cc;">
    <div style="color: #0052cc; font-weight: bold;">● {item.get('tag', 'BytePlus')}</div>
    <div style="font-size: 30px; font-weight: 800; margin: 10px 0;">{item['word']}</div>
    <p style="color: #475569;">{item['def']}</p>
</div>
""", unsafe_allow_html=True)

if st.button("Check Connectivity"):
    st.write(f"Current Target URL: {RAW_URL}")
