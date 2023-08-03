import pandas as pd


class DataFilterer:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Expected pandas DataFrame, got: {}".format(type(df)))
        self.data_frame = df
        self.filter_methods = {
            1: self.filter_apps_with_restricted_ppi_or_cash_payment_systems,
            2: self.filter_apps_with_restricted_ppi_or_cash_payment_systems,
            3: self.filter_apps_with_restricted_ppi_or_cash_payment_systems,
            4: self.filter_apps_with_restricted_ppi_or_cash_payment_systems
        }

    def filter_apps_with_restricted_ppi_or_cash_payment_systems(self):
        try:
            self.data_frame = self.data_frame[
                (self.data_frame['Deployment_Lifecycle_Phase'] == 'Production') &
                ((self.data_frame['Asset_Type'] == 'Application') |
                (self.data_frame['Asset_Type'] == 'Platform') |
                (self.data_frame['Asset_Type'] == 'Tool')) &
                ((self.data_frame['PPI_Classification'] == 'Restricted PPI') |
                (self.data_frame['Cash_Payment_systems'] == 'Yes')) &
                (self.data_frame['NFR_10'] != 'N/A')
            ]
        except KeyError as e:
            raise KeyError(f"DataFrame does not have necessary columns for filtering: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during data filtering: {str(e)}")

    # Define other filter methods here

    def apply_filter(self, filter_option):
        if filter_option not in self.filter_methods:
            raise ValueError(f'Invalid filter option: {filter_option}')
        try:
            self.filter_methods[filter_option]()
        except Exception as e:
            raise Exception(f"Failed to apply filter: {str(e)}")
