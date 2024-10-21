"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # from book:
    fringe = util.Stack()  # stack of tuples (state, path to state from root)
    visited = set()
    if problem.is_goal_state(problem.get_start_state()):
        return []
    fringe.push((problem.get_start_state(), []))
    visited.add(problem.get_start_state())

    while not fringe.isEmpty():
        last_state = fringe.pop()  # tuple (state,path)
        successors = problem.get_successors(last_state[0])  # list of triples (successor, action, stepCost)
        for triple in successors:
            if problem.is_goal_state(triple[0]):
                return [*last_state[1], triple[1]]  # efficient last_state path + triple action

            if triple[0] not in visited:
                visited.add(triple[0])
                fringe.push((triple[0], [*last_state[1], triple[1]]))
    return []


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # from book
    fringe = util.Queue()  # queue of tuples (state, path to state from root)
    visited = set()
    if problem.is_goal_state(problem.get_start_state()):
        return []
    fringe.push((problem.get_start_state(), []))
    visited.add(problem.get_start_state())

    while not fringe.isEmpty():
        last_state = fringe.pop()  # tuple (state,path)
        successors = problem.get_successors(last_state[0])  # list of triples (successor, action, stepCost)
        for triple in successors:
            if problem.is_goal_state(triple[0]):
                return [*last_state[1], triple[1]]  # efficient last_state path+ triple action

            if triple[0] not in visited:
                visited.add(triple[0])
                fringe.push((triple[0], [*last_state[1], triple[1]]))
    return []


class PriorityItem:
    """
    This class holds three items- state, cost of the state, path to state, so we can compare the items in
    our priority queue in the ucs and astar function.
    """

    def __init__(self, state, cost, path):
        self.state = state
        self.cost = cost
        self.path = path

    def __lt__(self, obj):
        return self.state < obj.state

    def get_state(self):
        return self.state

    def get_cost(self):
        return self.cost

    def get_path(self):
        return self.path


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    if problem.is_goal_state(problem.get_start_state()):
        return []

    fringe = util.PriorityQueue()  # priority queue of PriorityItems (state, path to state) the priority here is the
    # cost
    start_item = PriorityItem(problem.get_start_state(), 0, [])
    fringe.push(start_item, 0)
    visited = set()

    while not fringe.isEmpty():
        first_priority = fringe.pop()  # priority item (state,cost,path)
        if problem.is_goal_state(first_priority.get_state()):
            return first_priority.get_path()  # first_priority path
        if first_priority.get_state() not in visited:
            visited.add(first_priority.get_state())
            successors = problem.get_successors(
                first_priority.get_state())  # list of triples (successor, action, stepCost)
            for triple in successors:
                fringe.push(
                    PriorityItem(triple[0], first_priority.get_cost() + triple[2],
                                 [*first_priority.get_path(), triple[1]]),
                    first_priority.get_cost() + triple[2])
    return []


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    if problem.is_goal_state(problem.get_start_state()):
        return []

    fringe = util.PriorityQueue()  # priority queue of PriorityItems (state, path to state) the priority here is the
    # cost +huristic
    start_item = PriorityItem(problem.get_start_state(), 0, [])
    fringe.push(start_item, 0)
    visited = set()

    while not fringe.isEmpty():
        first_priority = fringe.pop()  # priority item (state,cost,path)
        if problem.is_goal_state(first_priority.get_state()):
            return first_priority.get_path()  # first_priority path
        if first_priority.get_state() not in visited:
            visited.add(first_priority.get_state())
            successors = problem.get_successors(
                first_priority.get_state())  # list of triples (successor, action, stepCost)
            for triple in successors:
                fringe.push(
                    PriorityItem(triple[0], first_priority.get_cost() + triple[2],
                                 [*first_priority.get_path(), triple[1]]),
                    first_priority.get_cost() + triple[2] + heuristic(triple[0], problem))
    return []


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
