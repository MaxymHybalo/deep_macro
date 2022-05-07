from PyQt6.QtWidgets import QGridLayout, QLabel
from models.windows import Windows
from gui.window_button import WindowButton

class CharLayout(QGridLayout):
    def __init__(self):
        super(CharLayout, self).__init__()
        self.windows = Windows()
        self.build()
    
    def build(self):
        for i, instance in enumerate(self.windows.instances):
            handle = instance
            name = self.windows.instances[handle]
            name_label = QLabel()
            name_label.setText(name)
            handle_label = QLabel()
            handle_label.setText(str(handle))
            self.addWidget(name_label, i, 0)
            self.addWidget(handle_label, i, 1)
            self.addWidget(WindowButton(instance), i, 2)