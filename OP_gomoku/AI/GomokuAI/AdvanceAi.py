import math

from AI.GomokuAI.BoardState.BoardState import BoardState
from AI.WeightedBoard import WeightedBoard
from AI.GomokuAI.BoardState.BoardStateTree import BoardStateTree


class AdvanceAi:
    def __init__(self, board_size, player, best_move_count=6):
        self.__player = player
        self.__turn = 0
        self.__board_size = board_size
        x_board = WeightedBoard(board_size, "X")
        o_board = WeightedBoard(board_size, "O")
        id_string = "".join("." for i in range(board_size * board_size))
        board_state = BoardState(board_size, id_string, x_board, o_board, 0, best_move_count)
        self.board_state_tree = BoardStateTree(board_state, 0, self.__get_new_depth(), best_move_count)

    def get_next_move(self):
        if self.__turn == 0:
            return math.floor(self.__board_size / 2), math.floor(self.__board_size / 2)

        self.board_state_tree.create_state_tree(self.__player)
        return self.board_state_tree.get_next_move(self.__player)

    def mark_cord(self, row, col, player):
        BoardStateTree.delete_depth(self.__turn)
        self.__turn += 1
        self.board_state_tree = self.board_state_tree.get_new_board_state_tree((row, col), player, self.__get_new_depth())

    def __get_new_depth(self):
        if self.__turn > 5:
            return 8
        if self.__turn > 3:
            return 6
        return 4

