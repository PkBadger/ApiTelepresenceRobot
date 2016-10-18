#!/usr/bin/python
#-*- coding: utf-8 -*-
from client import GetData
import time             #libreria time para delays
import os
from smbus2 import SMBus
import smbus2
import subprocess
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
def writeServo(servo,percent):
    string = "echo "+str(servo)+"="+str(percent)+"% > /dev/servoblaster"
    os.system(string)

bus = smbus2.SMBus(1) #Master
datos = [0,0,0,0,0,0]
os.system("sudo ./servod --pcm")

def callbackSpeedDir(motorL,motorR,dirL,dirR): #Callback del motor
    print "speed "+motorR +" "+ motorL + " " + dirL + " "+ dirR
    data = [int(float((motorL))),int(float(motorR)),int(float(dirL)),int(float(dirR))]
    datos[0] = data[0]
    datos[1] = data[1]
    datos[2] = data[2]
    datos[3] = data[3]
    datos[4] = 0
    datos[5] = 0
    if abs(data[0]-data[1]) == 1:
        data[1] = data[0]
    print (data)
    writeBlock(arduino,0,data)


def callbackCamera(x,y):   #callback de la camara
    print "x= "+x+" y= "+y
    convertx =float(x)/1.8
    converty = float(y)/1.8
    writeServo(2,convertx)
    writeServo(3,converty)

url = "10.33.10.18:8888/wsRPI"

data = GetData(url,callbackSpeedDir,callbackCamera)
time.sleep(.05)
