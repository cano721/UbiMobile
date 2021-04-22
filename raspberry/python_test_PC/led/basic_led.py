import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED = 21

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(LED, GPIO.HIGH)
