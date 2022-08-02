class PatternRecogniser:
    patterns_six = {
        ".||||.": 50000,
        ".|||..": 5000,
        "..|||.": 5000,
        ".||.|.": 500,
        ".|.||.": 500,
        "..||..": 100,
        ".||...": 100,
        "...||.": 100,
        "..|.|.": 100,
        ".|.|..": 100,
        ".|..|.": 50,
        "..|...": 10,
        "...|..": 10
    }

    patterns_five = {
        "|||||": 1000000,
        ".||||": 5000,
        "||||.": 5000,
        "||.||": 5000,
        "|.|||": 5000,
        "|||.|": 5000,
        "|||..": 200,
        ".|||.": 200,
        "..|||": 200,
        "||.|.": 200,
        ".|.||": 200,
        "||..|": 200,
        "|..||": 200,
        "|.|.|": 200,
    }

    def __init__(self, player):
        self.__player = player

    def __create_string(self, string, ind):
        char_list = list(string)
        char_list[ind] = "|"
        string = "".join(char_list)
        string = string.replace(self.__player, "|")
        return string

    def get_best_pattern_value_in_str(self, string, ind):
        string = self.__create_string(string, ind)

        string_for_six = PatternRecogniser.__get_relevant_substring(ind, string, 6)
        string_for_five = PatternRecogniser.__get_relevant_substring(ind, string, 5)

        return max(self.__five_pattern_value(string_for_five), self.__six_pattern_value(string_for_six))

    @staticmethod
    def __get_relevant_substring(ind, string, pattern_length):
        substring_start_ind = ind - (pattern_length - 1) if ind - (pattern_length - 1) > 0 else 0
        substring_end_ind = ind + pattern_length if ind + pattern_length < len(string) + 1 else len(string) + 1
        return string[substring_start_ind: substring_end_ind]

    def __five_pattern_value(self, string):
        max_value = 0
        for substring in [string[ind - 5:ind] for ind in range(5, len(string) + 1)]:
            if substring in self.patterns_five and self.patterns_five[substring] > max_value:
                max_value = self.patterns_five[substring]
        return max_value

    def __six_pattern_value(self, string):
        max_value = 0
        for substring in [string[ind - 6:ind] for ind in range(6, len(string) + 1)]:
            if substring in self.patterns_six and self.patterns_six[substring] > max_value:
                max_value = self.patterns_six[substring]
        return max_value

