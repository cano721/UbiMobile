import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

import servo

servo = GPIO.PWM(12, 50)  # GPIO12번 / 주파수50

class MyMqtt_Sub():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("172.30.1.57", 1883, 60)
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
        servo.stop()
        GPIO.cleanup()
