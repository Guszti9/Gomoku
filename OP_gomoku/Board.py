ABC = "ABCDEFGHIJKLMNOPQRST"


def create_margin(margin):
    re = ""
    for i in range(margin):
        re += ' '
    return re


class Board:
    def __init__(self, board_size, need_to_connect):
        self.__board_size = board_size
        self.__need_to_connect = need_to_connect
        self.__board = []

        for row in range(board_size):
            new_row = []
            for column in range(board_size):
                new_row.append(".")
            self.__board.append(new_row)

    def mark(self, player, row, col):
        self.__board[row][col] = player

    def is_coordinate_free(self, row, col):
        if self.__board[row][col] == '.':
            return True
        return False

    def is_full(self):
        for row in range(self.__board_size):
            for col in range(self.__board_size):
                if self.__board[row][col] == '.':
                    return False
        return True

    def __get_cells_in_row(self, row):
        return [self.__board[row][col] for col in range(self.__board_size)]

    def __get_cells_in_col(self, col):
        return [self.__board[row][col] for row in range(self.__board_size)]

    def __get_cells_in_down_diag(self, row, col):
        dif = row - col
        first_row = dif if dif > 0 else 0
        first_col = abs(dif) if dif < 0 else 0
        return [self.__board[first_row + d][first_col + d] for d in range(self.__board_size - abs(dif))]

    def __get_cells_in_up_diag(self, row, col):
        sum = row + col + 1
        dif = sum if sum <= self.__board_size else self.__board_size - (sum - self.__board_size)
        first_row = sum - 1 if sum < self.__board_size else self.__board_size - 1
        first_col = 0 if sum <= self.__board_size else sum - self.__board_size
        return [self.__board[first_row - d][first_col + d] for d in range(abs(dif))]

    def is_coordinate_won(self, player, row, col):
        row_win = self.__get_cells_in_row(row)
        if self.__is_coordinate_list_won(row_win, player):
            return True
        col_win = self.__get_cells_in_col(col)
        if self.__is_coordinate_list_won(col_win, player):
            return True
        diag_win_1 = self.__get_cells_in_down_diag(row, col)
        if self.__is_coordinate_list_won(diag_win_1, player):
            return True
        diag_win_2 = self.__get_cells_in_up_diag(row, col)
        if self.__is_coordinate_list_won(diag_win_2, player):
            return True
        return False

    def __is_coordinate_list_won(self, cell_list, player):
        connected = 0
        for cell in cell_list:
            if cell == player:
                connected += 1
                if connected == self.__need_to_connect:
                    return True
            else:
                connected = 0

        return False

    def is_valid_coordinate(self, row, col):
        if 0 <= row < self.__board_size and 0 <= col < self.__board_size:
            return True
        return False

    def create_str(self, margin=0):
        board_print = []
        for row in range(self.__board_size):
            row_print = ""
            for col in range(self.__board_size - 1):
                row_print += f" {self.__board[row][col]} |"
            row_print += ' ' + self.__board[row][self.__board_size - 1]
            board_print.append(row_print)

        first_line = create_margin(margin)
        for number in range(1, self.__board_size + 1):
            if number <= 10:
                first_line += f"   {number}"
            else:
                first_line += f"  {number}"

        blank_line = create_margin(margin) + "  ---"
        for i in range(self.__board_size - 1):
            blank_line += "+---"

        board_str = [first_line, create_margin(margin) + ABC[0] + ' ' + board_print[0]]
        for row in range(1, self.__board_size):
            row_print = create_margin(margin) + ABC[row] + ' ' + board_print[row]
            board_str.append(blank_line)
            board_str.append(row_print)
        board_str.append('\n')

        return board_str
