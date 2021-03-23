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
        self.directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1],           [0, 1],
            [1, -1], [1, 0], [1, 1],
        ]

    def putstone(self,pos):
        pos=(int(pos))
        x=int(pos/8)
        y=pos%8
        self.board[x][y]=1

    def get_flatten_board(self):
        x=list(self.board.flatten())
        x=[str(int(k)) for k in x]
        x=''.join(x)
        return x