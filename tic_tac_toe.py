from os import system
import random
import time

ABC = "ABCDEFGHIJKLMNOPQRST"
LOGO = "logo.txt"
GAME_OVER_1 = "game_over_1.txt"
GAME_OVER_2 = "game_over_2.txt"
X_WON = "x_won.txt"
O_WON = "o_won.txt"
TIED = "tie.txt"
MENTOR_BOSS = "mentorBoss_loading.txt"
PLAYERS = ['X', 'O']


# General functions

def switch_player(player):
    if player == 'X':
        return 'O'
    return 'X'


def is_valid_coordinate(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board):
        return True
    return False


def is_coordinate_free(board, row, col):
    if board[row][col] == '.':
        return True
    return False


# Board functions

def init_board(board_size=3):
    board = []
    for row in range(board_size):
        new_row = []
        for column in range(board_size):
            new_row.append(".")
        board.append(new_row)
    return board


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
            return O_WON
    if is_full(board):
        return TIED
    return None


# AI engin
# Minimax method

def get_ai_move_with_minimax(board, need_to_connect, x_best_move, max_depth, player='O'):
    simple_weight_board, board_statistice = create_weighted_board(board, need_to_connect, player)

    best_move = (-1, -1)

    best_val = -100000
    for coordinates in get_x_best_move(simple_weight_board, x_best_move):
        board[coordinates[0]][coordinates[1]] = player
        move_val = minimax_ai_move(board, need_to_connect, x_best_move, switch_player(player), max_depth)
        board[coordinates[0]][coordinates[1]] = '.'
        if best_val < move_val:
            best_val = move_val
            best_move = coordinates

    return best_move


def minimax_ai_move(board, need_to_connect, x_best_move, player='O', max_depth=4, depth=0):
    simple_weight_board, board_statistice = create_weighted_board(board, need_to_connect, player)

    if has_won(board, player, need_to_connect):
        if player == 'O':
            return 10000
        else:
            return -10000

    if has_won(board, switch_player(player), need_to_connect):
        if switch_player(player) == 'O':
            return 10000
        else:
            return -10000

    if is_full(board):
        return 0

    if depth == max_depth:
        if player == 'O':
            return board_statistice[0] - board_statistice[1]
        else:
            return board_statistice[1] - board_statistice[0]

    if player == 'O':
        best = - 100000
        for coordinates in get_x_best_move(simple_weight_board, x_best_move):
            board[coordinates[0]][coordinates[1]] = player

            best = max(best, minimax_ai_move(board, need_to_connect, x_best_move, switch_player(player), max_depth, depth + 1))

            board[coordinates[0]][coordinates[1]] = '.'

        return best
    else:
        best = 100000
        for coordinates in get_x_best_move(simple_weight_board, x_best_move):
            board[coordinates[0]][coordinates[1]] = player

            best = min(best, minimax_ai_move(board, need_to_connect, x_best_move, switch_player(player), max_depth, depth + 1))

            board[coordinates[0]][coordinates[1]] = '.'
        return best


def get_x_best_move(simple_weight_board, x):
    potential_steps = []
    r = 0
    for row in simple_weight_board:
        c = 0
        for col in row:
            if col >= 0:
                if len(potential_steps) < x:
                    potential_steps.append((r, c))
                else:
                    sort_potential_steps(simple_weight_board, potential_steps, x)
                    if col > simple_weight_board[potential_steps[x-1][0]][potential_steps[x-1][1]]:
                        potential_steps[x-1] = (r, c)
            c += 1
        r += 1

    return potential_steps


def sort_potential_steps(simple_weight_board, potential_steps, x):
    number_list = [simple_weight_board[row][col] for row, col in potential_steps]

    for i in range(10):
        max_val = max(number_list)
        max_index = number_list.index(max_val)
        number_list[max_index] = -100
        potential_steps.append(potential_steps[max_index])
    del potential_steps[0:x]


# Basic Method

def get_ai_move(board, need_to_connect, player='O'):
    simple_weight_board, board_statistice = create_weighted_board(board, need_to_connect, player)

    best_value = max([max(weighted_row) for weighted_row in simple_weight_board])
    potential_steps = get_all_potential(simple_weight_board, best_value)

    return random.choice(potential_steps)


def get_all_potential(simple_weight_board, best_value):
    r = 0
    potential_steps = []
    for row in simple_weight_board:
        c = 0
        for col in row:
            if col == best_value:
                potential_steps.append((r, c))
            c += 1
        r += 1

    return potential_steps


def create_weighted_board(board, need_to_connect, player):
    weight_board = []
    for row in range(len(board)):
        wighted_row = []
        for col in range(len(board)):
            if board[row][col] == '.':
                wighted_row.append(weight_field(board, row, col, need_to_connect, player))
            else:
                wighted_row.append(-1)
        weight_board.append(wighted_row)

    return get_simple_weight_board(weight_board), get_board_statistice(weight_board)


def get_simple_weight_board(weight_board):
    simple_weight_board = []
    for weighted_row in weight_board:
        simple_weight_row = []
        for element in weighted_row:
            if element == -1:
                simple_weight_row.append(-1)
            else:
                simple_weight_row.append(element[0] + element[1])
        simple_weight_board.append(simple_weight_row)

    return simple_weight_board


def get_board_statistice(weight_board):
    offens_statistice = 0
    defensive_statistice = 0
    for weighted_row in weight_board:
        for element in weighted_row:
            if not element == -1:
               offens_statistice += element[0]
               defensive_statistice += element[1]

    return offens_statistice, defensive_statistice


def weight_field(board, row, col, need_to_connect, player):
    row_list = [(row, c) for c in range(len(board))]
    weight_row_list = weight_list(board, row_list, row, col, need_to_connect, player)
    col_list = [(r, col) for r in range(len(board))]
    weight_col_list = weight_list(board, col_list, row, col, need_to_connect, player)
    diag_1_list = []
    diag_2_list = []
    for r in range(len(board)):
        c = col + r - row
        if len(board) - 1 >= c and c >= 0:
            diag_1_list.append((r, c))
        c = row + col - r
        if len(board) - 1 >= c and c >= 0:
            diag_2_list.append((r, c))
    weight_diag_1_list = weight_list(board, diag_1_list, row, col, need_to_connect, player)
    weight_diag_2_list = weight_list(board, diag_2_list, row, col, need_to_connect, player)

    offensive_value = weight_row_list[0] + weight_col_list[0] + weight_diag_1_list[0] + weight_diag_2_list[0]
    defensive_value = weight_row_list[1] + weight_col_list[1] + weight_diag_1_list[1] + weight_diag_2_list[1]

    return offensive_value, defensive_value


def weight_list(board, list, row, col, need_to_connect, player):
    index = list.index((row, col))
    character_list = [board[cord[0]][cord[1]] for cord in list]

    defensive_value = block_value(character_list, index, need_to_connect, player)
    offens_value = attack_value(character_list, index, need_to_connect, player)

    return offens_value, defensive_value


def attack_value(character_list, index, need_to_connect, player):
    count = 1
    half_blocked = 0

    if index > 0 and character_list[index - 1] == player:
        i = index - 1
        while i >= 0 and character_list[i] == player:
            count += 1
            i -= 1
            if i == 0 or character_list[i] == switch_player(player):
                half_blocked += 1

    if index < len(character_list) - 1 and character_list[index + 1] == player:
        i = index + 1
        while i < len(character_list) and character_list[i] == player:
            count += 1
            i += 1
            if i == len(character_list) or character_list[i] == switch_player(player):
                half_blocked += 1

    if index == 0 or character_list[index - 1] == switch_player(player):
        half_blocked += 1

    if index == len(character_list) - 1 or character_list[index + 1] == switch_player(player):
        half_blocked += 1

    return get_points_for_offens(count, half_blocked, need_to_connect)


def get_points_for_offens(count, half_blocked, need_to_connect):
    point = 0

    if count == need_to_connect:
        return 1000

    if count == need_to_connect - 1 and half_blocked == 0:
        return 100

    if count == 1 and half_blocked == 0:
        point = 0.5
    if count == 2:
        if half_blocked == 0:
            point = 4
        elif half_blocked == 1:
            point = 1
    if count == 3:
        if half_blocked == 0:
            point = 16
        elif half_blocked == 1:
            point = 4
    if count == 4 and half_blocked == 1:
        point = 15

    return point


def block_value(character_list, index, need_to_connect, player):
    point = 0

    if index > 0 and character_list[index - 1] == switch_player(player):
        count = 0
        is_ather_half_block = False
        i = index - 1
        while i >= 0 and character_list[i] == switch_player(player):
            count += 1
            i -= 1
            if i == 0 or character_list[i] == player:
                is_ather_half_block = True
        point += get_points_for_defense(count, is_ather_half_block, need_to_connect)

    if index < len(character_list) - 1 and character_list[index + 1] == switch_player(player):
        count = 0
        is_ather_half_block = False
        i = index + 1
        while i < len(character_list) and character_list[i] == switch_player(player):
            count += 1
            i += 1
            if i == len(character_list) or character_list[i] == player:
                is_ather_half_block = True
        point += get_points_for_defense(count, is_ather_half_block, need_to_connect)

    return point


def get_points_for_defense(count, is_ather_half_block, need_to_connect):
    if count == need_to_connect - 1:
        return 500

    if count == need_to_connect - 2 and not is_ather_half_block:
        return 50

    point = 0
    if count == 1:
        point = 1
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


# Print functions
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


def print_game_mode():
    clear()
    print_file(LOGO)
    print('''
               ---  1: Human vs Human       ---
               ---  2: Human vs Ai          ---
               ---  3: Human vs MentorBoss  ---
               ---  4: Ai vs Ai             ---
               ---          Quit            ---

    ''')


def print_mentorBoss_loading():
    clear()
    with open(MENTOR_BOSS, "r") as file:
        lines = [line.split(' @ ') for line in file]
        for line in lines:
            print(line[0])
            time.sleep(float(line[1].replace('\n', '')))

    time.sleep(5)


# Input functions
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


def x_best_move_by_board_size(board_size):
    if board_size == 3:
        return 9
    if board_size == 5:
        return 1
    return 3


def get_max_depth_by_board_size(board_size):
    if board_size == 3:
        return 4
    if board_size == 5:
        return 1
    return 2


def tictactoe_game(board_size=3, need_to_connect=3, board_margin=0, mode='HUMAN-HUMAN'):
    board = init_board(board_size)
    player = random.choice(PLAYERS)

    x_best_move = x_best_move_by_board_size(board_size)
    max_depth = get_max_depth_by_board_size(board_size)

    while(True):
        player = switch_player(player)
        clear()
        print_board(board)
        print(f"It is {player} turn!")

        if mode == 'HUMAN_HUMAN':
            coordinate = get_move(board)

        if mode == 'HUMAN-AI':
            if player == 'O':
                coordinate = get_ai_move(board, need_to_connect)
            else:
                coordinate = get_move(board)

        if mode == 'HUMAN-MENTORBOSS':
            if player == 'O':
                coordinate = get_ai_move_with_minimax(board, need_to_connect, x_best_move, max_depth)
            else:
                coordinate = get_move(board)

        if mode == 'AI-AI':
            coordinate = get_ai_move(board, need_to_connect, player)
            time.sleep(1)

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
            game_mode(board_margin=44)
        if inp == '2':
            game_mode(board_size=5, need_to_connect=4, board_margin=40)
        if inp == '3':
            game_mode(board_size=10, need_to_connect=5, board_margin=28)
        if inp == '4':
            game_mode(board_size=20, need_to_connect=5, board_margin=5)


def game_mode(board_size=3, need_to_connect=3, board_margin=0):
    while True:
        print_game_mode()
        inp = input()
        if inp.lower() == 'quit' or inp.lower() == 'q':
            return
        if inp == '1':
            tictactoe_game(board_size, need_to_connect, board_margin, mode='HUMAN-HUMAN')
            return
        if inp == '2':
            tictactoe_game(board_size, need_to_connect, board_margin, mode='HUMAN-AI')
            return
        if inp == '3':
            print_mentorBoss_loading()
            tictactoe_game(board_size, need_to_connect, board_margin, mode='HUMAN-MENTORBOSS')
            return
        if inp == '4':
            tictactoe_game(board_size, need_to_connect, board_margin, mode='AI-AI')
            return


# MAIN

if __name__ == '__main__':
    main_menu()
