import requests
import os
from dotenv import load_dotenv
import time

def get_chat_id():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token or "123456789" in token:
        print("❌ 오류: .env 파일에 TELEGRAM_BOT_TOKEN이 올바르게 설정되지 않았습니다.")
        return

    print(f"🤖 봇 토큰: {token[:10]}... (확인됨)")
    print("📡 텔레그램 서버에서 업데이트를 가져오는 중...")
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ API 오류: {data}")
            return

        results = data.get("result", [])
        
        if not results:
            print("\n⚠️ [중요] 메시지가 감지되지 않았습니다!")
            print("1. 텔레그램 앱을 켜세요.")
            print("2. 만든 봇을 찾아 들어가세요.")
            print("3. '시작' 버튼을 누르거나 'hello'라고 메시지를 보내세요.")
            print("4. 그 다음 이 프로그램을 다시 실행하세요.")
            return

        # 가장 최근 메시지에서 ID 추출
        last_update = results[-1]
        chat_id = last_update.get("message", {}).get("chat", {}).get("id")
        
        if chat_id:
            print(f"\n✅ Chat ID를 찾았습니다: {chat_id}")
            print(f"👉 .env 파일의 TELEGRAM_CHAT_ID 부분에 이 숫자를 입력해주세요.")
        else:
            print("❌ 메시지 구조를 파악할 수 없습니다. 다시 시도해주세요.")
            print(last_update)
            
    except Exception as e:
        print(f"❌ 연결 실패: {e}")

if __name__ == "__main__":
    get_chat_id()
