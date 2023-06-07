import cv2
from pyzbar.pyzbar import decode
import time
from barcode_crawling import *

def run_camera():
    # 카메라 켜기
    isbn = None
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    barcode_detected = False # 바코드 인식 확인
    previous_barcode_data = None # 이전에 인식된 바코드 데이터
    crawl_data = {}
    data = {}
    duplicate_timeout = 2 # 인식 후 2초 뒤 종료 변수
    while True:
        ret, frame = cap.read()


        # 바코드 인식
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)
        if barcodes is not None:
            for barcode in barcodes:    
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                # 인식된 ISBN 표시
                isbn = barcode.data.decode("utf-8")
                
                if isbn != previous_barcode_data or time.time() - previous_timestamp >= duplicate_timeout:
                    previous_barcode_data = isbn
                    previous_timestamp = time.time()
                    crawl_data = crawling_isbn(isbn)
                
                    
                cv2.putText(frame, isbn, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                # if crawl_data['isData']:
                #     text = crawl_data['title']
                # else:
                #     text = "No matching books found"
                # cv2.putText(frame, text, (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1)

                if crawl_data['isData']:
                    barcode_detected = crawl_data['isData']
                    data = {
                        "isbn":previous_barcode_data,
                        "title" :crawl_data['title'],
                        "textData" : crawl_data['text']
                    }
                    break
                crawl_data['isData'] = False
            if barcode_detected:
                break

        # 화면 업데이트
        cv2.imshow('Camera', frame)

        # 키 입력 대기
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    
    # 카메라 종료
    cap.release()
    cv2.destroyAllWindows() 
    return data


