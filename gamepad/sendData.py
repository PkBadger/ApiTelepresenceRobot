import requests

class SendData:
    def __init__(self,url):
        self.url = url

    def sendDirection(self,motorL,motorR):
        url = self.url+"/MotorDirection?motorL="+str(motorL)+"&motorR="+str(motorR)
        r = requests.get(url)

    def sendSpeed(self,motorL,motorR):
        url = self.url+"/MotorSpeed?motorL="+str(motorL)+"&motorR="+str(motorR)
        r = requests.get(url)

    def sendCameraAngle(self,x,y):
        url = self.url+"/cameraPos?X="+str(x)+"&Y="+str(y)
        r = requests.get(url)

    def sendSpeedAndDirection(self, motorL, motorR, dirL, dirR):
        url = self.url+"/movement?motorL="+str(motorL)+"&motorR="+str(motorR)+"&dirL="+str(dirL)+"&dirR="+str(dirR)
        r = requests.get(url)

