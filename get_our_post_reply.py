import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")
POST_ID = os.getenv("POST_ID")  # 替換為你想回覆的貼文 ID，請先從 `get_our_posts.py` 取得 ID

URL = f"https://graph.threads.net/v1.0/{POST_ID}/replies"
PARAMS = {
    "fields": "id,text",
    "access_token": ACCESS_TOKEN,
    "reverse": "true"  # 反向排序，最新的回覆會在最前面
}

try:
    response = requests.get(URL, params=PARAMS)
    response.raise_for_status()  # 如果回應碼不是 200，會拋出異常
    data = response.json()
    print("回覆列表：")
    for reply in data.get("data", []):
        print(f"ID: {reply['id']}, 內容: {reply['text']}")
except requests.exceptions.RequestException as e:
    print(f"❌ 請求發生錯誤：{e}")
except Exception as e:
    print(f"❌ 發生未預期的錯誤：{e}")