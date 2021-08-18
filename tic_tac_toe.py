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
MENTOR_BOSS = "mentorBoss_loading.txt"


#Board functions
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


def mark(board, player, row, col):
    if is_valid_coordinate(board, row, col):
        if is_coordinate_free(board, row, col):
            board[row][col] = player
        else:
            print("Coordinet in not free!")
    else:
        print("Coordinet is not on the board!")


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


def get_result(board, player, need_to_connect):
    if has_won(board, player, need_to_connect):
        if player == 'X':
            return X_WON
        else:
            return Y_WON
    if is_full(board):
        return TIED
    return None


#AI engin
def get_ai_move(board, player, need_to_connect):
    weight_board = create_weighted_board(board, need_to_connect)

    for row in weight_board:
        str_row = ''
        for elem in row:
            str_row += ' ' + str(elem)
        print(str_row)

    best_value = max([max(weighted_row) for weighted_row in weight_board])
    potential_steps = get_all_potential(weight_board, best_value)

    return random.choice(potential_steps)


def get_all_potential(weight_board, best_value):
    r = 0
    potential_steps = []
    for row in weight_board:
        c = 0
        for col in row:
            if col == best_value:
                potential_steps.append((r, c))
            c += 1
        r += 1
    return potential_steps


def create_weighted_board(board, need_to_connect):
    weight_board = []
    for row in range(len(board)):
        wighted_row = []
        for col in range(len(board)):
            if board[row][col] == '.':
                wighted_row.append(weight_field(board, row, col, need_to_connect))
            else:
                wighted_row.append(-1)
        weight_board.append(wighted_row)
    return weight_board


def weight_field(board, row, col, need_to_connect):
    row_list = [(row, c) for c in range(len(board))]
    weight_row_list = weight_list(board, row_list, row, col, need_to_connect)
    col_list = [(r, col) for r in range(len(board))]
    weight_col_list = weight_list(board, col_list, row, col, need_to_connect)
    diag_1_list = []
    diag_2_list = []
    for r in range(len(board)):
        c = col + r - row
        if len(board) - 1 >= c and c >= 0:
            diag_1_list.append((r, c))
        c = row + col - r
        if len(board) - 1 >= c and c >= 0:
            diag_2_list.append((r, c))
    weight_diag_1_list = weight_list(board, diag_1_list, row, col, need_to_connect)
    weight_diag_2_list = weight_list(board, diag_2_list, row, col, need_to_connect)

    offensive_value = weight_row_list[0] + weight_col_list[0] + weight_diag_1_list[0] + weight_diag_2_list[0]
    defensive_value = weight_row_list[1] + weight_col_list[1] + weight_diag_1_list[1] + weight_diag_2_list[1]

    return offensive_value + defensive_value


def weight_list(board, list, row, col, need_to_connect):
    index = list.index((row, col))
    character_list = [board[cord[0]][cord[1]] for cord in list]

    defensive_value = block_value(character_list, index)
    offens_value = attack_value(character_list, index, need_to_connect)

    return offens_value, defensive_value


def attack_value(character_list, index, need_to_connect):
    count = 1
    half_blocked = 0

    if index > 0 and character_list[index - 1] == "O":
        i = index - 1
        while i >= 0 and character_list[i] == "O":
            count += 1
            i -= 1
            if i == 0 or character_list[i] == 'X':
                half_blocked += 1

    if index < len(character_list) - 1 and character_list[index + 1] == "O":
        i = index + 1
        while i < len(character_list) and character_list[i] == "O":
            count += 1
            i += 1
            if i == len(character_list) or character_list[i] == 'X':
                half_blocked += 1

    if index == 0 or character_list[index - 1] == "X":
        half_blocked += 1

    if index == len(character_list) - 1 or character_list[index + 1] == "X":
        half_blocked += 1

    return get_points_for_offens(count, half_blocked, need_to_connect)


def get_points_for_offens(count, half_blocked, need_to_connect):
    point = 0

    if count == need_to_connect:
        return 1000

    if count == 1 and half_blocked == 0:
        point = 0.5
    if count == 2:
        if half_blocked == 0:
            point = 4
        elif half_blocked == 1:
            point = 1
    if count == 3:
        if half_blocked == 0:
            point = 9
        elif half_blocked == 1:
            point = 4

    return point


def block_value(character_list, index):
    point = 0

    if index > 0 and character_list[index - 1] == "X":
        count = 0
        is_ather_half_block = False
        i = index - 1
        while i >= 0 and character_list[i] == "X":
            count += 1
            i -= 1
            if i == 0 or character_list[i] == '0':
                is_ather_half_block = True
        point += get_points_for_defense(count, is_ather_half_block)

    if index < len(character_list) - 1 and character_list[index + 1] == "X":
        count = 0
        is_ather_half_block = False
        i = index + 1
        while i < len(character_list) and character_list[i] == "X":
            count += 1
            i += 1
            if i == len(character_list) or character_list[i] == '0':
                is_ather_half_block = True
        point += get_points_for_defense(count, is_ather_half_block)

    return point


def get_points_for_defense(count, is_ather_half_block):
    point = 0
    if count == 1:
        point += 1
    if count == 2:
        if is_ather_half_block:
            point = 2
        else:
            point = 5
    if count == 3:
        if is_ather_half_block:
            point = 5
        else:
            point = 16
    if count == 4:
        point = 32

    return point


#Print functions
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


def print_mentorBoss_loading():
    clear()
    with open(MENTOR_BOSS, "r") as file:
        lines = [line.split(' @ ') for line in file]
        for line in lines:
            print(line[0])
            time.sleep(float(line[1].replace('\n', '')))

    time.sleep(5)


#Input functions
def get_move(board):
    while True:
        inp = input("Enter your cordinate!")

        if inp.lower() == 'q' or inp.lower() == 'quit':
            return None

        if len(inp) > 1:
            if inp[0].upper() in ABC:
                row = int(ABC.find(inp[0].upper()))
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


def switch_player(player):
    if player == 'X':
        return 'O'
    return 'X'


def tictactoe_game(mode='HUMAN-HUMAN',  board_size=3, need_to_connect=3, board_margin=0):
    board = init_board(board_size)
    player = random.choice(['X', 'O'])

    while(True):
        player = switch_player(player)
        clear()
        print_board(board)
        print(f"It is {player} turn!")

        if mode == 'VS-AI':
            if player == 'O':
                coordinate = get_ai_move(board, player, need_to_connect)
            else:
                coordinate = get_move(board)
        else:
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
    print_mentorBoss_loading()

    while True:
        print_main_menu()
        inp = input()
        if inp.lower() == 'quit' or inp.lower() == 'q':
            return
        if inp == '1':
            tictactoe_game(mode='VS-AI', board_margin=44)
        if inp == '2':
            tictactoe_game(board_size=5, need_to_connect=4, board_margin=40)
        if inp == '3':
            tictactoe_game(mode='VS-AI', board_size=10, need_to_connect=5, board_margin=28)
        if inp == '4':
            tictactoe_game(board_size=20, need_to_connect=5, board_margin=5)


#MAIN
if __name__ == '__main__':
    main_menu()
