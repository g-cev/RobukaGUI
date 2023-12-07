import pygame
import sys
import RPi.GPIO as GPIO
import time

screen_width = 800
screen_height = 400
RED = (255, 0, 0)
GREEN = (117, 223, 25)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Robuka GUI Backend")
icon = pygame.image.load("images/Stevens_Ducks.svg")
pygame.display.set_icon(icon)

GPIO.setmode(GPIO.BCM)
servo_pin = 18  # whichever GPIO pin is being used

# Set up the GPIO pin for PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency for PWM

def set_angle(angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle (0.0 to 100.0)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Adjust this sleep time as needed
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def controlMotor(command_list):
    pwm.start(0)  # Start PWM with a duty cycle of 0 (neutral position)
    
    for command in command_list:
        if command == 0:
            pwm.ChangeDutyCycle(0)
        elif command == 90:
            pwm.ChangeDutyCycle(50)
            set_angle(90)

    # set_angle(command_list[0])

    # pwm.ChangeDutyCycle(0)
    # set_angle(command_list[1])
    # time.sleep(1) # sleep helps us know the difference

def drawBox(box_color, x_pos, y_pos):
    box_width = 50
    box_height = 50

    box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    pygame.draw.rect(screen, box_color, box, width=0)

    return box

def main():
    pygame.init()

    box1_color = RED
    box2_color = RED
    box3_color = RED
    box1_clicked = False
    box2_clicked = False
    box3_clicked = False


    x_pos = (screen_width-50)/2
    y_pos = (screen_height-50)/2

    command_list = []

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if box1.collidepoint(mouse_pos):
                    # toggle box_clicked
                    box1_clicked = not box1_clicked
                    if box1_clicked:
                        box1_color = GREEN
                        command_list.append(90)
                    else:
                        box1_color = RED
                        command_list.append(0)

                if box2.collidepoint(mouse_pos):
                    box2_clicked = not box2_clicked
                    if box2_clicked:
                        box2_color = GREEN
                        command_list.append(90)
                    else:
                        box2_color = RED
                        command_list.append(0)

                if box3.collidepoint(mouse_pos):
                    box3_clicked = not box3_clicked
                    if box3_clicked:
                        box3_color = GREEN
                        command_list.append(90)
                    else:
                        box3_color = RED
                        command_list.append(0)

        controlMotor(command_list)
        
        box1 = drawBox(box1_color, x_pos, y_pos)
        box2 = drawBox(box2_color, x_pos + 100, y_pos)
        box3 = drawBox(box3_color, x_pos + 200, y_pos)

        command_list = []

        # command_list = []  # Create a new list for each iteration
        pygame.display.flip()

try: 
    main()
finally:
    pwm.stop()
    GPIO.cleanup()