# This Program is responsible for playing the owner of the PR against a random
# opponent to determine if he can join the tournament
import os
import sys
import random
import importlib
import chess


def main():
    # Getting list of competing algorithms, then selecting a random opponent engine to play
    # actor = sys.argv[1]
    ######################
    actor = "curtisbucher"
    ######################
    actor_path = '.'.join(["competitors", actor, "main"])

    competitors = os.listdir('competitors')
    competitors.remove(actor)

    opponent = random.choice(competitors)
    opponent_path = '.'.join(["competitors", opponent, "main"])

    opp_engine = importlib.import_module(opponent_path)
    actor_engine = importlib.import_module(actor_path)

    # Competition Loop
    players = [opp_engine, actor_engine]
    random.shuffle(players)

    turn = 0
    Board = chess.Board()
    last_move = ""

    print("WHITE:", actor)
    print("BLACK:", opponent)

    while not Board.is_game_over():
        print(turn)
        if turn % 2:
            print("BLACK: ", end="")
        else:
            print("WHITE: ", end="")

        # Needs to tell them if they are white or black, or possibly have both be white
        last_move = players[turn % 2].make_move(last_move, Board)

        print(last_move)
        if chess.Move.from_uci(last_move) not in list(Board.legal_moves):
            print(Board)
            raise (BaseException("Illegal Move"))

        Board.push(chess.Move.from_uci(last_move))
        turn += 1

    print(Board.result())


if __name__ == "__main__":
    main()
