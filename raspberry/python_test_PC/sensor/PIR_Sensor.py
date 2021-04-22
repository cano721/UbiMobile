import RPi.GPIO as GPIO

import time
GPIO.setmode(GPIO.BCM)

pirPin = 26
GPIO.setup(pirPin, GPIO.IN)


while True:
    if GPIO.input(pirPin) == 1:
        print("Motion detected!")
    else:
        print("No motion")
    time.sleep(1000)