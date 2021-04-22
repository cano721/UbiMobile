import time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import WaveSensorTest
import pulsesensorTest

sensors = [
    # Sensor(5, (3, 10), 'iot/user1/temp'),
    # Sensor(7, (20, 60), 'iot/user1/humi'),
    # Sensor(10, (20, 80), 'iot/user1/illu'),
    # Sensor(12, (0, 1), 'iot/user1/dust'),
]
LED = 26
buzzer = 13
servoPin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)

class MyMqtt_Sub():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("172.30.1.56", 1883, 60)
        wave = WaveSensorTest.Wave(client, "")
        self.pulse = pulsesensorTest.PulseSensorTest(client,"")
        wave.start()
        servo.start(0)

        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("mydata/function")
        else:
            print("연결실패")

    def on_message(self, client, userdata, msg):

        myval = msg.payload.decode("utf-8")
        print(myval)
        print(msg.topic + "----" + str(myval))
        if myval == "buzzer_on":
            GPIO.output(buzzer, True)
        elif myval=="buzzer_off":
            GPIO.output(buzzer, False)
        elif myval == "UNLOCK":
            servo.ChangeDutyCycle(7.5)
            time.sleep(0.5)
        elif myval == "LOCK":
            servo.ChangeDutyCycle(2.5)
            time.sleep(0.5)
        elif myval=="pulse_on":
            self.pulse.start()
        elif myval=="pulse_off":
            self.pulse.stop()
        elif myval=="LED_ON":
            GPIO.output(LED, True)
        elif myval == "LED_OFF":
            GPIO.output(LED, False)


if __name__ == "__main__":
    try:
        mymqtt = MyMqtt_Sub()

    except KeyboardInterrupt:
        print("종료")
        servo.stop()
        GPIO.cleanup()