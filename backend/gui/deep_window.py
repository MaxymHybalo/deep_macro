from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from models.windows import Windows
from gui.char_layout import CharLayout
class DeepWindow(QMainWindow):

    def __init__(self):
        super(DeepWindow, self).__init__()
        self.setWindowTitle('Deep Macro')
        container = QWidget()
        container.setLayout(CharLayout())
        self.setCentralWidget(container)
