from PyQt6.QtWidgets import QPushButton

class WindowButton(QPushButton):

    def __init__(self, handle):
        super(WindowButton, self).__init__()
        self.setText('Image')
        self.clicked.connect(lambda: self._show_image(handle))
    
    def _show_image(self, handle):
        from screen_reader import get_window_image
        import cv2

        img = get_window_image(handle)
        cv2.imshow(str(handle), img)
        cv2.waitKey(0)