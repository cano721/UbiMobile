import time
import cv2
import numpy as np
import imageProcess


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 30)

    imageProcess.showTrackbar()

    while True:
        success, ori_img = camera.read()
        if not success:
            break
        else:
            img = cv2.resize(ori_img[:, 160:1120], (640, 480))
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            imageProcess.imageProcess(img)

        k = cv2.waitKey(33) & 0xff
        if k == 27:  # press 'ESC' to quit
            break
        elif k == 64:
            time.sleep(5)
    camera.release()
    cv2.destroyAllWindows()
