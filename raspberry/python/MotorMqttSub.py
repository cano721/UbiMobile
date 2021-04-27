from lib.Motor import Motor
import paho.mqtt.client as mqtt
from json import loads as loadsJson
import RPi.GPIO as GPIO


class MotorMqttSub:
    def __init__(self, hostname, port=1883):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(hostname, port, 60)
        self.motor = Motor.Motor(client)
        self.motor.start()
        self.motor.setup()
        self.manual = True
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("connect..." + str(rc))
        if rc == 0:
            client.subscribe("ubimobile/motor")
        else:
            print("연결실패")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        print(msg.topic + "----" + payload)
        try:
            m_json = loadsJson(payload)
            speed = m_json.get('speed')
            leftRatio = m_json.get('leftRatio')
            rightRatio = m_json.get('rightRatio')
            command = m_json.get('command')

            if speed is not None:
                if self.manual:
                    self.motor.move(speed, leftRatio, rightRatio)
                else:
                    print("Manual activity locked...")
            elif command == 'on':
                self.motor.setup()
                print("Motor on")
            elif command == 'off':
                self.motor.cleanup()
                print("Motor off")
            elif command == 'manual':
                self.manual = True
                print("Manual mode on")
            elif command == 'auto':
                self.manual = False
                print("Manual mode off")
            # data = payload.split(',')
            # if len(data) == 3:
            #     data[0] = int(data[0])
            #     data[1] = float(data[1])
            #     data[2] = float(data[2])
            #     print(data)
            else:
                print("Unknown command")
        except:
            print("Wrong input")


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    myname = "192.168.200.169"
    try:
        motormqtt = MotorMqttSub(myname)

    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
