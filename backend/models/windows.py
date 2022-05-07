from utils.deep_utils import get_active_windows
from screen_reader import get_window_image
from ocr import get_char_name

GAME_HANDLE = 'Rappelz'

class Windows():

    def __init__(self) -> None:
        self._instances = get_active_windows(GAME_HANDLE)
        self.instances = dict()
        self.set_state()

    def set_state(self):
        for handle in self._instances:
            self.instances[handle] = get_char_name(get_window_image(handle))