import streamlit as st
import json
import os
from datetime import datetime

# --- 1. 界面配置：打造原生 App 感官 ---
st.set_page_config(page_title="ByteStep Tech English", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    /* 全局背景与字体 */
    .stApp { background-color: #F8FAFC; }
    
    /* 移动端卡片容器 */
    .tech-card {
        background: white;
        padding: 24px;
        border-radius: 24px;
        border-bottom: 6px solid #0052cc;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* 标题与文字样式 */
    .category-tag {
        color: #0052cc;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .main-word {
        font-size: 32px;
        font-weight: 800;
        color: #1E293B;
        margin: 10px 0;
    }
    .definition {
        font-size: 16px;
        color: #475569;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心逻辑：数据管理 ---
def get_daily_content():
    """读取本地缓存，如果没有则返回默认高质量内容"""
    cache_path = 'data/lessons.json'
    
    # 默认题库 (基于 BytePlus 官网最新内容)
    default_lessons = [
        {
            "word": "Temporal Consistency",
            "tag": "Video Generation (Veo)",
            "def": "The ability to maintain stable objects and backgrounds across video frames.",
            "example": "BytePlus Veo ensures temporal consistency in long-sequence generation.",
            "quiz": "Which term describes stable backgrounds in AI video?"
        },
        {
            "word": "Multimodal Translation",
            "tag": "AI Intelligence",
            "def": "The process of translating content across different types of media like text, audio, and video.",
            "example": "Our platform supports multimodal translation for global content delivery.",
            "quiz": "Translation involving multiple media types is called ______."
        }
    ]
    
    # 如果有自动化脚本抓取的本地文件，优先读取
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default_lessons

# --- 3. App 渲染层 ---
# 获取内容并根据日期轮换
all_lessons = get_daily_content()
day_index = datetime.now().day % len(all_lessons)
today = all_lessons[day_index]

# 顶部导航
st.write(f"📅 {datetime.now().strftime('%A, %b %d')}")
st.title("ByteStep AI")
st.caption(f"Willbazinga's Tech Growth Hub")

# 核心卡片渲染
st.markdown(f"""
<div class="tech-card">
    <div class="category-tag">● {today['tag']}</div>
    <div class="main-word">{today['word']}</div>
    <p class="definition">{today['def']}</p>
    <div style="background: #F1F5F9; padding: 15px; border-radius: 12px; border-left: 4px solid #CBD5E1;">
        <p style="margin:0; font-style: italic; color: #64748B;">"{today['example']}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 互动操作
col1, col2 = st.columns(2)
with col1:
    if st.button("🔈 Pronunciation"):
        st.info("Simulating BytePlus Seed Speech...")
        # 后续可接入真实 API：st.audio(api_call(today['word']))

with col2:
    if st.button("💡 Show Answer"):
        st.toast(f"Quiz Hint: {today['word']}")

# 练习区
st.subheader("Interactive Challenge")
user_input = st.text_input("Type the sentence above to practice:")
if user_input.lower() == today['example'].lower().strip('"'):
    st.balloons()
    st.success("Perfect Matching! Accuracy: 100%")
