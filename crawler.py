import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import subprocess

def crawl():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options, headless=False)
    wait = WebDriverWait(driver, 15)

    try:
        print("🔄 메인 접속 중...")
        driver.get("https://info.nec.go.kr/main/main_load.xhtml")
        time.sleep(5)

        print("🔄 투·개표 클릭...")
        vote_menu = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.m_VC")
        ))
        driver.execute_script("arguments[0].click();", vote_menu)  # JS 클릭
        time.sleep(3)

        print("🔄 개표진행상황 클릭...")
        progress_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='gnb']/div[2]/ul/li[4]/a")
        ))
        driver.execute_script("arguments[0].click();", progress_menu)
        time.sleep(3)

        print("🔄 시·도지사선거 클릭...")
        election_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "electionId3")
        ))
        election_btn.click()
        time.sleep(3)

        print("🔄 서울특별시 선택...")
        city_select = Select(wait.until(EC.presence_of_element_located(
            (By.ID, "cityCode")
        )))
        city_select.select_by_value("1100")
        time.sleep(2)

        print("🔄 검색 클릭...")
        search_btn = driver.find_element(By.CSS_SELECTOR, "#spanSubmit input[type='image']")
        search_btn.click()
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        parse_and_save(soup)

    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()

def parse_and_save(soup):
    candidates = []

    rows = soup.select("table tr")

    name_row = None
    vote_row = None
    rate_row = None

    for i, row in enumerate(rows):
        tds = row.find_all("td")
        if not tds:
            continue

        # ✅ 후보자 이름 행 찾기 (strong 태그에 <br> 포함)
        strong_tags = row.find_all("strong")
        has_candidate = any(tag.find("br") for tag in strong_tags)
        if has_candidate and name_row is None:
            name_row = i
            names = []
            for td in tds:
                strong = td.find("strong")
                if strong and strong.find("br"):
                    parts = strong.get_text(separator="|").split("|")
                    if len(parts) == 2:
                        names.append({
                            "party": parts[0].strip(),
                            "name": parts[1].strip()
                        })
            print(f"👤 후보자: {names}")
            continue

        # ✅ 득표수 행 찾기 (후보자 수만큼 숫자 있는 행)
        if name_row is not None and vote_row is None:
            texts = [td.get_text(strip=True).replace(",", "") for td in tds]
            nums = []
            for t in texts[3:]:
                if t.isdigit() and int(t) > 100:  # 100 이상 숫자만 득표수로 판단
                    nums.append(int(t))
            if len(nums) >= len(names):
                votes = nums[:len(names)]
                vote_row = i
                print(f"🗳️ 득표수: {votes}")
            continue

        # ✅ 득표율 행 찾기 (소수점 숫자 후보자 수만큼)
        if vote_row is not None and rate_row is None:
            texts = [td.get_text(strip=True).replace("%", "").replace("&nbsp;", "").strip() for td in tds]
            rates = []
            for t in texts:
                try:
                    val = float(t)
                    if 0.0 < val <= 100.0:
                        rates.append(val)
                except:
                    pass
            if len(rates) == len(names):
                rate_row = i
                print(f"📈 득표율: {rates}")

    # ✅ 결과 조합
    for i, cand in enumerate(names):
        candidates.append({
            "party": cand["party"],
            "name": cand["name"],
            "votes": votes[i] if i < len(votes) else 0,
            "rate": rates[i] if i < len(rates) else 0.0
        })

    result = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "candidates": candidates
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 저장 완료!")
    print(json.dumps(result, ensure_ascii=False, indent=2))

def is_float(val):
    try:
        float(val)
        return True
    except:
        return False

if __name__ == "__main__":
    print("🚀 크롤러 시작!")
    while True:
        crawl()
        print("⏳ 60초 후 다시 실행...")
        time.sleep(60)
        # crawler.py 맨 끝에 추가
        
        subprocess.run(["git", "add", "data.json"])
        subprocess.run(["git", "commit", "-m", "update data"])
        subprocess.run(["git", "push"])