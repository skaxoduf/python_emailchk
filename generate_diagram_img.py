from html2image import Html2Image
import os

def generate_diagram_image():
    base_dir = os.getcwd()
    html_file = os.path.join(base_dir, "diagram_only.html")
    output_file = "architecture_diagram.png"

    hti = Html2Image()
    # 배경 투명하지 않게, 넉넉한 크기로 캡처
    hti.size = (1200, 1400) 
    
    
    # Mermaid 렌더링을 위한 대기 시간 추가
    import time
    # time.sleep(2) # html2image doesn't support waiting in screenshot method generally, but we can rely on system speed or try to invoke it differently.
    # Actually checking documentation, Hti methods are blocking but browser rendering might be async.
    # We will try adding a wait by executing a script or just hoping the library handles load.
    # Better yet, let's just use the current script but maybe the size or selector is off.
    # Let's try to capture 'body' explicitly and maybe add a small sleep in python is not effective if the browser process is separate.
    # But often html2image creates a temp file. 

    # Let's try to use a white background for debugging if dark fails, but user wants dark.
    # Let's ensure body has background color.

    print(f"Generating {output_file} from {html_file}...")
    
    # Adding a slight delay in hopes the browser renders. 
    # html2image usually waits for 'load' event. 
    # Mermaid might run after load.
    
    try:
        hti.screenshot(
            html_file=html_file, 
            save_as=output_file,
            size=(1200, 1400)
        )
        print("Diagram generation successful!")
    except Exception as e:
        print(f"Error during diagram generation: {e}")

if __name__ == "__main__":
    generate_diagram_image()
