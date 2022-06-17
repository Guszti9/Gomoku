import random
from Board import Board
from Printer import Printer

ABC = "ABCDEFGHIJKLMNOPQRST"
PLAYERS = ['X', 'O']
X_WON = "x_won.txt"
O_WON = "o_won.txt"
TIED = "tie.txt"


class Game:
    __board = None
    actual_player = "O"

    def __init__(self, board_size, need_to_connect):
        self.__board = Board(board_size, need_to_connect)

    def __get_move(self):
        while True:
            inp = input("Enter your coordinate!")

            if inp.lower() == 'q' or inp.lower() == 'quit':
                return None

            if len(inp) > 1:
                if inp[0].upper() in ABC:
                    row = int(ABC.find(inp[0].upper()))
                else:
                    print("First coordinate not valid")
                    continue
                try:
                    col = int(inp[1:]) - 1
                except ValueError:
                    print("Second coordinate is not number")
                    continue
                if self.__board.is_valid_coordinate(row, col):
                    if self.__board.is_coordinate_free(row, col):
                        return row, col
                    else:
                        print("Coordinate already occupied")
                else:
                    print("Coordinate is out of board!")
            else:
                print("Input is too short!")

    def switch_player(self):
        if self.actual_player == 'X':
            return 'O'
        return 'X'

    def play_game(self, board_margin=0):
        self.actual_player = random.choice(PLAYERS)

        while True:
            self.actual_player = self.switch_player()
            Printer.clear()
            Printer.print_board(self.__board.create_str())
            print(f"It is {self.actual_player} turn!")

            coordinate = self.__get_move()

            print(coordinate)

            if coordinate is None:
                return

            self.__board.mark(self.actual_player, coordinate[0], coordinate[1])

            result = self.__get_result(coordinate[0], coordinate[1])
            if result is not None:
                Printer.clear()
                Printer.print_result(result, self.__board, board_margin)
                return

    def __get_result(self, row, col):
        if self.__board.is_coordinate_won(self.actual_player, row, col):
            if self.actual_player == 'X':
                return X_WON
            else:
                return O_WON
        if self.__board.is_full():
            return TIED
        return None


