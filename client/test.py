import os
import time

os.system('sudo ./servod --pcm')
def writeServo(servo,percent):
    string = "echo "+str(servo)+"="+str(percent)+"% > /dev/servoblaster"
    print string
while True:
    os.system("echo 3=0% > /dev/servoblaster")
    time.sleep(1.5)
    os.system("echo 3=100% > /dev/servoblaster")
    #writeServo(2,100)
    time.sleep(2)
    #writeServo(1,50)
