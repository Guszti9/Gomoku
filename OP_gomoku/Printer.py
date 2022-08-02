import time
from os import system

GAME_OVER_1 = "Text/game_over_1.txt"
GAME_OVER_2 = "Text/game_over_2.txt"
MENTOR_BOSS = "Text/mentorBoss_loading.txt"
LOGO = "Text/logo.txt"


class Printer:
    @staticmethod
    def print_result(result, board, board_margin):
        for elapsed_time in range(12):
            Printer.clear()
            if elapsed_time % 2 == 0:
                Printer.__print_file(GAME_OVER_1)
            else:
                Printer.__print_file(GAME_OVER_2)
            Printer.__print_file(result)
            Printer.print_board(board.create_str(board_margin))
            time.sleep(0.5)

        time.sleep(2)

    @staticmethod
    def print_main_menu():
        Printer.clear()
        Printer.__print_file(LOGO)
        print('''
                      ---    1: Simple      ---
                      ---    2: Minimax     ---
                      ---    3: Advance     ---
                      ---       Quit        ---
        ''')

    @staticmethod
    def print_mentorBoss_loading():
        Printer.clear()
        with open(MENTOR_BOSS, "r") as file:
            lines = [line.split(' @ ') for line in file]
            for line in lines:
                print(line[0])
                time.sleep(float(line[1].replace('\n', '')))

        time.sleep(5)

    @staticmethod
    def print_board(board_str):
        for line in board_str:
            print(line)

    @staticmethod
    def clear():
        _ = system('clear')

    @staticmethod
    def __print_file(file_reference):
        with open(file_reference, "r") as file:
            print(file.read())

