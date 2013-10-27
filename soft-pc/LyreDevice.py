
import serial
from serial.tools import list_ports
from time import *
import ConfigParser

class LyreDevice:

    ser = None
    config = None
    configPath = ""

#working values
    pan=0
    tilt=0

# setup values
    MAX_TILT=32000
    MAX_PAN=32000
    MIN_TILT=0
    MIN_PAN=0

    INTENSITY=255
    FOCUS=100

    #mouse related, nothing to do there but easier
    PAN_RATIO=20
    TILT_RATIO=20

    DMX_TILT_1 = 1
    DMX_TILT_2 = 13
    DMX_PAN_1 = 2
    DMX_PAN_2 = 14
    DMX_INTENSITY = 11
    DMX_ROTATING_GOBO_WHEEL = 5
    DMX_ROTATING_GOBO_ROT = 6
    DMX_FOCUS = 8


#static values
    GOBOS_INDEX=[0,19,38,57,76,95,114,128,192]

    def __init__(self,configPath):
        self.configPath=configPath
        self.LoadConfig()

    def LoadConfig(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configPath)
        try:
            self.MAX_TILT=int(self.config.get('LYRE', "MAX_TILT"))
            self.MAX_PAN=int(self.config.get('LYRE', "MAX_PAN"))
            self.MIN_TILT=int(self.config.get('LYRE', "MIN_TILT"))
            self.MIN_PAN=int(self.config.get('LYRE', "MIN_PAN"))
            self.INTENSITY=int(self.config.get('LYRE', "INTENSITY"))
            self.FOCUS=int(self.config.get('LYRE', "FOCUS"))
            self.PAN_RATIO=int(self.config.get('LYRE', "PAN_RATIO"))
            self.TILT_RATIO=int(self.config.get('LYRE', "TILT_RATIO"))
            self.SetIntensity(self.INTENSITY)
        except Exception, e:
            self.SaveConfig()
            self.LoadConfig()


    def SaveConfig(self):
        cfgfile = open(self.configPath,'w')
        if (not self.config.has_section("LYRE")):
            self.config.add_section("LYRE")
        self.config.set('LYRE', "MAX_TILT", self.MAX_TILT)
        self.config.set('LYRE', "MAX_PAN", self.MAX_PAN)
        self.config.set('LYRE', "MIN_TILT", self.MIN_TILT)
        self.config.set('LYRE', "MIN_PAN", self.MIN_PAN)
        self.config.set('LYRE', "INTENSITY", self.INTENSITY)
        self.config.set('LYRE', "FOCUS", self.FOCUS)
        self.config.set('LYRE', "PAN_RATIO", self.PAN_RATIO)
        self.config.set('LYRE', "TILT_RATIO", self.TILT_RATIO)
        self.config.write(cfgfile)
        cfgfile.close()

    def Open(self):
        ports = [port[0] for port in list_ports.comports()]
        while True:
            for port in ports:
                print "Trying port:" + port
                try:
                    self.ser = serial.Serial(port, 9600, timeout=0.5)
                except Exception, e:
                    print "nope !"
                else:
                    sleep(2)
                    self.ser.write('?')
                    if (self.ser.read(12) == "I am the One"):
                        print "Lyre found on "+port
                        return port
                    else:
                        self.ser.close()
            sleep(0.5)

    def Send(self,channel,value):
        if (not self.ser):
            self.Open()
        self.ser.write(str(channel)+"c"+str(int(value))+"w")
        self.ser.flushInput()

    ### MOVEMENT ###

    def SetTilt(self,value):
        self.tilt=min(max(value,self.MIN_TILT),self.MAX_TILT)
        tilt_highbits = (int(self.tilt)&0xff00)>>8
        tilt_lowbits = (int(self.tilt)&0x00ff)
        self.Send(self.DMX_TILT_1,tilt_highbits)
        self.Send(self.DMX_TILT_2,tilt_lowbits)

    def IncrementTilt(self,value):
        self.SetTilt(self.tilt+value)
    
    def SetPan(self,value):
        self.pan=min(max(value,self.MIN_PAN),self.MAX_PAN)
        pan_highbits = (int(self.pan)&0xff00)>>8
        pan_lowbits = (int(self.pan)&0x00ff)
        self.Send(self.DMX_PAN_1,pan_highbits)
        self.Send(self.DMX_PAN_2,pan_lowbits)

    def IncrementPan(self,value):
        self.SetPan(self.pan+value)

    ### GOBOS ###

    def GoboSwitch(self,index):
        self.Send(self.DMX_ROTATING_GOBO_WHEEL,self.GOBOS_INDEX[index])

    def GoboRotate(self,speed):
        self.Send(self.DMX_ROTATING_GOBO_ROT,118-speed)

    ### SETUP ###

    def SetIntensity(self,value):
        self.INTENSITY=min(max(value,0),255)
        self.Send(self.DMX_INTENSITY,self.INTENSITY)
        print "INTENSITY="+str(self.INTENSITY)

    def IncrementIntensity(self,value):
        self.SetIntensity(self.INTENSITY+value)

    def IncrementMaxPan(self,value):
        self.MAX_PAN=min(max(self.MAX_PAN+value,0),65535)

    def IncrementMaxTilt(self,value):
        self.MAX_TILT=min(max(self.MAX_TILT+value,0),65535)

    def IncrementMinPan(self,value):
        self.MIN_PAN=min(max(self.MIN_PAN+value,0),65535)

    def IncrementMinTilt(self,value):
        self.MIN_TILT=min(max(self.MIN_TILT+value,0),65535)

    def SetFocus(self,value):
        self.FOCUS=min(max(value,0),255)
        self.Send(self.DMX_FOCUS,self.FOCUS)
        print "FOCUS="+str(self.FOCUS)

    def IncrementFocus(self,value):
        self.SetFocus(self.FOCUS+value)

    ###TODO ###
    
    def ColorSwitch(self,index):
        pass

    def Reset(self,value):
        pass

