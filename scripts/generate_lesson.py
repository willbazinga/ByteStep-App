import os
import json
import requests
from datetime import datetime

# --- 配置 ---
API_KEY = os.getenv("AI_API_KEY") 
API_URL = "https://api.deepseek.com/chat/completions" 

def generate_content():
    prompt = """
    Target: Generate a technical English lesson for a developer named Willbazinga.
    Format: Strict JSON.
    Content:
    1. 5 technical English words (word, def).
    2. 2 grammar points (rule, note).
    3. 1 tech spotlight (title, detail).
    4. scenario_dialogue: A 4-round technical dialogue using today's words.

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
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a tech English tutor."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return json.loads(response.json()['choices'][0]['message']['content'])

def main():
    try:
        new_lesson = generate_content()
        new_lesson['date'] = datetime.now().strftime("%Y-%m-%d")

        file_path = 'data/lessons.json'
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append(new_lesson)
        if len(data) > 7: data = data[-7:]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Successfully generated new lesson!")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
