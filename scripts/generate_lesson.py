import os
import json
import requests
from datetime import datetime

# --- 配置 ---
API_KEY = os.getenv("AI_API_KEY") 
API_URL = "https://api.deepseek.com/chat/completions" 

def generate_content():
    if not API_KEY:
        raise Exception("错误: 环境变量 AI_API_KEY 未设置。请检查 GitHub Secrets。")

    prompt = """
    Target: Generate a technical English lesson for Willbazinga.
    Format: Strict JSON.
    Content:
    1. 5 technical English words (word, def).
    2. 2 grammar points (rule, note).
    3. 1 tech spotlight.
    4. scenario_dialogue: A 4-round technical dialogue between 'Senior Dev' and 'Willbazinga'.

    JSON Structure:
    {
      "date": "YYYY-MM-DD",
      "vocabulary": [{"word": "", "def": ""}],
      "grammar": [{"rule": "", "note": ""}],
      "tech_spotlight": {"title": "", "detail": ""},
      "scenario_dialogue": [
        {"speaker": "Senior Dev", "text": "..."},
        {"speaker": "Willbazinga", "text": "..."}
      ]
    }
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}", 
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional tech English tutor. Always respond in valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    print("正在连接 DeepSeek API...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # 检查 HTTP 状态码
    if response.status_code != 200:
        print(f"API 请求失败! 状态码: {response.status_code}")
        print(f"错误详情: {response.text}")
        raise Exception(f"DeepSeek API 返回错误: {response.text}")

    res_data = response.json()
    
    # 鲁棒性检查: 确保 choices 存在
    if 'choices' not in res_data:
        print(f"API 响应结构异常: {res_data}")
        raise Exception("API 响应中缺少 'choices' 字段")

    content_str = res_data['choices'][0]['message']['content']
    return json.loads(content_str)

def main():
    try:
        # 1. 获取内容
        new_lesson = generate_content()
        new_lesson['date'] = datetime.now().strftime("%Y-%m-%d")

        # 2. 读写文件逻辑
        file_path = 'data/lessons.json'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        data = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list): data = []
                except:
                    data = []

        # 3. 追加并去重/限流
        data.append(new_lesson)
        if len(data) > 10: data = data[-10:] # 保留最近10天

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 成功! 已生成 {new_lesson['date']} 的新课程。")

    except Exception as e:
        print(f"❌ 运行失败: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main
