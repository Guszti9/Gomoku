from PatternRecogniser import PatternRecogniser

patternRecogniser = PatternRecogniser("O")

print(patternRecogniser.get_best_pattern_value_in_str("..OOO.OX..OO."))
print(patternRecogniser.get_best_pattern_value_in_str("OOOOO"))
print(patternRecogniser.get_best_pattern_value_in_str("OO"))
