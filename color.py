from PIL import Image
import numpy as np

# 이미지 불러오기
image_path = 'C:/map/element_screenshot_7.png'
image = Image.open(image_path)

# 이미지를 RGB 모드로 변환
image = image.convert('RGB')

# 이미지 크기 얻기
width, height = image.size

# 각 픽셀의 RGB 값 추출 및 그리드화
grid = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        r, g, b = image.getpixel((x, y))
        if (r, g, b) == (255, 255, 255) or (r, g, b) == (161, 153, 140):  # 도로 & 화살표
            (r, g, b) = (255, 255, 255)
        elif 235 <= r <= 237 and 235 <= g <= 237 and 235 <= b <= 237:  # 횡단보도
            (r, g, b) = (255, 0, 0)
        elif (r, g, b) == (105, 114, 21) or (r, g, b) == (201, 167, 84) or (r, g, b) == (247, 118, 54) or (r, g, b) == (58, 180, 73) or (r, g, b) == (181, 40, 59):  # 지하철
            (r, g, b) = (0, 0, 255)
        elif (r, g, b) == (248, 211, 154):  # 고가도로
            (r, g, b) = (0, 255, 0)
        else:  # 그외
            (r, g, b) = (31, 31, 31)
        grid[y, x] = [r, g, b]

# 10x10 픽셀 블록으로 이미지 축소
block_size = 10
small_height = height // block_size
small_width = width // block_size
small_grid = np.zeros((small_height, small_width, 3), dtype=np.uint8)

for y in range(small_height):
    for x in range(small_width):
        block = grid[y*block_size:(y+1)*block_size, x*block_size:(x+1)*block_size]
        avg_color = block.reshape(-1, 3).mean(axis=0).astype(np.uint8)
        small_grid[y, x] = avg_color

# # 작은 이미지를 원래 크기로 확대
# large_grid = np.kron(small_grid, np.ones((block_size, block_size, 1), dtype=np.uint8))

# 그리드화한 이미지를 Image 객체로 변환
grid_image = Image.fromarray(small_grid)

# 그리드화한 이미지 저장
grid_image.save('C:/map/dongjunplz.png')

# 이미지 크기 출력
print(image.size)