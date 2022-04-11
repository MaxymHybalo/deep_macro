from processes.click import Click


# cells in constructor expects list from two cell
class CombinationFlow:

    def __init__(self,cells, config):
        self.config = config
        self.cells = cells
        self.ONE = tuple(config['one_point'])


    def get_flow(self):
        return [
            Click(self.cells[0][0], self.cells[0][1], process='dclick'),
            # self.__select_count(5),
            # Click(676, 403),
            self.__select_count(2),
            self.__select_count(8),
            self.__select_count(0),
            Click(self.config['dial_ok'][0], self.config['dial_ok'][1]),
            Click(self.cells[1][0], self.cells[1][1], process='dclick'),
            self.__select_count(7),
            self.__select_count(0),
            Click(self.config['dial_ok'][0], self.config['dial_ok'][1]),
            Click(self.config['enhance'][0], self.config['enhance'][1], delay=1)
        ]

    def __select_count(self, digit):
        point = self.__combination_digit_grid(digit)
        return Click(point[0], point[1])

    def __combination_digit_grid(self, digit):
        one = list(self.ONE)
        delta = 20
        if digit > 3:
            one[1] -= delta
        if digit > 6:
            one[1] -= delta
        if digit in [8, 5, 2]:
            one[0] += delta
        if digit in [9, 6, 3]:
            one[0] += delta
            print(one)
        if digit == 0:
            return self.config['zero_point']
        return one
