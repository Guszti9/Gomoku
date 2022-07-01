from AI.PatternRecogniser import PatternRecogniser
from AI.WeightedBoard import WeightedBoard
from AI.AI import AI

patternRecogniser = PatternRecogniser("O")
print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX..OO.", 1))
print(patternRecogniser.get_best_pattern_value_in_str("OOOOO", 1))
print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX.O.O...OOXXO..OO.OO", 9))

weighted_board = WeightedBoard(10, "O")
weighted_board.mark_board(1, 1, 'X')
weighted_board.mark_board(2, 2, 'X')
weighted_board.mark_board(3, 4, 'X')
weighted_board.mark_board(3, 3, 'O')
weighted_board.mark_board(2, 3, 'O')
weighted_board.mark_board(5, 3, 'X')
print(weighted_board.create_string_weighted_board())


ai = AI(10, "X")
ai.mark_cord(3, 3, 'O')
ai.mark_cord(3, 4, 'O')
ai.mark_cord(3, 5, 'O')
ai.mark_cord(6, 3, 'O')
ai.mark_cord(7, 3, 'O')
ai.mark_cord(8, 3, 'O')
print(ai.create_string())

