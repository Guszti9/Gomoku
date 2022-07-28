from Game import Game
from Printer import Printer


def main_menu():
    while True:

        Printer.print_main_menu()
        inp = input()
        if inp.lower() == 'quit' or inp.lower() == 'q':
            return
        if inp == '1':
            game = Game(15, "AI-simple")
            game.play_game()
        if inp == '2':
            game = Game(15, "AI-minimax")
            game.play_game()


main_menu()

