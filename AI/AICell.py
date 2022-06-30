class WeightedCell:
    row_val = 0
    col_val = 0
    diag_down_val = 0
    diag_up_val = 0

    def change_row_val(self, value):
        self.row_val = value

    def change_col_val(self, value):
        self.col_val = value

    def change_diag_down_val(self, value):
        self.diag_down_val = value

    def change_diag_up_val(self, value):
        self.diag_up_val = value

    def get_cell_value(self):
        return self.row_val + self.col_val + self.diag_up_val + self.diag_down_val

