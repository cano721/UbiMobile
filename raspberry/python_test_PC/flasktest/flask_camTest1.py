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
        img_show, detected, i_param = imageProcess(img)

        if auto:
            frame = img_show

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

