'''
A Modified version of AIMA python Library

Reference:
https://github.com/aimacode/aima-python
https://github.com/marianafranco/missionaries-and-cannibals/blob/master/python/missionaries_and_cannibals.py
'''
import time

left = 'left'
right= 'right'


def FIFOQueue():
    return list()

def breadth_first_search(State):
    """[Figure 3.11]"""
    Initialnode = State(3,3,left,0,0)
    if Initialnode.isGoalReached():
        print "Goal reached"
        return Initialnode
    frontier = FIFOQueue()
    explored = set()
    frontier.append(Initialnode)
    iteration=0
    # print 'init frontier',frontier
    while frontier:
        iteration +=1
        print 'iteration:',iteration
        node = frontier.pop(0)
        if node.isGoalReached():
            print "Goal reached"
            return node
        explored.add(node)
        print '\n'
        for child in node.expand():
        # for child in expand(node):
            # print '-'*50
            # print 'child',child
            # print 'explored',explored
            # print 'frontier',frontier
            # print '-'*50
            if (child not in explored) or (child not in frontier):
                frontier.append(child)
        # time.sleep(0.5)
    return None

def printBranch(leafNode):
    path_back = []
    # print leafNode
    path_back.append(leafNode)
    parent = leafNode.parent
    while parent:
        # print parent
        path_back.append(parent)
        parent = parent.parent    
    path_back = list(reversed(path_back))
    print '-'*80
    print "\tML CL boat MR CR"
    for path in path_back:
        print path    
    print '-'*80

