import time
import cv2
import numpy as np
from imageProcess import imageProcess, showTrackbar


videoName = "videoTraff2.h264"


if __name__ == "__main__":
    video = cv2.VideoCapture(videoName)

    showTrackbar()

    while True:
        success, img = video.read()
        if not success:
            video = cv2.VideoCapture(videoName)
            continue
        else:
            img = cv2.resize(img, (640, 480))
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            img_show, detected, i_param = imageProcess(img)

        k = cv2.waitKey(33) & 0xff
        if k == 27:  # press 'ESC' to quit
            break
        elif k == 64:
            time.sleep(10)
    video.release()
    cv2.destroyAllWindows()
