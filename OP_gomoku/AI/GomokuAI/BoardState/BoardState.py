import math

from AI.AICell import WeightedCell
from copy import deepcopy


class BoardState:
    """
    This class store a Board State it is used to create a tree of Board States and calculate ahead using these.
    Every board state has a parameter name __children_board_states where its store the next possible states.
    Board states are also stored in the existing_board_states by there string_id, if a children board state is
    already calculated we just add the reference to the children list.
    """

    existing_board_states = {}

    # Calculate board state value. WHY DOES IT WORK???
    def get_state_value(self, player):
        if self.__state_value is not None:
            return self.__state_value
        if len(self.__children_board_states) == 0:
            return self.get_board_value(player)
        return max([state.get_state_value(BoardState.switch_player(player)) for state in self.__children_board_states])

    def get_board_value(self, player):
        return self.__board_value.get_value(player)

    def get_depth(self):
        return self.__depth

    def get_children_board_states(self):
        return self.__children_board_states

    def get_best_move(self, player):
        sorted_moves = sorted(self.__moves, key=lambda m: m.get_value(player), reverse=True)
        return sorted_moves[0].cord

    # Calculate the next BoardState by a move, coordinate(row, col)
    def get_next_board_state(self, cord, player):
        next_id_string = self.__create_next_id_string(cord, player)
        if next_id_string in self.existing_board_states:
            return self.existing_board_states[next_id_string]
        else:
            new_x_board = deepcopy(self.__x_board)
            new_x_board.mark_board(cord[0], cord[1], player)
            new_o_board = deepcopy(self.__o_board)
            new_o_board.mark_board(cord[0], cord[1], player)
            next_board_state = BoardState(self.__board_size, next_id_string, new_x_board, new_o_board,
                                          self.__depth + 1, self.__best_move_count)

            self.existing_board_states[next_id_string] = next_board_state
            return next_board_state

    def __init__(self, size, id_string, x_board, o_board, depth, best_move_count=10):
        self.__x_board = x_board
        self.__o_board = o_board
        self.__id_string = id_string
        self.__board_size = size
        self.__moves = []
        self.__board_value = None
        self.__state_value = None
        self.__children_board_states = []
        self.__depth = depth
        self.__best_move_count = best_move_count
        self.__calculate_state_datas()

    # Create an id string by the object itself
    def create_id_string(self):
        return_string = ""
        for row in range(self.__board_size):
            row_string = ""
            for col in range(self.__board_size):
                if isinstance(self.__x_board.get_cord(row, col), WeightedCell):
                    row_string += "."
                else:
                    row_string += self.__x_board.get_cord(row, col)
            return_string += row_string
        return return_string

    # Create an id string by a move, coordinate(row, col)
    def __create_next_id_string(self, cord, player):
        chars = list(self.__id_string)
        ind = cord[0] * self.__board_size + cord[1]
        chars[ind] = player
        return "".join(chars)

    # It calculates the moves, and their values, and the board value too
    def __calculate_state_datas(self):
        sum_x_value = 0
        sum_o_value = 0

        for row in range(self.__board_size):
            for col in range(self.__board_size):
                if isinstance(self.__x_board.get_cord(row, col), WeightedCell):
                    o_value = self.__o_board.get_cord_val(row, col) + self.__x_board.get_cord_val(row, col) / 2
                    x_value = self.__x_board.get_cord_val(row, col) + self.__o_board.get_cord_val(row, col) / 2
                    move = PlayersCellValue(x_value, o_value, row, col)
                    self.__moves.append(move)
                    sum_x_value += x_value - o_value
                    sum_o_value += o_value - x_value

        self.__board_value = PlayersValue(sum_x_value, sum_o_value)

    # It gives back the best moves from moves
    def __get_best_moves(self, player):
        best_moves = []
        sorted_moves = sorted(self.__moves, key=lambda m: m.get_value(player), reverse=True)

        best_move = sorted_moves[0]
        divider_value = best_move.get_value(player) / 2

        for move in sorted_moves:
            if move.get_value(player) >= divider_value:
                best_moves.append(move)
            else:
                break
        return best_moves if len(best_moves) <= self.__best_move_count else best_moves[:self.__best_move_count]

    # Add the children BoardStates to the object
    def __get_next_board_states(self, player):
        best_moves = self.__get_best_moves(player)
        if best_moves[0].get_value(player) > 1000000:
            return

        for move in best_moves:
            cord = move.cord
            next_board_state = self.get_next_board_state(cord, player)
            self.__children_board_states.append(next_board_state)

    # whir this function we can get the BoardState children, if it is not calculated yeet it calculates it
    def create_children_board_states(self, player):
        if len(self.__children_board_states) == 0:
            self.__get_next_board_states(player)
        return self.__children_board_states

    # get the move between two board state
    def get_move(self, next_board_state):
        board_state_char_list = list(self.create_id_string())
        next_board_state_char_list = list(next_board_state.create_id_string())

        for ind in range(len(board_state_char_list)):
            if next_board_state_char_list[ind] != board_state_char_list[ind]:
                col = ind % self.__board_size
                row = math.floor((ind - col) / self.__board_size)
                return row, col
        return None

    @staticmethod
    def switch_player(player):
        if player == "X":
            return "O"
        return "X"


class PlayersValue:
    def __init__(self, x_value, o_value):
        self.x_value = x_value
        self.o_value = o_value

    def get_value(self, player):
        if player == "X":
            return self.x_value
        else:
            return self.o_value


class PlayersCellValue:
    def __init__(self, x_value, o_value, row, col):
        self.x_value = x_value
        self.o_value = o_value
        self.cord = (row, col)

    def get_value(self, player):
        if player == "X":
            return self.x_value
        else:
            return self.o_value

    