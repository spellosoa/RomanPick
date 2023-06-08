# import cv2
# from pyzbar import pyzbar
# import time
# from barcode_crawling import *

# async def run_camera():
#     # 카메라 켜기
#     isbn = None
#     cap = cv2.VideoCapture(0)
#     barcode_detected = False # 바코드 인식 확인
#     previous_barcode_data = None # 이전에 인식된 바코드 데이터
#     crawl_data = {}
#     data = {}
#     while True:
#         ret, frame = cap.read()


#         # 바코드 인식
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         barcodes = pyzbar.decode(gray)
#         if barcodes is not None:
#             for barcode in barcodes:    
#                 (x, y, w, h) = barcode.rect
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
#                 # 인식된 ISBN 표시
#                 isbn = barcode.data.decode("utf-8")
                
#                 if isbn != previous_barcode_data:
#                     previous_barcode_data = isbn
#                     crawl_data = await crawling_isbn(isbn)
                
                    
#                 cv2.putText(frame, isbn, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                
#                 if crawl_data['isData']:
#                     barcode_detected = crawl_data['isData']
#                     data = {
#                         "isbn":previous_barcode_data,
#                         "title" :crawl_data['title'],
#                         "textData" : crawl_data['text']
#                     }
#                     time.sleep(5)
#                     break
#                 crawl_data['isData'] = False
#             if barcode_detected:
#                 break

#         # 화면 업데이트
#         cv2.imshow('Camera', frame)

#         # 키 입력 대기
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
            
    
#     # 카메라 종료
#     cap.release()
#     cv2.destroyAllWindows() 
#     return data


