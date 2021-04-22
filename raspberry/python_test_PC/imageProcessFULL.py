import cv2
import numpy as np


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


def roi(frame, start, roi_width):
    height, width = frame.shape[:2]
    # 왼쪽 아래, 왼쪽 위, 오른쪽 위, 오른쪽 아래
    # start 가로 시작 지점
    # 범위 폭
    start = 100
    roi_width = 200
    roi_height = 140
    # vertices1 = np.array([[(0, height), (start, 0),
    #                        (start + roi_width, 0), (roi_width, height)]], dtype=np.int32)
    # vertices2 = np.array([[(width - roi_width, height), (width - start - roi_width, 0),
    #                        (width - start, 0), (width, height)]], dtype=np.int32)

    # 도로 폭 10cm
    vertices1 = np.array([[(0, roi_height), (start, 0),
                           (start + roi_width, 0), (roi_width, roi_height)]], dtype=np.int32)
    vertices2 = np.array([[(width - roi_width, roi_height), (width - start - roi_width, 0),
                           (width - start, 0), (width, roi_height)]], dtype=np.int32)
    vertices3 = np.array([[(0, height), (0, roi_height),
                           (roi_width, roi_height), (roi_width, height)]], dtype=np.int32)
    vertices4 = np.array([[(width - roi_width, height), (width - roi_width, roi_height),
                           (width, roi_height), (width, height)]], dtype=np.int32)

    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, vertices1, 255)
    cv2.fillPoly(mask, vertices2, 255)
    cv2.fillPoly(mask, vertices3, 255)
    cv2.fillPoly(mask, vertices4, 255)

    masked = cv2.bitwise_and(frame, mask)
    return masked


def imageProcess(img):
    def onMouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("(%d, %d)" % (x, y))
            pixel = np.uint8([[img[y, x]]])
            print("BGR=", end='')
            print(pixel[0][0])
            pixel_hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
            print("HSV=", end='')
            print(pixel_hsv[0][0])

    def sobel(src):
        sobelX = np.array([[0, 1, 2],
                           [-1, 0, 1],
                           [-2, -1, 0]])
        gx = cv2.filter2D(src, cv2.CV_32F, sobelX)
        sobelY = np.array([[-2, -1, 0],
                           [-1, 0, 1],
                           [0, 1, 2]])
        gy = cv2.filter2D(src, cv2.CV_32F, sobelY)
        mag = cv2.magnitude(gx, gy)
        edge_sobel = cv2.normalize(mag, 0, 255, cv2.NORM_MINMAX)
        return edge_sobel

    def logFilter(ksize=7):
        k2 = ksize // 2
        sigma = 0.3 * (k2 - 1) + 0.8
        print('sigma=', sigma)
        LoG = np.zeros((ksize, ksize), dtype=np.float32)
        for y in range(-k2, k2 + 1):
            for x in range(-k2, k2 + 1):
                g = -(x * x + y * y) / (2.0 * sigma ** 2.0)
                LoG[y + k2, x + k2] = -(1.0 + g) * np.exp(g) / (np.pi * sigma ** 4.0)
        return LoG

    def zeroCrossing2(lap, thresh=0.01):
        width, height = lap.shape
        Z = np.zeros(lap.shape, dtype=np.uint8)
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                neighbors = [lap[y - 1, x], lap[y + 1, x], lap[y, x - 1],
                             lap[y, x + 1], lap[y - 1, x - 1], lap[y - 1, x + 1],
                             lap[y + 1, x - 1], lap[y + 1, x + 1]]
                pos = 0
                neg = 0
                for value in neighbors:
                    if value > thresh:
                        pos += 1
                    if value < thresh:
                        neg += 1
                if pos > 0 and neg > 0:
                    Z[y, x] = 255
        return Z

    def drawHough(src, color=(0, 0, 255), thickness=2, drawOne=0):
        # lines = cv2.HoughLines(edgesFrame, rho=1, theta=np.pi / 180.0, threshold=100)
        lines = cv2.HoughLinesP(src, rho=1, theta=np.pi / 180.0, threshold=100, minLineLength=100, maxLineGap=5)

        if lines is not None:
            lineList = []
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
                cv2.line(img, (x1, y1 + height // 2), (x2, y2 + height // 2), color, thickness)
                lineList.append(line[0])
            if drawOne:
                drawLine(src, lineList)
            return lineList

    def drawLine(src, lines, color=(0, 0, 255), thickness=5):
        if lines is None or len(lines) == 0:
            return
        draw_right = True
        draw_left = True

        # Find slopes of all lines
        # But only care about lines where abs(slope) > slope_threshold
        slope_threshold = 0.5
        slopes = []
        new_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]  # line = [[x1, y1, x2, y2]]

            # Calculate slope
            if x2 - x1 == 0.:  # corner case, avoiding division by 0
                slope = 999.  # practically infinite slope
            else:
                slope = (y2 - y1) / (x2 - x1)

            # Filter lines based on slope
            if abs(slope) > slope_threshold:
                slopes.append(slope)
                new_lines.append(line)

        lines = new_lines

        # Split lines into right_lines and left_lines, representing the right and left lane lines
        # Right/left lane lines must have positive/negative slope, and be on the right/left half of the image
        right_lines = []
        left_lines = []
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line[0]
            img_x_center = src.shape[1] / 2  # x coordinate of center of image
            if slopes[i] > 0 and x1 > img_x_center and x2 > img_x_center:
                right_lines.append(line)
            elif slopes[i] < 0 and x1 < img_x_center and x2 < img_x_center:
                left_lines.append(line)

        # Run linear regression to find best fit line for right and left lane lines
        # Right lane lines
        right_lines_x = []
        right_lines_y = []

        for line in right_lines:
            x1, y1, x2, y2 = line[0]

            right_lines_x.append(x1)
            right_lines_x.append(x2)

            right_lines_y.append(y1)
            right_lines_y.append(y2)

        if len(right_lines_x) > 0:
            right_m, right_b = np.polyfit(right_lines_x, right_lines_y, 1)  # y = m*x + b
        else:
            right_m, right_b = 1, 1
            draw_right = False

        # Left lane lines
        left_lines_x = []
        left_lines_y = []

        for line in left_lines:
            x1, y1, x2, y2 = line[0]

            left_lines_x.append(x1)
            left_lines_x.append(x2)

            left_lines_y.append(y1)
            left_lines_y.append(y2)

        if len(left_lines_x) > 0:
            left_m, left_b = np.polyfit(left_lines_x, left_lines_y, 1)  # y = m*x + b
        else:
            left_m, left_b = 1, 1
            draw_left = False

        # Find 2 end points for right and left lines, used for drawing the line
        trap_height = 0.4  # height of the trapezoid expressed as percentage of image height
        # y = m*x + b --> x = (y - b)/m
        y1 = src.shape[0]
        y2 = src.shape[0] * 1

        right_x1 = (y1 - right_b) / right_m
        right_x2 = (y2 - right_b) / right_m

        left_x1 = (y1 - left_b) / left_m
        left_x2 = (y2 - left_b) / left_m

        # Convert calculated end points from float to int
        y1 = int(y1)
        y2 = int(y2)
        right_x1 = int(right_x1)
        right_x2 = int(right_x2)
        left_x1 = int(left_x1)
        left_x2 = int(left_x2)

        # Draw the right and left lines on image
        if draw_right:
            cv2.line(src, (right_x1, y1), (right_x2, y2), color, thickness)
        if draw_left:
            cv2.line(src, (left_x1, y1), (left_x2, y2), color, thickness)

    ##################################################
    # ROI
    height, width = img.shape[:2]
    # print("%d %d" % (width, height))
    img_upper = img[:height // 2, :]
    img_lower = img[height - (height // 2):, :]

    # gray scaling
    gray = cv2.cvtColor(img_lower, cv2.COLOR_BGR2GRAY)

    # histogram equalization
    # gray = cv2.equalizeHist(gray)

    ycrcb = cv2.cvtColor(img_lower, cv2.COLOR_BGR2YCrCb)
    ycrcb = cv2.split(ycrcb)
    ycrcb[0] = cv2.equalizeHist(ycrcb[0])
    ycrcb = cv2.merge(ycrcb)
    equ = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    # Gaussian blur
    gray_blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0.0)
    blur = cv2.GaussianBlur(equ, ksize=(3, 3), sigmaX=0.0)

    # HSV color picker
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    blackL = (0, 0, 0)
    blackU = (150, 255, 60)
    # blackL, blackU = getTrackbar()
    hsvBlack = cv2.inRange(hsv, blackL, blackU)

    # Sobel
    # edges1 = sobel(gray_blur)

    # Canny
    edges = cv2.Canny(gray_blur, 100, 200)

    # LoG filtering, zero crossing
    # LoG = cv2.filter2D(gray, cv2.CV_32F, kernel=logFilter(15))
    # edges = zeroCrossing2(LoG)

    # apply roi in edges frame
    roi_start = 120
    roi_width = 100
    edges_roi = roi(edges, roi_start, roi_width)
    hsvBlack_roi = roi(edges, roi_start, roi_width)

    # Hough
    a = drawHough(hsvBlack, (100, 100, 100), 1, drawOne=0)
    b = drawHough(edges_roi, drawOne=0)
    c = drawHough(hsvBlack_roi, (0, 255, 0), 1, drawOne=0)
    d = drawHough(edges, (255, 0, 0), drawOne=0)

    # cv2.imshow('origin', ori_img)
    cv2.imshow('frame', img)
    cv2.imshow('gray', gray)
    cv2.imshow('equ', equ)
    # cv2.imshow('edges_sobel', edges1)
    cv2.imshow('edges', edges)
    cv2.imshow('edges roi', edges_roi)
    cv2.imshow('HSV Black', hsvBlack)
    cv2.imshow('HSV Black roi', hsvBlack_roi)
    cv2.setMouseCallback('frame', onMouse)

    ret, buffer = cv2.imencode('.jpg', img)
    frame = buffer.tobytes()

    return frame
