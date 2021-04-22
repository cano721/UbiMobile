import paho.mqtt.client as mqtt

"""
on_connect는 subscriber가 브로커에 연결하면서 호출할 함수
rc가 0이면 정상접속이 됐다는 의미
"""


def on_connect(client, userdata, flags, rc):
    print("connect.." + str(rc))
    if rc == 0:
        client.subscribe("mydata/led")
    else:
        print("연결실패")


def on_message(client, userdata, msg):
    myval = msg.payload.decode("utf-8")
    print(msg.topic + " " + str(myval))


mqttClient = mqtt.Client()
# 브로커에 연결이 되면 내가 정의해놓은 on_connect함수가 실행되도록 등록
mqttClient.on_connect = on_connect
# 브로커에서 메시지가 전달되면 내가 등록해 놓은 on_message함수가 실행
mqttClient.on_message = on_message
# 브로커에 연결하기
mqttClient.connect("192.168.200.198", 1883, 60)
# 토픽이 전달될 때 까지 수신대기
mqttClient.loop_forever()
