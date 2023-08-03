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

    def count_percent_ci_id(self):  # FIX THIS
        prev_ci_id = len(self.prev_month_data.data_frame['CI_ID'])
        curr_ci_id = len(self.curr_month_data.data_frame['CI_ID'])
        difference = curr_ci_id - prev_ci_id
        percent_difference = (difference / prev_ci_id) * 100
        return percent_difference

    # break down by PPI Classification

    def count_ppi_classification(self): # FIX THIS for restricted, confidential, nonpublic, public/N/A
        prev_ppi = self.prev_month_data.data_frame['PPI_Classification'].value_counts()
        curr_ppi = self.curr_month_data.data_frame['PPI_Classification'].value_counts()
        return prev_ppi, curr_ppi

