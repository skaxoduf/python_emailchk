import schedule
import time
import config
from email_checker import check_new_emails
from notifier import send_telegram_alert
import sys

def job():
    print(f"[확인 중] {time.strftime('%Y-%m-%d %H:%M:%S')}")
    found_emails = check_new_emails()
    
    if found_emails:
        for email in found_emails:
            msg = (
                f"🚨 [새로운 업무 메일 감지] 🚨\n\n"
                f"📅 시간: {email['date']}\n"
                f"👤 보낸사람: {email['sender']}\n"
                f"📝 제목: {email['subject']}\n"
            )
            # 텔레그램 전송
            send_telegram_alert(msg)
            print(f"[알림 발송 완료] {email['subject']}")
    else:
        print(" -> 새로운 메일 없음")

def run_test():
    """
    연결 테스트 모드: 설정된 정보로 로그인이 되는지, 알림이 가는지 확인
    """
    print("=== 연결 및 설정 테스트 시작 ===")
    
    # 1. 텔레그램 테스트
    print("1. 텔레그램 메시지 발송 테스트 중...")
    if send_telegram_alert("[TEST] 이메일 알리미 설정 확인 메시지입니다."):
        print("   -> 텔레그램 성공 확인")
    else:
        print("   -> 텔레그램 실패. .env 파일의 토큰과 Chat ID를 확인하세요.")
    
    # 2. 이메일 로그인 테스트
    print("2. 이메일 서버 로그인 테스트 중...")
    try:
        from imap_tools import MailBox
        with MailBox(config.EMAIL_SERVER).login(config.EMAIL_ACCOUNT, config.EMAIL_PASSWORD):
            print("   -> 이메일 로그인 성공")
    except Exception as e:
        print(f"   -> 이메일 로그인 실패: {e}")
        print("      (Gmail의 경우 앱 비밀번호를 사용해야 합니다.)")

    print("=== 테스트 종료 ===")

if __name__ == "__main__":
    # 명령행 인자로 'test'가 들어오면 테스트 모드 실행
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test()
    else:
        print(f"📧 업무 메일 알리미 시작 (주기: {config.CHECK_INTERVAL}초)")
        print("설정된 조건에 맞는 메일을 감시합니다... (종료하려면 Ctrl+C)")
        
        # 첫 시작 시 즉시 한 번 실행
        job()
        
        # 스케줄 등록
        schedule.every(config.CHECK_INTERVAL).seconds.do(job)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
