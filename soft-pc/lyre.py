 #! /usr/bin/env python
 
import pygame
import pygame.mixer
import serial
import struct
import os
import time

        

####################################################
#                      Setup                      ##
####################################################


MAX_TILT=65535
MAX_PAN=65535
MIN_TILT=0
MIN_PAN=0

SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080

PAN_RATIO=60
TILT_RATIO=60

PAN_CHANNEL=10
TILT_CHANNEL=11

lyre_pan=(MAX_PAN+MIN_PAN)/2
lyre_tilt=(MAX_TILT+MIN_TILT)/2

####################################################
#                      Program                    ##
####################################################

bgcolor = 0, 0, 0
linecolor = 255, 255, 255
running = 1

pygame.font.init()
pygame.init()
pygame.mixer.init
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# screen = pygame.display.set_mode((1920, 1080))
screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
sound = pygame.mixer.Sound(os.path.dirname(os.path.realpath(__file__))+"/criticalstop_short.wav")
font = pygame.font.Font(None,30)
pygame.mouse.set_visible(False)

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
    global lyre_pan,lyre_tilt,ser
    ser.write(str(PAN_CHANNEL)+"c")
    ser.write(str(lyre_pan)+"w")
    ser.write(str(TILT_CHANNEL)+"c")
    ser.write(str(lyre_tilt)+"w")
    while (ser.inWaiting()):
        print(ser.read())

def move(x,y):
    global lyre_pan,lyre_tilt
    lyre_pan=lyre_pan+x*PAN_RATIO
    lyre_tilt+=y*TILT_RATIO
    lyre_pan=min(max(lyre_pan,MIN_PAN),MAX_PAN)
    lyre_tilt=min(max(lyre_tilt,MIN_TILT),MAX_TILT)
    send()

while running:
    while True:
        event = pygame.event.poll()
        if (not event):
            break
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            sound.play()
            
    x, y = pygame.mouse.get_rel()
    if (x!=0 or y!=0):
        move(x,y)
        time.sleep(0.05)
    redraw()

ser.close()
