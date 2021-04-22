import random

import RPi.GPIO as GPIO
from flask import Flask, render_template, jsonify

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
LED = 20
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)


# 10초 마다 한 번씩 센서값을 추출해서 넘겨주기 위한 메소드
# 추출한 데이터를 json 형식으로 변환해서 리턴
@app.route("/update")
def update():
    msg = {
        "hum": random.randrange(40, 60),
        "temp": random.randrange(20, 25),
        "distance": random.randrange(20, 50)
    }
    return jsonify(msg)


@app.route("/<command>")
def action(command):
    if command == "on":
        GPIO.output(LED, GPIO.HIGH)
        message = "GPIO" + str(LED) + " ON"
    elif command == "off":
        GPIO.output(LED, GPIO.LOW)
        message = "GPIO" + str(LED) + " OFF"
    else:
        message = "Fail"

    msg = {
        "message": message,
        "status": GPIO.input(LED),
        "hum": random.randrange(40, 60),
        "temp": random.randrange(20, 25),
        "distance": random.randrange(20, 50)
    }
    return render_template("index.html", **msg)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port="8088", debug=True)
    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
