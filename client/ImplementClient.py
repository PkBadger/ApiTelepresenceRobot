from client import GetData
import RPi.GPIO as GPIO
 # -*- coding: utf-8 -*-
import time             #libreria time para delays
from smbus2 import SMBus
import smbus2
import subprocess
#from __main__ import *
arduino = 0x08              #se define la dirección del esclavo

def writeBlock(address,register,data):
        flag=1
        while(flag==1):
                try:
                        bus.write_i2c_block_data(address,register,data) #Data is list of bytes
                        flag=0
                except IOError:
                        flag=1


GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
pwmX = GPIO.PWM(27, 100)
pwmX.start(5)


GPIO.setup(18, GPIO.OUT)
pwmY = GPIO.PWM(18, 100)
pwmY.start(5)

pwmX.ChangeDutyCycle(13)
pwmY.ChangeDutyCycle(13)

def callbackSpeedDir(motorL,motorR,dirL,dirR):
    print "speed "+motorR +" "+ motorL + " " + dirL + " "+ dirR
    data = [motorR,motorL]
    writeBlock(arduino,0,data)


def callbackCamera(x,y):
    print "x= "+x+" y= "+y

url = "10.33.10.18:8888/wsRPI"

data = GetData(url,callbackSpeedDir,callbackCamera)
