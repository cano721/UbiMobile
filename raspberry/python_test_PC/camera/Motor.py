import RPi.GPIO as GPIO
import threading
from time import sleep


class Motor(threading.Thread):
    # 모터 채널
    MotorA = 0
    MotorB = 1

    # 모터 상태
    stop = 0
    forward = 1
    backward = 2

    def __init__(self, ENA=13, IN1=6, IN2=5, IN3=22, IN4=27, ENB=17):
        super().__init__()
        # 모터 핀 OUTPUT 설정
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)
        GPIO.setup(ENB, GPIO.OUT)

        # 모터 제어 파라미터 저장, 100kHz로 PWM 동작
        self.motorA = [GPIO.PWM(ENA, 100), IN1, IN2]
        self.motorB = [GPIO.PWM(ENB, 100), IN3, IN4]
        # PWM 멈춤
        self.motorA[0].start(0)
        self.motorB[0].start(0)

    # 모터 제어 함수
    def setMotor(self, motorNum, speed, stat):
        # 설정할 모터 가져오기
        if motorNum:  # motorB
            motor = self.motorB
        else:  # motorA
            motor = self.motorA

        # 모터 속도 제어 PWM
        motor[0].ChangeDutyCycle(speed)

        # 모터 회전 방향 제어
        if stat == Motor.stop:  # 정지
            GPIO.output(motor[1], GPIO.LOW)
            GPIO.output(motor[2], GPIO.LOW)

        elif stat == Motor.forward:  # 전진
            GPIO.output(motor[1], GPIO.HIGH)
            GPIO.output(motor[2], GPIO.LOW)

        elif stat == Motor.backward:  # 후진
            GPIO.output(motor[1], GPIO.LOW)
            GPIO.output(motor[2], GPIO.HIGH)

    # 정지
    def moveStop(self):
        self.setMotor(Motor.MotorA, 0, Motor.stop)
        self.setMotor(Motor.MotorB, 0, Motor.stop)

    # 전진
    def moveFront(self, speed):
        self.setMotor(Motor.MotorA, speed, Motor.forward)
        self.setMotor(Motor.MotorB, speed, Motor.forward)

    # 후진
    def moveBack(self, speed):
        self.setMotor(Motor.MotorA, speed, Motor.backward)
        self.setMotor(Motor.MotorB, speed, Motor.backward)

    # 제자리 좌회전
    def moveLeft(self, speed):
        self.setMotor(Motor.MotorA, speed, Motor.forward)
        self.setMotor(Motor.MotorB, speed, Motor.backward)

    # 제자리 우회전
    def moveRight(self, speed):
        self.setMotor(Motor.MotorA, speed, Motor.backward)
        self.setMotor(Motor.MotorB, speed, Motor.forward)

    # 전진하면서 커브를 그리며 회전
    # ratio는 회전하는 방향쪽 바퀴 속도 비율, 기본값은 0(피봇 턴)
    # 좌회전
    def moveLeftCurve(self, speed, ratio=0.0):
        self.setMotor(Motor.MotorA, speed * ratio, Motor.forward)
        self.setMotor(Motor.MotorB, speed, Motor.forward)

    # 우회전
    def moveRightCurve(self, speed, ratio=0.0):
        self.setMotor(Motor.MotorA, speed, Motor.forward)
        self.setMotor(Motor.MotorB, speed * ratio, Motor.forward)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    myMotor = Motor()

    mSpeed = int(input("input speed: "))
    mRatio = float(input("input curve ratio: "))
    sleepTime = int(input("input sleep time: "))  
    
    sleep(sleepTime)
    myMotor.moveFront(mSpeed)
    print("전진")
    sleep(sleepTime)
    myMotor.moveBack(mSpeed)
    print("후진")
    sleep(sleepTime)
    myMotor.moveLeft(mSpeed)
    print("좌회전")
    sleep(sleepTime)
    myMotor.moveRight(mSpeed)
    print("우회전")
    sleep(sleepTime)
    myMotor.moveLeftCurve(mSpeed)
    print("좌회전 피봇")
    sleep(sleepTime)
    myMotor.moveRightCurve(mSpeed)
    print("우회전 피봇")
    sleep(sleepTime)
    myMotor.moveLeftCurve(mSpeed, mRatio)
    print("좌회전")
    sleep(sleepTime)
    myMotor.moveRightCurve(mSpeed, mRatio)
    print("우회전")
    sleep(sleepTime)
    myMotor.moveStop()
    print("정지")
    
    GPIO.cleanup()
