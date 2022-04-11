
from enhancer.grid_identifier import SIZE

class Finder:

    def __init__(self):
        super().__init__()
        self.cols, self.rows = SIZE
        self.matrix = []
        count = 0
        for row in range(self.rows):
            self.matrix.append([])
            for col in range(self.cols):
                self.matrix[row].append(count)
                count += 1
    
    def by_id(self, x, y):
        return self.matrix[y][x]

    def point(self, point):
        from shapes.window import Window
        xy = point[:2]
        xy = Window().relative(xy)
        if len(point) is 4:
            return [*xy, *point[2:]]
        return list(xy)