import cv2
from pyzbar import pyzbar
import time
from barcode_isbn import *

def run_camera():
    # 카메라 켜기
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    barcode_detected = False
    # 이전에 인식된 바코드 데이터
    previous_barcode_data = None
    duplicate_timeout = 5
    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        # 바코드 인식
        barcodes = pyzbar.decode(frame)
        if barcodes is not None:
            for barcode in barcodes:    
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                # 인식된 ISBN 표시
                isbn = barcode.data.decode("utf-8")
                if isbn != previous_barcode_data or time.time() - previous_timestamp >= duplicate_timeout:
                    previous_barcode_data = isbn
                    previous_timestamp = time.time()
                crawling_isbn(isbn)
                cv2.putText(frame, isbn, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                # 바코드가 인식되었음을 표시
                barcode_detected = True

        # 화면 업데이트
        cv2.imshow('Camera', frame)

        # 키 입력 대기
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 카메라 종료
    cap.release()
    cv2.destroyAllWindows()


