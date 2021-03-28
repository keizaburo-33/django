from othello_learner import OthelloPlayer
from board import Board
from neural_network import NeuralNetwork
import numpy as np

board = Board()
othello_learner = OthelloPlayer()
inputs = othello_learner.evaluate(board.board)
nn = NeuralNetwork(19, 50, 1, 0.3)


def calc(c):
    return 0.5 + c / 128


def calcstonefromsigmoid(x):
    return (x - 0.5) * 128


print(inputs)
d = calc(-50)
b = calcstonefromsigmoid(d)
for i in range(10000):
    nn.train(inputs, d)
x = nn.query(inputs)
ans = calcstonefromsigmoid(x)
print(ans)
