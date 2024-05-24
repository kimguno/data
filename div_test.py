import requests

def get_map_image(lat, lng, zoom=18, width=900, height=900):
    # 네이버 API 호출을 위한 인증 키
    client_id = '8czde6gect'
    client_secret = 'Ud4bmqKsa2MOxkkLCHFc3ETe7MmJYBELPBqDUET4'
    
    # 네이버 지도 API 호출 URL
    url = f'https://naveropenapi.apigw.ntruss.com/map-static/v2/raster?w={width}&h={height}&center={lng},{lat}&level={zoom}&maptype=default'
    
    # API 호출
    headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret}
    response = requests.get(url, headers=headers)
    
    # 호출 결과 확인
    if response.status_code == 200:
        # 이미지 저장
        with open('map_image.png', 'wb') as f:
            f.write(response.content)
        print("지도 이미지를 성공적으로 다운로드했습니다.")
    else:
        print("지도 이미지를 다운로드하는 중 오류가 발생했습니다.")

def get_bounding_coordinates(lat, lng):
    # 동서남북 끝 좌표를 계산
    # 여기서는 임의의 값으로 계산하는 예제를 들었지만, 실제로는 좌표계 변환이 필요할 수 있습니다.
    north = lat + 0.01
    south = lat - 0.01
    east = lng + 0.01
    west = lng - 0.01
    return north, south, east, west

# 사용자가 찾고자 하는 좌표
desired_lat = 37.5665
desired_lng = 126.9780

# 지도 이미지 가져오기
get_map_image(desired_lat, desired_lng)

# 동서남북 끝 좌표 계산
north, south, east, west = get_bounding_coordinates(desired_lat, desired_lng)
print("North:", north)
print("South:", south)
print("East:", east)
print("West:", west)
