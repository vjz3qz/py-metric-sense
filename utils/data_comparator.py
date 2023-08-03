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

    def count_percent_ci_id(self):  # FIX THIS: percentage of applications storing restricted PPI/Cash Payment Systems
        # from all that have data at rest encryption
        prev_ci_id = len(self.prev_month_data.data_frame['CI_ID'])
        curr_ci_id = len(self.curr_month_data.data_frame['CI_ID'])
        difference = curr_ci_id - prev_ci_id
        percent_difference = (difference / prev_ci_id) * 100
        return percent_difference

    # break down by PPI Classification

    def count_ppi_classification(self):  # FIX THIS for restricted, confidential, nonpublic, public/N/A
        prev_ppi = self.prev_month_data.data_frame['PPI_Classification'].value_counts()
        curr_ppi = self.curr_month_data.data_frame['PPI_Classification'].value_counts()
        return prev_ppi, curr_ppi

    def compare_fields(self, fields):
        """
        Compare specified fields between the previous and current month's data.
        Return a dictionary of changes, where each key is a tuple (prev_value, curr_value) and
        the value is a list of CI_IDs that had this change.
        """
        changes = {field: {} for field in fields}
        merged_data = pd.merge(self.prev_month_data.data_frame, self.curr_month_data.data_frame, how='outer',
                               on='CI_ID', suffixes=('_prev', '_curr'))

        for field in fields:
            for _, row in merged_data.iterrows():
                prev_value, curr_value = row[f'{field}_prev'], row[f'{field}_curr']
                if prev_value != curr_value:
                    change_key = (prev_value, curr_value)
                    if change_key not in changes[field]:
                        changes[field][change_key] = []
                    changes[field][change_key].append(row['CI_ID'])

        return changes
