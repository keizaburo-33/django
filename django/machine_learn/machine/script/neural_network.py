import numpy as np


class NeuralNetwork:
    def __init__(self, inodes, hnodes, onodes, lr=0.3):
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes
        self.lr = lr
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        self.sigmoid = lambda x: 1 / (1 + np.exp(-x))

    def train(self, inputs, targets):
        inputs = np.array(inputs, ndmin=2).T
        targets = np.array(targets, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.sigmoid(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.sigmoid(final_inputs)
        print((final_outputs-0.5)*128)

        outputs_errors = targets - final_outputs
        hidden_errors = np.dot(self.who.T, outputs_errors)

        self.who += self.lr * np.dot(
            (outputs_errors * final_outputs * (1 - final_outputs)), np.transpose(hidden_outputs))
        self.wih += self.lr + np.dot((hidden_errors * hidden_outputs * (1 - hidden_outputs)), np.transpose(inputs))

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.sigmoid(hidden_inputs)
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.sigmoid(final_inputs)

        return final_outputs
