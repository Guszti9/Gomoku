from os import system
import random
import time


ABC = "ABCDEFGHIJKLMNOPQRST"
LOGO = "logo.txt"
GAME_OVER_1 = "game_over_1.txt"
GAME_OVER_2 = "game_over_2.txt"
X_WON = "x_won.txt"
Y_WON = "y_won.txt"
TIED = "tie.txt"


def init_board(board_size=3):
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
    while True:
        inp = input("Enter your cordinate!")

        if inp.lower() == 'q' or inp.lower() == 'quit':
            return None

        if len(inp) > 1:
            if inp[0] in ABC:
                row = int(ABC.find(inp[0]))
            else:
                print("First cordinate not valid")
                continue
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
                print("Cordinate is out of board!")
        else:
            print("Input is too short!")


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


def is_coordinate_wons(board, row, col, player, need_to_connect=3):
    row_win = [(row + r, col) for r in range(need_to_connect)]
    if is_coordinate_list_wons(board, row_win, player):
        return True
    col_win = [(row, col + c) for c in range(need_to_connect)]
    if is_coordinate_list_wons(board, col_win, player):
        return True
    diag_win_1 = [(row + d, col + d) for d in range(need_to_connect)]
    if is_coordinate_list_wons(board, diag_win_1, player):
        return True
    diag_win_2 = [(row - d, col + d) for d in range(need_to_connect)]
    if is_coordinate_list_wons(board, diag_win_2, player):
        return True
    return False


def has_won(board, player, need_to_connect):
    for row in range(len(board)):
        for col in range(len(board)):
            if is_coordinate_wons(board, row, col, player, need_to_connect):
                return True
    return False


def is_full(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '.':
                return False
    return True


def clear():
    _ = system('clear')


def create_margin(margin):
    re = ""
    for i in range(margin):
        re += ' '
    return re


def print_board(board, margin=0):
    board_print = []
    for row in range(len(board)):
        row_print = ""
        for col in range(len(board) - 1):
            row_print += f" {board[row][col]} |"
        row_print += ' ' + board[row][len(board) - 1]
        board_print.append(row_print)

    first_line = create_margin(margin)
    for number in range(1, len(board) + 1):
        if number <= 10:
            first_line += f"   {number}"
        else:
            first_line += f"  {number}"

    blank_line = create_margin(margin) + "  ---"
    for i in range(len(board) - 1):
        blank_line += "+---"

    print(first_line)
    print(create_margin(margin) + ABC[0] + ' ' + board_print[0])
    for row in range(1, len(board)):
        row_print = create_margin(margin) + ABC[row] + ' ' + board_print[row]
        print(blank_line)
        print(row_print)
    print('\n')


def print_result(result, board, board_margin):
    for elapsed_time in range(12):
        clear()
        if elapsed_time % 2 == 0:
            print_file(GAME_OVER_1)
        else:
            print_file(GAME_OVER_2)
        print_file(result)
        print_board(board, board_margin)
        time.sleep(0.5)

    time.sleep(2)


def print_file(file_reference):
    with open(file_reference, "r") as file:
        print(file.read())


def print_main_menu():
    clear()
    print_file(LOGO)
    print('''
                  ---  1: Tic-Tac-Toe   ---
                  ---  2: Small Board   ---
                  ---  3: Madium Board  ---
                  ---  4:  Huge Board   ---
                  ---       Quit        ---

    ''')


def get_result(board, player, need_to_connect):
    if has_won(board, player, need_to_connect):
        if player == 'X':
            return X_WON
        else:
            return Y_WON
    if is_full(board):
        return TIED
    return None


def switch_player(player):
    if player == 'X':
        return 'o'
    return 'X'


def tictactoe_game(mode='HUMAN-HUMAN',  board_size=3, need_to_connect=3, board_margin=0):
    board = init_board(board_size)
    player = random.choice(['X', 'O'])

    while(True):
        player = switch_player(player)
        clear()
        print_board(board)

        print(f"It is {player} turn!")
        coordinate = get_move(board)
        if coordinate is None:
            return
        mark(board, player, coordinate[0], coordinate[1])

        result = get_result(board, player, need_to_connect)
        if result is not None:
            clear()
            print_result(result, board, board_margin)
            return


def main_menu():
    while True:
        print_main_menu()
        inp = input()
        if inp.lower() == 'quit' or inp.lower() == 'q':
            return
        if inp == '1':
            tictactoe_game(board_margin=44)
        if inp == '2':
            tictactoe_game(board_size=5, need_to_connect=4, board_margin=40)
        if inp == '3':
            tictactoe_game(board_size=10, need_to_connect=5, board_margin=28)
        if inp == '4':
            tictactoe_game(board_size=20, need_to_connect=5, board_margin=5)


if __name__ == '__main__':
    main_menu()
