import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")
KEEP_KEYWORDS = ["封鎖", "看球", "動畫", "今天","網紅","Josh","季後賽"]

# print("使用的 USER_ID:", USER_ID)
# print("使用的 ACCESS_TOKEN:", ACCESS_TOKEN[:10] + "..." + ACCESS_TOKEN[-10:])

# Threads Graph API 基本 URL
BASE_URL = "https://graph.threads.net/v1.0"

# 讀取自己的 Threads 貼文
def get_my_threads():
    url = f"{BASE_URL}/{USER_ID}/threads"
    params = {"access_token": ACCESS_TOKEN , "fields": "id,text"}
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json().get("data", [])

# 刪除 Threads 貼文
def delete_thread(thread_id):
    url = f"{BASE_URL}/{thread_id}"
    params = {"access_token": ACCESS_TOKEN}
    res = requests.delete(url, params=params)
    if res.status_code == 200:
        print(f"🗑️ 已刪除貼文 {thread_id}")
    else:
        print(f"⚠️ 無法刪除貼文 {thread_id}: {res.text}")

# 主流程
def main():
    threads = get_my_threads()
    for post in threads:
        # print(post)
        text = post.get("text", "")
        thread_id = post.get("id")

        if text == "":
            print(f"🗑️ 刪除空貼文：{thread_id}")
            delete_thread(thread_id)
            # 記錄已刪除貼文數量
            if not hasattr(main, "deleted_count"):
                main.deleted_count = 0
            main.deleted_count += 1
            if main.deleted_count >= 100:
                print("已刪除 100 篇貼文，停止執行。")
                break

        # if any(k in text for k in KEEP_KEYWORDS):
        #     print(f"✅ 保留：{text[20:]}...")
        # else:
        #     print(f"🗑️ 刪除：{text}...")
        #     # delete_thread(thread_id)
        # break  # 測試時只處理一篇貼文，正式使用時可移除

if __name__ == "__main__":
    main()
