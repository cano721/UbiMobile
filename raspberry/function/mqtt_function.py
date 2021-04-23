import time
import spidev
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from threading import Thread
import WaveSensorTest
import pulsesensorTest

sensors = [
    # Sensor(5, (3, 10), 'iot/user1/temp'),
    # Sensor(7, (20, 60), 'iot/user1/humi'),
    # Sensor(10, (20, 80), 'iot/user1/illu'),
    # Sensor(12, (0, 1), 'iot/user1/dust'),
]
LED = 26
buzzer = 19
servoPin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)

class Shocksensor(Thread):
    def __init__(self,client,value):
        super().__init__()
        self.client = client
        self.cond = value
        # 딜레이 시간(센서 측정 간격)
        self.delay = 1
        # MCP3008 채널 중 센서에 연결한 채널 설정
        self.pot_channel = 1
        # SPI 인스턴스 spi 생성
        self.spi = spidev.SpiDev()
        # SPI 통신 시작하기
        self.spi.open(0, 0)
        # SPI 통신 속도 설정
        self.spi.max_speed_hz = 1350000
        # 0 ~7 까지 8개의 채널에서 SPI 데이터 읽기

    def readadc(self,adcnum):
        if adcnum < 0 or adcnum > 7:
            return -1
        r = self.spi.xfer2([1, 8 + adcnum << 4, 0])
        data = ((r[1] & 3) << 8) + r[2]
        return data

    def run(self):
        while True:
            # readadc 함수로 pot_channel의 SPI 데이터를 읽기
            self.pot_value = self.readadc(self.pot_channel)
            if self.pot_value < 20:
                self.value = 'shocked'
                print("shocked!")
                print("POT value: %d" % self.pot_value)
                time.sleep(1)
                self.client.publish("iot/shock", self.value)

            if str(self.cond) in "stop":
                print("run종료")
                break;





class MyMqtt_Sub():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("192.168.0.202", 1883, 60)
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
            self.pulse.data = "stop"
        elif myval=="LED_ON":
            GPIO.output(LED, True)
        elif myval == "LED_OFF":
            GPIO.output(LED, False)
        elif myval=="shock_on":
            self.shock = Shocksensor(client,"basic")
            self.shock.start()
        elif myval=="shock_off":
            self.shock.cond = "stop"
            if self.shock.cond in "stop" :
                print("test")



if __name__ == "__main__":
    try:
        mymqtt = MyMqtt_Sub()

    except KeyboardInterrupt:
        print("종료")
        servo.stop()
        GPIO.cleanup()