#!/usr/bin/python
#----------------------------------------------------------------------------#
# Author : Ameya Wagh
# Reference - https://www.youtube.com/watch?v=xouin83ebxE
#----------------------------------------------------------------------------#

import time
import random
import numpy as np
from geneticAlgorithm import geneticAlgorithm


class Board:

    def __init__(self, n=8):
        self.n = n
        self.board = np.array([[0 for i in range(self.n)]
                               for j in range(self.n)])
        self.sequence = []

    def printBoard(self):
        for row in self.board:
            print row

    def update(self, sequence):
        self.board = np.array([[0 for i in range(self.n)]
                               for j in range(self.n)])
        self.sequence = sequence
        for i in range(len(sequence)):
            self.board[:, i][sequence[i]] = 1

    def validate(self, sequence):
        fitness = 10.0
        # print self.board
        for col in range(self.n):
            row = sequence[col]
            
            right = False
            right_up = False
            right_down = False
            # print '\n'
            # print 'col:',col,'fitness:',fitness
            # print "curr:",self.board[row, col]
            if col < self.n-1:
                right = (self.board[row, col] == self.board[row, col+1])
                # print "right:",self.board[row, col+1]
                
                if row > 0:
                    right_up = (self.board[row, col] == self.board[row-1, col+1])
                    # print "right_up:",self.board[row-1, col+1]
                
                if row < self.n-1:
                    right_down = (self.board[row, col] == self.board[row+1, col+1])
                    # print "right_down:",self.board[row+1, col+1]
            
            if right or right_up or right_down:
                # print "col:",col,"row:",row,right,right_up,right_down
                fitness -= 1.0
        return fitness


if __name__ == '__main__':
    board = Board()

    ga = geneticAlgorithm(board.validate, genePool=range(8),
                          nGen=1000, nSize=20, pMutation=0.5, fitnessThres=10)
    [seq,fitnss] = ga.evolve()
    # seq=[4,2,3,0,5,6,7,1]
    print seq,fitnss
    board.update(seq)
    print board.validate(seq)
    board.printBoard()
    # print '>'
    
    # print board.board[4,:]
    # for i in range(8):
    #     print board.board[4,i]
