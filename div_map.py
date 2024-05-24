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
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:9090/html_project/study/test.jsp')

try:
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'map')))

    driver.save_screenshot('full_screenshot.png')

    location = element.location
    size = element.size

    image = Image.open('full_screenshot.png')
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    element_screenshot = image.crop((left, top, right, bottom))

    directory = 'C:/map'
    os.makedirs(directory, exist_ok=True)

    filename = get_next_filename(directory, 'element_screenshot_', '.png')
    element_screenshot.save(os.path.join(directory, filename))
finally:
    driver.quit()