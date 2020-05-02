"""Play the owner of the PR against a random player to determine if he can enter the tournament"""
import os
import sys
import getopt
import random
import importlib
import chess
import typing
import time
import traceback
from func_timeout import func_timeout, FunctionTimedOut


class Competitor:
    def __init__(self, username):
        self.name = username
        self.path = '.'.join(["competitors", username, "main"])
        self.engine = importlib.import_module(self.path)


def compete(playerA: str, playerB: str, TIME_LIMIT, QUIET=False) -> bool:
    """
    Play playerA against playerB and return true if playerA wins. If player B wins return false.
    If match ends in a draw, return random bool.
    """
    # Dealing with byes
    if not playerA:
        return False
    elif not playerB:
        return True
    # Getting the path to the PR actors' chess algorithm
    actor = Competitor(playerA)

    # Getting the path to a random opponent's chess algorithm
    opponent = Competitor(playerB)

    players = [actor, opponent]
    random.shuffle(players)

    print("WHITE:", players[0].name)
    print("BLACK:", players[1].name, "\n")

    turn = 0
    Board = chess.Board()
    last_move = ""

    # Competition Loop
    while not Board.is_game_over():
        try:
            last_move = func_timeout(
                TIME_LIMIT, players[turn % 2].engine.get_move, args=(last_move, TIME_LIMIT))

        except FunctionTimedOut:
            # Handling function timeout from chess engines
            print(players[turn % 2].name,
                  "'s chess engine took to long to play, forfeiting the match to",
                  players[(turn + 1) % 2].name)
            return players[turn % 2] != actor

        except Exception as e:
            # Handle exceptions from chess engines
            print(players[turn % 2].name + "'s chess engine raised the following error, forfeiting the match to",
                  players[(turn + 1) % 2].name, "\n")
            traceback.print_exc()
            # Return true if the `actor` is the winning player
            return players[turn % 2] != actor

        try:
            chess.Move.from_uci(last_move)

        except ValueError as v:
            # Handle incorrectly formatted moves
            print(players[turn % 2].name,
                  "'s chess engine made an incorrectly formatted move")
            print("Move: '" + last_move + "'\n")
            print(
                "The move must be a UCI string of length 4 or 5. For details, check out README.md")
            print("Forfeiting the match to", players[(turn + 1) % 2].name)
            # Return true if the `actor` is the winning player
            return players[turn % 2] != actor

        if chess.Move.from_uci(last_move) not in list(Board.legal_moves):
            # Handle illegal move from chess engines
            print(players[turn % 2].name +
                  "'s chess engine made the following illegal move:", last_move, "\n")
            # Printing the board and the illegal move
            print("A B C D E F G H\n----------------")
            print(Board)
            print("----------------\nA B C D E F G H\n")
            # Return true if the `actor` is the winning player
            return players[turn % 2] != actor

        if not QUIET:
            # Printing State if not in quiet mode
            print("Turn:", turn)
            print("Player:", players[turn % 2].name)
            print("Side:", ["WHITE", "BLACK"][turn % 2])
            print("Move:", last_move)
            print(Board, "\n")
        else:
            print("Progress: ", turn, "turn" + (turn != 1) * "s", end="\r")

        Board.push(chess.Move.from_uci(last_move))
        turn += 1

    print("\nTurns:", turn, "\nResults:", Board.result())

    actor_win = Board.king(players[0] == actor)
    return actor_win


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hq")
    except getopt.GetoptError:
        print(
            "usage: match.py [-q quiet] [-h help] <playerA> <playerB> <time limit (seconds)>")
        sys.exit(2)
    if not args:
        print(
            "usage: match.py [-q quiet] [-h help] <playerA> <playerB> <time limit (seconds)>")
        sys.exit(2)

    playerA = args[0]
    playerB = args[1]
    time_limit = int(args[2])
    run_quiet = '-q' in dict(opts).keys()
    help = '-h' in dict(opts).keys()

    compete(playerA, playerB, time_limit, run_quiet)
