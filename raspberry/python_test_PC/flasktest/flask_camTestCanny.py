from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO
import picamera
import cv2
import numpy as np
import time
import io
import threading

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
LED = 20
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)


# Camera 클래스는 비디오 스트리밍 - 하나의 프로세스 안에서 독립적인 실행흐름으로 처리하기 위해 쓰레드로 처리
class Camera:
    thread = None
    frame = None
    img = None
    start_time = 0

    # streaming 이라는 함수 메소드를 쓰레드로 관리하고 화면으로 보내주는 메소드
    def getStreaming(self):
        Camera.start_time = time.time()
        if Camera.thread is None:
            # 백 그라운드의 쓰레드를 시작 - 쓰레드로 작업하기 위해 Thread 클래스를 생성해서 작업
            # ==> 클래스를 만들 때 Thread 클래스를 상속받아 만들 수 있다.
            # streaming 메소드의 실행을 쓰레드로 처리하겠다는 의미
            Camera.thread = threading.Thread(target=self.streaming)
            Camera.thread.start()  # 쓰레드를 시작하겠다는 의미
            while self.frame is None:
                time.sleep(1)
        return self.frame, self.img

    # 독립적인 실행의 한 단위로 파이카메라로 찍은 영상을 프레임단위로 지속적으로 보내주는 역할을 하는 메소드
    @classmethod
    def streaming(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            camera.hflip = True
            camera.vflip = True

            time.sleep(2)  # camera warm-up time

            stream = io.BytesIO()
            for frame in camera.capture_continuous(stream, "jpeg", use_video_port=True):
                stream.seek(0)  # 파일의 맨 처음 위치로 커서를 이동
                cls.frame = stream.read()
                file_bytes = np.asarray(bytearray(cls.frame), dtype=np.uint8)
                cls.img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                stream.seek(0)
                stream.truncate()  # 파일의 내용을 비움


def imageProcess(img):
    # gray scaling
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Canny
    blur = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0.0)
    edges = cv2.Canny(blur, 50, 100)

    # LoG filtering, zero crossing
    # LoG = cv2.filter2D(gray, cv2.CV_32F, kernel=logFilter(15))
    # edges = zeroCrossing2(LoG)

    # Hough
    # lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180.0, threshold=100)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180.0, threshold=100, minLineLength=75, maxLineGap=10)

    if lines is None:
        # print(' no lines')
        pass
    else:
        # print(len(lines))
        for line in lines:
            # rho, theta = line[0]
            # c = np.cos(theta)
            # s = np.sin(theta)
            # x0 = c * rho
            # y0 = s * rho
            # x1 = int(x0 + 1000 * (-s))
            # y1 = int(y0 + 1000 * c)
            # x2 = int(x0 - 1000 * (-s))
            # y2 = int(y0 - 1000 * c)
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # cv2.imshow('origin', ori_img)
    cv2.imshow('frame', img)
    cv2.imshow('Canny', edges)


# 만들어낸 프레임을 전송하는 역할을 하는 메소드
def show(camera):
    while True:
        frame, img = camera.getStreaming()
        imageProcess(camera)
        cv2.waitKey(41)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/show")
def showVideo():
    return Response(show(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/<command>")
def action(command):
    if command == "on":
        GPIO.output(LED, GPIO.HIGH)
        message = "GPIO" + str(LED) + " ON"
    elif command == "off":
        GPIO.output(LED, GPIO.LOW)
        message = "GPIO" + str(LED) + " OFF"
    else:
        message = "Fail"

    msg = {
        "message": message,
        "status": GPIO.input(LED)
    }
    return render_template("video.html", **msg)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port="8088", debug=True, threaded=True)
    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
