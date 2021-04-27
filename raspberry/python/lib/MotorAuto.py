from flasktest.Motor import Motor
from time import sleep

# param values
# NONE = -1
FRONT = 0
STOP = 1
LEFTLINE = 2
RIGHTLINE = 3

# detected lines
d_NONE = 0
d_LEFT = 1
d_RIGHT = 2
d_BOTH = 3
# parameters
thresh_start_point = 80

def MotorAuto(detected, param, motor, width=640, height=480):
    def inverse_slope(line):
        if line[3] - line[1] < 1:
            result = 999.
        else:
            result = (line[2] - line[0]) / (line[3] - line[1])
        return result

    if param == FRONT:
        near_detected, near_line = detected[0]
        mid_detected, mid_line = detected[1]

        if near_detected is not d_NONE:
            inv_slope = inverse_slope(near_line)
            if near_detected == d_BOTH:
                if abs(inv_slope) > 0.7:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0)
                    else:
                        motor.move(speed=40, rightRatio=0)
                elif abs(inv_slope) > 0.4:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0.4)
                    else:
                        motor.move(speed=40, rightRatio=0.4)

                else:
                    start_point = near_line[2] - (width // 2)
                    if start_point < -thresh_start_point:
                        motor.move(speed=40, rightRatio=0.8)
                    elif start_point > thresh_start_point:
                        motor.move(speed=40, leftRatio=0.8)
                    else:
                        motor.move(speed=40)

            elif near_detected == d_LEFT:
                if abs(inv_slope) > 0.7:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0)
                    else:
                        motor.move(speed=40, rightRatio=0)
                elif abs(inv_slope) > 0.4:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0.4)
                    else:
                        motor.move(speed=40, rightRatio=0.4)
                else:
                    motor.move(speed=40, rightRatio=0.85)

            elif near_detected == d_RIGHT:
                if abs(inv_slope) > 0.7:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0)
                    else:
                        motor.move(speed=40, rightRatio=0)
                elif abs(inv_slope) > 0.4:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0.4)
                    else:
                        motor.move(speed=40, rightRatio=0.4)
                else:
                    motor.move(speed=40, rightRatio=0.85)

        elif mid_detected is not d_NONE:
            inv_slope = inverse_slope(mid_line)
            if mid_detected == d_BOTH:
                if abs(inv_slope) > 1:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0)
                    else:
                        motor.move(speed=40, rightRatio=0)
                elif abs(inv_slope) > 0.5:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0.4)
                    else:
                        motor.move(speed=40, rightRatio=0.4)

                else:
                    start_point = mid_line[2] - (width // 2)
                    if start_point < -thresh_start_point:
                        motor.move(speed=40, rightRatio=0.8)
                    elif start_point > thresh_start_point:
                        motor.move(speed=40, leftRatio=0.8)
                    else:
                        motor.move(speed=40)

            elif mid_detected == d_LEFT:
                if abs(inv_slope) > 0.7:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0)
                    else:
                        motor.move(speed=40, rightRatio=0)
                elif abs(inv_slope) > 0.4:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0.4)
                    else:
                        motor.move(speed=40, rightRatio=0.4)
                else:
                    motor.move(speed=40, rightRatio=0.85)

            elif mid_detected == d_RIGHT:
                if abs(inv_slope) > 0.7:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0)
                    else:
                        motor.move(speed=40, rightRatio=0)
                elif abs(inv_slope) > 0.4:
                    if inv_slope < 0:
                        motor.move(speed=40, leftRatio=0.4)
                    else:
                        motor.move(speed=40, rightRatio=0.4)
                else:
                    motor.move(speed=40, rightRatio=0.85)

            else:
                pass

        else:
            motor.move(speed=-30)
            sleep(2)
    elif param == STOP:
        motor.stop()
    elif param == LEFTLINE:
        motor.move(speed=60, leftRatio=0.5)
        sleep(3)
    elif param == RIGHTLINE:
        motor.move(speed=60, rightRatio=0.5)
        sleep(3)

