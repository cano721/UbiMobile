import time
import cv2
import numpy as np
from imageProcess import imageProcess, showTrackbar


videoName = "video427R.h264"
saveName = "save427R.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videocap = None


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
            # if videocap is None:
            #     videocap = cv2.VideoWriter(saveName, fourcc, 20.0, (640, 480))
            # else:
            #     videocap.write(img_show)

        k = cv2.waitKey(33) & 0xff
        if k == 27:  # press 'ESC' to quit
            break
        elif k == 64:
            time.sleep(10)
    # videocap.release()
    video.release()
    cv2.destroyAllWindows()
