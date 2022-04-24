from utils.configurator import Configurator
from enhancer.inventory import Inventory
from enhancer.tasks.enhancer import Enhancer
from enhancer.tasks.unpacker import Unpacker
from enhancer.tasks.destructor import Destructor
class InventoryDispatcher:
    
    def __init__(self, config, cfg):
        if type(config) is dict:
            self.config = config
        else:
            self.config = Configurator(config).from_yaml()
        self.handle = cfg['handle']
        self.inventory = Inventory(self.config, cfg)
        self.config['enhancement']['cycles'] = cfg['cycles']
        self.enhancers_setup = {
            'options': self.config['enhancement'],
            'assets': self.config['recognize'],
            'mode': self.config['mode']
        }

    def enhance(self):
        print('Window:')
        Enhancer(self.enhancers_setup, self.inventory).proceed()

    def unpack(self):
        Unpacker(self.enhancers_setup, self.inventory).proceed()
    
    def destroy(self):
        Destructor(self.enhancers_setup, self.inventory).proceed()
