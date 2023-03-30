import sys
from PyQt6.QtWidgets import QApplication

from launcher import clients_state, run
from ui.dashboard import DashboardWindow
app = QApplication(sys.argv)

window = DashboardWindow({
    'state': clients_state,
    'run': run
    })
window.show()

app.exec()
