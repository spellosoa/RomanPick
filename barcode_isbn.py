from PIL import Image
from pyzbar.pyzbar import decode
import asyncio

# 바코드 이미지 파일 경로
image_path = 'isbn.jpg'
async def crawling_isbn(isbn):
    # 이미지 열기
    image = Image.open(image_path)

    # 이미지에서 바코드 인식
    barcodes = decode(image)

    # 바코드 정보 출력
    for barcode in barcodes:
        barcode_type = barcode.type
        barcode_data = barcode.data.decode('utf-8')
        if barcode_type == 'EAN13':  # ISBN은 EAN-13 형식으로 인식됩니다.
            isbn = barcode_data
            break

    if 'isbn' in locals():
        print(f"인식된 ISBN: {isbn}")
    else:
        print("ISBN을 찾을 수 없습니다.")
        
        #바코드를 인식할 때 중복 저장을 방지하기 위해 일정 시간 동안 같은 바코드를 인식하지 않도록 제어하는 방법을 구현할 수 있습니다. 이를 위해 코드에 일정한 딜레이를 추가하여 중복 인식을 제어할 수 있습니다. 아래의 코드는 중복 인식 방지를 위해 5초간 동일한 바코드를 인식하지 않도록 하는 예시입니다.

import cv2
from pyzbar import pyzbar
import requests
import time

# 이전에 인식된 바코드 데이터
previous_barcode_data = None
# 중복 인식 제한 시간 (초)
duplicate_timeout = 5

def capture_and_process():
    # 카메라 연결
    cap = cv2.VideoCapture(0)

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 바코드 인식
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            # 바코드 정보 추출
            barcode_data = barcode.data.decode("utf-8")

            # 중복 인식 제어
            if barcode_data != previous_barcode_data or time.time() - previous_timestamp >= duplicate_timeout:
                # 바코드 이미지 저장
                cv2.imwrite("barcode.jpg", frame)

                # 크롤링 및 데이터 처리
                crawl_and_process(barcode_data)

                # 이전 인식된 바코드 데이터와 타임스탬프 업데이트
                previous_barcode_data = barcode_data
                previous_timestamp = time.time()

        # 화면에 프레임 출력
        cv2.imshow("Barcode Scanner", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 카메라 연결 종료
    cap.release()
    cv2.destroyAllWindows()

def crawl_and_process(barcode_data):
    # 크롤링할 웹페이지 URL
    url = "http://example.com"

    # 바코드 데이터를 파라미터로 추가
    params = {"barcode": barcode_data}

    # 요청 보내기
    response = requests.get(url, params=params)

    # 데이터 처리
    # ...

# 메인 함수
if __name__ == '__main__':
    # 카메라 캡처 및 처리 시작
    capture_and_process()

# 위의 코드에서 `previous_barcode_data` 변수는 이전에 인식된 바코드 데이터를 저장하고, `previous_timestamp` 변수는 이전 인식 시간을 저장합니다. 중복 인식을 제어하기 위해 현재 인식된 바코드 데이터와 이전에 저장된 바코드 데이터를 비교하고, 일정 시간(`duplicate_timeout`) 이상 지난 경우에만 새로운 바코드를 저장하고 처리합니다.

# 이렇게 중복 인식을 제어하는 방법을 통해 동일한 바코드가 여러 번 인식되는 것을 방지할 수 있습니다. 필요에 따라 `duplicate_timeout` 값을 조정하여 중복 인식 제한 시간을 변경할 수 있습니다.