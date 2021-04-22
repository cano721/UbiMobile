from threading import Thread
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO


class Pir(Thread):
    def __init__(self, client, value):
        super().__init__()
        self.value = ""
        self.client = client

    def run(self):
        while True:
            GPIO.setmode(GPIO.BCM)
            pirPin = 26
            GPIO.setup(pirPin, GPIO.IN)
            time.sleep(0.5)
            if GPIO.input(pirPin) == 1:
                self.value = 'motion detect'
                print("on")
            else:
                self.value = 'off'
                print("off")

            self.client.publish("iot/pir2", self.value)
            # self.client.loop(2)
