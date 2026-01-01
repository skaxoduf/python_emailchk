from html2image import Html2Image
import os
import time

def generate_jpg():
    # 현재 디렉토리 경로
    base_dir = os.getcwd()
    html_file = os.path.join(base_dir, "analysis_report.html")
    output_file = "analysis_report.jpg"

    hti = Html2Image()
    
    # 브라우저 크기 설정 (스크롤 없이 전체 캡처를 위해 충분히 크게)
    hti.size = (900, 2000) 
    
    print(f"Converting {html_file} to {output_file}...")
    
    # 윈도우 환경에서 실행 시, Chrome 경로를 못 찾을 경우를 대비해 예외처리나 경로 지정이 필요할 수 있음
    # 기본적으로 html2image는 시스템의 Chrome/Edge를 찾음
    try:
        hti.screenshot(
            html_file=html_file, 
            save_as=output_file
        )
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    generate_jpg()
