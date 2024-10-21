211491014
318879574
*****
Comments:
    Description of our evaluation function, Question 7:

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
        distances. This give more weight for wanted states- where the max tile is closer to the corners of the board.
        We subtract this value because we want to minimize it.

    5. Score:
        We include in our evaluation function the score of the state. In that way, states with higher scores,
        have more weight.

    6. Max tile value:
        We add to our evaluation function the value of the max tile on the board.
        In that way, states with higher Max tile value, have more weight.