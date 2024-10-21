from board import Board
from search import SearchProblem, ucs
import util
import numpy as np

class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.corners = [(0, 0), (0, board_w - 1), (board_h - 1, 0), (board_h - 1, board_w - 1)]

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        returns true if and only if all the corners are filled
        :param state:
        :return:
        """
        for corner in self.corners:
            if state.get_position(corner[1], corner[0]) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost = 0
        for action in actions:
            cost += action.piece.get_num_tiles()
        return cost


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    visited = set()
    sum = 0
    for corner in problem.corners:
        if state.get_position(corner[1], corner[0]) == -1:
            if corner in visited:
                continue
            sum += 1
            # check your diagonal neighbor
            if corner == (0, 0):
                neighbor = (1, 1)
            elif corner == (0, problem.board.board_w - 1):
                neighbor = (1, problem.board.board_w - 2)
            elif corner == (problem.board.board_h - 1, 0):
                neighbor = (problem.board.board_h - 2, 1)
            else:
                neighbor = (problem.board.board_h - 2, problem.board.board_w - 2)

            # check if valid (in bounds)
            if (neighbor[0] < 0 or neighbor[0] >= problem.board.board_w or neighbor[1] < 0 or
                    neighbor[1] >= problem.board.board_h):
                continue
            if neighbor not in visited and state.get_position(neighbor[1], neighbor[0]) == -1:
                sum += 1  # if the corner not colored, we will have to color the diagonal neighbor
                visited.add(neighbor)
            visited.add(corner)
    return sum

    # # return number of corners that are not covered - naive
    # corners_uncovered = 0
    # for corner in problem.corners:
    #     if state.get_position(corner[1], corner[0]) == -1:
    #         corners_uncovered += 1
    # return corners_uncovered


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.get_position(target[1], target[0]) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost = 0
        for action in actions:
            cost += action.piece.get_num_tiles()
        return cost

def get_neighbors( target,problem):
    """
    this function helps find the valid neighbors of the target
    """
    diagonal_neighbors = [(target[0] - 1, target[1] - 1), (target[0] + 1, target[1] - 1),
                          (target[0] + 1, target[1] + 1),
                          (target[0] - 1, target[1] + 1)]
    valid_diagonal_neighbors = []
    for dn in diagonal_neighbors:
        if dn[0] < 0 or dn[0] >= problem.board.board_w or dn[1] < 0 or dn[1] >= problem.board.board_h:
            continue
        valid_diagonal_neighbors.append(dn)

    cross_neighbors = [(target[0] - 1, target[1]), (target[0] + 1, target[1]), (target[0], target[1] + 1),
                       (target[0], target[1] - 1)]
    valid_cross_neighbors = []

    for cn in cross_neighbors:
        if cn[0] < 0 or cn[0] >= problem.board.board_w or cn[1] < 0 or cn[1] >= problem.board.board_h:
            continue
        valid_cross_neighbors.append(cn)
    return valid_diagonal_neighbors , valid_cross_neighbors


def blokus_cover_heuristic(state, problem):
    visited = set()
    sum = 0
    for target in problem.targets:
        if target not in visited and state.get_position(target[1], target[0]) == -1:
            diagonal_neighbors, cross_neighbors = get_neighbors(target, problem)

            for cn in cross_neighbors:
                if state.get_position(cn[1], cn[0]) != -1:
                    return float('inf')  # no solution-return infinity as said in form

            sum += 1  # for the target itself

            found_diagonal_colored_tile = False
            for dn in diagonal_neighbors:
                if dn in visited or state.get_position(dn[1], dn[0]) != -1:
                    # if neighbor is colored or there is neighbor overlapping
                    found_diagonal_colored_tile = True
                if dn in problem.targets and dn not in visited:
                    sum += 1  # for the neighbor target
                    found_diagonal_colored_tile = True
                visited.add(dn)
            if not found_diagonal_colored_tile:
                sum += 1

            for cn in cross_neighbors:
                if cn in problem.targets and cn not in visited:
                    sum += 1  # for the neighbor target
                    visited.add(cn)
            visited.add(target)
    return sum

    ## naive- return number of targets that are not covered
    # targets_uncovered = 0
    # for target in problem.targets:
    #     if state.get_position(target[1], target[0]) == -1:
    #         targets_uncovered += 1
    # return targets_uncovered
