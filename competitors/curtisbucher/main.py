import chess
import chess.engine
import random
from copy import copy

board = chess.Board()
chess.engine.


def make_move(last_move, current_board):
    global board
    # Accomidating last move
    if last_move:
        board.push(chess.Move.from_uci(last_move))
    # Calculating new move and altering board to fit
    next_move = random.choice(list(board.legal_moves))
    board.push(next_move)

    return next_move.uci()
