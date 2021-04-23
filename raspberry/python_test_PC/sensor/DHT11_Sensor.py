import  time
import Adafruit_DHT as dht11
sensor = dht11.DHT11
pin = 17

while True:
    hum, temp = dht11.read_retry(dht11.DHT11, pin)
    if hum is not None and temp is not None:
        print(str(hum)+","+str(temp))
    else:
        print("error")
    time.sleep(1)
