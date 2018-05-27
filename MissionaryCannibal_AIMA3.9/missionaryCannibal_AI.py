#!/usr/bin/python

#---------------------------------------------------------------------------#
# Name: Ameya Wagh
# AIMA problem 3.9
# Reference:
# https://github.com/aimacode/aima-python
# https://github.com/marianafranco/missionaries-and-cannibals/blob/master/python/missionaries_and_cannibals.py

#---------------------------------------------------------------------------#

import os
from AIMAsearch import * 

# rootNode = Node(3,3,left,0,0)

class Node():
    '''
        State Space Model of game
    '''
    def __init__(self,Mleft,Cleft,boatState,Mright,Cright):

        # self.state = {
        # left:{ Missionary:Mleft,
        #         Cannibal:Cleft},
        # boat:boatState,
        # right:{ Missionary:Mright,
        #         Cannibal:Cright}
        # }
        self.leftMissionaries = Mleft
        self.leftCannibals = Cleft
        self.boat = boatState
        self.rightMissionaries = Mright
        self.rightCannibals = Cright

        self.parent=None
        self.state = (self.leftMissionaries,self.leftCannibals,
            self.boat,
            self.rightMissionaries,self.rightCannibals)
        self.goalState = (0,0,right,3,3)

    def isGoalReached(self):
        '''
            Check if all the Cannibals and Missionaries are on the Right
        '''
        if self.state == self.goalState:
            return True
        else:
            return False

    def isValidCondition(self):
        '''
            Rule:
                Missionaries >= Cannibals
                Cannibals > Missionaries only when Missionaries == 0
        '''
        def checkIfCountPositive():
            return self.leftMissionaries >= 0 and self.rightMissionaries >= 0 \
                   and self.leftCannibals >= 0 and self.rightCannibals >= 0

        def checkIfM_ge_C():
            return (self.leftMissionaries == 0 or \
                    self.leftMissionaries >= self.leftCannibals) \
                   and (self.rightMissionaries == 0 or \
                    self.rightMissionaries >= self.rightCannibals)

        
        if checkIfCountPositive() and checkIfM_ge_C():
            return True
            
        # Neither of the sides can go negative
        else:
            return False
        
    
    def expand(self):
        '''
            expand child nodes of given node
            All cases:
            if boat on left, it can carry 1M,1C,2M,2C,MC to right
            if boat on right, it can carry 1M,1C,2M,2C,MC to left
        '''
        currState = self
        childNodes = []
        # (1,0) i.e 1M and 0C moved.
        actionSpace = [(1,0),(0,1),(2,0),(0,2),(1,1)]
        for action in actionSpace: 
            Mcount = action[0]
            Ccount = action[1]
            # print "action",action
            # if curr_state[boat] == left:
            if currState.boat == left:
                
                childNode = Node(
                    currState.leftCannibals -Ccount, 
                    currState.leftMissionaries - Mcount, 
                    right,
                    currState.rightCannibals + Ccount,
                    currState.rightMissionaries + Mcount)

                if childNode.isValidCondition():
                    childNodes.append(childNode)
                    childNode.parent=currState
            else:
                
                childNode = Node(
                    currState.leftCannibals +Ccount, 
                    currState.leftMissionaries + Mcount, 
                    left,
                    currState.rightCannibals - Ccount,
                    currState.rightMissionaries - Mcount)

                if childNode.isValidCondition():
                    childNodes.append(childNode)
                    childNode.parent=currState

        # print "childNodes",'\n'.join([str(node.state) for node in childNodes])
        return childNodes    

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __hash__(self):
        return hash(
            (self.leftCannibals, self.leftMissionaries, 
                self.boat, 
                self.rightCannibals, self.rightMissionaries))
        # return hash(
        #     (self.state[left][Missionary],self.state[left][Cannibal],
        #     self.state[boat],
        #     self.state[right][Missionary],self.state[right][Cannibal])
        # )
        


if __name__ == '__main__':
    # game=Node(3,3,left,0,0)
    # game.displayState(1)
    # game.displayState(2)
    # game.displayState(3)
    # print game.isGoalReached()
    print "BFS output"
    leafNode = breadth_first_search(Node)
    # print "leafNode",leafNode
    printBranch(leafNode)