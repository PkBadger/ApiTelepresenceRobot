from client import GetData
import RPi.GPIO as GPIO

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
def callbackCamera(x,y):
    print "x= "+x+" y= "+y

url = "10.33.10.18:8888/wsRPI"

data = GetData(url,callbackSpeedDir,callbackCamera)
