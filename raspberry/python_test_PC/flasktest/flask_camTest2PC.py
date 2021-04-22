from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import time
import io
import threading

app = Flask(__name__)


class Camera:
    thread = None
    img = None
    start_time = 0

    def getStreaming(self):
        Camera.start_time = time.time()
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self.streaming)
            Camera.thread.start()
            while self.img is None:
                time.sleep(1)
        return self.img

    @classmethod
    def streaming(c):
        camera = cv2.VideoCapture(0)
        camera.set(3, 640)
        camera.set(4, 480)

        time.sleep(2)  # camera warm-up time

        success, c.img = camera.read()


# 만들어낸 프레임을 전송하는 역할을 하는 메소드
def show(camera):
    while True:
        img = camera.getStreaming()

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        cv2.imshow('frame', img)
        cv2.waitKey(30)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/show")
def showVideo():
    return Response(show(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/<command>")
def action(command):
    if command == "on":
        message = "GPIO" + " ON"
    elif command == "off":
        message = "GPIO" + " OFF"
    else:
        message = "Fail"

    msg = {
        "message": message
    }
    return render_template("video.html", **msg)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port="8088", debug=True, threaded=True)
    except KeyboardInterrupt:
        print("종료")
        cv2.destroyAllWindows()
