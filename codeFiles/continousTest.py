import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin = 18  # whichever GPIO pin is being used

# Set up the GPIO pin for PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency for PWM

# Function to set the servo angle
def set_angle(angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle (0.0 to 100.0)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Adjust this sleep time as needed
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    pwm.start(0)  # Start PWM with a duty cycle of 0 (neutral position)
   
    while True:
        set_angle(180)
        """
        # Move the servo back and forth (0 to 180 degrees)
        print("angle: 0")
        set_angle(0)  # Slowest speed in one direction
        time.sleep(2)  # Wait for a moment
        print("angle: 90")
        set_angle(90)  # Middle position (stop)
        time.sleep(2)  # Wait for a moment
        print("angle: 180")
        set_angle(180)  # Fastest speed in the other direction
        time.sleep(2)  # Wait for a moment
        """

    


# instead of going 0-180 in one direction, it looks like its 0-90 cw, 90-180 ccw

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()