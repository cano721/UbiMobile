import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)
stream_status = False


@app.route("/")
def index():
    return render_template("index.html")


def gen_frames():
    while True:
        success, frame1 = camera.read()
        frame1 = cv2.flip(cv2.flip(frame1, 0), 1)
        # cv2.imshow('frame', frame1)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame1)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="8088", debug=True)
