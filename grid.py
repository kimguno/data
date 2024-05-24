import numpy as np
from PIL import Image

# 이미지 불러오기
image_path = 'C:/map/element_screenshot_6.png'
image = Image.open(image_path)
image = image.convert('RGB')

# 이미지 크기 얻기
width, height = image.size

# 각 픽셀의 RGB 값 추출 및 그리드화
grid = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        r, g, b = image.getpixel((x, y))
        grid[y, x] = [r, g, b]

# 10x10 픽셀 블록으로 이미지 축소
block_size = 10
small_height = height // block_size
small_width = width // block_size
small_grid = np.zeros((small_height, small_width, 3), dtype=np.uint8)

# 각 그리드의 평균 RGB 값 계산
for y in range(small_height):
    for x in range(small_width):
        block = grid[y*block_size:(y+1)*block_size, x*block_size:(x+1)*block_size]
        avg_color = block.reshape(-1, 3).mean(axis=0).astype(np.uint8)
        small_grid[y, x] = avg_color

# 그리드의 평균 RGB 값과 목표 값(255, 255, 255 또는 31, 31, 31) 사이의 거리 계산하여 점수 할당
score_grid = np.zeros((small_height, small_width), dtype=int)

for y in range(small_height):
    for x in range(small_width):
        avg_color = small_grid[y, x]
        dist_white = np.linalg.norm(avg_color - [255, 255, 255])  # 흰색과의 거리
        dist_black = np.linalg.norm(avg_color - [31, 31, 31])  # 검정색과의 거리
        if dist_white < dist_black:
            score_grid[y, x] = 1
        else:
            score_grid[y, x] = -1

# 점수 그리드를 이미지로 변환하여 저장
score_grid_image = Image.fromarray((score_grid + 1) * 127)  # 0~2를 0~255로 매핑
score_grid_image = score_grid_image.convert('L')  # 흑백 이미지로 변환

# 그리드화한 이미지 저장
score_grid_image.save('C:/map/score_grid_naver_gangnam2.png')

# 이미지 크기 출력
print(image.size)
