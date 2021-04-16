import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

servo = GPIO.PWM(12,50) #GPIO12번 / 주파수50
servo.start(0)

try:
    while True:
        servo.ChangeDutyCycle(3)
        time.sleep(1)

        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()