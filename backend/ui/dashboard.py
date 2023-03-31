from PyQt6.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import QProcess

from functools import partial

class DashboardWindow(QMainWindow):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.state = env['state']()
        self.threads = dict()
        # print(env['state']())
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


        for handle in enumerate(self.state):
            print(self.state)
            layout.addWidget(QLabel(str(handle)))
            layout.addWidget(QLabel(str(self.state[handle]['char_name'])))
            layout.addWidget(QLabel(str(self.state[handle]['type'])))
            
            activate = QPushButton('Activate')

            deactivate = QPushButton('Deactivate')
            deactivate.setEnabled(False)

            activate.clicked.connect(partial(self.activate, handle, self.state[handle]['char_name'], deactivate))
            deactivate.clicked.connect(partial(self.deactivate, handle, activate))
            
            layout.addWidget(activate)
            layout.addWidget(deactivate)

        enableAllButton = QPushButton('Activate All')
        enableAllButton.clicked.connect(self.enable_all)

        killAllButton = QPushButton('Disable All')
        killAllButton.clicked.connect(self.kill_all)
        
        layout.addWidget(enableAllButton, layout.rowCount() -1, 3)
        layout.addWidget(killAllButton, layout.rowCount() -1 , 4)

        self.layout = layout
        container = QWidget()
        container.setLayout(layout)

        
        self.setCentralWidget(container)

    def activate(self, handle, char_name, deactivate):
        sender = self.sender()
        thread = QProcess()
        thread.start('python',  ['invoke.py', str(handle), char_name])
        deactivate.setEnabled(True)
        sender.setEnabled(False)
        self.threads[handle] = thread

    def deactivate(self, handle, activate):
        sender = self.sender()
        self.threads[handle].kill()
        activate.setEnabled(True)
        sender.setEnabled(False)

    def enable_all(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget.text().lower() == 'activate':
                widget.clicked.emit()

    def kill_all(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget.text().lower() == 'activate':
                widget.setEnabled(True)
            if widget.text().lower() == 'deactivate':
                widget.setEnabled(False)
            
        for handle in self.threads:
            self.threads[handle].kill()