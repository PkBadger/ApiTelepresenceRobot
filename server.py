#importss
import tornado.ioloop
import tornado.web
import json
from tornado import gen, websocket
from tornado.options import define, options, parse_command_line

#------------------------------------#
# Arguments                          #
#------------------------------------#

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

#--------------------------------------#
#  Clients list raspberry and IOS      #
#--------------------------------------#
clRpi = []
clIOS = []
'''
class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.render("index.html")
'''

#---------------------------------------#
#Socket handlers for both devices       #
#---------------------------------------#

#Save Raspberry clients
class SocketRPIHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clRpi:
            clRpi.append(self)
        print(clRpi)

    def on_close(self):
        if self in clRpi:
            clRpi.remove(self)

#Save IOS clients
class SocketIOSHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clIOS:
            clIOS.append(self)
        print(clIOS)

    def on_close(self):
        if self in clIOS:
            clIOS.remove(self)

#--------------------------------#
# Motor control Handlers         #
#--------------------------------#

#Speed Control receive motorR and motorL
class SpeedHandler(websocket.WebSocketHandler):
    def get(self):
        motorR = self.get_argument("motorR")
        motorL = self.get_argument("motorL")
        data = {"action":"speed","motorR":motorR,"motorL":motorL}
        for c in clRpi:
            c.write_message(data)

    def post(self):
        pass

#Direcion control receive motorL and motorR
class DirectionHandler(websocket.WebSocketHandler):
    def get(self):
        motorR = self.get_argument("motorR")
        motorL = self.get_argument("motorL")
        data = {"action":"direction","motorR":motorR,"motorL":motorL}
        for c in clRpi:
            c.write_message(data)

    def post(self):
        pass
#---------------------------------#
# Sensor Handlers                 #
#---------------------------------#

class SwitchHandler(websocket.WebSocketHandler):
    def get(self):
        value = self.get_argument("value")
        data = {"action":"switch"}
        for c in clIOS:
            c.write_message(data)
    def post(self):
        pass

class TempHandler(websocket.WebSocketHandler):
    def get(self):
        value = self.get_argument("value")
        data = {"action":"temp","value":value}
        for c in clIOS:
            c.write_message(data)
    def post(self):
        pass

class SpeedSensorHandler(websocket.WebSocketHandler):
    def get(self):
        value = self.get_argument("value")
        data = {"action":"speed","value":value}
        for c in clIOS:
            c.write_message(data)
    def post(self):
        pass

#--------------------------------------#
#Camera Position handler               #
#--------------------------------------#

class CameraPosHandler(websocket.WebSocketHandler):
    def get(self):
        X = self.get_argument("X")
        Y = self.get_argument("Y")
        data = {"action":"camera","X":X,"Y":Y}
        for c in clRpi:
            c.write_message(data)

    def post(self):
        pass

#--------------------------------------#
# Main function                        #
#--------------------------------------#

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/wsRPI", SocketRPIHandler),
            (r"/wsIOS", SocketIOSHandler),
            (r"/temp", TempHandler),
            (r"/speedSensor", SpeedSensorHandler),
            (r"/MotorSpeed", SpeedHandler),
            (r"/MotorDirection",DirectionHandler),
            (r"/switch",SwitchHandler),
            (r"/cameraPos",CameraPosHandler),
            ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        xsrf_cookies=True,
        debug=options.debug,
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
