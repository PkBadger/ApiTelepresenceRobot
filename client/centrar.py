import os
import time

os.system('sudo ./servod --pcm')
def writeServo(servo,percent):
    string = "echo "+str(servo)+"="+str(percent)+"% > /dev/servoblaster"
    print string
while True:
    os.system("echo 2=50% > /dev/servoblaster")
    os.system("echo 3=50% > /dev/servoblaster")
    time.sleep(1.5)
