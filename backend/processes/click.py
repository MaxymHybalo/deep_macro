import pyautogui as ui
from processes.wait import Wait

CLICK = b'C'

class Click:

    def __init__(self, x, y, process='click', delay=0):
        self.x = x
        self.y = y
        self.process = process
        self.delay = delay

    # param click mean Click instance
    def make_click(self, serial=None):
        # Move().moveTo(self.x, self.y)
        # serial.write(CLICK)
        double = self.process == 'dclick' or self.process == 'double'
        clicks = 2 if double else 1
        print('DOUBLE', double, clicks)
        ui.moveTo(self.x, self.y)
        ui.click(clicks = clicks)
        Wait(self.delay).delay()

    
    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)