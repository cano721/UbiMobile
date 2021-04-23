from threading import Thread
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

buzzer = 19
TRIGER = 24
ECHO = 21


class Wave(Thread):
    def __init__(self, client, value):
        super().__init__()
        self.value = ""

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(TRIGER, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

        self.client = client

    def clarkon(self):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(buzzer, GPIO.LOW)

    def clarkoff(self):
        GPIO.output(buzzer, GPIO.LOW)

    def run(self):
        print("test")
        while True:
            GPIO.output(TRIGER, False)
            time.sleep(1)
            GPIO.output(TRIGER, True)
            time.sleep(0.00001)  # 아주 짧은 시간 이후 초음파 신호를 끈다. 10마이크로초단위로 트리거 신호 송신
            GPIO.output(TRIGER, False)

            # 이제 에코값이 돌아오는 것을 계산한다.
            while GPIO.input(ECHO) == 0:  # 에코핀이 아직 초음파를 받지 못했을떄
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            if distance <= 20:
                self.value = 'warning'
                print("on")
                self.clarkon()
            else:
                self.value = 'safe'
                print("off")
                self.clarkoff()

            self.client.publish("iot/pir2", self.value)
            # self.client.loop(2)
