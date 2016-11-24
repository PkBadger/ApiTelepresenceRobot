from client import GetData
import time
import os
import array
import subprocess
import serial

lastDir = [0,0]
os.system("sudo ./servod --pcm")
ser =serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=10
)
ser.flushInput()
ser.flushOutput()

def writeServo(servo,percent):
    string = "echo "+str(servo)+"="+str(percent)+"% > /dev/servoblaster"
    os.system(string)

def callbackSpeedDir(motorL,motorR,dirL,dirR):
    #print motorL + " " + motorR + " " + dirL + " "+ dirR
    buffer_out = [int(float((motorR))),int(float(dirR)),int(float(motorL)),int(float(dirL))]
    if abs(buffer_out[0]-buffer_out[2]) == 1:
        buffer_out[2] = buffer_out[0]
    if buffer_out[0] == 0 and buffer_out[2] == 0:
        if lastDir[0] == 0 and lastDir[1] == 0:
            buffer_out[1] = 0
            buffer_out[3] = 0
        elif lastDir[0] == 0 and lastDir[1] == 1:
            buffer_out[1] = 0
            buffer_out[3] = 1
        elif lastDir[0] == 1 and lastDir[1] == 0:
            buffer_out[1] = 1
            buffer_out[3] = 0
        elif lastDir[0] == 1 and lastDir[1] == 1:
            buffer_out[1] = 1
            buffer_out[3] = 1
    print(buffer_out)
    ser.write(str(buffer_out[0]))
    ser.write("\n")
    ser.write(str(buffer_out[1]))
    ser.write("\n")
    ser.write(str(buffer_out[2]))
    ser.write("\n")
    ser.write(str(buffer_out[3]))
    ser.write("\n")
    lastDir[0] = buffer_out[1]
    lastDir[1] = buffer_out[3]

def callbackCamera(x,y):
    print "x = "+x+" y = " + y
    convertx = float(x)/1.8
    converty = float(y)/1.8
    writeServo(2,convertx)
    writeServo(3,converty)

def callbackLight(light):
    print light

def callbackBrake(brake):
    print brake


url = "192.168.42.16:8888/wsRPI"
data = GetData(url,callbackSpeedDir,callbackCamera,callbackLight,callbackBrake)
