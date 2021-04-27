import RPi.GPIO as GPIO
import threading
from time import sleep


class Motor(threading.Thread):
    # 모터 채널
    MotorA = 0
    MotorB = 1

    def __init__(self, client):
        super().__init__()

        self.client = client
        self.pinList = None
        self.motorA = None
        self.motorB = None

    def setup(self, ENA=13, IN1=6, IN2=5, ENB=17, IN3=22, IN4=27):
        # 모터 핀 OUTPUT 설정
        self.pinList = [ENA, IN1, IN2, ENB, IN3, IN4]
        for pin in self.pinList:
            GPIO.setup(pin, GPIO.OUT)

        # 모터 제어 파라미터 저장, 70kHz로 PWM 동작
        pwm_freq = 70
        self.motorA = [GPIO.PWM(self.pinList[0], pwm_freq), self.pinList[1], self.pinList[2]]
        self.motorB = [GPIO.PWM(self.pinList[3], pwm_freq), self.pinList[4], self.pinList[5]]
        # PWM 멈춤
        self.motorA[0].start(0)
        self.motorB[0].start(0)

    # 모터 종료
    def cleanup(self):
        for pin in self.pinList:
            GPIO.cleanup(pin)

    # 모터 제어 함수
    def setMotor(self, motorNum, speed):
        # 설정할 모터 가져오기
        if motorNum:  # motorB
            motor = self.motorB
        else:  # motorA
            motor = self.motorA

        # 입력값 제한
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        # 모터 속도 제어 PWM
        motor[0].ChangeDutyCycle(abs(speed))

        # 모터 회전 방향 제어
        if speed == 0:  # 정지
            GPIO.output(motor[1], GPIO.LOW)
            GPIO.output(motor[2], GPIO.LOW)

        elif speed > 0:  # 전진
            GPIO.output(motor[1], GPIO.HIGH)
            GPIO.output(motor[2], GPIO.LOW)

        else:  # 후진
            GPIO.output(motor[1], GPIO.LOW)
            GPIO.output(motor[2], GPIO.HIGH)


    # 정지
    def stop(self):
        self.setMotor(Motor.MotorA, 0)
        self.setMotor(Motor.MotorB, 0)

    # 이동
    def move(self, speed, leftRatio=1.0, rightRatio=1.0):
        print(speed, leftRatio, rightRatio)
        # 입력값 제한
        if abs(speed) < 0.01:
            self.stop()
        else:
            if leftRatio > 1:
                leftRatio = 1.0
            elif leftRatio < -1:
                leftRatio = -1.0
            if rightRatio > 1:
                rightRatio = 1.0
            elif rightRatio < -1:
                rightRatio = -1.0

            self.setMotor(Motor.MotorA, int(speed * leftRatio))
            self.setMotor(Motor.MotorB, int(speed * rightRatio))


# 테스트용 메인 함수
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    myMotor = Motor(None)
    myMotor.setup()

    mSpeed = int(input("input speed: "))
    mRatio = float(input("input curve ratio: "))
    sleepTime = int(input("input sleep time: "))

    sleep(sleepTime)
    myMotor.move(mSpeed)
    print("전진")
    sleep(sleepTime)
    myMotor.move(-mSpeed)
    print("후진")
    sleep(sleepTime)
    myMotor.move(0.0099)

    print("정지")
    sleep(sleepTime)
    myMotor.move(mSpeed, rightRatio=-1)
    print("제자리 좌회전")
    sleep(sleepTime)
    myMotor.move(mSpeed, leftRatio=-1)
    print("제자리 우회전")
    sleep(sleepTime)
    myMotor.move(mSpeed, rightRatio=0)
    print("좌회전 피봇 턴")
    sleep(sleepTime)
    myMotor.move(mSpeed, leftRatio=0)
    print("우회전 피봇 턴")
    sleep(sleepTime)
    myMotor.move(mSpeed, rightRatio=mRatio)
    print("좌회전")
    sleep(sleepTime)
    myMotor.move(mSpeed, leftRatio=mRatio)
    print("우회전")
    sleep(sleepTime)
    myMotor.stop()
    print("정지")

    GPIO.cleanup()
