import launcher
from utils.configurator import Configurator

SETTINGS_FILE = 'configs/_commands'

class Settings():
    
    def __init__(self) -> None:
        self.types = [*launcher.operations]

        print(self.types)
    
    def save(self, data, instances):
        type, value, handle = data['type'], data['value'], data['handle']
        print('instances', instances)
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

    def launcher_config(self, name):
        settings = self.load(name)
        for type, v in settings.items():
            if v['value']['active'] == True:
                props = v['value']
                props['type'] = type
                return props
        return {}

    def load(self, name):
        config = Configurator(SETTINGS_FILE + '_' + name + '.yml')
        return config.import_config()

    def _disable_all(self, settings):
        print('disable', settings)
        if settings is None:
            return settings
        for key, value in settings.items():
            print('disable_all', key, value)
            if 'active' in value['value']:
                settings[key]['value']['active'] = False
        return settings