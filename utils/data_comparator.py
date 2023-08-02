import pandas as pd


class DataComparator:
    def __init__(self, prev_month_data, curr_month_data):
        self.prev_month_data = prev_month_data
        self.curr_month_data = curr_month_data

    def count_ci_id(self):
        # compare
        prev_ci_id = len(self.prev_month_data.data_frame['CI_ID'])
        curr_ci_id = len(self.curr_month_data.data_frame['CI_ID'])
        difference = curr_ci_id - prev_ci_id
        return prev_ci_id, curr_ci_id, abs(difference)
