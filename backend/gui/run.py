from distutils.debug import DEBUG
import sys
from PyQt6.QtWidgets import QApplication
from gui.deep_window import DeepWindow


def init():
    app = QApplication(sys.argv)
    window = DeepWindow()
    window.show()
    app.exec()