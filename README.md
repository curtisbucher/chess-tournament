# chess-tournament
A competitive chess tournament run weekly in this repository. Contestants are added by cloning the repository and opening a pull request with your new chess engine.

---

### Here's how it works

1. Prospective competitors clone this chess-tournament repo onto their local machine, using `git clone https://github.com/curtisbucher/chess-tournament`
2. Competitor creates a folder in the `/competitors` directory that matches their github username exactly. For example, my own folder is be under `/competitors/curtisbucher`
3. Competitors develope their chess engine in this user folder. We wanna see the best chess engines possible, so rules are pretty lax considering how you design your engine. While you are developing your chess engine, developers can run `qualify.py [-q] <username>` to your engine against a random opponent, or use `tournament.py` to see how your engine stacks up against the competition.
4. Once you, the developer, are happy with your chess engine, you will submit a pull request to branch `master ` of the  `chess-tournament` repository, where your PR will be run through a series of tests, to determine your engines eligibility. Your chess engine is eligible to play in tournaments if it
    * Doesn't break any of our (very few) rules.
    * And beats our default chess engine. (Don't worry it plays poorly)

---

### Getting Started

##### Structure

We have a few requirements for each developer's chess engine. The main functions `tournament.py` and `qualify.py` communicate with each user's engine by importing `main.py` from the user's home folder in the `/competitors` directory. Here is an example repository structure.

```
.
├── tournament.py
├── qualify.py
├── competitors
|   ├── usernameA
|		├── usernameB
|   └── curtisbucher
|		|   └── main.py
|		|   └── requirements.txt (if you import other modules)
```

From `/competitors/username/main.py` the engine calls the function `get_move(last_move, time_limit)`. Our protocol aims to be as simple and universal as possible, so each developer's chess engine is responsible for keeping track of the current board state, providing only the last move played by the opponent. A chess engine can determine whether it is black or white the first time `get_move(last_move, time_limit)` is called. If `last_move` is an empty string, than your chess engine is white, and plays first. If last move is anything else, than your chess engine is black and plays second.

##### Move Notation

We use [UCI chess notation](https://en.wikipedia.org/wiki/Universal_Chess_Interface) to communicate between chess engines. We assign every column (file) on the board a letter, and every row (rank) a number. This way, each square on the board has its own unique identifier.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/SCD_algebraic_notation.svg/1200px-SCD_algebraic_notation.svg.png" alt="chessboard" style="zoom: 33%;" />


A move is denoted by first stating the origin coordinates (file, rank) of the piece, then the destination coordinates (file, rank) of the peice. For example, to move the left black knight forward in this picture, the engine could send the string `"b8c6"` or `"b8a6"`. Pawn promotions are denoted by adding an extra fifth character to the end stating the desired promotion. For example, `"a7a8q"` to promote a white pawn to a queen.

The structure is as follows `[Origin File][Origin Rank][Destination File][Destination Rank]{Promoted Peice}`

##### Rules

We have a few rules to keep the repository clean and to maintain a fair playing environment.

* **Time Limit**: Chess engines must play within the time passed to the `get_move(last_move, time_limit)` function. Failing to return a valid chess move withing this time will forfeit the game to the opponent. To limit the duration of qualifying and tournaments, the time limit for current chess engines is set at **10 seconds**. It is recommended that you have a timer in your program to send your current best move before your time is over. There are many clever ways of doing this.
* **Valid Play**: Making an illegal or invalid move during tournament play or qualifying results in a forfeited game or a failure to qualify. An illegal move is a valid UCI move that cannot be played at that time. An invalid move is an invalid UCI move, like "`foo`" or `a1b2h4`.
* **General Mischeif**: Don't do anything sneaky like messing with other people's programs in the repository or messing with the qualifying and tournament software. We have tests for this, and any mischeif will permanently ban a developer from the tournament.

