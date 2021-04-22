import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
LED = 20


def led_control(value):
    if value == "led_on":
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)


def on_connect(client, userdata, flags, rc):
    print("connect.." + str(rc))
    if rc == 0:
        client.subscribe("mydata/led")
    else:
        print("연결실패")


def on_message(client, userdata, msg):
    myval = msg.payload.decode("utf-8")
    print(msg.topic + " " + str(myval))
    led_control(str(myval))


GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
try:
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect("192.168.200.198", 1883, 60)
    mqttClient.loop_forever()
except KeyboardInterrupt:
    pass

GPIO.cleanup()
