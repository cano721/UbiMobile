from flasktest.Motor import Motor
from time import sleep


def MotorAuto(detected, motor, width=640, height=480):
    def inverse_slope(line):
        if line[3] - line[1] < 1:
            result = 999.
        else:
            result = (line[2] - line[0]) / (line[3] - line[1])
        return result

    # detected lines
    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3
    # parameters
    thresh_start_point = 80

    near_detected, near_line = detected[0]
    mid_detected, mid_line = detected[1]

    if near_detected is not NONE:
        inv_slope = inverse_slope(near_line)
        if near_detected == BOTH:
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

        elif near_detected == LEFT:
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

        elif near_detected == RIGHT:
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

    elif mid_detected is not NONE:
        inv_slope = inverse_slope(mid_line)
        if mid_detected == BOTH:
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
                start_point = near_line[2] - (width // 2)
                if start_point < -thresh_start_point:
                    motor.move(speed=40, rightRatio=0.8)
                elif start_point > thresh_start_point:
                    motor.move(speed=40, leftRatio=0.8)
                else:
                    motor.move(speed=40)
        elif mid_detected == LEFT:
            pass
        elif mid_detected == RIGHT:
            pass
        else:
            pass
    else:
        motor.move(speed=-30)
        sleep(2)
