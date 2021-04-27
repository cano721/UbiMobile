from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import cv2
from lib.Camera import Camera
from lib.imageProcess import imageProcess
from lib.Motor import Motor
from lib.MotorAuto import MotorAuto
# from MotormqttSub import MotormqttSub

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
auto = False

d_NONE = 0
d_LEFT = 1
d_RIGHT = 2
d_BOTH = 3
last_detected = [[d_NONE, None], [d_NONE, None]]
last_param = -1


# 만들어낸 프레임을 전송하는 역할을 하는 메소드
def show(camera):
    global auto, last_detected, last_param
    while True:
        frame, img = camera.getStreaming()
        frame, detected, i_param = imageProcess(img)
        if auto:
            
            if detected[0][0]:
                last_detected[0] = detected[0]
                last_param = i_param

            if detected[1][0]:
                last_detected[1] = detected[1]
                last_param = i_param

            MotorAuto(last_detected, last_param, motor)

        cv2.waitKey(41)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/show")
def showVideo():
    return Response(show(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/<command>")
def action(command):
    global auto
    if command == "on":
        message = "Auto ON"
        auto = True
    elif command == "off":
        message = "Auto OFF"
        motor.stop()
        auto = False
    else:
        message = "Fail"

    msg = {
        "message": message,
    }
    return render_template("video.html", **msg)


if __name__ == "__main__":
    try:
        motor = Motor(None)
        motor.setup()
        app.run(host="0.0.0.0", port="8088", debug=True, threaded=True)
    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()

