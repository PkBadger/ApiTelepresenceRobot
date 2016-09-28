from client import GetData

def callbackSpeed(motorL,motorR):
    print "speed "+motorR +" "+ motorL
def callbackDirection(motorL,motorR):
    print "direction "+motorR +" "+ motorL
def callbackCamera(x,y):
    print "x= "+x+" y= "+y
url = "localhost:8888/wsRPI"

data = GetData(url,callbackSpeed,callbackDirection,callbackCamera)
