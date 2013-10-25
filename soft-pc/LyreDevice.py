
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
    MAX_TILT=255
    MAX_PAN=255
    MIN_TILT=0
    MIN_PAN=0

    INTENSITY=20

    DMX_TILT_1 = 1
    DMX_TILT_2 = 14
    DMX_PAN_1 = 2
    DMX_PAN_2 = 13
    DMX_INTENSITY = 11
    DMX_ROTATING_GOBO_WHEEL = 5
    DMX_ROTATING_GOBO_ROT = 6


#static values
    GOBOS_INDEX=[0,19,38,57,76,95,114,128,192]

    def __init__(self,configPath):
        self.configPath=configPath
        self.LoadConfig()

    def LoadConfig(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configPath)
        if (not self.config.has_section("LYRE")):
            self.config.add_section("LYRE")
            self.config.set('LYRE', "MAX_TILT", self.MAX_TILT)
            self.config.set('LYRE', "MAX_PAN", self.MAX_PAN)
            self.config.set('LYRE', "MIN_TILT", self.MIN_TILT)
            self.config.set('LYRE', "MIN_PAN", self.MIN_PAN)
            self.config.set('LYRE', "INTENSITY", self.INTENSITY)
            self.SaveConfig()

        self.SetIntensity(self.INTENSITY)

    def SaveConfig(self):
        cfgfile = open(self.configPath,'w')
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

    def SetTilt(self,value):
        self.tilt=min(max(value,self.MIN_TILT),self.MAX_TILT)
        self.Send(self.DMX_TILT_1,self.tilt)

    def IncrementTilt(self,value):
        self.SetTilt(self.tilt+value)
    
    def SetPan(self,value):
        self.pan=min(max(value,self.MIN_PAN),self.MAX_PAN)
        self.Send(self.DMX_PAN_1,self.pan)

    def IncrementPan(self,value):
        self.SetPan(self.pan+value)

    def SetIntensity(self,value):
        self.INTENSITY=value
        self.Send(self.DMX_INTENSITY,value)

    def GoboSwitch(self,index):
        self.Send(self.DMX_ROTATING_GOBO_WHEEL,self.GOBOS_INDEX[index])

    def GoboRotate(self,speed):
        self.Send(self.DMX_ROTATING_GOBO_ROT,118-speed)

    def ColorSwitch(self,index):
        pass

    def SetFocus(self,value):
        pass

    def Reset(self,value):
        pass
