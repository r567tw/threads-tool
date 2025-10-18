import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")

# Threads Graph API 基本 URL
BASE_URL = "https://graph.threads.net/v1.0"

# 讀取自己的 Threads 貼文
def get_my_threads():
    url = f"{BASE_URL}/{USER_ID}/threads?fields=id,text"
    params = {"access_token": ACCESS_TOKEN}
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json().get("data", [])

# 主流程
def main():
    threads = get_my_threads()
    for post in threads:
        print(post)
        text = post.get("text", "")
        thread_id = post.get("id")
        if text == "":
            print(f"ID: {thread_id}, 內容: {text}")

if __name__ == "__main__":
    main()
