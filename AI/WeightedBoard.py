from AICell import WeightedCell
from PatternRecogniser import PatternRecogniser


class WeightedBoard:
    __board_size = 0
    __need_to_connect = 5
    __board = []
    __player = None
    __pattern_recogniser = None

    def __init__(self, board_size, player):
        self.__board_size = board_size
        self.__player = player
        self.__pattern_recogniser = PatternRecogniser(player)
        for row in range(board_size):
            new_row = []
            for column in range(board_size):
                new_row.append(WeightedCell())
            self.__board.append(new_row)
        for row in range(self.__board_size):
            for col in range(self.__board_size):
                self.__calculate_cord_value(row, col)

    def mark_board(self, row, col, player):
        self.__board[row][col] = player

        cells_in_row = self.get_cells_in_row(row)
        for cord_1, cord_2 in WeightedBoard.__get_relevant_sublist(col, cells_in_row, 6):
            if isinstance(self.__board[cord_1][cord_2], WeightedCell):
                self.__calculate_cord_value(cord_1, cord_2)

        cells_in_col = self.get_cells_in_col(col)
        for cord_1, cord_2 in WeightedBoard.__get_relevant_sublist(row, cells_in_col, 6):
            if isinstance(self.__board[cord_1][cord_2], WeightedCell):
                self.__calculate_cord_value(cord_1, cord_2)

        cells_in_down_diag = self.get_cells_in_down_diag(row, col)
        for cord_1, cord_2 in WeightedBoard.__get_relevant_sublist(min(row, col), cells_in_down_diag, 6):
            if isinstance(self.__board[cord_1][cord_2], WeightedCell):
                self.__calculate_cord_value(cord_1, cord_2)

        cells_in_up_diag = self.get_cells_in_up_diag(row, col)
        for cord_1, cord_2 in WeightedBoard.__get_relevant_sublist(min(self.__board_size - row - 1, col), cells_in_up_diag, 6):
            if isinstance(self.__board[cord_1][cord_2], WeightedCell):
                self.__calculate_cord_value(cord_1, cord_2)

    def __calculate_cord_value(self, row, col):
        cell = self.__board[row][col]

        cells_in_row = self.get_cells_in_row(row)
        string_in_row = self.__create_string(cells_in_row)
        cell.change_row_val(self.__pattern_recogniser.get_best_pattern_value_in_str(string_in_row, col))

        cells_in_col = self.get_cells_in_col(col)
        string_in_col = self.__create_string(cells_in_col)
        cell.change_col_val(self.__pattern_recogniser.get_best_pattern_value_in_str(string_in_col, row))

        cells_in_down_diag = self.get_cells_in_down_diag(row, col)
        string_in_down_diag = self.__create_string(cells_in_down_diag)
        cell.change_diag_down_val(self.__pattern_recogniser
                                      .get_best_pattern_value_in_str(string_in_down_diag, min(row, col)))

        cells_in_up_diag = self.get_cells_in_up_diag(row, col)
        string_in_up_diag = self.__create_string(cells_in_up_diag)
        cell.change_diag_up_val(self.__pattern_recogniser
                                    .get_best_pattern_value_in_str(string_in_up_diag, min(self.__board_size - row - 1, col)))

    def __create_string(self, cord_list):
        char_list = []
        for cord in cord_list:
            if isinstance(self.__board[cord[0]][cord[1]], WeightedCell):
                char_list.append('.')
            else:
                char_list.append(self.__board[cord[0]][cord[1]])
        return "".join(char_list)

    def get_cells_in_row(self, row):
        return [(row, col) for col in range(self.__board_size)]

    def get_cells_in_col(self, col):
        return [(row, col) for row in range(self.__board_size)]

    def get_cells_in_down_diag(self, row, col):
        dif = row - col
        first_row = dif if dif > 0 else 0
        first_col = abs(dif) if dif < 0 else 0
        return [(first_row + d, first_col + d) for d in range(self.__board_size - abs(dif))]

    def get_cells_in_up_diag(self, row, col):
        sum = row + col + 1
        dif = sum if sum <= self.__board_size else self.__board_size - (sum - self.__board_size)
        first_row = sum - 1 if sum < self.__board_size else self.__board_size - 1
        first_col = 0 if sum <= self.__board_size else sum - self.__board_size
        return [(first_row - d, first_col + d) for d in range(abs(dif))]

    def create_string_weighted_board(self):
        string = ""
        for row in range(self.__board_size):
            new_row = ""
            for col in range(self.__board_size):
                if isinstance(self.__board[row][col], WeightedCell):
                    new_row += f"{self.__board[row][col].get_cell_value(): <5}  "
                else:
                    new_row += f"{self.__board[row][col]: <5}  "
            new_row += "\n\n"
            string += new_row

        return string

    @staticmethod
    def __get_relevant_sublist(ind, cord_list, pattern_length):
        substring_start_ind = ind - (pattern_length - 1) if ind - (pattern_length - 1) > 0 else 0
        substring_end_ind = ind + pattern_length if ind + pattern_length < len(cord_list) + 1 else len(cord_list) + 1
        return cord_list[substring_start_ind: substring_end_ind]
