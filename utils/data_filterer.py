import pandas as pd


class DataFilterer:
    def __init__(self, df):
        self.data_frame = df

    # Encapsulated the filter method inside the class
    def filter_apps_with_restricted_ppi_or_cash_payment_systems(self):
        self.data_frame = self.data_frame[
            (self.data_frame['Deployment_Lifecycle_Phase'] == 'Production') &
            ((self.data_frame['Asset_Type'] == 'Application') |
             (self.data_frame['Asset_Type'] == 'Platform') |
             (self.data_frame['Asset_Type'] == 'Tool')) &
            ((self.data_frame['PPI_Classification'] == 'Restricted PPI') |
             (self.data_frame['Cash_Payment_systems'] == 'Yes')) &
            (self.data_frame['NFR_10'] != 'N/A')
            ]

