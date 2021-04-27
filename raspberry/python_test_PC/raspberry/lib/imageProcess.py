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


def inverse_slope(line):
    if line[3] - line[1] < 1:
        result = 999.
    else:
        result = (line[2] - line[0]) / (line[3] - line[1])
    return result


def get_roi_square(hsv_src, bin_src, show_src, start_height, end_height):
    def get_points(target_area):
        p1 = None
        p2 = None
        p3 = None
        p4 = None
        check_len = 5
        for i in range(target_area[2] - target_area[0] - check_len):
            if p1 is None:
                if list(bin_src[target_area[1], (target_area[0] + i):(target_area[0] + i + check_len)]).count(0) < 3:
                    p1 = target_area[0] + i
            if p2 is None:
                if list(bin_src[target_area[1], (target_area[2] - i - check_len):(target_area[2] - i)]).count(0) < 3:
                    p2 = target_area[2] - i
            if p3 is None:
                if list(bin_src[target_area[3], (target_area[0] + i):(target_area[0] + i + check_len)]).count(0) < 3:
                    p3 = target_area[0] + i
            if p4 is None:
                if list(bin_src[target_area[3], (target_area[2] - i - check_len):(target_area[2] - i)]).count(0) < 3:
                    p4 = target_area[2] - i
            if p1 is not None and p2 is not None and p3 is not None and p4 is not None:
                return p1, p2, p3, p4
        return None, None, None, None

    ##################################################
    height, width = show_src.shape[:2]
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(hsv_src[start_height:end_height, :])
    min_pixels = 500
    area1 = [0, 0, 0, 0, 0]
    area2 = [0, 0, 0, 0, 0]
    area_left = [0, 0, 0, 0, 0]
    area_right = [0, 0, 0, 0, 0]
    area_one = [0, 0, 0, 0, 0]
    # detected lines
    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3
    thresh_inv_slope = 0.6
    thresh_side_width = 100

    for i in range(1, retval):
        (x, y, w, h, area) = stats[i]

        # select two biggest areas
        if area > min_pixels:
            # adjust width and height
            x = max(1, x - 5)
            w = min(width - x - 1, w + 5)
            if end_height == height:
                h = h - 5
            rectangle = [x, start_height + y, x + w, start_height + y + h, area]
            if area1[4] == 0:
                area1 = rectangle
            elif area2[4] == 0:
                area2 = rectangle
            elif area > area1[4] or area > area2[4]:
                if area1[4] < area2[4]:
                    area1 = rectangle
                else:
                    area2 = rectangle

    if area1[4] and area2[4]:
        if area1[0] < area2[0]:
            area_left = area1
            area_right = area2
        else:
            area_left = area2
            area_right = area1
    elif area1[4]:
        if start_height / height > 0.6:
            if area1[2] < width // 2:
                area_left = area1
            else:
                area_right = area1
        else:
            area_one = area1

    # cv2.rectangle(show_src, (area_left[0], area_left[1]), (area_left[2], area_left[3]), (0, 0, 255))
    # cv2.rectangle(show_src, (area_right[0], area_right[1]), (area_right[2], area_right[3]), (255, 0, 0))
    # if area_one is not None:
    #     cv2.rectangle(show_src, (area_one[0], area_one[1]), (area_one[2], area_one[3]), (255, 0, 255))

    vertices = []
    line = None
    left_line = None
    right_line = None
    detected = NONE
    if area_left[4]:
        # x1, x2, x3, x4 = get_points(area_left)
        x2, x1, x4, x3 = get_points(area_left)
        if x1 is not None:
            vertices1 = np.array([[(x1, area_left[1]), (x2, area_left[1]), (x4, area_left[3]), (x3, area_left[3])]], dtype=np.int32)
            vertices.append(vertices1)

            if x1 < 2 or x3 < 2:
                left_line = [x2, area_left[1], x4, area_left[3]]
            else:
                left_line = [(x1 + x2) // 2, area_left[1], (x3 + x4) // 2, area_left[3]]

            cv2.polylines(show_src, vertices1, True, (255, 0, 255), 1)
            cv2.line(show_src, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (0, 0, 255), 2)

    if area_right[4]:
        w1, w2, w3, w4 = get_points(area_right)
        if w1 is not None:
            vertices2 = np.array([[(w1, area_right[1]), (w2, area_right[1]), (w4, area_right[3]), (w3, area_right[3])]], dtype=np.int32)
            vertices.append(vertices2)

            if w2 > width - 3 or w4 > width - 3:
                right_line = [w1, area_right[1], w3, area_right[3]]
            else:
                right_line = [(w1 + w2) // 2, area_right[1], (w3 + w4) // 2, area_right[3]]

            cv2.polylines(show_src, vertices2, True, (255, 0, 255), 1)
            cv2.line(show_src, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (255, 0, 0), 2)

    # decision line
    if left_line is not None and right_line is not None:
        line = [(left_line[0] + right_line[0]) // 2,
                (left_line[1] + right_line[1]) // 2,
                (left_line[2] + right_line[2]) // 2,
                (left_line[3] + right_line[3]) // 2]
        # line = [width // 2 + (left_line[0] + right_line[0] - left_line[2] - right_line[2]) // 2,
        #         (left_line[1] + right_line[1]) // 2,
        #         width // 2,
        #         (left_line[3] + right_line[3]) // 2]
        detected = BOTH

    elif left_line is not None:
        line = [width // 2 - int((inverse_slope(left_line) + thresh_inv_slope) * (end_height - start_height)),
                start_height,
                width // 2,
                end_height]
        detected = LEFT

    elif right_line is not None:

        line = [width // 2 - int((inverse_slope(right_line) - thresh_inv_slope) * (end_height - start_height)),
                start_height,
                width // 2,
                end_height]
        detected = RIGHT

    if line is not None:
        cv2.line(show_src, (line[2], line[3]), (line[0], line[1]), (0, 255, 255), 2)

    return vertices, [detected, line]


def imageProcess(img):
    NONE = -1
    FRONT = 0
    STOP = 1
    LEFTLINE = 2
    RIGHTLINE = 3
    i_param = NONE

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
    # weighted_img(img, img)

    # gray scaling
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    gray_blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0.0)
    blur = cv2.GaussianBlur(img, ksize=(3, 3), sigmaX=0.0)

    # HSV color
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_Green = (65, 100, 50)
    upper_Green = (80, 255, 255)
    lower_Blue = (95, 75, 30)
    upper_Blue = (120, 255, 255)
    hsvGreen = cv2.inRange(hsv, lower_Green, upper_Green)
    hsvBlue = cv2.inRange(hsv, lower_Blue, upper_Blue)

    # pinkL, pinkU = getTrackbar()
    # hsvPink = cv2.inRange(hsv, pinkL, pinkU)

    # Canny
    edges = cv2.Canny(gray_blur, 50, 100)

    # add hsv and edges binary image
    img_bin = cv2.add(edges, hsvGreen)


    ## ROI
    height, width = img.shape[:2]
    # traffic light ROI
    hsvBlue_roi = roi(hsvBlue, np.array([[(width // 2, 0), (width, 0), (width, int(height * 0.6)),
                                          (width // 2, int(height * 0.6))]], dtype=np.int32))

    # delete small objects
    kernel = np.ones((7, 7), np.uint8)
    hsvBlue_roi = cv2.morphologyEx(hsvBlue_roi, cv2.MORPH_CLOSE, kernel)

    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(hsvBlue_roi)
    min_pixels = 1000
    blue_vertices = []
    for i in range(1, retval):
        (x, y, w, h, area) = stats[i]

        # select two biggest areas
        if area > min_pixels:
            vertices1 = np.array([[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], dtype=np.int32)
            blue_vertices.append(vertices1)
    hsvBlue_roi = roi(hsvBlue_roi, blue_vertices)

    _, contours, hierarchy = cv2.findContours(hsvBlue_roi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    # find traffic light
    lower_GL = (60, 0, 200)
    upper_GL = (100, 100, 255)
    lower_RL = (0, 0, 150)
    upper_RL = (30, 100, 255)
    for i in range(len(contours)):
        approx = cv2.approxPolyDP(contours[i], cv2.arcLength(contours[i], True) * 0.02, True)
        vtc = len(approx)
        if vtc == 4 and hierarchy[0][i][2] != -1:
            inner_cont = hierarchy[0][i][2]
            approx = cv2.approxPolyDP(contours[inner_cont], cv2.arcLength(contours[inner_cont], True) * 0.02, True)
            vtc = len(approx)
            if vtc == 4:
                (c_x, c_y, c_w, c_h) = cv2.boundingRect(contours[inner_cont])
                hsv_TL = hsv[c_y:c_y + c_h, c_x:c_x + c_w]
                hsv_TL_green = cv2.inRange(hsv_TL, lower_GL, upper_GL)
                hsv_TL_red = cv2.inRange(hsv_TL, lower_RL, upper_RL)
                # cv2.imshow('TL_G', hsv_TL_green)
                cv2.imshow('TL_R', hsv_TL_red)
                for i in hsv_TL_red:
                    if list(i).count(255) > 2:
                        i_param = STOP
                        cv2.rectangle(img_show, (c_x, c_y), (c_x + c_w, c_y + c_h), (255, 0, 0), 1)
                        cv2.putText(img_show, 'Light', (c_x, c_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
                        break
                for i in hsv_TL_green:
                    if list(i).count(255) > 5:
                        i_param = FRONT
                        cv2.rectangle(img_show, (c_x, c_y), (c_x + c_w, c_y + c_h), (255, 0, 0), 1)
                        cv2.putText(img_show, 'Light', (c_x, c_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
                        break
                if i_param == NONE:
                    cv2.rectangle(img_show, (c_x, c_y), (c_x + c_w, c_y + c_h), (255, 0, 0), 1)
                    cv2.putText(img_show, 'Light', (c_x, c_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255))

    if i_param == NONE:
        i_param = FRONT

    # line ROI
    near_roi_height = 100
    mid_roi_height = 80
    # far_roi_height = 80
    near_height = height - near_roi_height
    mid_height = height - near_roi_height - mid_roi_height
    # far_height = height - near_roi_height - mid_roi_height - far_roi_height

    # detect line
    near_vertices, near_detected = get_roi_square(hsvGreen, img_bin, img_show, near_height, height)
    mid_vertices, mid_detected = get_roi_square(hsvGreen, img_bin, img_show, mid_height, near_height)
    # far_vertices, far_lines = get_roi_square(hsvGreen, img_bin, img_show, far_height, mid_height)
    roi_bin = roi(img_bin, near_vertices + mid_vertices)

    detected = [near_detected, mid_detected]

    # draw center line
    cv2.line(img_show, (width // 2, height), (width // 2, height // 2), (50, 180, 50), 2)

    # cv2.imshow('origin', ori_img)
    cv2.imshow('frame', img_show)
    cv2.imshow('edges', edges)
    cv2.imshow('HSV green', hsvGreen)
    cv2.imshow('roi_bin', roi_bin)
    cv2.setMouseCallback('frame', onMouse)

    ret, buffer = cv2.imencode('.jpg', img_show)
    frame = buffer.tobytes()

    return frame, detected, i_param
