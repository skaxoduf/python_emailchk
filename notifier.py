import requests
import config

def send_telegram_alert(message):
    """
    텔레그램 봇을 통해 메시지를 전송합니다.
    """
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("설정 오류: 텔레그램 토큰 또는 Chat ID가 설정되지 않았습니다.")
        return False

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[전송 성공] {message}")
            return True
        else:
            print(f"[전송 실패] Status Code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"[전송 중 에러 발생] {e}")
        return False
