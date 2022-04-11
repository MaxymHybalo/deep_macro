import logging
import serial
import random
from utils.singleton import Singleton
class SerialController(metaclass=Singleton):

    def __init__(self):
        self.id = random.randint(1, 1000)
        self.serial = None
        self.config = None

    def run_serial(self, config):
        self.config = config
        try:
            port = 'COM' + str(self.config['port'])
            baudrate = self.config['baudrate']
            logging.info('Trying connect to Arduino via {0}'.format(port))
            self.serial = serial.Serial(port, baudrate)
            self.serial.timeout = 0.01
            if self.serial.is_open:
                self.serial.close()
                logging.info('Serial closed at: {0}'.format(port))
            if not self.serial.is_open:
                self.serial.open()
                logging.info('Serial opened at: {0}'.format(port))
        except serial.SerialException:
            logging.error('Serial connection error')
            self.serial = None
