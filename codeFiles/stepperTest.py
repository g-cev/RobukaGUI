import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO pins
STEP_PIN = 19
DIR_PIN = 26

# set outputs
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# set initial direction and freq aka speed
GPIO.output(DIR_PIN, GPIO.HIGH) # high for one dir, low for other
frequency = 1000                # set in hz

# create PWM object\
pwm = GPIO.PWM(26, 50)

choice = 1

try:
    while choice == 1:
        # rotate cw
        GPIO.output(DIR_PIN, GPIO.HIGH)

        # generate PWM signal for stepping
        GPIO.set_servo(STEP_PIN, frequency)
        GPIO.sleep(2)

        # rotate ccw
        GPIO.output(DIR_PIN, GPIO.LOW)

        # another PWM signal
        GPIO.set_servo(STEP_PIN, frequency)
        GPIO.sleep(2)

except KeyboardInterrupt:
    # exit on ctrl+c
    GPIO.cleanup()
