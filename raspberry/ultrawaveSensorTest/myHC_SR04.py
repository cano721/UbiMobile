import RPi.GPIO as GPIO
import time
from pymongo import MongoClient

client = MongoClient("172.30.1.3",27017)
print(client.list_database_names())
db = client["mydb"]
my_collection = db["wave_sensor"]


GPIO.setmode(GPIO.BCM)

TRIGER = 24
ECHO = 21

GPIO.setup(TRIGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def getDistance():
    GPIO.output(TRIGER, False)
    time.sleep(1)
    GPIO.output(TRIGER, True)
    time.sleep(0.00001)  # 아주 짧은 시간 이후 초음파 신호를 끈다. 10마이크로초단위로 트리거 신호 송신
    GPIO.output(TRIGER, False)

    # 이제 에코값이 돌아오는 것을 계산한다.
    while GPIO.input(ECHO) == 0: # 에코핀이 아직 초음파를 받지 못했을떄
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance2 = round(distance, 2)
    my_data = [{"distance": distance2}]
    result = my_collection.insert_many(my_data)
    print(result)
    #return distance


if __name__ == "__main__":
    try:
        while True:
            distance_value = getDistance()
            if 2 < distance_value < 400:
                print("distance: %.2f cm" % distance_value)
            else:
                print("out of range")

    except KeyboardInterrupt:
        print("key error")
        GPIO.cleanup()
