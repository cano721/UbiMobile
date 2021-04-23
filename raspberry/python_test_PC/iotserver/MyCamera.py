import io
import threading
import picamera
import time


# 이 클래스에서 비디오도 조절하고 차도 조절하는 별도의 작업을 해야 하기 때문에 쓰레드로 처리해서 작업해야 한다.
# 비디오 처리에 집중하다가 자동차를 처리하는 작업을 늦게 하면 사고가 날 수 있다.
# 다른 작업과 분리하는 개념이 쓰레드다 하나의 프로세스 안에서 독립적인 실행흐름을 갖고자 한다.
class MyCamera:
    thread = None
    frame = None
    start_time = 0

    # streaming이라는 함수를 쓰레드로 관리하고 화면을 보내주는 함수
    def getStreaming(self):
        MyCamera.start_time = time.time()
        if MyCamera.thread is None:
            # 백그라운드의 쓰레드를 시작한다.
            MyCamera.thread = threading.Thread(target=self.streaming)
            MyCamera.thread.start()
            while self.frame is None:
                time.sleep(0)
        return self.frame

    # 독립적인 실행의 한 단위로 파이카메라로 찍은 영상을 프레임단위로 지속적으로 보내주는 역할을 하는 메소드
    @classmethod
    def streaming(c):
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            # 캡쳐한 것을 지속적으로 스트림에 jpeg형식으로 저장
            #  캡춰 실행시 비디오 포트 True 세팅으로 해결
            #  디폴트 값인 이미지 포트(Image port)를 사용하면     동작은 느리지만 고화질 사진을 얻을 수 있음.

            for f in camera.capture_continuous(stream, "jpeg", use_video_port=True):
                # seek 함수는 해당 위치로 파일의 커서를 옮깁니다. 파일의 맨 처음 위치는 0 입니다.
                stream.seek(0)
                c.frame = stream.read()
                # 파일            내용을                비움(
                stream.seek(0)
                stream.truncate()
