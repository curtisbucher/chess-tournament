import chessboard
import copy
board = chessboard.board()

pieces = copy.copy(board.pieces)

count = 0
newstring = ""
for row in pieces:
    for square in row:
        if square == ' ':
            count += 1
        elif count > 0:
            newstring += str(count)
            count = 0
        else:
            newstring += square
    if count > 0:
        newstring += str(count)
        count = 0
    newstring += "/"


print(count)
print(newstring)
