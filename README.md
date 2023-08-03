# Py_Metric_Sense

## Project Overview

Py_Metric_Sense is a Python tool designed to automate the comparison of monthly Excel data. The tool highlights the differences across various months based on user-selected criteria. The users will be prompted to select two Excel files corresponding to the first and second month, specify the name of the sheets within the files, and select a filter criteria. Upon successful data filtering, the tool will write the filtered data to a new Excel file and display the comparative analysis of the selected data.

## Dependencies

The following Python packages are required to run Py_Metric_Sense:

- Python
- Pandas
- openpyxl

## Installation

To install the required Python packages, run:
    ```
   pip install -r requirements.txt
    ```

## Packaging

The project can be packaged as an executable using PyInstaller:

1. Clone this repository.
2. Install PyInstaller with pip:
    ```
   pip install pyinstaller
    ```

3. Create a single executable file with PyInstaller:
    ```
   pyinstaller --onefile main.py
    ```

## Usage

When executed, Py_Metric_Sense will prompt you to select 2 Excel files from your file system and to specify the sheet names within these files. Following this, it will ask for your preferred filter criteria. Upon completion, an Excel file containing the comparison results will be generated.

## Next Steps

1. Refine comparison logic.
2. Integrate comprehensive error handling.
3. Visualize the comparison results using Matplotlib, seaborn, or Tableau.
4. Log the comparison results in an Excel sheet.

5. Develop more options for data comparison.
6. Expand support for comparison of more than two files.
7. Automate the process of generating the comparison results with a Bash script.
8. Log errors and exceptions.


## Classes
import tkinter as tk
from tkinter import filedialog
import sys


class ArgumentHandler:

    # Create a function to open a file dialog and return the selected file path
    @staticmethod
    def select_file(message):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title=message)  # Open the file dialog and get the selected file path
        if not file_path:
            print("Error: No file selected. Exiting.")
            sys.exit(1)
        return file_path

    @staticmethod
    def get_filter_type():
        print("Please select a filter type:")
        print("1. Restricted")
        print("2. Cash Payment")
        print("3. NFR")
        print("4. All")
        while True:
            try:
                user_input = int(input("Enter your choice (1-4): "))
                if 1 <= user_input <= 4:
                    return user_input
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Error: Please enter a number.")

    @staticmethod
    def get_sheet_name():
        while True:
            sheet_name = input("Enter the name of the sheet to read from: ")
            if sheet_name:  # If the string is not empty
                return sheet_name
            else:
                print("Error: Sheet name cannot be empty.")
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
import os
import pandas as pd


class FileEditor:

    @staticmethod
    def read_excel_file(file_path, sheet_name):
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            if df is None:
                print(f"Error: Failed to read excel data. Exiting.")
                exit(1)

            return df

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return None

        except Exception as e:
            print(f"Error: An unexpected error occurred while reading the file {file_path}. {str(e)}")
            return None

    @staticmethod
    def write_to_excel_file(df, file_name):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        filtered_data_file_path = os.path.join(current_dir, file_name)

        try:
            df.to_excel(filtered_data_file_path, index=False)

        except Exception as e:
            print(f"Error: An unexpected error occurred while writing to the file {filtered_data_file_path}. {str(e)}")
import tableauserverclient as tsc


class TableauPublisher:
    def __init__(self, file_path, project_id, data_source_name):
        self.file_path = file_path
        self.project_id = project_id
        self.data_source_name = data_source_name

    def publish_to_tableau_server(self):
        try:
            tableau_auth = tsc.TableauAuth('USERNAME', 'PASSWORD', 'SITE_ID')
            server = tsc.Server('http://SERVER_URL')

            with server.auth.sign_in(tableau_auth):
                new_datasource = tsc.DatasourceItem(self.project_id, name=self.data_source_name)
                new_datasource = server.datasources.publish(new_datasource, self.file_path, 'Overwrite')
                print(f'Successfully published datasource {self.data_source_name} to Tableau Server.')
        except Exception as e:
            print(f"Error: An unexpected error occurred while publishing to Tableau Server. {str(e)}")
from enum import Enum


class Field(Enum):
    CI_ID = 'CI_ID'
    NFR_10 = 'NFR_10'
    DEPLOYMENT_LIFECYCLE_PHASE = 'Deployment_Lifecycle_Phase'
    ASSET_TYPE = 'Asset_Type'
    PPI_CLASSIFICATION = 'PPI_Classification'
    INFORMATION_CLASSIFICATION = 'Information_Classification'
    CASH_PAYMENT_SYSTEMS = 'Cash_Payment_Systems'
from utils.argument_handler import ArgumentHandler
from utils.data_filterer import DataFilterer
from utils.data_comparator import DataComparator
from utils.file_editor import FileEditor

# from utils.tableau_publisher import TableauPublisher


def main():
    print("Welcome to Py_Metric_Sense!")
    # Get the file paths
    first_month_file_path = ArgumentHandler.select_file("Select the Excel file for the first month")
    second_month_file_path = ArgumentHandler.select_file("Select the Excel file for the second month")

    # Get the sheet names
    first_month_sheet_name = ArgumentHandler.get_sheet_name()
    second_month_sheet_name = ArgumentHandler.get_sheet_name()

    # Read the first month data
    first_month_df = FileEditor.read_excel_file(first_month_file_path,
                                                first_month_sheet_name)  # sheet_name='Restricted'
    first_month_data = DataFilterer(first_month_df)

    # Read the second month data
    second_month_df = FileEditor.read_excel_file(second_month_file_path, second_month_sheet_name)
    second_month_data = DataFilterer(second_month_df)

    # Accept user input for the filter criteria
    filter_option = ArgumentHandler.get_filter_type()

    # Filter the data
    first_month_data.apply_filter(filter_option)
    second_month_data.apply_filter(filter_option)

    # Write the filtered data to an Excel file
    FileEditor.write_to_excel_file(second_month_data.data_frame, 'filtered_data.xlsx')

    fields_to_compare = ['NFR_10', 'Deployment_Lifecycle_Phase', 'Asset_Type', 'PPI_Classification',
                         'Information_Classification', 'Cash_Payment_Systems']
    changes = DataComparator.compare_fields(fields_to_compare)
    for field, change_dict in changes.items():
        for (prev_value, curr_value), ci_ids in change_dict.items():
            print(f"For field '{field}', the value changed from '{prev_value}' to '{curr_value}' for CI_IDs: {ci_ids}")

    # Compare the data
    data_comparator = DataComparator(first_month_data, second_month_data)
    print(data_comparator.count_ci_id())

    # Publish the filtered data to Tableau Server
    # publish_to_tableau_server(filtered_data_file_path, 'PROJECT_ID', 'FilteredData')


if __name__ == '__main__':
    main()
