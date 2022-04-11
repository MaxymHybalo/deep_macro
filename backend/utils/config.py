import logging
from utils.singleton import Singleton
from utils.configurator import Configurator

class Config(metaclass=Singleton):
    
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger('config')
        self.mode = 'test'
    
    def load_config(self, config):
        if not hasattr(self, 'config'):
            self.log.info('load config')
            self.config = Configurator(config).from_yaml()

    def isWorks(self):
        return self.mode == 'enabled'
    
    def disable(self):
        self.mode = 'disabled'

    def enable(self):
        self.mode = 'enabled'

    def initialize_configs(self, config):
        import jobs.helpers.configs as markers
        import sys
        
        config = Configurator(config).from_yaml()
        
        for c in config['templates']:
            setattr(self, c['name'], getattr(sys.modules['jobs.helpers.configs'], c['name']))
            for field, value in c.items():
                if field is not 'name':
                    setattr(getattr(self, c['name']), field, value)
