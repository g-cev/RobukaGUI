import pygame
import sys
import RPi.GPIO as GPIO

screen_width = 800
screen_height = 400
RED = (255, 0, 0)
GREEN = (117, 223, 25)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Test")

GPIO.setmode(GPIO.BCM)
servo_pin = 18  # whichever GPIO pin is being used

# Set up the GPIO pin for PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency for PWM

def set_angle(angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle (0.0 to 100.0)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    # No sleep here for instantaneous action
    # time.sleep(1)  # Adjust this sleep time as needed
    # GPIO.output(servo_pin, False)
    # pwm.ChangeDutyCycle(0)

def controlMotor(box_color):
    pwm.start(0)  # Start PWM with a duty cycle of 0 (neutral position)

    if box_color == GREEN:
        pwm.ChangeDutyCycle(50)
        set_angle(90)
    elif box_color == RED:
        pwm.ChangeDutyCycle(0)
        # No need to set angle for RED, assuming it goes back to neutral automatically

def drawBox(box_color):
    box_width = 100
    box_height = 100

    x_pos = (screen_width - box_width) / 2
    y_pos = (screen_height - box_height) / 2

    box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    pygame.draw.rect(screen, box_color, box, width=0)

    return box

def main():
    pygame.init()

    box_color = RED
    box_clicked = False
    box = None  # Initialize box outside the loop

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if box and box.collidepoint(mouse_pos):
                    # toggle box_clicked
                    box_clicked = not box_clicked

        if box_clicked:
            box_color = GREEN
        else:
            box_color = RED

        screen.fill((0, 0, 0))
        box = drawBox(box_color)
        controlMotor(box_color)
        pygame.display.flip()

try:
    main()
finally:
    pwm.stop()
    GPIO.cleanup()
