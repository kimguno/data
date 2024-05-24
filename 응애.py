from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import os

# 다음 파일 이름을 결정하는 함수
def get_next_filename(directory, prefix, extension):
    files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
    if not files:
        return f"{prefix}1{extension}"
    numbers = [int(f[len(prefix):-len(extension)]) for f in files if f[len(prefix):-len(extension)].isdigit()]
    next_number = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_number}{extension}"

# 크롬 드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# 웹드라이버 설정 및 웹페이지 로드
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:9090/html_project/study/kakaomap.jsp')

# 페이지 로드 대기 (WebDriverWait 사용)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'map')))

# 전체 페이지 스크린샷 저장
driver.save_screenshot('full_screenshot.png')

# 요소의 위치와 크기 가져오기
location = element.location
size = element.size

# 이미지 열기
image = Image.open('full_screenshot.png')

# 요소의 위치에 맞춰 잘라내기
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']

element_screenshot = image.crop((left, top, right, bottom))

# 디렉토리 생성
directory = 'C:/map'
os.makedirs(directory, exist_ok=True)

# 파일명 생성
filename = get_next_filename(directory, 'element_screenshot_', '.png')

# 잘라낸 이미지 저장
element_screenshot.save(os.path.join(directory, filename))

# 웹드라이버 종료
driver.quit()