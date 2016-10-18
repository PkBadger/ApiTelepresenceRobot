#!/usr/bin/python
#-*- coding: utf-8 -*-
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
while True:
	writeNumber(gyro,0x6B,0)   #Selecting Register
	datos[0] = 255
	datos[1] = 255
	datos[2] = 1
	datos[3] = 1

	datos[4] = readNumber(gyro, 0x47)
	datos[5] = readNumber(gyro, 0x48)
	writeBlock(arduino,0,datos)
	print datos




time.sleep(.05)
