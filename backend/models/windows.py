from utils.deep_utils import get_active_windows
from screen_reader import get_window_image
from ocr import get_char_name
import launcher
from models.process import Process

GAME_HANDLE = 'Rappelz'

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