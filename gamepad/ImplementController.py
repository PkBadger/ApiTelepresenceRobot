from sendData import SendData
import evdev
import argparse
from threading import Thread
from processor import get_directions, get_directions2, translate_grades

class Controller(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setup()

    def get_gamepad(self):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if "Gamepad" in device.name:
                self.gamepad = evdev.InputDevice(device.fn)
                return

    def build_package(self, data):
        r2, l2, axis_x, axis_y = data
        package = {"l2": l2, "r2": r2, "axis_x": axis_x, "axis_y": axis_y}
        return package

    def setup(self):
        self.direccion = True
        self.get_gamepad()

        parser = argparse.ArgumentParser()
        parser.add_argument("-j", "--julian", action="store_true")
        parser.add_argument("-c", "--cesar", action="store_true")
        self.args = parser.parse_args()
        self.data_package = self.build_package((0,0,0,0))

        self.sender = Sender()
        self.sender.start()
        print "Thread Controller running with gamepad %s\n" % self.gamepad

    def run(self):
        toggleLights = 0
        for event in self.gamepad.read_loop():
            #R2
            if(event.code == 5):
                self.data_package["r2"] = int(event.value)
                if self.args.cesar:
                    self.sender.send(get_directions2(self.data_package["axis_x"],self.data_package["axis_y"],self.data_package["r2"]))
                else:
                    #holder = self.data_package["r2"]
                    self.sender.send(get_directions(self.data_package["axis_x"],
                    self.data_package["l2"], self.data_package["r2"]))

            #L2
            elif(event.code == 2):
                self.data_package["l2"] = int(event.value)
                if self.args.cesar:
                    self.sender.send(get_directions2(self.data_package["axis_x"],self.data_package["axis_y"],self.data_package["r2"]))
                else:
                    self.sender.send(get_directions(self.data_package["axis_x"],
                    self.data_package["l2"], self.data_package["r2"]))
                    #holder = -self.data_package["l2"]
                    #self.sender.send(get_directions(self.data_package["axis_x"], -self.data_package["l2"]))

            #D-Pad Y
            elif(event.code == 17):
                if event.value == -1:
                    toggleLights = 0 if toggleLights == 1 else 1
                    self.sender.sendLights(toggleLights)
                else:
                    pass

            #Left Stick X
            elif(event.code == 0 and event.type == 3):
                self.data_package["axis_x"] = translate_grades(event.value, 'x')
                if self.args.julian:
                    #self.sender.send(get_directions(self.data_package["axis_x"], holder))
                    self.sender.send(get_directions(self.data_package["axis_x"],
                    self.data_package["l2"], self.data_package["r2"]))
                elif self.args.cesar:
                    self.sender.send(get_directions2(self.data_package["axis_x"],self.data_package["axis_y"],self.data_package["r2"]))
                else:
                    self.sender.send(self.data_package)

            #Left Stick Y
            elif(event.code == 1 and event.type == 3):
                self.data_package["axis_y"] = translate_grades(event.value, 'y')
                if self.args.julian:
                    pass
                    #self.sender.send(get_directions(self.data_package["axis_x"], holder))
                    #self.sender.send(get_directions(self.data_package["axis_x"], self.data_package["l2"], self.data_package["r2"))
                elif self.args.cesar:
                    self.sender.send(get_directions2(self.data_package["axis_x"],self.data_package["axis_y"],self.data_package["r2"]))
                else:
                    self.sender.send(self.data_package)

            else:
                continue

class Sender(Thread):
    def __init__(self):
        Thread.__init__(self)
        ip, port = "localhost", 8888
        self.data = SendData("http://" + ip + ":" + str(port))

    def run(self):
        print "Thread Sender running...\n"

    def send(self, values):
        motorL, motorR = values['left_val'], values['right_val']
        directionL, directionR = values['to_left'], values['to_right']
        print(values)
        self.data.sendSpeedAndDirection(motorL, motorR, directionL, directionR)

    def sendLights(self, toggle):
        print(toggle)
        self.data.sendLights(toggle)

if __name__ == '__main__':
    controller_thread = Controller()
    controller_thread.start()
