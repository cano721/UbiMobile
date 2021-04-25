import cv2
import numpy as np


def showTrackbar():
    def onChange(pos):
        pass
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


def weighted_img(img, initial_img, alpha=0.8, beta=1.0, gamma=0.0):
    return cv2.addWeighted(initial_img, alpha, img, beta, gamma)


def roi(image, vertices):
    mask = np.zeros_like(image)

    if len(image.shape) > 2:
        channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    if len(vertices) == 1:
        cv2.fillPoly(mask, vertices, ignore_mask_color)
    else:
        for arg in vertices:
            cv2.fillPoly(mask, arg, ignore_mask_color)

    masked = cv2.bitwise_and(image, mask)
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
            cv2.setTrackbarPos("LowH", "Trackbar Windows", pixel_hsv[0][0][0] - 25)
            cv2.setTrackbarPos("HighH", "Trackbar Windows", pixel_hsv[0][0][0] + 25)
            cv2.setTrackbarPos("LowS", "Trackbar Windows", pixel_hsv[0][0][1] - 35)
            cv2.setTrackbarPos("HighS", "Trackbar Windows", pixel_hsv[0][0][1] + 35)
            cv2.setTrackbarPos("LowV", "Trackbar Windows", pixel_hsv[0][0][2] - 40)
            cv2.setTrackbarPos("HighV", "Trackbar Windows", pixel_hsv[0][0][2] + 40)

    def hough(src):
        lines = cv2.HoughLinesP(src, rho=2, theta=np.pi / 180.0, threshold=50, minLineLength=50, maxLineGap=20)
        return lines

    def drawLines(src, lines, color=(0, 0, 255), thickness=2):
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(src, (x1, y1 + height // 2), (x2, y2 + height // 2), color, thickness)

    def drawOneLine(src, lines, color=(0, 0, 255), thickness=5):
        if lines is None or len(lines) == 0:
            return
        draw_right = True
        draw_left = True

        # Find slopes of all lines
        # But only care about lines where abs(slope) > slope_threshold
        slope_threshold = 0.1
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
            img_x_center = src.shape[1] // 2  # x coordinate of center of image
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

            right_lines_y.append(y1 + height // 2)
            right_lines_y.append(y2 + height // 2)

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

            left_lines_y.append(y1 + height // 2)
            left_lines_y.append(y2 + height // 2)

        if len(left_lines_x) > 0:
            left_m, left_b = np.polyfit(left_lines_x, left_lines_y, 1)  # y = m*x + b
        else:
            left_m, left_b = 1, 1
            draw_left = False

        # Find 2 end points for right and left lines, used for drawing the line
        # y = m*x + b --> x = (y - b)/m
        y1 = height
        y2 = height // 2

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
        if draw_right and draw_left:
            center_x1 = (right_x1 + left_x1) // 2
            center_x2 = (right_x2 + left_x2) // 2
            cv2.line(src, (center_x1, y1), (center_x2, y2), (0, 255, 0), 3)
            if center_x2 - center_x1 == 0.:
                slope = 999.
            else:
                slope = (y2 - y1) / (center_x2 - center_x1)
            return slope

    ##################################################
    weighted_img(img, img)
    img_show = img.copy()
    # ROI
    height, width = img.shape[:2]
    img_upper = img[:height // 2, :]
    img_lower = img[height - (height // 2):, :]

    top_start = 200
    top_width = 120
    bot_start = 40
    bot_width = 200

    vertices1 = np.array([[(bot_start, height), (top_start, 0),
                           (top_start + top_width, 0), (bot_start + bot_width, height)]], dtype=np.int32)
    vertices2 = np.array([[(width - bot_start - bot_width, height), (width - top_start - top_width, 0),
                           (width - top_start, 0), (width - bot_start, height)]], dtype=np.int32)

    # gray scaling
    gray = cv2.cvtColor(img_lower, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    gray_blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0.0)
    blur = cv2.GaussianBlur(img_lower, ksize=(3, 3), sigmaX=0.0)

    # HSV color picker
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_Oran = (0, 40, 40)
    upper_Oran = (25, 255, 255)
    hsvOran = cv2.inRange(hsv, lower_Oran, upper_Oran)
    hsvO_roi = roi(hsvOran, (vertices1, vertices2))

    # pinkL, pinkU = getTrackbar()
    # hsvPink = cv2.inRange(hsv, pinkL, pinkU)

    # diff = [30, 30, 40]
    # pixel = hsv[int(height // 2 * 0.95), width // 2]
    # centerL = pixel - diff
    # centerH = pixel + diff
    # hsvCenter = 255 - cv2.inRange(hsv, centerL, centerH)

    # Canny
    edges = cv2.Canny(gray_blur, 50, 100)
    edges_hsvO = cv2.Canny(hsvOran, 100, 200)
    # edges_hsvC = cv2.Canny(hsvCenter, 100, 200)

    # apply roi in edges frame
    # edges_roi = roi(edges, (vertices1, vertices2))
    # edges_hsvO_roi = roi(edges_hsvO, (vertices1, vertices2))
    # edges_hsvC_roi = roi(edges_hsvC, (vertices1, vertices2))

    # Hough
    # lines_edgesRoi = hough(edges_roi)
    # lines_edgesO_Roi = hough(edges_hsvO_roi)
    # lines_edgesC_Roi = hough(edges_hsvC_roi)
    lines_hsvO_Roi = hough(hsvO_roi)

    # 직선 / 곡선 감지
    # ROI 표시
    vertices1_full = np.array([[(bot_start, height), (top_start, height // 2),
                           (top_start + top_width, height // 2), (bot_start + bot_width, height)]], dtype=np.int32)
    vertices2_full = np.array([[(width - bot_start - bot_width, height), (width - top_start - top_width, height // 2),
                           (width - top_start, height // 2), (width - bot_start, height)]], dtype=np.int32)
    cv2.polylines(img_show, vertices1_full, True, (255, 0, 255), 1)
    cv2.polylines(img_show, vertices2_full, True, (255, 0, 255), 1)

    # drawLines(img_show, lines_edgesRoi, (255, 100, 100))
    # drawLines(img_show, lines_edgesO_Roi)
    # drawLines(img_show, lines_edgesC_Roi, (180, 0, 180))
    try:
        slope = drawOneLine(img_show, lines_hsvO_Roi)
    except:
        slope = None

    if slope is None:
        # lines_edges = hough(edges)
        lines_hsvO = hough(hsvOran)
        # drawLines(img_show, lines_edgesRoi, (255, 100, 255))
        # drawLines(img_show, lines_hsvO_Roi, (255, 0, 0), 1)
        try:
            slope = drawOneLine(img_show, lines_hsvO)
        except:
            slope = None

    # decision
    decision = None
    if slope is not None:
        if abs(slope) < 10:
            decision_left = slope > 0
            decision_right = slope < 0
            decision = [decision_left, decision_right, abs(slope)]

    # draw center line
    cv2.line(img_show, (width // 2, height), (width // 2, height // 2), (180, 50, 50), 3)

    # cv2.imshow('origin', ori_img)
    cv2.imshow('frame', img_show)
    cv2.imshow('blur', blur)
    cv2.imshow('edges', edges)
    # cv2.imshow('edges roi', edges_roi)
    cv2.imshow('edges HSV Oran', edges_hsvO)
    # cv2.imshow('edges HSV Oran roi', edges_hsvO_roi)
    # cv2.imshow('edges HSV center line', edges_hsvC)
    # cv2.imshow('edges HSV center roi', edges_hsvC_roi)
    # cv2.imshow('HSV Pink', hsvPink)
    # cv2.setMouseCallback('frame', onMouse)

    ret, buffer = cv2.imencode('.jpg', img_show)
    frame = buffer.tobytes()

    return frame, decision
