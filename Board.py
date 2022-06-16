class Board:
    board_size = 0
    need_to_connect = 0
    board = []

    def __init__(self, board_size, need_to_connect):
        self.board_size = board_size
        self.need_to_connect = need_to_connect

        for row in range(board_size):
            new_row = []
            for column in range(board_size):
                new_row.append(".")
            self.board.append(new_row)

    def mark(self, player, row, col):
        self.board[row][col] = player

    def is_coordinate_free(self, row, col):
        if self.board[row][col] == '.':
            return True
        return False

    def is_full(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == '.':
                    return False
        return True

    def is_coordinate_won(self, player, row, col):
        row_win = [(row + r, col) for r in range(self.need_to_connect)]
        if self.__is_coordinate_list_wons(row_win, player):
            return True
        col_win = [(row, col + c) for c in range(self.need_to_connect)]
        if self.__is_coordinate_list_wons(col_win, player):
            return True
        diag_win_1 = [(row + d, col + d) for d in range(self.need_to_connect)]
        if self.__is_coordinate_list_wons(diag_win_1, player):
            return True
        diag_win_2 = [(row - d, col + d) for d in range(self.need_to_connect)]
        if self.__is_coordinate_list_wons(diag_win_2, player):
            return True
        return False

    def __is_coordinate_list_wons(self, cord_list, player):
        for coordinates in cord_list:
            if self.__is_valid_coordinate(coordinates[0], coordinates[1]):
                if not self.board[coordinates[0]][coordinates[1]] == player:
                    return False
            else:
                return False

        return True

    def __is_valid_coordinate(self, row, col):
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return True
        return False


