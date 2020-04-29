# chess-tournament
 [[In Progress]]
Contestants make a PR to add a directory with their github username into the "contestants" folder.
When the PR is run, a workflow runs the program against a randomely selected program.
If the new program wins, it is added to the tournament, and every weekday the tournament is run to determine who is in first place.

Each contestant must have a method in their program called `get_move(move)` that takes in a string representing the other players move in chess coordinate notation. For example, `b1c3` to move a peice, or `a7a8q` to promote a pawn to a queen. The first move of the game is denoted by a blank string for `move`. This also indicates to the chess engine that they are the white player. If the engine receives a move on it's first round, then it is the black player.

The structure is as follows `[Origin File][Origin Rank][Destination File][Destination Rank]{Promoted Peice}`