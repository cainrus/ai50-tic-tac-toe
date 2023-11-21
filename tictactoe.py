"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None

diagonal_intersections = [
    [0, 4, 8],
    [2, 4, 6],
]

intersections = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
] + diagonal_intersections

corners = [0, 2, 6, 8]


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = [item for row in board for item in row].count(X)
    o_count = [item for row in board for item in row].count(O)
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = []
    for index, value in enumerate(flatten(board)):
        if value is None:
            possible_actions += divmod(index, 3)
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if 0 <= i <= 2 and 0 <= j <= 2:
        new_board = copy.deepcopy(board)
        new_board[i][j] = player(board)
        return new_board

    raise ValueError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    flat_board = flatten(board)
    for symbol in [X, O]:
        if is_winner(flat_board, symbol):
            return symbol
    return None


def flatten(board):
    return [item for row in board for item in row]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    flat_board = flatten(board)

    if flat_board.count(EMPTY) == 0:
        return True

    if winner(board) is not None:
        return True

    return False


def is_winner(flat_board, symbol):
    for intersection in intersections:
        subset = [flat_board[i] for i in intersection]
        if subset.count(symbol) == 3:
            return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    flat_board = flatten(board)
    if is_winner(flat_board, X):
        return 1
    if is_winner(flat_board, 0):
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return EMPTY

    current_player = player(board)
    another_player = O if current_player == X else X
    flat_board = flatten(board)
    center = board[1][1]

    # Optimal start
    if center is EMPTY and flat_board.count(another_player) <= 1:
        return [1, 1]

    # Defense
    for intersection in intersections:
        subset = [flat_board[i] for i in intersection]
        if EMPTY in subset and subset.count(another_player) == 2:
            index = intersection[subset.index(EMPTY)]
            return divmod(index, 3)

    # Attack from center
    if center == current_player:
        for intersection in diagonal_intersections:
            subset = [flat_board[i] for i in intersection]
            if subset.count(EMPTY) == 2:
                index = intersection[subset.index(EMPTY)]
                return divmod(index, 3)

    # Finish attack
    for intersection in intersections:
        subset = [flat_board[i] for i in intersection]
        if subset.count(current_player) == 2 and EMPTY in subset:
            index = intersection[subset.index(EMPTY)]
            return divmod(index, 3)

    # Defend corners
    if center == another_player:
        for corner in corners:
            if flat_board[corner] is EMPTY:
                return divmod(corner, 3)

    return divmod(flat_board.index(EMPTY), 3)
