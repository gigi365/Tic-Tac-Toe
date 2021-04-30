import math
import copy

X = 'X'
O = 'O'
EMPTY = None


def initial():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    returns current player
    """
    Xs = 0
    Os = 0
    for row in board:
        Xs += row.count(X)
        Os += row.count(O)

    if Xs > Os:
        return O
    else:
        return X


def actions(board):
    """
    return possible actions for the player
    """
    moves = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    returns resulting board from current
    board and action
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError

    current = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current
    return new_board


def winner(board):
    """
    returns the winner of the board
    """

    Xscore = [0, 0, 0, 0, 0, 0, 0, 0]
    Oscore = [0, 0, 0, 0, 0, 0, 0, 0]

    for i, row in enumerate(board):
        Xscore[i] += row.count(X)
        Oscore[i] += row.count(O)
        for j, value in enumerate(row):
            if value == O:
                Oscore[3+j] += 1
            elif value == X:
                Xscore[3+j] += 1
            if i == j:
                if value == O:
                    Oscore[6] += 1
                elif value == X:
                    Xscore[6] += 1
            if i + j == 2:
                if value == O:
                    Oscore[7] += 1
                elif value == X:
                    Xscore[7] += 1

    if 3 in Oscore:
        return O
    if 3 in Xscore:
        return X
    return None


def terminal(board):
    """
    returns True if there is winner or
    no more moves can be made
    otherwise False
    """
    if winner(board) is not None:
        return True

    # check for any possible moves
    moves = actions(board)
    return len(moves) == 0


def utility(board):
    """
    return number score representation of the current game
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    determine best action to make
    """
    if terminal(board):
        return None

    currentPlayer = player(board)
    if currentPlayer == O:
        score, action = minvalue(board)
    else:
        score, action = maxvalue(board)
    return action


def minvalue(board):
    """
    find lowest possible value for the game
    """
    if terminal(board):
        return utility(board), None

    lowest = 999
    savedAction = None
    for action in actions(board):
        resultingBoard = result(board, action)
        if winner(resultingBoard) == O:
            return -1, action
        score, move = maxvalue(resultingBoard)
        if score == -1:
            return -1, action
        if score < lowest:
            savedAction = action
            lowest = score
    return lowest, savedAction


def maxvalue(board):
    """
    find highest possible value for the game
    """
    if terminal(board):
        return utility(board), None

    highest = -999
    savedAction = None
    for action in actions(board):
        resultingBoard = result(board, action)
        if winner(resultingBoard) == X:
            return 1, action
        score, move = minvalue(resultingBoard)
        if score == 1:
            return 1, action
        if score > highest:
            highest = score
            savedAction = action
    return highest, savedAction
