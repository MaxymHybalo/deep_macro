from utils.serial_controller import SerialController

class Process:

    def __init__(self, config):
        self.config = config
    
    def run_serial(self):
        return SerialController().serial
        # try:
        #     port = 'COM' + str(self.config['port'])
        #     baudrate = self.config['baudrate']
        #     logging.critical('Trying connect to Arduino via {0}'.format(port))
        #     s = serial.Serial(port, baudrate)
        #     s.timeout = 0.01
        #     if s.is_open:
        #         s.close()
        #         logging.info('Serial closed at: {0}'.format(port))
        #     if not s.is_open:
        #         s.open()
        #         logging.info('Serial opened at: {0}'.format(port))
        # except serial.SerialException:
        #     logging.critical('Serial connection error')
        #     s = None
        # return s