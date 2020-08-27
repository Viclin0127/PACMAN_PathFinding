# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = []
    startNode = problem.getStartState()
    stack.push([startNode, []])
    while not(stack.isEmpty()):
        curNode, actions = stack.pop()
        if (problem.isGoalState(curNode)):
            return actions
        if curNode not in visited:
            visited.append(curNode)
            succ = problem.getSuccessors(curNode)
            for successor, action, cost in succ:
                if successor not in visited:
                    nextAction = actions + [action]
                    stack.push([successor, nextAction])
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = []
    startNode = problem.getStartState()
    queue.push([startNode, []])
    while not queue.isEmpty():
        curNode, actions = queue.pop()
        if (problem.isGoalState(curNode)):
            return actions
        if curNode not in visited:
            visited.append(curNode)
            succ = problem.getSuccessors(curNode)
            for successor, action, cost in succ:
                if successor not in visited:
                    nextAction = actions + [action]
                    queue.push([successor, nextAction])
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# In both pratical task and Assignment 1
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE FOR TASK 3 ***"
    startNode = problem.getStartState()

    actions = []
    visited = []
    # create a priority queue to store nodes with their f(n) = g(n) + h(n)
    pQueue = util.PriorityQueue()
    pQueue.push([startNode, actions], 0)
    while not pQueue.isEmpty():
        curNode, curAction = pQueue.pop()
        if curNode not in visited:
            visited.append(curNode)
            if problem.isGoalState(curNode):
                return curAction
            succ = problem.getSuccessors(curNode)
            for successor, action, cost in succ:
                if successor not in visited:
                    nextAction = curAction + [action]
                    # retrieve f value
                    f_value = cost + heuristic(successor, problem)
                    pQueue.push([successor, nextAction], f_value)

    return actions
    util.raiseNotDefined()

# Extensions Assignment 1
def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE FOR TASK 1 ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    # setting limit
    limit = 0
    # in each limit, iterating from startNode to search the goal state by DFS
    while limit<999:
        stack = util.Stack()
        visited = []
        startNode = problem.getStartState()
        stack.push([startNode, []])
        while not(stack.isEmpty()):
            curNode, actions = stack.pop()
            if (problem.isGoalState(curNode)):
                return actions
            if curNode not in visited:
                visited.append(curNode)
                succ = problem.getSuccessors(curNode)
                for successor, action, cost in succ:
                    if (successor not in visited):
                        nextAction = actions + [action]
                        # child's action should be no larger than limit
                        # ex: in limit=1, which means in the second tier(only startNode and its children)
                        if len(nextAction) <= limit:
                            stack.push([successor, nextAction])
        limit +=1
    return []
    util.raiseNotDefined()

def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second arguement (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    # design the improve function, using bfs to find h(s') < h(s) and return node, action
    def improve(state, action):
        queue = util.Queue()
        node = state
        nodeAction = action
        visited = []
        hvalue_init = heuristic(node, problem)
        queue.push([node, nodeAction])
        while not queue.isEmpty():
            curNode, curAction = queue.pop()
            hvalue_current = heuristic(curNode, problem)
            # h(s') < h(s)
            if hvalue_current < hvalue_init:
                return curNode, curAction
            if curNode not in visited:
                visited.append(curNode)
                succ = problem.getSuccessors(curNode)
                for successor, succAction, cost in succ:
                    if successor not in visited:
                        nextAction = curAction + [succAction]
                        queue.push([successor, nextAction])

    startNode = problem.getStartState()
    actions = []
    while not problem.isGoalState(startNode):
        startNode, actions = improve(startNode, actions)
    return actions
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
ehc = enforcedHillClimbing