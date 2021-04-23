from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO
import time
import io
import threading
import cv2
import numpy as np
import picamera
import CameraRasp as Camera
import imageProcess as imgP


app = Flask(__name__)
GPIO.setmode(GPIO.BCM)


# 만들어낸 프레임을 전송하는 역할을 하는 메소드
def show(camera):
    while True:
        frame, img = camera.getStreaming()

        if auto:
            imgP.imageProcess(img)

        cv2.waitKey(41)  # Rasp
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/show")
def showVideo():
    return Response(show(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/<command>")
def action(command):
    global auto
    if command == "on":
        message = "Auto drive ON"
        auto = True
    elif command == "off":
        message = "Auto drive OFF"
        auto = False
    else:
        message = "Fail"
        auto = False

    msg = {
        "message": message,
        "status": auto
    }
    return render_template("video.html", **msg)


if __name__ == "__main__":
    try:
        auto = False
        app.run(host="0.0.0.0", port="8088", debug=True, threaded=True)
    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
