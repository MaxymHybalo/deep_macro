from utils.configurator import Configurator
from enhancer.inventory import Inventory
from enhancer.tasks.enhancer import Enhancer
from enhancer.tasks.unpacker import Unpacker
from enhancer.tasks.destructor import Destructor
from enhancer.tasks.awakening import Awakening
from enhancer.tasks.combinator import Combinator
from enhancer.tasks.searcher import Searcher
from enhancer.tasks.keeper import Keeper

class InventoryDispatcher:

    def __init__(self, config, cfg):
        if type(config) is dict:
            self.config = config
        else:
            self.config = Configurator(config).from_yaml()
        self.handle = cfg['handle']
        self.inventory = Inventory(self.config, cfg)
        self.config['enhancement']['cycles'] = cfg['cycles'] if 'cycles' in cfg else self.config['enhancement']['cycles']
        self.enhancers_setup = {
            'options': self.config['enhancement'],
            'assets': self.config['recognize'],
            'mode': self.config['mode'],
            'config': cfg
        }

    def refresh(self):
        self.inventory = Inventory(self.config, cfg)

    def enhance(self):
        print('Window:')
        Enhancer(self.enhancers_setup, self.inventory).proceed()

    def unpack(self):
        Unpacker(self.enhancers_setup, self.inventory).proceed()
    
    def destroy(self):
        Destructor(self.enhancers_setup, self.inventory).proceed()

    def awake(self):
        Awakening(self.enhancers_setup, self.inventory).proceed()

    def combinate(self):
        Combinator(self.enhancers_setup, self.inventory).proceed()

    def search(self):
        Searcher(self.enhancers_setup, self.inventory).proceed()

    def keeper(self):
        Keeper(self.enhancers_setup, self.inventory).proceed()
