import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# 第一步：建立貼文草稿
url = "https://graph.threads.net/v1.0/me/threads"
params = {
    "access_token": ACCESS_TOKEN,
    "media_type": "TEXT",
    "text": "Hello this is a test post from API",
}

try:
    response = requests.post(url, params=params)
    print("建立草稿回應：")
    print(response.text)
    
    # 解析回應以取得 creation_id
    if response.status_code == 200:
        data = response.json()
        creation_id = data.get("id")
        
        if creation_id:
            print(f"草稿 ID: {creation_id}")
            
            # 第二步：發布貼文
            publish_url = "https://graph.threads.net/v1.0/me/threads_publish"
            publish_params = {
                "access_token": ACCESS_TOKEN,
                "creation_id": creation_id,
            }
            
            publish_response = requests.post(publish_url, params=publish_params)
            print("發布回應：")
            print(publish_response.text)
            
            if publish_response.status_code == 200:
                print("✅ 貼文發布成功！")
            else:
                print(f"❌ 發布失敗，狀態碼：{publish_response.status_code}")
        else:
            print("❌ 無法取得草稿 ID")
    else:
        print(f"❌ 建立草稿失敗，狀態碼：{response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ 請求發生錯誤：{e}")
except Exception as e:
    print(f"❌ 發生未預期的錯誤：{e}")
