from sendData import SendData
data = SendData("http://localhost:8888")
#sendSpeed(motorL,motorR)
data.sendSpeed(100,100)
#sendDirection(motorL,motorR)
data.sendDirection(200,200)
#sendCameraAngle(x,y)
data.sendCameraAngle(80,30)
