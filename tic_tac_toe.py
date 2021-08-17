from typing import Text


abc = "ABCDEFGHIJKLMNOPQRST"

def init_board(board_size):
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


def is_valid_coordinate(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board):
        return True
    return False


def is_coordinate_free(board, row, col):
    if board[row][col] == '.':
        return True
    return False


def get_move(board):
    """Returns the coordinates of a valid move for player on board."""
    while True:
        inp = input("Enter your cordinate!")
        if inp[0] in abc:
            row = int(abc.find(inp[0]))
        else:
            print("First cordinate not valid")
        try:
            col = int(inp[1:]) - 1
        except ValueError:
            print("Second coordinat is not number")
            continue
        if is_valid_coordinate(board, row, col):
            if is_coordinate_free(board, row, col):
                return row, col
            else:
                print("Cordinat already occupied")
        else:
            print("Cordinate is not on the board!")


def mark(board, player, row, col):
    if is_valid_coordinate(board, row, col):
        if is_coordinate_free(board, row, col):
            board[row][col] = player
        else:
            print("Coordinet in not free!")
    else:
        print("Coordinet is not on the board!")


def get_ai_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    row, col = 0, 0
    return row, col


def is_coordinate_list_wons(board, list, player):
    for coordinates in list:
        if is_valid_coordinate(board, coordinates[0], coordinates[1]):
            if not board[coordinates[0]][coordinates[1]] == player:
                return False
        else:
            return False

    return True


def is_coordinate_wons(board, row, col, player):
    row_win = [(row + r, col) for r in range(3)]
    if is_coordinate_list_wons(board, row_win, player):
        return True
    col_win = [(row, col + c) for c in range(3)]
    if is_coordinate_list_wons(board, col_win, player):
        return True
    diag_win_1 = [(row + d, col + d) for d in range(3)]
    if is_coordinate_list_wons(board, diag_win_1, player):
        return True
    diag_win_2 = [(row - d, col + d) for d in range(3)]
    if is_coordinate_list_wons(board, diag_win_2, player):
        return True
    return False


def has_won(board, player):
    for row in board:
        for col in board:
            if is_coordinate_wons(board, row, col, player):
                return True
    return False


def is_full(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '.':
                return False
    return True


def print_board(board):
    board_print = []
    for row in range(len(board)):
        row_print = ""
        for col in range(len(board) - 1):
            row_print += f" {board[row][col]} |"
        row_print += board[row][len(board) - 1]
        board_print.append(row_print)

    blank_line = "  ---"
    for i in range(len(board) - 1):
        blank_line += "+---"

    first_line = ""
    for number in range(1, len(board) + 1):
        first_line += f"   {number}"

    print(first_line)
    print(abc[0] + ' ' + board_print[0])
    for row in range(1, len(board)):
        row_print = abc[row] + ' ' + board_print[row]
        print(blank_line)
        print(row_print)


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
    print_board([['.', '.', '.', 'X'], ['.', '.', '.', 'Q'], ['.', '.', '.', 'X']])
    main_menu()
