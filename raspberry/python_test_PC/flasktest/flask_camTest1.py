from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO
import picamera
import cv2
import numpy as np
import io
import threading
from time import sleep
from Camera import Camera
from imageProcess import imageProcess
from Motor import Motor
# from MotormqttSub import MotormqttSub
from collections import deque

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
auto = False
myname = "192.168.200.183"
# mqttSub = MotormqttSub(myname)

MAX_DECISION_LENGTH = 30
decisions = deque([])
FRONT = 0
LEFT = 1
RIGHT = 2
STOP = 3


# 만들어낸 프레임을 전송하는 역할을 하는 메소드
def show(camera):
    global auto
    while True:
        frame, img = camera.getStreaming()
        img_show, decision = imageProcess(img)

        if auto:
            frame = img_show
            # mqttSub.manual = False

            if decision is not None:
                speed = 30
                if decision[2] > 5:
                    ratio = 0.8
                elif decision[2] > 3:
                    ratio = 0.5
                else:
                    ratio = 0
                if decision[0]:
                    print("Left %d" % decision[2])
                    # mqttSub.motor.move(speed, leftRatio=ratio)
                    motor.move(speed, leftRatio=ratio)
                    decisions.append(LEFT)
                elif decision[1]:
                    print("Right %d" % decision[2])
                    # mqttSub.motor.move(speed, rightRatio=ratio)
                    motor.move(speed, rightRatio=ratio)
                    decisions.append(RIGHT)
                else:
                    # mqttSub.motor.move(70)
                    motor.move(50)
                    decisions.append(FRONT)
                if len(decisions) > MAX_DECISION_LENGTH:
                    decisions.popleft()
            else:
                if len(decisions) == 0:
                    # mqttSub.motor.move(0)
                    motor.move(0)
                    decisions.append(STOP)
                else:
                    decision = decisions.popleft()
                    if decision == FRONT:
                        # mqttSub.motor.move(50)
                        motor.move(40)
                    elif decision == LEFT:
                        # mqttSub.motor.move(40, leftRatio=0)
                        motor.move(30, leftRatio=0)
                    elif decision == RIGHT:
                        # mqttSub.motor.move(40, RightRatio=0)
                        motor.move(30, rightRatio=0)
                    else:
                        # mqttSub.motor.move(0)
                        motor.move(0)

        else:
            # mqttSub.manual = True
            pass

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

