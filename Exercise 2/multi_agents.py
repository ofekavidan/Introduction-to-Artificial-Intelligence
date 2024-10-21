import numpy as np
import abc
import util
from game import Agent, Action

MAX_LAYER_AGENT_INDEX = 0
MIN_LAYER_AGENT_INDEX = 1


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """
        # Useful information you can extract from a GameState (game_state.py)
        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score

        # find max_tile last coordinates
        max_tile_coordinates_old = [0, 0]
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == max_tile:
                    max_tile_coordinates_old = [i, j]
                    break

        # calculate manhattan distance from the highest tile coordinates to the corners (giving the last
        # corners extra weight)
        corners = [[0, 0], [0, len(board)+1], [len(board) +1, 0], [len(board) +1, len(board[0]) +1]]
        manhattan_distances_old = [util.manhattanDistance(max_tile_coordinates_old, corner) for corner in corners]
        return score - min(manhattan_distances_old)


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        value, move = self.max_layer(game_state, self.depth)
        return move

    def max_layer(self, game_state, cur_depth):
        actions = game_state.get_legal_actions(MAX_LAYER_AGENT_INDEX)
        if cur_depth == 0 or len(actions) == 0:
            return self.evaluation_function(game_state), Action.STOP

        max_val, max_move = float('-inf'), Action.STOP
        for action in actions:
            successor = game_state.generate_successor(MAX_LAYER_AGENT_INDEX, action)
            cur_val, _ = self.min_layer(successor, cur_depth)
            if cur_val > max_val:
                max_val, max_move = cur_val, action
        return max_val, max_move

    def min_layer(self, game_state, cur_depth):
        actions = game_state.get_legal_actions(MIN_LAYER_AGENT_INDEX)
        if cur_depth == 0 or len(actions) == 0:
            return self.evaluation_function(game_state), Action.STOP

        min_val, min_move = float('inf'), Action.STOP
        for action in actions:
            successor = game_state.generate_successor(MIN_LAYER_AGENT_INDEX, action)
            cur_val, _ = self.max_layer(successor, cur_depth - 1)
            if cur_val < min_val:
                min_val, min_move = cur_val, action
        return min_val, min_move


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        value, move = self.max_layer(game_state, self.depth, float('-inf'), float('inf'))
        return move

    def max_layer(self, game_state, cur_depth, alpha, beta):
        actions = game_state.get_legal_actions(MAX_LAYER_AGENT_INDEX)
        if cur_depth == 0 or len(actions) == 0:
            return self.evaluation_function(game_state), Action.STOP

        max_val, max_move = float('-inf'), Action.STOP
        for action in actions:
            successor = game_state.generate_successor(MAX_LAYER_AGENT_INDEX, action)
            cur_val, _ = self.min_layer(successor, cur_depth, alpha, beta)
            if cur_val > max_val:
                max_val, max_move = cur_val, action
                alpha = max(alpha, max_val)
            if max_val >= beta:
                return max_val, max_move
        return max_val, max_move

    def min_layer(self, game_state, cur_depth, alpha, beta):
        actions = game_state.get_legal_actions(MIN_LAYER_AGENT_INDEX)
        if cur_depth == 0 or len(actions) == 0:
            return self.evaluation_function(game_state), Action.STOP

        min_val, min_move = float('inf'), Action.STOP
        for action in actions:
            successor = game_state.generate_successor(MIN_LAYER_AGENT_INDEX, action)
            cur_val, _ = self.max_layer(successor, cur_depth - 1, alpha, beta)
            if cur_val < min_val:
                min_val, min_move = cur_val, action
                beta = min(beta, min_val)
            if min_val <= alpha:
                return min_val, min_move
        return min_val, min_move


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        value, move = self.max_layer(game_state, self.depth)
        return move

    def max_layer(self, game_state, cur_depth):
        actions = game_state.get_legal_actions(MAX_LAYER_AGENT_INDEX)
        if cur_depth == 0 or len(actions) == 0:
            return self.evaluation_function(game_state), Action.STOP

        max_val, max_move = float('-inf'), Action.STOP
        for action in actions:
            successor = game_state.generate_successor(MAX_LAYER_AGENT_INDEX, action)
            cur_val = self.chance_layer(successor, cur_depth)
            if cur_val > max_val:
                max_val, max_move = cur_val, action
        return max_val, max_move

    def chance_layer(self, game_state, cur_depth):
        actions = game_state.get_legal_actions(MIN_LAYER_AGENT_INDEX)
        if cur_depth == 0 or len(actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        total_val = 0
        uniformly_prob = 1 / len(actions)
        for action in actions:
            successor = game_state.generate_successor(MIN_LAYER_AGENT_INDEX, action)
            cur_val, _ = self.max_layer(successor, cur_depth - 1)
            total_val += (cur_val * uniformly_prob)

        return total_val


def count_empty_cells(current_game_state):
    """
    this function counts how many empty cells there are on the board in the current game state
    :param current_game_state: the current state of the game
    :return: number of empty cells on the board
    """
    return np.sum(current_game_state.get_empty_tiles())


def calc_monotonic(current_game_state):
    """
    this function evaluates how strictly-monotonic the board is.
    the function do this efficiently by calculating the differences between neighboring tiles in both horizontal and
    vertical directions.
    :param current_game_state: the current state of the game
    :return: how monotonic the board is, low value indicate higher monotonicity.
    """
    board = current_game_state.board
    without_left_col = board[:, 1:]
    without_right_col = board[:, :-1]
    without_up_row = board[1:, :]
    without_down_row = board[:-1, :]

    # calc differences between horizontal neighbors
    horizontal_diffs = without_left_col - without_right_col
    # calc differences between vertical neighbors
    vertical_diffs = without_up_row - without_down_row

    # choose best monotonic direction (up/down and left/right)
    horizontal_monotonic = min(np.sum(horizontal_diffs > 0), np.sum(horizontal_diffs < 0))
    vertical_monotonic = min(np.sum(vertical_diffs > 0), np.sum(vertical_diffs < 0))

    return horizontal_monotonic + vertical_monotonic


def calc_neighboring_differences(current_game_state):
    """
    This function calculates, efficiently, the sum of absolute differences between each tile and its neighboring
    tiles. The function calculates the value differences for each tile relative to its right and down neighbors (to
    avoid duplicates).
    The value returned, represents how "unmerged" the board is- lower value indicates that more tiles
    are neighbors with tiles of the same value.

    :param current_game_state: the current state of the game
    :return: how "unmerged" the board is.
    """
    board = current_game_state.board
    without_left_col = board[:, 1:]
    without_right_col = board[:, :-1]
    without_up_row = board[1:, :]
    without_down_row = board[:-1, :]

    sum_diffs = 0

    # differences with the right neighbor
    right_diffs = np.abs(without_right_col - without_left_col)
    sum_diffs += np.sum(right_diffs)

    # differences with the down neighbor
    down_diffs = np.abs(without_down_row - without_up_row)
    sum_diffs += np.sum(down_diffs)
    return sum_diffs


def calc_max_tile_dist(current_game_state):
    """
    This function calculates the minimum manhattan distance from the max tile to the corners.
    :param current_game_state: the current state of the game
    :return: the minimum manhattan distance from the max tile to the corners
    """
    board = current_game_state.board
    max_tile = current_game_state.max_tile

    max_tile_coordinates = np.argwhere(board == max_tile)[0]
    rows, cols = board.shape
    corners = np.array([[0, 0], [0, cols - 1], [rows - 1, 0], [rows - 1, cols - 1]])
    manhattan_distances = np.sum(np.abs(max_tile_coordinates - corners), axis=1)
    min_distance = np.min(manhattan_distances)
    return min_distance


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION:
    We utilized information from various internet sources, and followed a known strategy to win the 2048 game,
    that involves arranging the board to be monotonic. In that way, tiles with similar values will be near each
    other, and the max tile is on one of the corners of the board.
    We included some more factors to the evaluation to add more weight to more ideal board states:

    1. Monotonic board:
        We want to make sure that the max tile is on one of the corners. The ideal is to get to a monotonic board
        (so the tiles numbers are increasing / decreasing on the up/down and left/right directions).
        We evaluate how monotonic the board is by calculating horizontal and vertical differences between the tiles.

    2. Tiles' value differences:
        The ideal is to get each tile to be a neighbor of tiles with the same value, so those tiles can be merged.
        We calculated the value differences for each of tiles to their (legal) neighbors.
        We want to have as much as possible of tiles that are neighbors with tiles with the same number.
        Thus, we subtract this from the result (because we want to minimize the value differences).

    3. Empty cells:
        We calculate the number of empty cells on the board. The ideal is to have as much as possible empty cells,
        to have more room for new tiles.

    4. Min manhattan distance from the max tile to the corners:
        As mentioned before, we want to make sure that the max tile is on one of the corners.
        We calculate the Manhattan distance from the max tile to each of the corners and take the minimum of the
        distances. This give more weight for wanted states - where the max tile is closer to the corners of the board.
        We subtract this value because we want to minimize it.

    5. Score:
        We include in our evaluation function the score of the state. In that way, states with higher scores,
        have more weight.

    6. Max tile value:
        We add to our evaluation function the value of the max tile on the board.
        In that way, states with higher Max tile value, have more weight.
    """

    # count empty cells
    empty_cells_count = count_empty_cells(current_game_state)

    # evaluate how monotonic the board is
    monotonic_board_eval = calc_monotonic(current_game_state)

    # calc value differences on neighboring tiles
    val_differences = calc_neighboring_differences(current_game_state)

    # calc manhattan dist of the max tile from the corners
    max_tile_dist = calc_max_tile_dist(current_game_state)

    return current_game_state.score + current_game_state.max_tile + empty_cells_count + \
           monotonic_board_eval - val_differences - max_tile_dist



# Abbreviation
better = better_evaluation_function