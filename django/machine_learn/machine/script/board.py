import numpy as np


class Board:
    def __init__(self, size=8):
        self.size = size
        self.board = np.zeros((self.size, self.size))
        self.black = 1
        self.white = 2
        self.blank = 0
        mid = int(self.size / 2)
        self.board[mid - 1][mid] = self.black
        self.board[mid][mid - 1] = self.black
        self.board[mid - 1][mid - 1] = self.white
        self.board[mid][mid] = self.white
        self.turn = 1
        self.pss = 0
        self.directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1],
        ]

    def turn_change(self):
        self.turn = self.black if self.turn == self.white else self.white

    def is_inside(self, y, x):
        return 0 <= y <= self.size - 1 and 0 <= x <= self.size - 1

    def num_to_pos(self, num):
        num = int(num)
        return [int(num / self.size), num % self.size]

    def is_available(self, pos):
        y = pos[0]
        x = pos[1]
        if self.board[y][x] != self.blank:
            return False
        opp = self.black if self.turn == self.white else self.white
        for direction in self.directions:
            yy = y
            xx = x
            s = direction[0]
            t = direction[1]
            yy += s
            xx += t
            if not self.is_inside(yy, xx):
                continue
            if self.board[yy][xx] != opp:
                continue
            while True:
                yy += s
                xx += t
                if not self.is_inside(yy, xx):
                    break
                if self.board[yy][xx] == self.blank:
                    break
                if self.board[yy][xx] == self.turn:
                    return True
        return False

    def search_available(self):
        pos_list = np.where(self.board == self.blank)
        return [[y, x] for y, x in zip(pos_list[0], pos_list[1]) if self.is_available([y, x])]

    def put_stone(self, pos):
        y = pos[0]
        x = pos[1]
        self.board[y][x] = self.turn
        opp = self.black if self.turn == self.white else self.white
        for direction in self.directions:
            yy = y
            xx = x
            s = direction[0]
            t = direction[1]
            yy += s
            xx += t
            if not self.is_inside(yy, xx):
                continue
            if self.board[yy][xx] != opp:
                continue
            reverse_list = [[yy, xx]]
            flag = False
            while True:
                yy += s
                xx += t
                if not self.is_inside(yy, xx):
                    break
                if self.board[yy][xx] == self.blank:
                    break
                if self.board[yy][xx] == self.turn:
                    flag = True
                    break
                reverse_list.append([yy, xx])
            if flag:
                for reverse_pos in reverse_list:
                    self.board[reverse_pos[0]][reverse_pos[1]] = self.turn
        self.pss = 0
        self.turn_change()

    def end_check(self):
        return self.pss == 2 or len(np.where(self.board == self.blank)[0]) == 0

    def get_flatten_board(self):
        x = list(self.board.flatten())
        x = [str(int(k)) for k in x]
        x = ''.join(x)
        return x
