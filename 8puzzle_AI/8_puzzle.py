#!/usr/bin/python

#-------------------------------------------------#
# Name: Ameya Wagh
# Reference:
# https://www.codeproject.com/Articles/365553/Puzzle-solving-using-the-A-algorithm-using-Pytho
#-------------------------------------------------#
from random import randint
from solver import *

class EightPuzzle():
    def __init__(self):
        '''
        An 8 puzzle game environment
        '''
        self.board = range(1,9)+[0]
        self.pos = self.board.index(0)
        self.shuffleBoard(5)
        self.goalState = range(1,9)+[0]
        self.state = tuple(self.board)

    def printNode(self):
        for offset in range(0,9,3):
            print self.state[offset:offset+3]

    def shuffleBoard(self,n):
        # shuffle board n times
        while n:
            self.action(randint(1,4))
            n-=1

    def action(self,action):
        '''
            Action is 1-up,2-left,3-right,4-down
        '''
        temp=0
        # move up
        if action == 1:
            if (self.pos-3)>=0:
                temp = self.board[self.pos-3]
                self.pos=self.pos-3
                self.board[self.pos]=0
                self.board[self.pos+3]=temp

        
        # move left
        elif action == 2:
            if (self.pos-1)>=0:
                temp = self.board[self.pos-1]
                self.pos=self.pos-1
                self.board[self.pos]=0
                self.board[self.pos+1]=temp
        
        # move right
        elif action == 3:
            if (self.pos+1)<=8:
                temp = self.board[self.pos+1]
                self.pos=self.pos+1
                self.board[self.pos]=0
                self.board[self.pos-1]=temp
        
        # move down
        elif action == 4:
            if (self.pos+3)<=8:
                temp = self.board[self.pos+3]
                self.pos=self.pos+3
                self.board[self.pos]=0
                self.board[self.pos-3]=temp

#---------------------------------------------------------------------#
class Node():
    
    def __init__(self,_board,initState,action):
        self.goalState = range(1,9)+[0]
        # print 'gAction',action
        # print 'oldboard',board
        self.board = self.action(action,_board)
        # print 'newboard',self.board
        self.pos = self.board.index(0)
        self.parent = None
        # self.shuffleBoard(10)
        self.initState = initState
        self.state = tuple(self.board)
        self.f=0
        # self.action(action)


    def isGoalReached(self):
        return (self.board == self.goalState)

    def printNode(self):
        for offset in range(0,9,3):
            print self.state[offset:offset+3]


    
    def action(self,action,board):
        '''
            Action is 1-up,2-left,3-right,4-down
        '''
        temp=0
        board = list(board)
        pos = board.index(0)
        # move up
        if action == 1:
            if (pos)>3:
                temp = board[pos-3]
                pos=pos-3
                board[pos]=0
                board[pos+3]=temp
        # move left
        elif action == 2:
            if (pos%3)>0:
                temp = board[pos-1]
                pos=pos-1
                board[pos]=0
                board[pos+1]=temp        
        # move right
        elif action == 3:
            if (pos%3)<2:
                temp = board[pos+1]
                pos=pos+1
                board[pos]=0
                board[pos-1]=temp
        # move down
        elif action == 4:
            if (pos)<6:
                temp = board[pos+3]
                pos=pos+3
                board[pos]=0
                board[pos-3]=temp
        else:
            pass

        return board

    def heuristic(self):
        #look up table for x,y co-ordinates of placeHolders
        LUT = [(0,0),(1,0),(2,0),
                (0,1),(1,1),(2,1),
                (0,2),(1,2),(2,2)]

        def getManhattanDist(i):
            x,y = LUT[self.board.index(i)]
            xg,yg = LUT[self.goalState.index(i)]
            xi,yi = LUT[self.initState.index(i)]
            # return dist from node-goal and init-node
            # print (x,y),(xg,yg),(xi,yi)
            return (abs(x-xg)+abs(y-yg),abs(x-xi)+abs(y-yi))
                    
        manhDistToGoal=0    
        manhDistFromInit=0  

        for i in range(9):
            NodeToGoal,InitToNode = getManhattanDist(i) 
            manhDistToGoal += NodeToGoal # h(n)
            manhDistFromInit += InitToNode # g(n)
        # f(n)= g(n)+h(n)
        return manhDistToGoal+manhDistFromInit

    def expand(self):
        childNodes = list()
        currState = self

        for _action in range(1,5):
            # print "actionInNode",_action,
            child = Node(self.board,self.initState,_action)
            # print "childInNode:",child.board,child
            if child not in childNodes:
                childNodes.append(child)
                child.parent = currState
        # print 'childrenINNode:',[child.state for child in childNodes]
        return childNodes

    
    def __eq__(self,other):
        return isinstance(other, Node) and self.board == other.board

    
    def __hash__(self):
        # print hash(tuple(self.board))
        # print "board in hash",self.state,"hash:",hash(self.state)
        return hash(self.state)





#---------------------------------------------------------------------#




if __name__ == '__main__':
    try:
        initialNode = EightPuzzle()

        print "initialNode"
        initialNode.printNode()

        leafNodeASTAR,exploredAstar = Astar(Node,initialNode.state)
        # print leafNode
        print '-'*80
        print "\t\t Output of A*"
        print '-'*80
        printBranch(leafNodeASTAR)
        print 'explored nodes in A*:',len(exploredAstar)
        raw_input("press any key to continue")
        leafNodeRBFS,exploredRBFS = recursive_best_first_search(Node,initialNode.state)
        print '-'*80
        print "\t\t Output of RBFS"
        print '-'*80
        printBranch(leafNodeRBFS)
        print 'explored nodes in RBFS:',len(exploredRBFS)

        
    except KeyboardInterrupt:
        quit()
