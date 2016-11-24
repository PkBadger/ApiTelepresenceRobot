import websocket
import thread
import time
import json

#-------------------------------------------------#
# Client class that will be conected to tornado   #
#-------------------------------------------------#
class Client:
    def __init__(self,url,callback):
        websocket.enableTrace(True)
        urlString = "ws://" + url
        print(urlString)
        ws = websocket.WebSocketApp(urlString,
                                    on_message = callback,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        ws.run_forever()




    def on_error(self,ws, error):
        print error

    def on_close(self,ws):
        print "### closed ###"

#-----------------------------------------#
# Class for data translation              #
#-----------------------------------------#

class GetData:
    def __init__(self,url,dirSpeed,camera,light,brake):
        self.DirSpeed = dirSpeed
        self.camera = camera
        client = Client(url,self.on_message)

    def on_message(self,ws,message):
        message = json.loads(message)
        if(message["action"] == "movement"):
            self.DirSpeed(message["motorL"],message["motorR"],message["dirL"],message["dirR"])
        if(message["action"] == "camera"):
            self.camera(message["X"],message["Y"])
        if(message["action"] == "light"):
            self.light(message["light"])
