import pygame
import sys
import RPi.GPIO as GPIO
import time
import mido

screen_width = 800
screen_height = 400
RED = (255, 0, 0)
GREEN = (117, 223, 25)
BLUE = (66, 209, 237)
PURPLE = (175, 57, 196)
WHITE = (255, 255, 255)
BROWN = (138, 92, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Robuka GUI Backend")

GPIO.setmode(GPIO.BCM)
servo_pin = 18  # whichever GPIO pin is being used

# Set up the GPIO pin for PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency for PWM

def set_angle(angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle (0.0 to 100.0)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    # time.sleep(1)  # Adjust this sleep time as needed
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def controlMotor(command_list):
    pwm.start(0)  # Start PWM with a duty cycle of 0 (neutral position)
    for command in command_list:
        if command == 0:
            # print("REST")
            pwm.ChangeDutyCycle(0)
        elif command == 90:
            # print("GO")
            pwm.ChangeDutyCycle(50)
            for _ in range(8):  # Rotate four times for 90 degrees each
                set_angle(90)
                time.sleep(0.1)
        time.sleep(0.5)

def drawBox(box_color, x_pos, y_pos):
    box_width = 50
    box_height = 50

    box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    pygame.draw.rect(screen, box_color, box, width=0)

    return box

def drawSubmit(box_color, x_pos, y_pos):
    box_width = 200
    box_height = 50
    
    submit_box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    pygame.draw.rect(screen, box_color, submit_box, width=0)

    font = pygame.font.Font(None, 24)
    text_surface = font.render("SUBMIT", True, WHITE)

    text_rect = text_surface.get_rect()
    text_rect.center = submit_box.center

    screen.blit(text_surface, text_rect)

    return submit_box

def drawExport(box_color, x_pos, y_pos):
    box_width = 200
    box_height = 50
    
    export_box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    pygame.draw.rect(screen, box_color, export_box, width=0)

    font = pygame.font.Font(None, 24)
    text_surface = font.render("EXPORT", True, WHITE)

    text_rect = text_surface.get_rect()
    text_rect.center = export_box.center

    screen.blit(text_surface, text_rect)

    return export_box

def drawClear(box_color, x_pos, y_pos):
    box_width = 200
    box_height = 50
    
    clear_box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    pygame.draw.rect(screen, box_color, clear_box, width=0)

    font = pygame.font.Font(None, 24)
    text_surface = font.render("CLEAR", True, WHITE)

    text_rect = text_surface.get_rect()
    text_rect.center = clear_box.center

    screen.blit(text_surface, text_rect)

    return clear_box

def bpm2tempo(bpm):
    msec = 60000 / bpm
    midi_ticks = msec * 480 / 1000
    return int(midi_ticks)

def convert2drum(note):
    drum_map = {'36': 35, '38': 38, '42': 42, '46': 46}
    return drum_map.get(note, 0)

def main():
    # create midi file and track
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    pygame.init()

    box1_color = RED
    box2_color = RED
    box3_color = RED
    box4_color = RED
    
    box1_clicked = False
    box2_clicked = False
    box3_clicked = False
    box4_clicked = False
    val1, val2, val3, val4 = 0, 0, 0, 0
    command_list = [val1, val2, val3, val4]

    submit_pressed = False
    clear_pressed = False

    x_pos = (screen_width-50)/2
    y_pos = (screen_height-50)/2

    # MIDI setup
    vel_val = 126
    time_sig = bpm2tempo(80)

    doum = mido.Message('note_on', note=36, velocity=vel_val, time=time_sig, channel=9)
    doum_off = mido.Message('note_off', note=36, velocity=vel_val, time=time_sig, channel=9)

    rest = mido.Message('note_off', note=1, velocity=vel_val, time=time_sig, channel=9)
    

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if submit_box.collidepoint(mouse_pos):
                    submit_pressed = True
                    clear_pressed = False

                if export_box.collidepoint(mouse_pos):
                    print("export clicked")
                    for command in command_list:
                        if command == 0:
                            track.append(rest)
                        elif command == 90:
                            track.append(doum)
                            track.append(doum_off)
                    mid.save('output.mid')

                if box1.collidepoint(mouse_pos):
                    # toggle box_clicked
                    box1_clicked = not box1_clicked
                    if box1_clicked:
                        box1_color = GREEN
                        val1 = 90
                    elif box1_clicked == False:
                        box1_color = RED
                        val1 = 0

                if box2.collidepoint(mouse_pos):
                    box2_clicked = not box2_clicked
                    if box2_clicked:
                        box2_color = GREEN
                        val2 = 90
                    elif box2_clicked == False:
                        box2_color = RED
                        val2 = 0

                if box3.collidepoint(mouse_pos):
                    box3_clicked = not box3_clicked
                    if box3_clicked:
                        box3_color = GREEN
                        val3 = 90
                    elif box3_clicked == False:
                        box3_color = RED
                        val3 = 0

                if box4.collidepoint(mouse_pos):
                    box4_clicked = not box4_clicked
                    if box4_clicked:
                        box4_color = GREEN
                        val4 = 90
                    elif box4_clicked == False:
                        box4_color = RED
                        val4 = 0
                
                if clear_box.collidepoint(mouse_pos):
                    clear_pressed = True
                    submit_pressed = False

                    val1, val2, val3, val4 = 0, 0, 0, 0
                    pwm.ChangeDutyCycle(0)
                    # prevents lag
                    box1_clicked = not box1_clicked
                    box1_color = RED
                    box2_clicked = not box2_clicked
                    box2_color = RED
                    box3_clicked = not box3_clicked
                    box3_color = RED
                    box4_clicked = not box4_clicked
                    box4_color = RED

        # print(command_list)

        if clear_pressed:
            pygame.display.flip()
            clear_pressed = False

        if submit_pressed:
            controlMotor(command_list)
        
        box1 = drawBox(box1_color, x_pos, y_pos)
        box2 = drawBox(box2_color, x_pos + 100, y_pos)
        box3 = drawBox(box3_color, x_pos + 200, y_pos)
        box4 = drawBox(box4_color, x_pos + 300, y_pos)

        submit_box = drawSubmit(BLUE, 50, 100)
        clear_box = drawClear(PURPLE, 50, 150)
        export_box = drawExport(BROWN, 50, 200)

        command_list = [val1, val2, val3, val4]

        pygame.display.flip()

try: 
    main()
finally:
    pwm.stop()
    GPIO.cleanup()