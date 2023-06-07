from fastapi import FastAPI, WebSocket
import cv2
from pyzbar import pyzbar
import time

app = FastAPI()

# 카메라 연결 및 바코드 인식 함수
async def run_camera(websocket: WebSocket):
    await websocket.accept()

    # 카메라 켜기
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    try:
        while True:
            ret, frame = cap.read()

            # 바코드 인식
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # 인식된 ISBN 표시
                isbn = barcode.data.decode("utf-8")
                cv2.putText(frame, isbn, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # 화면 업데이트
            _, jpeg = cv2.imencode('.jpg', frame)
            await websocket.send_bytes(jpeg.tobytes())

            # 5초 대기 후 종료
            if time.time() - start_time > 5:
                break
    finally:
        # 카메라 종료
        cap.release()


