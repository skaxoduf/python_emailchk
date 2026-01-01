import base64
import requests
import sys

def download_tokyo_diagram():
    # Tokyo Night Colors
    # Background: #1a1b26
    # Primary (Blue): #7aa2f7
    # Secondary (Purple): #bb9af7
    # Text: #c0caf5
    # Card/Node BG: #24283b
    
    graph = """
graph TD
    %% Theme Configuration for Tokyo Night
    classDef default fill:#24283b,stroke:#7aa2f7,stroke-width:2px,color:#c0caf5;
    classDef highlight fill:#1f2335,stroke:#bb9af7,stroke-width:3px,color:#fff;
    linkStyle default stroke:#7aa2f7,stroke-width:2px;

    User((사용자)) -->|프로그램 실행| Main[main.py: 메인 컨트롤러]
    
    subgraph 초기화 [초기 설정 및 스케줄링]
        style 초기화 fill:#1a1b26,stroke:#414868,color:#7dcfff
        Env[.env 파일] -->|환경변수| Config[config.py]
        Config -->|설정 주입| Main
        Config -->|설정 주입| Checker[email_checker.py]
        Config -->|설정 주입| Notifier[notifier.py]
        Main -->|스케줄러 시작| Schedule{스케줄러}
    end

    subgraph 반복 [작업 실행 루프]
        style 반복 fill:#1a1b26,stroke:#414868,color:#7dcfff
        Schedule -->|설정된 주기마다| Job[job 함수 실행]
        Job -->|호출| Checker
    end

    subgraph 로직 [이메일 확인 프로세스]
        style 로직 fill:#1a1b26,stroke:#414868,color:#7dcfff
        Checker -->|1. 로그인| MailServer[("이메일 서버 (IMAP)")]
        MailServer -->|2. 안 읽은 메일 조회| Filter{3. 필터링}
        
        Filter -- 조건 불일치 --> Ignore[무시]
        Filter -- 조건 일치 --> NewMail[새 이메일 목록]
        
        subgraph 필터조건
            style 필터조건 fill:#24283b,stroke:#565f89,color:#bb9af7
            Cond1[날짜 필터]
            Cond2[보낸사람 필터]
            Cond3[제목 키워드]
        end
        Cond1 -.-> Filter
        Cond2 -.-> Filter
        Cond3 -.-> Filter
    end

    subgraph 알림 [알림 발송]
        style 알림 fill:#1a1b26,stroke:#414868,color:#7dcfff
        NewMail -->|데이터 반환| Job
        Job -->|메시지 구성| Notifier
        Notifier -->|HTTP POST| TeleAPI["텔레그램 Bot API"]
        TeleAPI -->|푸시 알림| UserDevice[("사용자 텔레그램")]
    end
    """
    
    graph_bytes = graph.encode('utf8')
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode('ascii')
    
    # bgColor for Tokyo Night background
    url = f"https://mermaid.ink/img/{base64_string}?bgColor=1a1b26"
    
    print(f"Downloading from: {url[:50]}...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open("tokyo_diagram.png", "wb") as f:
                f.write(response.content)
            print("Successfully downloaded tokyo_diagram.png")
            print(f"File size: {len(response.content)} bytes")
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_tokyo_diagram()
