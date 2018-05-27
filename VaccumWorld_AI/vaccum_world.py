#!/usr/bin/python

#----------------------------------------------------------------------#
#   Author: Ameya Wagh
#   Date: 09/09/2017
#----------------------------------------------------------------------#

import time
import random as r


class VaccumCleanerEnvironment():
    '''
        Environment for vaccum cleaner problem
    '''

    def __init__(self, shape=[2, 1]):
        self.len = shape[0]*shape[1]
        self.loc_labels = [chr(i) for i in range(ord('A'), ord('A')+self.len)]
        self.no_of_labels = len(self.loc_labels)
        self.map = []
        for case in range(pow(2, self.no_of_labels)):
            caseList = list(
                format(case, '#0{}b'.format(self.no_of_labels+2))[2:])
            caseList = [self.ifDirty(_case) for _case in caseList]
            self.map.append(
                zip([label for label in self.loc_labels], caseList))
        self.performanceList = []
        self.performanceCount = 0
        self.vaccumPosition = "A"
        self.agentPosition = 0
        self.execTime = 100  # milliseconds
        self.vacc_PositionHistory = []

    def banner(self, case):
        print "\n"*3
        print "="*80
        print "\t\t\tcase {}".format(case)
        print "="*80
        print "\n"*3

    def message(self,msg):
        print "."*80
        print "\t\t\t{}".format(msg)
        print "."*80

    def displayMap(self):
        self.message("MAP")
        for _map in self.map:
            print "\t",_map

    def ifDirty(self, stat):
        if stat == '1':
            return "DIRTY"
        else:
            return "CLEAN"

    def checkIfAllRoomsClean(self, submap):
        #check if robot has travelled through all the rooms
        #check if status of all rooms is CLEAN 
        if set(self.vacc_PositionHistory).issubset(['A','B','C']):
            
            roomStatus = list(set(zip(*submap)[1]))
            if len(roomStatus) == 1 and roomStatus[0] == "CLEAN":
                print set(self.vacc_PositionHistory).issubset(['A','B','C'])
                return True
            else:
                return False

    def average(self, perfList):
        return float(reduce(lambda x, y: x+y, perfList))/float(len(perfList))

    def performance(self):
        return self.performanceList, self.average(self.performanceList)

    def updateRooms(self, action, room):
        if action == "SUCK":
            self.submap[self.submap.index(room)][1] = "CLEAN"
        elif action == "LEFT" and self.agentPosition > 0:
            self.agentPosition -= 1
        elif action == "RIGHT" and self.agentPosition < (self.no_of_labels-1):
            self.agentPosition += 1
        else:
            pass

    def evalAgent(self, agent):
        self.message("Evaluating")
        for self.subMap in self.map:
            self.banner(self.map.index(self.subMap))
            # considering all initial cases from where the vacuum cleaner starts
            for initialRoom in self.loc_labels:
                # submap is a tuple which are immutable, thus converting it into
                # list of list
                self.submap = [[room, status] for room, status in self.subMap]
                print "-"*80
                print "Rooms before cleaning:", self.submap
                #------------------------------#
                self.performanceCount = 0
                self.vacc_PositionHistory = []
                self.agentPosition = self.loc_labels.index(initialRoom)
                print "\nStarting from Room:", initialRoom
                print "Room   Status  Action"
                while True:
                    currentRoom = self.submap[self.agentPosition]
                    print currentRoom,
                    self.vacc_PositionHistory.append(currentRoom[0])
                    action = agent(currentRoom)
                    self.updateRooms(action, currentRoom)
                    print action
                    self.performanceCount += 1
                    if self.checkIfAllRoomsClean(self.submap):
                        break
                    time.sleep(float(self.execTime)/1000.0)
                #------------------------------#
                print "\nRooms after cleaning:", self.submap
                print "are rooms cleaned:", self.checkIfAllRoomsClean(
                    self.submap)
                self.performanceList.append(self.performanceCount)
        print "Cost per case:", self.performance()[0],
        print "Average Cost:", self.performance()[1]


"""
This is a Simple Reflex Agent with a rule base for 3 continuously connected rooms
"""


def SimpleReflexAgent(percept):
    # percept is tuple of location and status
    location = percept[0]
    status = percept[1]
    if status == "DIRTY":
        return "SUCK"
    elif location == "A":
        return "RIGHT"
    elif location == "C":
        return "LEFT"
    elif location == "B":
        return ["LEFT", "RIGHT"][r.randint(0, 1)]
    else:
        return "NoOp"


if __name__ == '__main__':
    # currently the environment works only for (X,1) shape
    env = VaccumCleanerEnvironment(shape=[3, 1])
    env.displayMap()
    env.evalAgent(SimpleReflexAgent)
