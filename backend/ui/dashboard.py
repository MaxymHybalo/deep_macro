from PyQt6.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import QProcess

from functools import partial

class DashboardWindow(QMainWindow):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.state = env['state']()
        print(env['state']())
        self.setWindowTitle("Rappelz Wizard")

        self.pidLabel = QLabel('PID')
        self.charNameLabel = QLabel('Name')
        self.typeLabel = QLabel('Type')
        self.actionLabel = QLabel('Action')


        layout = QGridLayout()
        layout.addWidget(self.pidLabel, 0, 0)
        layout.addWidget(self.charNameLabel, 0, 1)
        layout.addWidget(self.typeLabel, 0, 2)
        layout.addWidget(self.actionLabel, 0, 3)
        layout.addWidget(self.actionLabel, 0, 4)


        for index, handle in enumerate(self.state):
            print(self.state)
            layout.addWidget(QLabel(str(handle)))
            layout.addWidget(QLabel(str(self.state[handle]['char_name'])))
            layout.addWidget(QLabel(str(self.state[handle]['type'])))
            activate = QPushButton('Activate')
            activate.clicked.connect(partial(self.activate, handle))
            layout.addWidget(activate)

            deactivate = QPushButton('Deactivate')
            deactivate.clicked.connect(self.deactivate)
            layout.addWidget(deactivate)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def activate(self, handle):

        self.thread = QProcess()
        self.thread.start('python',  ['io.py'])

    def deactivate(self):
        self.thread.kill()