from threading import Thread

import spidev
import time
import paho.mqtt.client as mqtt


# 딜레이 시간(센서 측정 간격)
delay = 1
# MCP3008 채널 중 센서에 연결한 채널 설정
pot_channel = 0
pot_channel2 = 1
# SPI 인스턴스 spi 생성
spi = spidev.SpiDev()
# SPI 통신 시작하기
spi.open(0, 0)
# SPI 통신 속도 설정
spi.max_speed_hz = 1350000
# 0 ~7 까지 8개의 채널에서 SPI 데이터 읽기
class Pressure(Thread):
    def __init__(self,client):
        super(Pressure, self).__init__()
        self.client = client
        self.client.connect("192.168.0.202", 1883, 60)

    def readadc(self,adcnum):
        if adcnum < 0 or adcnum > 7:
            return -1
        r = spi.xfer2([1, 8+adcnum <<4, 0])
        data = ((r[1] & 3) << 8) + r[2]
        return data

    def run(self):
        parking = 0
        parking2 = 0
        while True:
            pot_value = self.readadc(pot_channel)
            pot_value2 = self.readadc(pot_channel2)
            if parking ==1:
                if pot_value < 10:
                    self.client.publish("mydata/park", "park,1,0")
                    parking = 0
            else:
                if pot_value > 100:
                    self.client.publish("mydata/park", "park,1,1")
                    parking = 1

            if parking2 ==1:
                if pot_value2 < 10:
                    self.client.publish("mydata/park", "park,2,0")
                    parking2 = 0
            else:
                if pot_value2 > 100:
                    self.client.publish("mydata/park", "park,2,1")
                    parking2 = 1


if __name__ == "__main__":
    try:
        client = mqtt.Client()
        mymqtt = Pressure(client)
        mymqtt.start()

    except KeyboardInterrupt:
        print("종료")


