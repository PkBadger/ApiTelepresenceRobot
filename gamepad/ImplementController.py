from sendData import SendData
import evdev

direccion = True

device = evdev.InputDevice("/dev/input/event18")
print(device)
data = SendData("http://localhost:8888")
data.sendDirection(1,1)
for event in device.read_loop():
    #R2
    if(event.code == 5):
        print(event)
        if(not direccion):
            data.sendDirection(1,1)
            direccion = True
        data.sendSpeed(event.value,event.value)

    #L2
    if(event.code == 2):
        if(direccion):
            data.sendDirection(0,0)
            direccion= False
        print(event)
        data.sendSpeed(event.value,event.value)
    #Left Stick X
    if(event.code == 0 and event.type == 3):
        print(event)

data = SendData("http://localhost:8888")
#sendSpeed(motorL,motorR)
data.sendSpeed(100,100)
#sendDirection(motorL,motorR)
data.sendDirection(200,200)
#sendCameraAngle(x,y)
data.sendCameraAngle(80,30)
