from cv2 import VideoCapture, resize, imencode
from cv2 import CAP_PROP_FRAME_WIDTH
from cv2 import CAP_PROP_FRAME_HEIGHT
from cv2 import CAP_PROP_FPS
import threading
import time


# Camera 클래스는 비디오 스트리밍 - 하나의 프로세스 안에서 독립적인 실행흐름으로 처리하기 위해 쓰레드로 처리
class Camera:
    thread = None
    frame = None
    img = None
    start_time = 0

    def getStreaming(self):
        Camera.start_time = time.time()
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self.streaming)
            Camera.thread.start()
            while self.frame is None:
                time.sleep(1)
        return self.frame, self.img

    @classmethod
    def streaming(cls):
        with VideoCapture(0) as camera:
            camera.set(CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(CAP_PROP_FRAME_HEIGHT, 720)
            camera.set(CAP_PROP_FPS, 30)

            time.sleep(2)  # camera warm-up time

            success, cls.img = camera.read()
            cls.img = resize(cls.img[:, 160:1120].copy(), (640, 480))
            ret, buffer = imencode('.jpg', cls.img)
            cls.frame = buffer.tobytes()


            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            cv2.imshow('frame', img)