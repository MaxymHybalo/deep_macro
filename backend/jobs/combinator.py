import logging
from utils.configurator import Configurator
from processes.click import Click
from processes.key import Key
from processes.wait import Wait


class Combinator:

    def __init__(self, config):
        self.log = logging.getLogger('combinator')
        self.config = config
        self.config = self.config['combination']
        
    def process(self):
        cycles = int(self.config['cycles'])
        print(self.config)
        for i in range(cycles):
            self.round = i
            self.combinate()
        self.log.debug('End Combination process')

    def combinate(self):
        x,y = self.config['cell_0']
        Click(x, y, delay=0.5, process='dclick').make_click()
        self.write_code(self.config[self.config['mode']])
        Key('E').press()
        Wait(1).delay()
        x,y = self.config['cell_1']
        Click(x, y, delay=0.5, process='dclick').make_click()
        self.write_code(self.config['partials'])
        Key('E').press()
        x,y = self.config['enhance']
        Click(x, y, delay=1).make_click()
    
    def write_code(self, sequence):
        for s in sequence:
            Key(str(s)).press()


# add to config

# combination:
#   armor: [2, 8, 0]
#   atack: [5, 6, 0]
#   cell_0: [429, 449]
#   cell_1: [467, 448]
#   cycles: 10
#   enhance: [339, 490]
#   mode: armor
#   partials: [7, 0]