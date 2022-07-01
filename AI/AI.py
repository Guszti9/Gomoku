import random
from AI.WeightedBoard import WeightedBoard


class AI:
    def __init__(self, board_size, player):
        self.__player = player
        self.__board_size = board_size
        self. __calculated_board = []
        self.__board_X = WeightedBoard(board_size, "X")
        self.__board_O = WeightedBoard(board_size, "O")

        for r in range(self.__board_size):
            row = []
            for c in range(self.__board_size):
                row.append(0)
            self.__calculated_board.append(row)

    def mark_cord(self, row, col, player):
        self.__board_X.mark_board(row, col, player)
        self.__board_O.mark_board(row, col, player)
        self.__calculated_board[row][col] = None

    def __calculate_board(self):
        for row in range(self.__board_size):
            for col in range(self.__board_size):
                if self.__calculated_board[row][col] is not None:
                    cell_x_val = self.__board_X.get_cord_val(row, col)
                    cell_o_val = self.__board_O.get_cord_val(row, col)
                    cell_value = cell_x_val + cell_o_val/2 if self.__player == "X" else cell_x_val/2 + cell_o_val
                    self.__calculated_board[row][col] = cell_value

    def __get_best_move(self):
        self.__calculate_board()
        best_moves = []
        best_move_val = 0

        for row in range(self.__board_size):
            for col in range(self.__board_size):
                cell_val = self.__calculated_board[row][col]
                if cell_val is not None:
                    if cell_val > best_move_val:
                        best_move_val = cell_val
                        best_moves = [(row, col)]
                    elif cell_val == best_move_val:
                        best_moves.append((row, col))
        return best_moves

    def create_string(self):
        string = ""
        for row in range(self.__board_size):
            new_row = ""
            for col in range(self.__board_size):
                if self.__calculated_board[row][col] is not None:
                    new_row += f"{self.__calculated_board[row][col]: <7}  "
                else:
                    new_row += f"{'X': <7}  "
            new_row += "\n\n"
            string += new_row
        return string

    def get_next_move(self):
        best_moves = self.__get_best_move()
        return random.choice(best_moves)
