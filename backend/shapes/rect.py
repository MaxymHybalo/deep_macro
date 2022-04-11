from shapes.shape import Shape
from processes.click import Click
import cv2


DEFAULT_COLOR = (90, 200, 100)
DEFAULT_THINKNESS = 1


class Rect(Shape):

    def __init__(self, rect, shape=None):
        self.rect = rect
        if shape is None:
            super().__init__(DEFAULT_COLOR, DEFAULT_THINKNESS)
        else:
            super().__init__(shape.color, shape.thinkness)

    def click(self):
        x, y, w, h = self.rect
        return Click(x+w/2, y+h/2, process='dclick')

    def draw(self, image):
        if self.rect:
            x, y, w, h = self.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), self.color, self.thinkness)

    def center(self):
        x, y, w, h = self.rect
        return int(x + w / 2), int(y + h / 2)