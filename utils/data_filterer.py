import pandas as pd


class DataFilterer:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Expected pandas DataFrame, got: {}".format(type(df)))
        self.data_frame = df
        self.filter_methods = {
            1: self.filter_apps_with_restricted_ppi_or_cash_payment_systems(),
            2: self.filter_data_at_rest_encryption_for_restricted_ppi_or_cash_payment_systems(),
            3: self.filter_apps_storing_restricted_data(),
            4: self.filter_data_at_rest_encryption_status_for_restricted_data()
        }

    def filter_apps_with_restricted_ppi_or_cash_payment_systems(self):
        try:
            self.data_frame = self.data_frame[
                self.in_production() &
                self.app_or_platform_or_tool() &
                self.restricted_ppi_or_cash_payment_system() &
                self.valid_nfr_10()
                ]
        except KeyError as e:
            raise KeyError(f"DataFrame does not have necessary columns for filtering: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during data filtering: {str(e)}")

    def valid_nfr_10(self):
        return self.data_frame['NFR_10'] != 'N/A'

    def filter_data_at_rest_encryption_for_restricted_ppi_or_cash_payment_systems(self):
        try:
            self.data_frame = self.data_frame[
                self.in_production() &
                self.app_or_platform_or_tool() &
                self.restricted_ppi_or_cash_payment_system() &
                self.valid_nfr_10() &
                self.pass_or_waive_nfr_10()
                ]
        except KeyError as e:
            raise KeyError(f"DataFrame does not have necessary columns for filtering: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during data filtering: {str(e)}")

    def pass_or_waive_nfr_10(self):
        return (self.data_frame['NFR_10'] == 'Pass') | (self.data_frame['NFR_10'] == 'Waive')

    def restricted_ppi_or_cash_payment_system(self):
        return ((self.data_frame['PPI_Classification'] == 'Restricted PPI') |
                (self.data_frame['Cash_Payment_Systems'] == 'Yes'))

    def app_or_platform_or_tool(self):
        return ((self.data_frame['Asset_Type'] == 'Application') |
                (self.data_frame['Asset_Type'] == 'Platform') |
                (self.data_frame['Asset_Type'] == 'Tool'))

    def in_production(self):
        return self.data_frame['Deployment_Lifecycle_Phase'] == 'Production'

    def filter_apps_storing_restricted_data(self):
        try:
            self.data_frame = self.data_frame[
                self.in_production() &
                self.app_or_platform_or_tool() &
                self.restricted_information_classification() &
                self.valid_nfr_10()
                ]
        except KeyError as e:
            raise KeyError(f"DataFrame does not have necessary columns for filtering: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during data filtering: {str(e)}")

    def filter_data_at_rest_encryption_status_for_restricted_data(self):
        try:
            self.data_frame = self.data_frame[
                self.in_production() &
                self.app_or_platform_or_tool() &
                self.restricted_information_classification() &
                self.valid_nfr_10()
                ]
        except KeyError as e:
            raise KeyError(f"DataFrame does not have necessary columns for filtering: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during data filtering: {str(e)}")

    def restricted_information_classification(self):
        return self.data_frame['Information_Classification'] == 'Restricted'

    def apply_filter(self, filter_option):
        if filter_option not in self.filter_methods:
            raise ValueError(f'Invalid filter option: {filter_option}')
        try:
            self.filter_methods[filter_option]
        except Exception as e:
            raise Exception(f"Failed to apply filter: {str(e)}")

    def get_data_frame(self):
        return self.data_frame
