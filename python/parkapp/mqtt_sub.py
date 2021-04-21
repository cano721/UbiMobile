from threading import Thread
from django.apps import AppConfig
import paho.mqtt.client as mqtt


class MyMqtt(Thread):
    def __init__(self,client):
        super().__init__()
        self.client = mqtt.Client()

    def run(self):
        self.client.connect("192.168.0.202", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("mydata/park")
        else:
            print("연결실패")

    def on_message(self, client, userdata, msg):
        myval = msg.payload.decode("utf-8")
        data = list[myval.split(",")]
        from parkapp.models import Parking_floor
        # Parking_floor.objects.put(int(data[1]),pf_id=int(data[0]))


class Parksub(AppConfig):
    name = 'parkapp'
    verbose_name = "My App"

    def ready(self):
        client = mqtt.Client()
        mymqtt = MyMqtt(client)
        mymqtt.start()