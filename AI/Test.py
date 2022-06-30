from PatternRecogniser import PatternRecogniser

patternRecogniser = PatternRecogniser("O")

print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX..OO.", 1))
print(patternRecogniser.get_best_pattern_value_in_str("OOOOO", 1))
print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX.OOO...OOXXO..OO.OO", 9))
