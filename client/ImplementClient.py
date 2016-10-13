#!/usr/bin/python
#-*- coding: utf-8 -*-
from client import GetData
import RPi.GPIO as GPIO
import time             #libreria time para delays
from smbus2 import SMBus
import smbus2
import subprocess
#from __main__ import *
arduino = 0x08              #se define la dirección del arduino esclavo
gyro = 0x68                 #se define la dirección del gyro


def writeBlock(address,register,data):
        flag=1
        while(flag==1):
                try:
                        bus.write_i2c_block_data(address,register,data) #Data is list of bytes
                        flag=0
                except IOError:
                        flag=1
def writeNumber(address,register,value):         #función para escribir al bus
        flag=1
        while(flag==1):
                try:
                        bus.write_byte_data(address,register,value)
                        flag=0
                except IOError:
                        flag=1
        return -1

def readNumber(address,register):            #funcion para leer el número
        flag=1
        while(flag==1):
                try:
                        number = bus.read_byte_data(address,register)   #lee un byte y lo guarda en number
                        flag=0
                except IOError:
                        flag=1

        return number            #regresa la variable number

bus = smbus2.SMBus(1) #Master
datos = [0,0,0,0,0,0]
#writeNumber(gyro,0x6B,0) # PWR_MGMT_1 register

#GyZ1= readNumber(gyro,0x47)
#GyZ2 = readNumber(gyro,0x48)
#datos[4] = GyZ1
#datos[5] = GyZ2
#writeBlock(arduino,0,datos)

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
    data = [int(float((motorR))),int(float(motorL)),int(float(dirL)),int(float(dirR))]
    datos[0] = data[0]
    datos[1] = data[1]
    datos[2] = data[2]
    datos[3] = data[3]
    datos[4] = 0
    datos[5] = 0
    #writeNumber(gyro,0x6B,0)

    writeBlock(arduino,0,data)


def callbackCamera(x,y):
    print "x= "+x+" y= "+y

url = "10.33.10.18:8888/wsRPI"

data = GetData(url,callbackSpeedDir,callbackCamera)
time.sleep(.05)
