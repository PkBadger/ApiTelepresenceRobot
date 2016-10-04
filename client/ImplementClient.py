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

def callbackSpeed(motorL,motorR):
    print "speed "+motorR +" "+ motorL
def callbackDirection(motorL,motorR):
    print "direction "+motorR +" "+ motorL
def callbackCamera(x,y):
    print "x= "+x+" y= "+y
    pwmX.ChangeDutyCycle(x)
    pwmY.ChangeDutyCycle(y)
url = "10.33.28.197:8888/wsRPI"

data = GetData(url,callbackSpeed,callbackDirection,callbackCamera)
