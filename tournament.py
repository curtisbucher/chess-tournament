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
from match import compete


def main(TIME_LIMIT: int, QUIET=False) -> str:
    """ Sets up a bracket, pits all the engines against one another and returns
        the name of the winner """
    # Get list of all the algorithms
    competitors = [name for name in os.listdir('competitors')]

    # Storing the competitors in reverse order of how well they did
    rankings: List[str] = []

    # Adding byes to make list length a power of 2
    extra = 2 ** round(math.log2(len(competitors))) - len(competitors)
    competitors += [None] * extra

    # Randomizing
    random.shuffle(competitors)

    # Compete until one winner left
    while len(competitors) > 1:
        print("Competitors:", [name if name !=
                               None else "None" for name in competitors], "\n")
        winners: List[str] = []
        for x in range(0, len(competitors), 2):
            if compete(competitors[x], competitors[x + 1], TIME_LIMIT, QUIET):
                winners += competitors[x]
                if competitors[x+1]:
                    rankings += competitors[x + 1]
                print(competitors[x], "beat", competitors[x + 1])
            else:
                winners += competitors[x + 1]

                print(competitors[x+1], "beat", competitors[x])

        competitors = list(winners)

    # Return winners name
    print(competitors[0])
    return competitors[0]


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hq")
    except getopt.GetoptError:
        print(
            "usage: tournament.py [-q quiet] <time limit (seconds)>")
        sys.exit(2)

    if '-h' in dict(opts).keys() or not args:
        print(
            "usage: tournament.py [-q quiet] <time limit (seconds)>")
        sys.exit(2)

    time_limit = int(args[0])
    run_quiet = '-q' in dict(opts).keys()
    main(time_limit, run_quiet)
