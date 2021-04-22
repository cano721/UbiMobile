import time
import cv2
import numpy as np
from imageProcess import imageProcess, showTrackbar


if __name__ == "__main__":
    video = cv2.VideoCapture("video.h264")

    showTrackbar()

    while True:
        success, img = video.read()
        if not success:
            video = cv2.VideoCapture("video.h264")
            continue
        else:
            img = cv2.resize(img, (640, 480))
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            img_show, decision = imageProcess(img)
            if decision is not None:
                if decision[0]:
                    print("Left %d" % decision[2])
                if decision[1]:
                    print("Right %d" % decision[2])

        k = cv2.waitKey(33) & 0xff
        if k == 27:  # press 'ESC' to quit
            break
        elif k == 64:
            time.sleep(10)
    video.release()
    cv2.destroyAllWindows()
