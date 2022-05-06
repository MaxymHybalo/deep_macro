# from ocr import get_awaking
# from utils import awaking_aggregator, reporter
# from driver import send
# if __name__ == '__main__':
    # res = awaking_aggregator.normalize(get_awaking())
    # comp = awaking_aggregator.compare(res, 'configs/stats_set_1.yml')
    # print(res)
    # print('comparation:', comp)
    # file = 'reports/test.csv'
    # reporter.initialize('awaking', file)

    # reporter.report('awaking', file, (0, res, comp, 'test file name'))


from PyQt6.QtWidgets import QApplication, QWidget

import sys # Только для доступа к аргументам командной строки

app = QApplication(sys.argv)

window = QWidget()
window.show()  # Важно: окно по умолчанию скрыто.

app.exec()