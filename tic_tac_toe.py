from typing import Text



def init_board(board_size, ):
    """
        tested: True
    """
    board = []
    for row in range(board_size):
        new_row = []
        for column in range(board_size):
            new_row.append(".")
        board.append(new_row)
    return board


def print_board(board):
    play_board = []
    for i in board:
        for k in i:
            if k == 0:
                play_board.append('.')
            elif k == 1:
                play_board.append('X')
            else:
                play_board.append('O')
    print('')
    print('     1   2   3')
    print('')
    print('       |   |')
    print(' A   %s | %s | %s' % (play_board[0], play_board[1], play_board[2]))
    print('       |   |')
    print('   ----+---+----')
    print('       |   |')
    print(' B   %s | %s | %s' % (play_board[3], play_board[4], play_board[5]))
    print('       |   |')
    print('   ----+---+----')
    print('       |   |')
    print(' C   %s | %s | %s' % (play_board[6], play_board[7], play_board[8]))
    print('       |   |')
    return


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


def is_valid_coordinate(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board):
        return True
    return False


def get_ai_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    row, col = 0, 0
    return row, col


def mark(board, player):
    row, column = get_move(board)
    if player == 0:
        board[row][column] = "X"
    else:
        board[row][column] = "O"


def has_won(board, player):
    """Returns True if player has won the game."""
    

    return False


def is_full(board):
    for row in board:
        for column in row:
            if board[row][column] == '.':
                return False
    return True


def print_board(board):
    """Prints a 3-by-3 board on the screen with borders."""
    pass


def print_result(winner):
    """Congratulates winner or proclaims tie (if winner equals zero)."""
    pass


def tictactoe_game(mode='HUMAN-HUMAN'):
    board = init_board()

    # use get_move(), mark(), has_won(), is_full(), and print_board() to create game logic
    print_board(board)
    row, col = get_move(board, 1)
    mark(board, 1, row, col)

    winner = 0
    print_result(winner)


def main_menu():
    tictactoe_game('HUMAN-HUMAN')


if __name__ == '__main__':
    main_menu()
