from urllib import response
from utils.configurator import Configurator
from utils.deep_utils import get_active_windows
from screen_reader import get_window_image
from ocr import get_char_name
import launcher
from models.process import Process

GAME_HANDLE = 'Rappelz'
SETTINGS_FILE = 'configs/_commands'

class Windows():

    def __init__(self) -> None:
        self._instances = get_active_windows(GAME_HANDLE)
        self.instances = dict()
        self.processes = dict()
        self.set_state()

    def set_state(self):
        for handle in self._instances:
            name = get_char_name(get_window_image(handle))
            self.instances[name] = handle

    def run(self, handle):
        process = launcher.run(handle)
        self.processes[handle] = Process(process)
        return self.processes[handle].jsonify()

    def tasks(self):
        # returns all runned proceses
        pass
    
    def stop(self, handle):
        process = self.processes[handle]
        process.stop()
        process.destroy()

        return process.jsonify()

    def set_prop(self, data):
        type, value, handle = data['type'], data['value'], data['handle']

        name = list(self.instances.keys())[list(self.instances.values()).index(handle)]

        config = Configurator(SETTINGS_FILE + '_' + name + '.yml')
        settings = config.import_config()
        if settings == None:
            settings = dict()

        if type in settings:
            settings[type]['value'] = value
        else:
            value = value or {}
            settings[type] = dict({'value': { **value}})
        
        config.dump_yaml(settings)

    def settings(self):
        response = dict()
        for handle in self.instances.keys():
            config = Configurator(SETTINGS_FILE + '_' + handle + '.yml')
            settings = config.import_config()
            response[handle] = settings or dict()
            response[handle]['process_id'] = self.instances[handle]
        return response