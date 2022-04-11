import logging
from utils.serial_controller import SerialController

class Key:
    
    COMMAND = b'K'
    RELEASE = b'Q'

    def __init__(self, key, pressed=None):
        self.key = key
        self.pressed = pressed
        self.log = logging.getLogger('key')

    def press(self, serial=SerialController()):
        if hasattr(serial, 'serial'):
            serial = serial.serial
        serial.write(self.COMMAND)
        
        if self.pressed is not None:
            serial.write(self.pressed.encode())
            return
        
        serial.write(self.key.encode())
        serial.write(self.RELEASE)
        self.log.debug('Press key: {0}'.format(self.key))

    def combination(self):
        self.press()
        self.pressed = None
        self.press()