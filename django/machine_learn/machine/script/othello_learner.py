import copy
import sys
import random
import numpy as np

sys.setrecursionlimit(10000)


class OthelloPlayer:
    def __init__(self, turn=1, size=8, start_read=8):
        self.turn = turn
        self.read_his = None
        self.start_read = start_read
        self.directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1],
        ]
        self.black = 1
        self.white = 2
        self.blank = 0
        self.size = size

    @staticmethod
    def turn_change(turn):
        turn = 1 if turn == 2 else 2
        return turn

    @staticmethod
    def get_flatten_board(board):
        x = list(board.flatten())
        x = [str(int(k)) for k in x]
        x = ''.join(x)
        return x

    def is_inside(self, y, x):
        return 0 <= y <= self.size - 1 and 0 <= x <= self.size - 1

    def is_available(self, pos, board_copy, turn):
        y = pos[0]
        x = pos[1]
        if board_copy[y][x] != self.blank:
            return False
        opp = self.black if turn == self.white else self.white
        for direction in self.directions:
            yy = y
            xx = x
            s = direction[0]
            t = direction[1]
            yy += s
            xx += t
            if not self.is_inside(yy, xx):
                continue
            if board_copy[yy][xx] != opp:
                continue
            while True:
                yy += s
                xx += t
                if not self.is_inside(yy, xx):
                    break
                if board_copy[yy][xx] == self.blank:
                    break
                if board_copy[yy][xx] == turn:
                    return True
        return False

    def search_available(self, board_copy, turn):
        pos_list = np.where(board_copy == self.blank)
        return [[y, x] for y, x in zip(pos_list[0], pos_list[1]) if self.is_available([y, x], board_copy, turn)]

    def put_stone(self, pos, board_copy, turn):
        y = pos[0]
        x = pos[1]
        board_copy[y][x] = turn
        opp = self.black if turn == self.white else self.white
        for direction in self.directions:
            yy = y
            xx = x
            s = direction[0]
            t = direction[1]
            yy += s
            xx += t
            if not self.is_inside(yy, xx):
                continue
            if board_copy[yy][xx] != opp:
                continue
            reverse_list = [[yy, xx]]
            flag = False
            while True:
                yy += s
                xx += t
                if not self.is_inside(yy, xx):
                    break
                if board_copy[yy][xx] == self.blank:
                    break
                if board_copy[yy][xx] == turn:
                    flag = True
                    break
                reverse_list.append([yy, xx])
            if flag:
                for reverse_pos in reverse_list:
                    board_copy[reverse_pos[0]][reverse_pos[1]] = turn
        return board_copy

    def get_stone_count(self, board):
        black_count = len(np.where(board == self.black)[0])
        white_count = len(np.where(board == self.white)[0])
        return black_count - white_count

    @staticmethod
    def get_max_of_turn(ll, turn):
        n = max(ll) if turn == 1 else min(ll)
        return n

    @staticmethod
    def get_flatten_board_str_with_turn(board, turn):
        return ''.join([str(int(k)) for k in np.append(board, turn).flatten()])

    def read_all(self, board_copy, turn, pss):
        board_copy = copy.deepcopy(board_copy)
        score_dict = {}

        def read(new_board, new_turn, new_pss):
            available_list = self.search_available(new_board, new_turn)
            if len(available_list) == 0:
                new_pss += 1
                if new_pss == 2:
                    stone_count = self.get_stone_count(new_board)
                    score_dict.update({self.get_flatten_board_str_with_turn(new_board, new_turn): stone_count})
                    return stone_count
                score = read(new_board, self.turn_change(new_turn), new_pss)
                score_dict.update({self.get_flatten_board_str_with_turn(new_board, new_turn): score})
                return score
            score_list = []
            for pos in available_list:
                new_board_copy = copy.deepcopy(new_board)
                new_board_copy = self.put_stone(pos, new_board_copy, new_turn)
                next_turn = self.turn_change(new_turn)
                new_flatten_turn_board = self.get_flatten_board_str_with_turn(new_board_copy, next_turn)
                if new_flatten_turn_board in score_dict:
                    score_list.append(score_dict[new_flatten_turn_board])
                    continue
                score_list.append(read(new_board_copy, next_turn, 0))
            max_stone_count = self.get_max_of_turn(score_list, new_turn)
            score_dict.update({self.get_flatten_board_str_with_turn(new_board, new_turn): max_stone_count})

            return max_stone_count

        read(board_copy, turn, pss)
        return score_dict

    def get_agent_put_pos(self, board, turn, pss):
        if len(np.where(board == 0)[0]) <= self.start_read:
            if self.read_his is None:
                self.read_his = self.read_all(board, turn, pss)
            pos, max_count = self.get_max_pos_from_read_his(board, turn)
            winner_str = "引き分け"
            if max_count > 0:
                winner_str = "黒の勝ち"
            elif max_count < 0:
                winner_str = "白の勝ち"
            print(f"{winner_str}:{max_count}")
            return pos
        return random.choice(self.search_available(board, turn))

    def get_max_pos_from_read_his(self, board, turn):
        ll = []
        pos_list = self.search_available(board, turn)
        for pos in pos_list:
            board_copy = copy.deepcopy(board)
            board_copy = self.put_stone(pos, board_copy, turn)
            board_copy = self.get_flatten_board_str_with_turn(board_copy, self.turn_change(turn))
            ll.append(self.read_his[board_copy])
        max_score = self.get_max_of_turn(ll, turn)
        return pos_list[ll.index(max_score)], max_score

    # ここから評価関数用のパラメータ
    # 何手目かを取得
    @staticmethod
    def get_num(board):
        return (64 - len(np.where(board == 0)[0])) / 64 + 0.01

    # 自分の石の数
    def get_my_stone_count(self, board):
        return len(np.where(board == self.turn)[0])

    # 相手の石の数
    def get_opp_stone_count(self, board):
        turn = 1 if self.turn == 2 else 2
        return len(np.where(board == turn)[0])

    # 着手可能数
    def get_my_available_count(self, board):
        return len(self.search_available(board, self.turn)) / 10 * 0.99 + 0.01

    # 4隅の形
    def get_shape_of_corner(self, board):
        opp = 1 if self.turn == 2 else 2
        board = np.copy(board)
        np.place(board, board == self.turn, 1)
        np.place(board, board == opp, -1)
        corner1 = board[0:2, 0:2]
        corner2 = board[0:2, 6:8]
        corner3 = board[6:8, 0:2]
        corner4 = board[6:8, 6:8]
        return np.array([corner1, corner2, corner3, corner4]).reshape(-1) * 0.99 + 0.01

    def evaluate(self, board):
        eval_array = np.array(
            [self.get_num(board), (self.get_my_stone_count(board) - self.get_opp_stone_count(board)) / 20 * 0.99 + 0.01,
             self.get_my_available_count(board)])
        eval_array = np.concatenate([self.get_shape_of_corner(board), eval_array])
        eval_array = np.array(eval_array).flatten()
        return eval_array

    def get_pattern(self,board,turn):
        opp = 1 if turn == 2 else 2
        board = np.copy(board)
        np.place(board, board == turn, 1)
        np.place(board, board == opp, -1)
        eval_array=np.array([])
        np.diag(board)


    # diag4

