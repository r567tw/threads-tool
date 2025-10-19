import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")
KEEP_KEYWORDS = ["封鎖", "看球", "動畫", "今天","網紅","Josh","季後賽","樂天","中信","富邦","味全","統一"]

# Threads Graph API 基本 URL
BASE_URL = "https://graph.threads.net/v1.0"

# 讀取自己的 Threads 貼文
def get_my_threads():
    threads = []
    url = f"{BASE_URL}/{USER_ID}/threads"
    params = {"access_token": ACCESS_TOKEN , "fields": "id,text"}
    res = requests.get(url, params=params)
    res.raise_for_status()

    data = res.json().get("data", [])
    next_page = res.json().get("paging", {}).get("next")

    while next_page:
        # print("取得更多貼文...: ")
        for item in data:
            if not any(keyword in item.get("text", "") for keyword in KEEP_KEYWORDS):
                threads.append(item)
        res = requests.get(next_page)
        res.raise_for_status()
        data = res.json().get("data", [])
        next_page = res.json().get("paging", {}).get("next")

    return threads

# 主流程
def main():
    threads = get_my_threads()
    print("取得的貼文數量:", len(threads))
    with open("to_delete_threads.txt", "w", encoding="utf-8") as f:
        for post in threads:
            thread_id = post.get("id")
            text = post.get("text", "")
            f.write(f"{thread_id}\t{text}\n")


        

if __name__ == "__main__":
    main()
