import pandas as pd


class DataComparator:
    def __init__(self, prev_month_data, curr_month_data):
        self.prev_month_data = prev_month_data
        self.curr_month_data = curr_month_data

    def count_ci_id(self):
        # compare
        prev_ci_id = len(self.prev_month_data.get_data_frame()['CI_ID'])
        curr_ci_id = len(self.curr_month_data.get_data_frame()['CI_ID'])
        difference = curr_ci_id - prev_ci_id
        return prev_ci_id, curr_ci_id, abs(difference)

    def count_percent_ci_id(self):  # FIX THIS: percentage of applications storing restricted PPI/Cash Payment Systems
        # from all that have data at rest encryption
        prev_ci_id = len(self.prev_month_data.get_data_frame()['CI_ID'])
        curr_ci_id = len(self.curr_month_data.get_data_frame()['CI_ID'])
        difference = curr_ci_id - prev_ci_id
        percent_difference = (difference / prev_ci_id) * 100
        return percent_difference

    # break down by PPI Classification

    def count_ppi_classification(self):  # FIX THIS for restricted, confidential, nonpublic, public/N/A
        prev_ppi = self.prev_month_data.get_data_frame()['PPI_Classification'].value_counts()
        curr_ppi = self.curr_month_data.get_data_frame()['PPI_Classification'].value_counts()
        return prev_ppi, curr_ppi

    def compare_fields(self, fields):
        """
        Compare specified fields between the previous and current month's data.
        Return a dictionary of changes, where each key is a CI_ID and the value is a
        dictionary mapping each field to a tuple of previous and current values.
        """
        changes = {}
        merged_data = pd.merge(self.prev_month_data.get_data_frame(), self.curr_month_data.get_data_frame(),
                               how='outer',
                               on='CI_ID', suffixes=('_prev', '_curr'))

        full_merged_data = pd.merge(self.prev_month_data.get_original_data_frame(),
                                    self.curr_month_data.get_original_data_frame(), how='outer',
                                    on='CI_ID', suffixes=('_prev', '_curr'))

        merged_ci_ids = merged_data['CI_ID'].unique()

        for field in fields:
            for ci_id in merged_ci_ids:
                prev_row = full_merged_data[full_merged_data['CI_ID'] == ci_id + '_prev']
                curr_row = full_merged_data[full_merged_data['CI_ID'] == ci_id + '_curr']

                if not prev_row.empty and not curr_row.empty:
                    prev_value, curr_value = prev_row[field].values[0], curr_row[field].values[0]
                    if prev_value != curr_value:
                        if ci_id not in changes:
                            changes[ci_id] = {}
                        changes[ci_id][field] = (prev_value, curr_value)

        return changes
