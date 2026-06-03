from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # ✅ 여기
import time

app = Flask(__name__)
CORS(app)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

@app.route('/votes')
def get_votes():
    driver = get_driver()

    try:
        driver.get("https://info.nec.go.kr/electioninfo/electionInfo_report.xhtml")
        time.sleep(5)  # 대기 시간 늘림

        # iframe 확인
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"=== iframe 개수: {len(iframes)} ===")
        for i, iframe in enumerate(iframes):
            print(f"iframe[{i}] id={iframe.get_attribute('id')} src={iframe.get_attribute('src')}")

        # iframe 안으로 진입
        if iframes:
            driver.switch_to.frame(iframes[0])
            time.sleep(2)

        print("=== 페이지 타이틀 ===")
        print(driver.title)
        print("=== 링크 목록 ===")

        elements = driver.find_elements(By.TAG_NAME, "a")
        for el in elements:
            text = el.text.strip()
            if text:
                print(f"링크: {text} | href: {el.get_attribute('href')}")

        elements2 = driver.find_elements(By.TAG_NAME, "button")
        for el in elements2:
            text = el.text.strip()
            if text:
                print(f"버튼: {text}")

        # 페이지 소스 일부 출력
        print("=== 페이지 소스 앞부분 ===")
        print(driver.page_source[:2000])

    except Exception as e:
        print(f"에러: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()

    return jsonify({"message": "콘솔 확인하세요"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
