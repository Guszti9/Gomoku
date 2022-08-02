from AI.BoardState import BoardState


class BoardStateTree:
    def get_new_board_state_tree(self, cord, player, depth):
        new_start_board_state = self.__start_board_state.get_next_board_state(cord, player)
        return BoardStateTree(new_start_board_state, self.__move_count + 1, depth, self.__best_move_count)

    def __init__(self, start_board_state, move_count, depth, best_move_count):
        self.__start_board_state = start_board_state
        self.__move_count = move_count
        self.__depth = depth
        self.__max_depth = move_count + depth
        self.__best_move_count = best_move_count

    def get_next_move(self, player):
        best_state = None
        best_value = - 10000000
        if not self.__start_board_state.get_children_board_states():
            return self.__start_board_state.get_best_move(player)

        for next_board_states in self.__start_board_state.get_children_board_states():
            value = self.__calculate_next_step(next_board_states, player)
            print(value)
            if value > best_value or best_state is None:
                best_state = next_board_states
                best_value = value
        return self.__start_board_state.get_move(best_state)

    def create_state_tree(self, player):
        self.__create_new_states(self.__start_board_state, player)

    def __create_new_states(self, board_state, player):
        if board_state.get_depth() < self.__max_depth:
            for child_state in board_state.create_children_board_states(player):
                self.__create_new_states(child_state, BoardStateTree.switch_player(player))

    def __calculate_next_step(self, board_state, player):
        player = BoardStateTree.switch_player(player)
        max_value = -10000000

        if not board_state.get_children_board_states():
            return board_state.get_board_value(player)
        else:
            for children_board_state in board_state.get_children_board_states():
                value = self.__calculate_next_step(children_board_state, player)
                if value > max_value:
                    max_value = value
        return max_value

    @staticmethod
    def delete_depth(depth):
        delete_keys = []
        for key, value in BoardState.existing_board_states.items():
            if value.get_depth == depth:
                delete_keys.append(key)
        for key in delete_keys:
            del BoardState.existing_board_states[key]

    @staticmethod
    def switch_player(player):
        if player == "X":
            return "O"
        return "X"
