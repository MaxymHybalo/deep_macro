import launcher
from utils.configurator import Configurator

SETTINGS_FILE = 'configs/_commands'

class Settings():
    
    def __init__(self) -> None:
        self.types = [*launcher.operations]

        print(self.types)
    
    def save(self, data, instances):
        type, value, handle = data['type'], data['value'], data['handle']

        name = list(instances.keys())[list(instances.values()).index(handle)]

        config = Configurator(SETTINGS_FILE + '_' + name + '.yml')
        settings = config.import_config()

        if 'active' in value:
            settings = self._disable_all(settings)

        if settings == None:
            settings = dict()

        if type in settings:
            settings[type]['value'] = value
        else:
            value = value or {}
            settings[type] = dict({'value': { **value}})
        config.dump_yaml(settings)
        
        return settings


    def _disable_all(self, settins):
        for key, value in settins.items():
            print('disable_all', key, value)
            if 'active' in value['value']:
                settins[key]['value']['active'] = False
        return settins