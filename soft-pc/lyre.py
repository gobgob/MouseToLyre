 #! /usr/bin/env python
 
import pygame
import pygame.mixer
import serial
import struct

        

####################################################
#                      Setup                      ##
####################################################


MAX_TILT=65535
MAX_PAN=65535

SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080

PAN_RATIO=60
TILT_RATIO=60

lyre_pan=MAX_PAN/2
lyre_tilt=MAX_TILT/2

####################################################
#                      Program                    ##
####################################################

bgcolor = 0, 0, 0
linecolor = 255, 255, 255
running = 1
first_move=True

pygame.font.init()
pygame.init()
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# screen = pygame.display.set_mode((800, 600))
screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
sound = pygame.mixer.Sound("criticalstop_short.wav")
font=pygame.font.Font(None,30)

def redraw():
    global lyre_pan,lyre_tilt
    screen.fill(bgcolor)
    scr_x=(lyre_pan*SCREEN_WIDTH)/MAX_PAN
    scr_y=(lyre_tilt*SCREEN_HEIGHT)/MAX_TILT
    pygame.draw.line(screen, linecolor, (scr_x, 0), (scr_x, SCREEN_HEIGHT))
    pygame.draw.line(screen, linecolor, (0, scr_y), (SCREEN_WIDTH, scr_y))
    text=font.render("pan ="+str(lyre_pan)+" tilt ="+str(lyre_tilt), 1,(255,255,255))
    screen.blit(text, (0, 100))
    text=font.render("  x ="+str(scr_x)+"    y ="+str(scr_y), 1,(255,255,255))
    screen.blit(text, (0, 0))
    pygame.display.flip()


def send():
    global lyre_pan,lyre_tilt
    data = struct.pack('I', lyre_pan*(2^16)+lyre_tilt)
    # ser.write(data)
    # ser.write('\n')

def move(x,y):
    global lyre_pan,lyre_tilt
    lyre_pan=lyre_pan+x*PAN_RATIO
    lyre_tilt+=y*TILT_RATIO
    if (lyre_pan>MAX_PAN):lyre_pan=MAX_PAN
    if (lyre_tilt>MAX_TILT):lyre_tilt=MAX_TILT
    if (lyre_pan<0):lyre_pan=0
    if (lyre_tilt<0):lyre_tilt=0
    send()

while running:
    global ser
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
            ser.close()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        sound.play()
    elif event.type == pygame.MOUSEMOTION:
        x, y = event.rel
        if not (first_move): #flag to avoid big mouvement at launch
           move(x,y)
        first_move=False
    redraw()
    