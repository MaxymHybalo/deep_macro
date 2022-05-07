from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from models.windows import Windows

class DeepWindow(QMainWindow):

    def __init__(self):
        super(DeepWindow, self).__init__()
        self.setWindowTitle('Deep Macro')
        # print(Windows().instances)
        widget = self.add_active_char_state(Windows().instances)
        self.setCentralWidget(widget)

    def add_active_char_state(self, instances):
        container = QWidget()
        layout = QGridLayout()

        for i, instance in enumerate(instances):
            handle = instance
            name = instances[handle]
            name_label = QLabel()
            name_label.setText(name)
            handle_label = QLabel()
            handle_label.setText(str(handle))
            layout.addWidget(name_label, i, 0)
            layout.addWidget(handle_label, i, 1)
            button = self._window_img_button(handle)
            layout.addWidget(button, i, 3)
        container.setLayout(layout)
        return container
    
    def _window_img_button(self, handle):
        button = QPushButton('Image')
        button.clicked.connect(lambda: self._show_image(handle))
        return button

    def _show_image(self, handle):
        print('cliked', self)
        from screen_reader import get_window_image
        import cv2

        img = get_window_image(handle)
        cv2.imshow(str(handle), img)
        cv2.waitKey(0)