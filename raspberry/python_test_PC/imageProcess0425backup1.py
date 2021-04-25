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
        channel_count = image.shape[2]
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


def get_roi_square(hsv_src, bin_src, show_src, start_height, end_height):
    height, width = show_src.shape[:2]
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(hsv_src[start_height:end_height, :])
    min_pixels = 300
    max_line_width = 50
    area1 = [0, 0, 0, 0, 0]
    area2 = [0, 0, 0, 0, 0]

    for i in range(1, retval):
        (x, y, w, h, area) = stats[i]
        if end_height == height:
            h = h - 5
        if area > min_pixels:
            if area1[4] == 0:
                area1 = [x, start_height + y, x + w - 1, start_height + y + h, area]
            elif area2[4] == 0:
                area2 = [x, start_height + y, x + w - 1, start_height + y + h, area]
            elif area > area1[4] or area > area2[4]:
                if area1[4] < area2[4]:
                    area1 = [x, start_height + y, x + w - 1, start_height + y + h, area]
                else:
                    area2 = [x, start_height + y, x + w - 1, start_height + y + h, area]

    # cv2.rectangle(show_src, (area1[0], area1[1]), (area1[2], area1[3]), (0, 255, 255))
    # cv2.rectangle(show_src, (area2[0], area2[1]), (area2[2], area2[3]), (0, 255, 255))

    vertices = []
    if area1[4] > 0:
        # vertices1 = np.array([[(area1[0], area1[1]), (area1[2], area1[1]), (area1[2], area1[3]), (area1[0], area1[3])]], dtype=np.int32)
        x1 = min(area1[0], area1[2])
        y1 = max(area1[1], area1[3])
        x2 = max(area1[0], area1[2])
        y2 = min(area1[1], area1[3])
        vertices1 = np.array([[(x1, y1), (), (), ()]], dtype=np.int32)
        vertices.append(vertices1)
    if area2[4] > 0:
        # vertices2 = np.array([[(area2[0], area2[1]), (area2[2], area2[1]), (area2[2], area2[3]), (area2[0], area2[3])]], dtype=np.int32)

        vertices2 = np.array([[(area2[0], area2[1]), (area2[0] + max_line_width, area2[1]), (area2[2], area2[3]), (area2[2] - max_line_width, area2[3])]], dtype=np.int32)
        vertices.append(vertices2)
    return vertices


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
        lines = cv2.HoughLinesP(src, rho=2, theta=np.pi / 180.0, threshold=50, minLineLength=20, maxLineGap=10)
        return lines

    ##################################################
    img_show = img.copy()
    weighted_img(img, img)

    # gray scaling
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    gray_blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0.0)
    blur = cv2.GaussianBlur(img, ksize=(3, 3), sigmaX=0.0)

    # HSV color
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_Green = (65, 100, 50)
    upper_Green = (80, 255, 200)
    hsvGreen = cv2.inRange(hsv, lower_Green, upper_Green)

    pinkL, pinkU = getTrackbar()
    # hsvPink = cv2.inRange(hsv, pinkL, pinkU)

    # Canny
    edges = cv2.Canny(gray_blur, 50, 100)
    edges_hsvG = cv2.Canny(hsvGreen, 100, 200)

    # add hsv and edges binary image
    img_bin = cv2.add(edges, hsvGreen)

    # ROI
    height, width = img.shape[:2]
    near_roi_height = 80
    mid_roi_height = 80
    far_roi_height = 80
    near_height = height - near_roi_height
    mid_height = height - near_roi_height - mid_roi_height
    far_height = height - near_roi_height - mid_roi_height - far_roi_height

    near_vertices = get_roi_square(hsvGreen, img_bin, img_show, near_height, height)
    roi_near = roi(img_bin, near_vertices)
    mid_vertices = get_roi_square(hsvGreen, img_bin, img_show, mid_height, near_height)
    roi_mid = roi(img_bin, mid_vertices)
    far_vertices = get_roi_square(hsvGreen, img_bin, img_show, far_height, mid_height)
    roi_far = roi(img_bin, far_vertices)
    cv2.polylines(img_show, near_vertices, True, (255, 0, 255), 1)
    cv2.polylines(img_show, mid_vertices, True, (255, 0, 255), 1)
    cv2.polylines(img_show, far_vertices, True, (255, 0, 255), 1)
    # cv2.imshow('roi', cv2.add(roi_near, roi_mid))
    # cv2.imshow('roi', cv2.add(cv2.add(roi_near, roi_mid), roi_far))

    # apply roi in edges frame
    # edges_roi = roi(edges, (vertices1, vertices2))
    # edges_hsvG_roi = roi(edges_hsvG, (vertices1, vertices2))
    # edges_hsvC_roi = roi(edges_hsvC, (vertices1, vertices2))

    # Hough
    # lines_edgesRoi = hough(edges_roi)
    # lines_edgesO_Roi = hough(edges_hsvG_roi)
    # lines_edgesC_Roi = hough(edges_hsvC_roi)
    # lines_hsvG_Roi = hough(hsvG_roi)

    # 직선 / 곡선 감지
    # ROI 표시
    # vertices1_full = np.array([[(bot_start, height), (top_start, height - roi_height),
    #                             (top_start + top_width, height - roi_height), (bot_start + bot_width, height)]], dtype=np.int32)
    # vertices2_full = np.array([[(width - bot_start - bot_width, height), (width - top_start - top_width, height - roi_height),
    #                             (width - top_start, height - roi_height), (width - bot_start, height)]], dtype=np.int32)
    # cv2.polylines(img_show, vertices1_full, True, (255, 0, 255), 1)
    # cv2.polylines(img_show, vertices2_full, True, (255, 0, 255), 1)

    # drawLines(img_show, lines_edgesRoi, (255, 100, 100))
    # drawLines(img_show, lines_edgesO_Roi)
    # drawLines(img_show, lines_edgesC_Roi, (180, 0, 180))
    # try:
    #     slope = drawOneLine(img_show, lines_hsvG_Roi)
    # except:
    #     slope = None
    #
    # if slope is None:
    #     lines_edges = hough(edges)
    #     lines_hsvG = hough(hsvGreen)
    #     drawLines(img_show, lines_edges, (255, 100, 255))
    #     drawLines(img_show, lines_hsvG, (255, 0, 0), 1)
    #     try:
    #         slope = drawOneLine(img_show, lines_hsvG)
    #     except:
    #         slope = None
    #
    # # decision
    # decision = None
    # if slope is not None:
    #     if abs(slope) < 10:
    #         decision_left = slope > 0
    #         decision_right = slope < 0
    #         decision = [decision_left, decision_right, abs(slope)]

    # draw center line
    cv2.line(img_show, (width // 2, height), (width // 2, height // 2), (180, 50, 50), 3)

    # cv2.imshow('origin', ori_img)
    cv2.imshow('frame', img_show)
    # cv2.imshow('blur', blur)
    cv2.imshow('edges', edges)
    cv2.imshow('HSV green', hsvGreen)
    # cv2.imshow('edges roi', edges_roi)
    # cv2.imshow('edges HSV green', edges_hsvG)
    # cv2.imshow('edges HSV Green roi', edges_hsvG_roi)
    # cv2.imshow('edges HSV center line', edges_hsvC)
    # cv2.imshow('edges HSV center roi', edges_hsvC_roi)
    # cv2.imshow('HSV Pink', hsvPink)
    cv2.setMouseCallback('frame', onMouse)

    ret, buffer = cv2.imencode('.jpg', img_show)
    frame = buffer.tobytes()

    return frame  #, decision
