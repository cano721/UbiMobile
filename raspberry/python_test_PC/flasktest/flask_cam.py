import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)


def onChange(pos):
    pass


def showTrackbar():
    cv2.namedWindow("Trackbar Windows")
    cv2.createTrackbar("LowH", "Trackbar Windows", 0, 179, onChange)
    cv2.createTrackbar("HighH", "Trackbar Windows", 0, 179, onChange)
    cv2.createTrackbar("LowS", "Trackbar Windows", 0, 255, onChange)
    cv2.createTrackbar("HighS", "Trackbar Windows", 0, 255, onChange)
    cv2.createTrackbar("LowV", "Trackbar Windows", 0, 255, onChange)
    cv2.createTrackbar("HighV", "Trackbar Windows", 0, 255, onChange)


def getTrackbar():
    LowH = cv2.getTrackbarPos("LowH", "Trackbar Windows")
    HighH = cv2.getTrackbarPos("HighH", "Trackbar Windows")
    LowS = cv2.getTrackbarPos("LowS", "Trackbar Windows")
    HighS = cv2.getTrackbarPos("HighS", "Trackbar Windows")
    LowV = cv2.getTrackbarPos("LowV", "Trackbar Windows")
    HighV = cv2.getTrackbarPos("HighV", "Trackbar Windows")

    lowerb = (LowH, LowS, LowV)
    upperb = (HighH, HighS, HighV)
    return lowerb, upperb


@app.route("/")
def index():
    return render_template("index.html")


def gen_frames():
    while True:
        success, ori_img = camera.read()
        if not success:
            break
        else:
            img = cv2.resize(ori_img[:, 160:1120].copy(), (640, 480))
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            img_roi = img[240:480, :]
            ### dst
            hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
            lowerb = (60, 0, 0)
            upperb = (179, 100, 120)
            # lowerb, upperb = getTrackbar()
            dst = cv2.inRange(hsv, lowerb, upperb)

            ### Hough
            # gray scaling
            gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)

            # Canny
            blur = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0.0)
            edges = cv2.Canny(blur, 50, 100)

            # LoG filtering, zero crossing
            # LoG = cv2.filter2D(gray, cv2.CV_32F, kernel=logFilter(15))
            # edges = zeroCrossing2(LoG)

            # Hough
            # lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180.0, threshold=100)
            lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180.0, threshold=90, minLineLength=100, maxLineGap=10)

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
                    cv2.line(img, (x1, y1 + 240), (x2, y2 + 240), (0, 0, 255), 2)

            # cv2.imshow('origin', ori_img)
            cv2.imshow('frame', img)
            cv2.imshow('Canny', edges)
            cv2.imshow('dst', dst)
            cv2.waitKey(33)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 30)

    app.run(host="0.0.0.0", port="8088", debug=True)
