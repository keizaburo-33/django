from othello_learner import OthelloPlayer
from board import Board
import numpy as np

board = Board()
turn = 1
othello_player = OthelloPlayer(turn,start_read=8)
b=0
w=0
draw=0
board.play(40)
print(board.board)
print(np.diag(board.board,3))
# for i in range(30):
#     board.__init__(8)
#     othello_player.__init__(turn,start_read=8)
#     while True:
#         if not board.available_turn():
#             board.pss += 1
#             if board.pss == 2:
#                 break
#             continue
#         if board.turn == turn:
#             pos = othello_player.get_agent_put_pos(board.board, board.turn, board.pss)
#             board.put_stone(pos)
#             othello_player.evaluate(board.board)
#         else:
#             board.random_put()
#     winner,stone=board.get_winner()
#     if winner==1:
#         b+=1
#     elif winner==2:
#         w+=1
#     else:
#         draw+=1
#     print(stone)
#
# print(b,w,draw)