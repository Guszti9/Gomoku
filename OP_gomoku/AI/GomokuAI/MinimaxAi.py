from AI.WeightedBoard import WeightedBoard
from AI.GomokuAI.Move.Move import Move


class MinimaxAi:
    def __init__(self, size, player, max_depth=6, best_move_count=5):
        self.__player = player
        self.__current_player = player
        self.__max_depth = max_depth
        self.__best_move_count = best_move_count

        self.__moves = []
        self.__board_value = 0
        self.__board_size = size
        self.__calculated_board = []
        self.__board_X = WeightedBoard(size, "X")
        self.__board_O = WeightedBoard(size, "O")

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
        self.__moves = []
        self.__board_value = 0

        for row in range(self.__board_size):
            for col in range(self.__board_size):
                if self.__calculated_board[row][col] is not None:
                    cell_x_val = self.__board_X.get_cord_val(row, col)
                    cell_o_val = self.__board_O.get_cord_val(row, col)
                    cell_value = cell_x_val + cell_o_val/2 if self.__current_player == "X" else cell_x_val/2 + cell_o_val

                    self.__moves.append(Move(cell_value, (row, col)))
                    self.__board_value += cell_x_val - cell_o_val if self.__player == "X" else cell_o_val - cell_x_val
                    self.__calculated_board[row][col] = cell_value

        self.__moves.sort(key=lambda e: e.get_value(), reverse=True)

    def __get_best_moves(self):
        best_moves = []
        self.__calculate_board()
        best_move = self.__moves[0]
        divider_value = best_move.get_value() / 2

        for move in self.__moves:
            if move.get_value() >= divider_value:
                best_moves.append(move)
            else:
                break

        return best_moves if len(best_moves) <= self.__best_move_count else best_moves[:self.__best_move_count]

    def __delete_move(self, move):
        cord = move.get_cord()
        self.__board_O.delete_mark(cord[0], cord[1])
        self.__board_X.delete_mark(cord[0], cord[1])
        self.__calculated_board[cord[0]][cord[1]] = 0

    def get_next_move(self):
        self.__current_player = self.__player
        best_moves = self.__get_best_moves()
        best_move = best_moves[0]
        best_val = -10000000
        for move in best_moves:
            cord = move.get_cord()
            self.mark_cord(cord[0], cord[1], self.__current_player)
            minmax_val = self.__minimax_ai_move()
            if best_val < minmax_val:
                best_val = minmax_val
                best_move = move
            self.__delete_move(move)
        return best_move.get_cord()

    def __minimax_ai_move(self, depth=0):
        self.switch_player()
        best_moves = self.__get_best_moves()

        if best_moves[0].get_value() >= 1000000 or depth == self.__max_depth:
            cord = best_moves[0].get_cord()
            self.mark_cord(cord[0], cord[1], self.__current_player)
            self.__calculate_board()
            self.__delete_move(best_moves[0])
            return self.__board_value

        if self.__current_player == self.__player:
            best_board_val = -10000000
            for move in best_moves:
                cord = move.get_cord()
                self.mark_cord(cord[0], cord[1], self.__current_player)
                best_board_val = max(self.__minimax_ai_move(depth+1), best_board_val)
                self.__delete_move(move)
            return best_board_val
        else:
            worst_board_val = 10000000
            for move in best_moves:
                cord = move.get_cord()
                self.mark_cord(cord[0], cord[1], self.__current_player)
                worst_board_val = min(self.__minimax_ai_move(depth+1), worst_board_val)
                self.__delete_move(move)
            return worst_board_val

    def switch_player(self):
        if self.__current_player == "X":
            self.__current_player = "O"
        else:
            self.__current_player = "X"

