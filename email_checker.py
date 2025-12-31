from imap_tools import MailBox, AND
import config
import time

# 이미 알림을 보낸 메일의 UID를 저장할 집합
processed_uids = set()

def check_new_emails():
    """
    새로운 메일을 확인하고 조건에 맞는 메일이 있으면 딕셔너리 리스트로 반환합니다.
    """
    new_emails = []
    try:
        # 날짜 필터 설정 확인
        search_criteria = {'seen': False} # 기본 조건: 안 읽은 메일
        
        if config.TARGET_START_DATE:
            try:
                from datetime import datetime
                # 문자열(YYYY-MM-DD)을 날짜 객체로 변환
                start_date = datetime.strptime(config.TARGET_START_DATE.strip(), "%Y-%m-%d").date()
                search_criteria['date_gte'] = start_date
            except ValueError:
                print(f"[설정 오류] 날짜 형식이 올바르지 않습니다: {config.TARGET_START_DATE} (예: 2024-01-01)")

        # MailBox 객체 생성 및 로그인
        with MailBox(config.EMAIL_SERVER).login(config.EMAIL_ACCOUNT, config.EMAIL_PASSWORD) as mailbox:
            # 설정된 조건(date_gte 등)을 포함하여 fetch
            # mark_seen=False 설정: 메일을 가져와도 '읽음' 처리를 하지 않음 (사용자 요청 사항)
            for msg in mailbox.fetch(AND(**search_criteria), mark_seen=False):
                # 이미 처리한 메일인지(프로그램 실행 중 중복 방지)
                if msg.uid in processed_uids:
                    continue

                is_target = False
                
                # 1. 발신자 조건 체크 (설정된 경우에만)
                if config.TARGET_SENDERS:
                    if any(sender in msg.from_ for sender in config.TARGET_SENDERS):
                        is_target = True

                # 2. 제목 키워드 조건 체크 (설정된 경우에만)
                # 발신자 조건이 만족 안 됐더라도, 제목 키워드가 맞으면 알림 (OR 조건)
                # 만약 AND 조건을 원하시면 로직을 수정해야 합니다. 지금은 "이거거나 저거면" 알림입니다.
                if not is_target and config.TARGET_SUBJECT_KEYWORDS:
                    if any(keyword in msg.subject for keyword in config.TARGET_SUBJECT_KEYWORDS):
                        is_target = True
                
                # 설정값이 아예 없으면? -> 모든 읽지 않은 메일 알림 (원치 않으시면 이 부분을 False로 두세요)
                if not config.TARGET_SENDERS and not config.TARGET_SUBJECT_KEYWORDS:
                    # 조건이 아무것도 없으면 모든 메일 알림
                    is_target = True

                if not is_target:
                    continue

                # 조건 만족 시 리스트에 추가 및 처리된 UID로 등록
                email_info = {
                    "sender": msg.from_,
                    "subject": msg.subject,
                    "date": msg.date_str,
                    "uid": msg.uid
                }
                new_emails.append(email_info)
                processed_uids.add(msg.uid)

    except Exception as e:
        print(f"[이메일 확인 중 에러] {e}")

    return new_emails
