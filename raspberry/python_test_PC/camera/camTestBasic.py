import numpy as np
import cv2

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FPS, 30)

while True:
    success, img = camera.read()
    if not success:
        break
    else:
        resize_img = cv2.resize(img[:, 160:1120].copy(), (640, 480))
        ret, buffer = cv2.imencode('.jpg', resize_img)
        frame = buffer.tobytes()
        # cv2.imshow('origin', img)
        cv2.imshow('frame', resize_img)

    k = cv2.waitKey(33) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
camera.release()
cv2.destroyAllWindows()
