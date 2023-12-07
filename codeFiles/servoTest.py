import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

# period of the square wave
p = GPIO.PWM(18, 50)

# dc of 100% should be 270 dg, dc of 0% is 0 dg


try:
    p.start(0)
    while True:
        print("30")
        p.ChangeDutyCycle(30)
        time.sleep(1)
        print("80")
        p.ChangeDutyCycle(80)
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

