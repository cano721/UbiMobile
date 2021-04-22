import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED = 20

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
try:
    while 1:
        GPIO.output(LED, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
