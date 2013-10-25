 #! /usr/bin/env python
 
import pygame
import pygame.mixer
import serial
import struct
import os
from time import *
import ConfigParser

from LyreDevice import LyreDevice


####################################################
#                      Setup                      ##
####################################################

SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080

PAN_RATIO=0.2
TILT_RATIO=0.2

PROGRAMM_PATH=os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH=PROGRAMM_PATH+"/config.ini"
####################################################
#                      Program                    ##
####################################################


running = 1


lyre = LyreDevice(CONFIG_PATH)

pygame.font.init()
pygame.init()
pygame.mixer.init
# screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sound = pygame.mixer.Sound(PROGRAMM_PATH+"/criticalstop_short.wav")
font = pygame.font.Font(None,30)
pygame.mouse.set_visible(False)

def redraw():
    global lyre
    bgcolor = 0, 0, 0
    linecolor = 255, 255, 255
    screen.fill(bgcolor)
    scr_y=(lyre.pan*SCREEN_WIDTH)/lyre.MAX_PAN
    scr_x=(lyre.tilt*SCREEN_HEIGHT)/lyre.MAX_TILT
    pygame.draw.line(screen, linecolor, (scr_x, 0), (scr_x, SCREEN_HEIGHT))
    pygame.draw.line(screen, linecolor, (0, scr_y), (SCREEN_WIDTH, scr_y))
    text=font.render("pan ="+str(lyre.pan)+" tilt ="+str(lyre.tilt), 1,(255,255,255))
    screen.blit(text, (0, 100))
    text=font.render("  x ="+str(scr_x)+"    y ="+str(scr_y), 1,(255,255,255))
    screen.blit(text, (0, 0))
    pygame.display.flip()

def move(x,y):
    global lyre
    lyre.IncrementTilt(-x*TILT_RATIO)
    lyre.IncrementPan(-y*PAN_RATIO)

def click():
    sound.play()
    lyre.GoboSwitch(1)
    lyre.GoboRotate(40)
    sleep(2)
    lyre.GoboRotate(0)
    lyre.GoboSwitch(0)
    

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
            click()

    x, y = pygame.mouse.get_rel()
    if (x!=0 or y!=0):
        move(x,y)
        sleep(0.025)
    redraw()

ser.close()
