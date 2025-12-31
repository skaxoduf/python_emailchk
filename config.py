import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 이메일 설정
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "imap.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# 알림 조건 설정
# 쉼표(,)로 구분하여 여러 개 입력 가능
_senders_str = os.getenv("TARGET_SENDER", "")
TARGET_SENDERS = [s.strip() for s in _senders_str.split(",") if s.strip()]

_keywords_str = os.getenv("TARGET_SUBJECT_KEYWORD", "")
TARGET_SUBJECT_KEYWORDS = [k.strip() for k in _keywords_str.split(",") if k.strip()]

# 텔레그램 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# 날짜 필터 (YYYY-MM-DD)
# 이 날짜 "이후" (당일 포함)에 온 메일만 확인
TARGET_START_DATE = os.getenv("TARGET_START_DATE", "")

# 주기 설정 (초 단위)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
