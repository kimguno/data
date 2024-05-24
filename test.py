from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import os

def get_next_filename(directory, prefix, extension):
    files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
    if not files:
        return f"{prefix}1{extension}"
    numbers = [int(f[len(prefix):-len(extension)]) for f in files if f[len(prefix):-len(extension)].isdigit()]
    next_number = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_number}{extension}"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:9090/html_project/study/kakaomap.jsp')

try:
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'map')))

    # 요소의 위치와 크기 가져오기
    location = element.location
    size = element.size

    # 필요한 부분만 스크린샷
    driver.set_window_size(size['width'], size['height'])
    element.screenshot('element_screenshot.png')

    # 디렉토리 생성
    directory = 'C:/map'
    os.makedirs(directory, exist_ok=True)

    # 파일명 생성 및 저장
    filename = get_next_filename(directory, 'element_screenshot_', '.png')
    os.rename('element_screenshot.png', os.path.join(directory, filename))
finally:
    driver.quit()
