from PatternRecogniser import PatternRecogniser
from WeightedBoard import WeightedBoard

patternRecogniser = PatternRecogniser("O")
print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX..OO.", 1))
print(patternRecogniser.get_best_pattern_value_in_str("OOOOO", 1))
print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX.O.O...OOXXO..OO.OO", 9))

weighted_board = WeightedBoard(10, "X")
weighted_board.mark_board(1, 1, 'X')
weighted_board.mark_board(2, 2, 'X')
weighted_board.mark_board(3, 4, 'X')
weighted_board.mark_board(3, 3, 'O')
weighted_board.mark_board(2, 3, 'O')
weighted_board.mark_board(5, 3, 'X')
print(weighted_board.create_string_weighted_board())
