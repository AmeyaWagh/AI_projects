#!/usr/bin/python
from Queue import PriorityQueue
import time
import sys
sys.setrecursionlimit(10000)

infinity = float('inf')

def isNotInQueue(x,q):
    with q.mutex:
        return x not in q.queue

def Astar(Node,initBoard):
    
    newNode = Node(initBoard,initBoard,0)
    # print dir(newNode)
    
    if newNode.isGoalReached():
        print "goalReached"
        return newNode,tuple([1])

    # make a priority queue with heuristic as priority
    frontier = PriorityQueue()
    frontier.put((newNode.heuristic(),newNode))
    explored = set()

    iteration=0
    while not frontier.empty():
        iteration +=1
        print '\n\niteration:',iteration
        
        if frontier.empty():
            print "queue empty"

        # get a node from queue
        newNode = frontier.get()[1]

        print 'newNode:',newNode.board

        # check if goal state
        if newNode.isGoalReached():
            print "goalReached"
            return newNode,explored

        # if not goal, add to explored
        explored.add(newNode)

        # expand tree and get children
        children = newNode.expand()
        # print 'children',children
        for child in children:
            # print "child",child.board
            # print "explored",explored
            # print (child not in explored)
            # print isNotInQueue(child,frontier)
            if (child not in explored) and isNotInQueue(child,frontier):
                print "child added:",child.board
                frontier.put((child.heuristic(),child))
        # time.sleep(0.5)
    print "queue empty:",frontier.empty() 
    print "Done"
    return None

def printBranch(leafNode):
    if leafNode is not None:
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
        print "\t8 puzzle solver"
        iteration=0
        for path in path_back:
            print '\n->',iteration
            path.printNode()
            iteration+=1    
        print '-'*80
    else:
        print None

#---------------------------------------------------------------------#
    
def recursive_best_first_search(Node,initBoard):
    """[Figure 3.26]"""
    
    def RBFS(node, flimit,explored):
        print '\n\nin RBFS'
        # print node.state
        # time.sleep(0.5)
        # iteration+=1

        # explored.add(node.__hash__())

        if node.isGoalReached():
            print "goal reached"
            return node, 0,explored   # (The second value is immaterial)
        
        successors = node.expand()
        successors = list(set(successors))
        # print "hashList:",successors

        # remove child node which same as parent node
        if node in successors: 
            successors.pop(successors.index(node))

        for child in successors:
            if child.__hash__() in explored:
                successors.pop(successors.index(child))

        # print 'explored',explored

        # print "successors"
        # print [s.state for s in successors]
        
        # reached leafNode
        if len(successors) == 0:
            print "no successor"
            return None, infinity, explored
        
        # update f values
        for s in successors:
            s.f = max(s.heuristic(), node.f)
            # print 'state:',s.state,'f_val:',s.f
        
        # iterat = 0
        while True:
            print 'in loop'
            # Order by lowest f value
            # print 'beforeSort',successors
            successors.sort(key=lambda x: x.f)
            # print 'AfterSort',successors
            best = successors[0]
            explored.add(best.__hash__())
            # print "best",best.state,'f:',best.f

            if best.f > flimit:
                # print 'bestf',best.f,'limit',flimit
                return None, best.f, explored

            # next best successor    
            if len(successors) > 1:
                alternative = successors[1].f
            
            else:
                alternative = infinity
                
            # print 'alt:',alternative,'limit',flimit

            print 'going into recursion:',best.state
            result, best.f, _expl = RBFS(best, min(flimit, alternative),explored)
            print 'out of recursion'
            
            # node.f = best.f
            if result is not None:
                return result, best.f, explored

    # frontier = PriorityQueue()
    explored = set()
    node = Node(initBoard,initBoard,0)
    node.f = node.heuristic()
    # explored.add(node)
    # frontier.put((node,node.f))
    result, bestf, explored = RBFS(node, infinity,explored)
    return result,explored