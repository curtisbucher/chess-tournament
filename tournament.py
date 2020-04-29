""" Play all the algorithms against each other and determine a winner """

import os
import sys
import getopt
import random
import importlib
import chess
import typing
from typing import List, Union
import traceback
from func_timeout import func_timeout, FunctionTimedOut
import math


class Competitor:
    def __init__(self, username):
        """ init """
        self.name = username
        self.path = '.'.join(["competitors", username, "main"])
        self.engine = importlib.import_module(self.path)

    def reset_engine(self):
        """ Resets engine to play another round """
        self.engine = importlib.reload(self.engine)


def main(TIME_LIMIT: int, QUIET=False) -> str:
    """ Sets up a bracket, pits all the engines against one another and returns
        the name of the winner """
    # Get list of all the algorithms
    competitors = [Competitor(name) for name in os.listdir('competitors')]

    # Adding byes to make list length a power of 2
    extra = 2 ** round(math.log2(len(competitors))) - len(competitors)
    competitors += [None] * extra

    # Randomizing
    random.shuffle(competitors)

    # Compete until one winner left
    while len(competitors) > 1:
        print("Competitors:", [x.name if x !=
                               None else "None" for x in competitors], "\n")
        winners: List[Competitor] = []
        for x in range(0, len(competitors), 2):
            winners += [compete(competitors[x], competitors[x + 1],
                                TIME_LIMIT, QUIET)]
        competitors = list(winners)

    # Return winners name
    print(competitors[0].name)
    return competitors[0].name


def compete(player1: Competitor, player2: Competitor, TIME_LIMIT: int, QUIET: bool) -> Competitor:
    """ Plays two chess engines and returns the winner"""
    # Returning an automatic win if playing a bye
    if not player1:
        print(player2.name, "has a bye")
        return player2
    elif not player2:
        print(player1.name, "has a bye")
        return player1

    print("Playing:", player1.name, player2.name)

    player1.reset_engine()
    player2.reset_engine()
    players = player1, player2

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
            return players[(turn + 1) % 2]

        except Exception as e:
            # Handle exceptions from chess engines
            print(players[turn % 2].name + "'s chess engine raised the following error, forfeiting the match to",
                  players[(turn + 1) % 2].name, "\n")
            traceback.print_exc()
            # Return true if the `actor` is the winning player
            return players[(turn + 1) % 2]

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
            return players[(turn + 1) % 2]

        if chess.Move.from_uci(last_move) not in list(Board.legal_moves):
            # Handle illegal move from chess engines
            print(players[turn % 2].name +
                  "'s chess engine made the following illegal move:", last_move, "\n")
            # Printing the board and the illegal move
            print("A B C D E F G H\n----------------")
            print(Board)
            print("----------------\nA B C D E F G H\n")
            # Return true if the `actor` is the winning player
            return players[(turn + 1) % 2]

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

    # Returning the winning player
    result = Board.result()
    if len(result) > 3:  # Returning a random player in the event of a draw (1/2,1/2). (Not Ideal)
        winner = random.choice(players)
        print("Draw: Coin flip goes to", winner.name)
        return winner
    else:  # Returning the winner
        if int(result[0]):
            print("Winner:", players[0])
            return players[0]
    print("Winner:", player[1])
    return players[1]


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hq")
    except getopt.GetoptError:
        print(
            "usage: qualify.py [-q quiet] <time limit (seconds)>")
        sys.exit(2)

    if '-h' in dict(opts).keys() or not args:
        print(
            "usage: qualify.py [-q quiet] <time limit (seconds)>")
        sys.exit(2)

    time_limit = int(args[0])
    run_quiet = '-q' in dict(opts).keys()
    main(time_limit, run_quiet)
