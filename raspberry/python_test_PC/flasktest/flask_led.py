from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
LED = 20
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)


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
        "status": GPIO.input(LED)
    }

    return render_template("led.html", **msg)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port="8088", debug=True)
    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
