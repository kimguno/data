import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def image_to_scoreboard(image_path):
    # 이미지 열기
    image = Image.open(image_path)
    width, height = image.size
    
    # 점수 판 초기화
    scoreboard = np.zeros((height, width))
    
    # 각 픽셀에 대해 점수 매기기
    for y in range(height):
        for x in range(width):
            # 픽셀의 색상 가져오기
            pixel = image.getpixel((x, y))
            
            # 흰색(255, 255, 255)이면 1점, 그 외의 경우 0점 부여
            score = 1 if pixel == (255, 255, 255) else 0
            scoreboard[y, x] = score
    
    return scoreboard

# 이미지 파일 경로
image_path = "C:/map/dongjunplz.png"

# 이미지를 점수 판으로 변환
scoreboard = image_to_scoreboard(image_path)

# 점수 판 이미지를 Matplotlib을 사용하여 표시
plt.imshow(scoreboard, cmap='gray', interpolation='nearest')
plt.show()
