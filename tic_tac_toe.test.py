def get_move(board):
    abc = "ABC"
    """Returns the coordinates of a valid move for player on board."""
    while True:
        inp = input("Enter your cordinate!")
        if not len(inp) == 2:
            print("Not valid")
        else:
            if inp[0] in abc:
                row = int(abc.find(inp[0]))
            else:
                print("First cordinate not valid")
            try:
                col = int(inp[1]) - 1
            except ValueError:
                print("Second coordinat is not number")
                continue
            if not row == -1 and 0 <= col < len(board):
                if board[row][col] == '.':
                    return row, col
                else:
                    print("Cordinat already occupied")
            else:
                print("Cordinate not on the board!")

get_move()