import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

import servo


class MyMqtt_Sub():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("172.30.1.57", 1883, 60)
        servo = GPIO.PWM(12, 50)  # GPIO12번 / 주파수50
        servo.start()
        client.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("mydata/door")
        else:
            print("연결실패")

    def on_message(self,client, userdata, msg):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        myval = msg.payload.decode("utf-8")
        print(myval)
        print(msg.topic + "----" + str(myval))
        if myval == "UNLOCK":
            servo.ChangeDutyCycle(7.5)
        else:
            servo.ChangeDutyCycle(3)

if __name__ == "__main__":
    try:
        mymqtt = MyMqtt_Sub()

    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()



try:
    while True:
        servo.ChangeDutyCycle(3)
        time.sleep(1)

        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()