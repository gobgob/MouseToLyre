 #! /usr/bin/env python
 
import pygame
import pygame.mixer
import serial
import os
import sys
from time import *
import ConfigParser

from LyreDevice import LyreDevice


PROGRAMM_PATH=os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH=PROGRAMM_PATH+"/config.ini"

running = 1

lyre = LyreDevice(CONFIG_PATH)
lyre.GoboSwitch(5)

pygame.font.init()
pygame.init()
pygame.mixer.init

if (len(sys.argv)>1):
    SCREEN_WIDTH=480
    SCREEN_HEIGHT=234
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
else:
    SCREEN_WIDTH=1280
    SCREEN_HEIGHT=1024
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sound = pygame.mixer.Sound(PROGRAMM_PATH+"/criticalstop_short.wav")
font = pygame.font.Font(None,30)
pygame.mouse.set_visible(False)

sound.play()

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
    lyre.IncrementTilt(-x*lyre.TILT_RATIO)
    lyre.IncrementPan(-y*lyre.PAN_RATIO)

def click():
    sound.play()
    lyre.GoboSwitch(6)
    lyre.GoboRotate(40)
    sleep(2)
    lyre.GoboRotate(0)
    lyre.GoboSwitch(5)

class menus:
    MENU_NORMAL="MENU_NORMAL"
    MENU_LUMINOSITY="MENU_LUMINOSITY"
    MENU_MAX_PAN="MENU_MAX_PAN"
    MENU_MIN_PAN="MENU_MIN_PAN"
    MENU_MAX_TILT="MENU_MAX_TILT"
    MENU_MIN_TILT="MENU_MIN_TILT"
    MENU_PAN_RATIO="MENU_PAN_RATIO"
    MENU_TILT_RATIO="MENU_TILT_RATIO"
    MENU_FOCUS="MENU_FOCUS"

currentMenu = menus.MENU_NORMAL

def menu(key):
    global currentMenu, lyre
    if(key==pygame.K_KP0) : currentMenu = menus.MENU_NORMAL
    if(key==pygame.K_KP1) : currentMenu = menus.MENU_LUMINOSITY
    if(key==pygame.K_KP2) : currentMenu = menus.MENU_MAX_PAN
    if(key==pygame.K_KP3) : currentMenu = menus.MENU_MIN_PAN
    if(key==pygame.K_KP4) : currentMenu = menus.MENU_MAX_TILT
    if(key==pygame.K_KP5) : currentMenu = menus.MENU_MIN_TILT
    if(key==pygame.K_KP6) : currentMenu = menus.MENU_PAN_RATIO
    if(key==pygame.K_KP7) : currentMenu = menus.MENU_TILT_RATIO
    if(key==pygame.K_KP8) : currentMenu = menus.MENU_FOCUS
    # if(key==pygame.K_KP9) : currentMenu = menus.MENU_MIN_TILT
    print currentMenu

    if(currentMenu==menus.MENU_LUMINOSITY):
        if(key==pygame.K_KP_PLUS) : lyre.IncrementIntensity(10)
        if(key==pygame.K_KP_MINUS) : lyre.IncrementIntensity(-10)

    if(currentMenu==menus.MENU_MAX_PAN):
        if(key==pygame.K_KP_PLUS) : lyre.IncrementMaxPan(100)
        if(key==pygame.K_KP_MINUS) : lyre.IncrementMaxPan(-100)
        lyre.SetPan(lyre.MAX_PAN)

    if(currentMenu==menus.MENU_MIN_PAN):
        if(key==pygame.K_KP_PLUS) : lyre.IncrementMinPan(100)
        if(key==pygame.K_KP_MINUS) : lyre.IncrementMinPan(-100)
        lyre.SetPan(lyre.MIN_PAN)

    if(currentMenu==menus.MENU_MAX_TILT):
        if(key==pygame.K_KP_PLUS) : lyre.IncrementMaxTilt(100)
        if(key==pygame.K_KP_MINUS) : lyre.IncrementMaxTilt(-100)
        lyre.SetTilt(lyre.MAX_TILT)

    if(currentMenu==menus.MENU_MIN_TILT):
        if(key==pygame.K_KP_PLUS) : lyre.IncrementMinTilt(100)
        if(key==pygame.K_KP_MINUS) : lyre.IncrementMinTilt(-100)
        lyre.SetTilt(lyre.MIN_TILT)

    if(currentMenu==menus.MENU_PAN_RATIO):
        if(key==pygame.K_KP_PLUS) : lyre.PAN_RATIO+=1
        if(key==pygame.K_KP_MINUS) : lyre.PAN_RATIO-=1

    if(currentMenu==menus.MENU_TILT_RATIO):
        if(key==pygame.K_KP_PLUS) : lyre.TILT_RATIO+=1
        if(key==pygame.K_KP_MINUS) : lyre.TILT_RATIO-=1

    if(currentMenu==menus.MENU_FOCUS):
        if(key==pygame.K_KP_PLUS) : lyre.IncrementFocus(1)
        if(key==pygame.K_KP_MINUS) : lyre.IncrementFocus(-1)

    lyre.SaveConfig()

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
            else:
                menu(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click()

    if (currentMenu in [menus.MENU_NORMAL,menus.MENU_TILT_RATIO,menus.MENU_PAN_RATIO]):
        x, y = pygame.mouse.get_rel()

        # in thoses menues we limit the movement to 1 axe at the time
        if(currentMenu==menus.MENU_TILT_RATIO):y=0
        if(currentMenu==menus.MENU_PAN_RATIO):x=0

        if (x!=0 or y!=0):
            move(x,y)
            sleep(0.025)
        redraw()
