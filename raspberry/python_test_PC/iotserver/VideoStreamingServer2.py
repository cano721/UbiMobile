from flask import Flask, render_template, request, Response
import MyCamera
import RPi.GPIO as GPIO

from MyMqttSub import MyMqtt_Sub

app = Flask(__name__)


def show(camera):
    while True:
        frame = camera.getStreaming()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def hello():
    return "Hello Raspberry Pi IoT Project"


@app.route("/show")
def showVideo():
    return Response(show(MyCamera.MyCamera()), mimetype="multipart/x-mixed-replace;boundary=frame")


@app.route("/<command>")
def action(command):
    if command == "on":

        message = "GPIO" + " ON"
    elif command == "off":
        message = "GPIO" + " ON"
    else:
        message = "Unknown command"

    msg = {
        "message": message,
        "status": True
    }
    return render_template("video.html", **msg)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True, threaded=True)

    except KeyboardInterrupt:
        print("종료")
