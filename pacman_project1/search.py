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

    stack = util.Stack()
    return generalSearch(problem, stack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    Frontier = util.Queue()
    Visited = []
    Frontier.push( (problem.getStartState(), []) )
    #print 'Start',problem.getStartState()
    #Visited.append( problem.getStartState() )

    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()

        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            if n_state not in Visited:
                if problem.isGoalState(n_state):
                    #print 'Find Goal'
                    return actions + [n_direction]
                Frontier.push( (n_state, actions + [n_direction]) )
                Visited.append( n_state )


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    cost = lambda path: problem.getCostOfActions([x[1] for x in path][1:])
    priorityQueue = util.PriorityQueueWithFunction(cost)
    return generalSearch(problem, priorityQueue)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0


def generalSearch(problem, data_structure):
    # lista koordinata obradjenih stanja
    visited = []
    # dodaje stanje (triplet): [(x,y), akcija(N,S,E,W,Stop), cena]
    data_structure.push([(problem.getStartState(), "Stop", 0)])
    # print ("Start: ", problem.getStartState())

    while not data_structure.isEmpty():
        ''' svaki element iz path je stanje, koje je triplet:
        [koordinate - (x,y), akcija - (N,S,E,W), cena]
        '''
        path = data_structure.pop()
        # od poslednjeg u listi dobavlja (x, y)
        current_state = path[-1][0]
        # od poslednjeg u listi dobavlja akciju (N, S, E, W, Stop)
        # print ("Going direction ", path[-1][1])
        # print ("State is ", current_state)

        if problem.isGoalState(current_state):
            ''' uzima se akcija (index 1 u tripletu) iz svakog elementa liste
            i tako se rekonstruise putanja - vraca se lista akcija koja od
            pocetnog stanja vodi do cilja
            '''
            return [state[1] for state in path][1:]

        if current_state not in visited:
            visited.append(current_state)

            # uzimaju se sva sledeca moguca stanja za tekuce stanje
            for successor in problem.getSuccessors(current_state):
                if successor[0] not in visited:
                    successorPath = path[:]
                    successorPath.append(successor)
                    data_structure.push(successorPath)

    # ako nije pronadjena putanja do cilja, vraca se prazna lista
    return []



def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    cost = lambda path: problem.getCostOfActions([state[1] for state in path][1:]) + heuristic(path[-1][0], problem)
    priorityQueue = util.PriorityQueueWithFunction(cost)
    return generalSearch(problem, priorityQueue)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
