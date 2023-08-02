import pandas as pd
import os
import tableauserverclient as tsc
import tkinter as tk
from tkinter import filedialog

from utils.data_filterer import DataFilterer
from utils.data_comparator import DataComparator


def read_excel_file(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the file {file_path}. {str(e)}")
        return None


def write_to_excel_file(df, file_path):
    try:
        df.to_excel(file_path, index=False)
    except Exception as e:
        print(f"Error: An unexpected error occurred while writing to the file {file_path}. {str(e)}")


def publish_to_tableau_server(file_path, project_id, data_source_name):
    try:
        tableau_auth = tsc.TableauAuth('USERNAME', 'PASSWORD', 'SITE_ID')
        server = tsc.Server('http://SERVER_URL')

        with server.auth.sign_in(tableau_auth):
            new_datasource = tsc.DatasourceItem(project_id, name=data_source_name)
            new_datasource = server.datasources.publish(new_datasource, file_path, 'Overwrite')
            print(f'Successfully published datasource {data_source_name} to Tableau Server.')
    except Exception as e:
        print(f"Error: An unexpected error occurred while publishing to Tableau Server. {str(e)}")


# Create a function to open a file dialog and return the selected file path
def select_file(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=message)  # Open the file dialog and get the selected file path
    return file_path

def get_filter_type():
    print("Please select a filter type:")
    print("1. Restricted")
    print("2. Cash Payment")
    print("3. NFR")
    print("4. All")
    options = {
        '1': 'Restricted PPI',
    }
    while True:
        user_input = input("Enter your choice (1-4): ")
        if user_input in ['1', '2', '3', '4']:
            return user_input
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Use the function to get the file paths
    first_month_file_path = select_file("Select the Excel file for the first month")
    second_month_file_path = select_file("Select the Excel file for the second month")

    # Read the first month data
    first_month_df = read_excel_file(first_month_file_path, 'Restricted')
    if first_month_df is None:
        print("Failed to read first month data. Exiting.")
        exit(1)
    first_month_data = DataFilterer(first_month_df)

    # Read the second month data
    second_month_df = read_excel_file(second_month_file_path, 'Restricted')
    if second_month_df is None:
        print("Failed to read second month data. Exiting.")
        exit(1)
    second_month_data = DataFilterer(second_month_df)

    # Accept user input for the filter criteria
    filter_type = get_filter_type()

    # Filter the data
    first_month_data.filter_apps_with_restricted_ppi_or_cash_payment_systems()
    second_month_data.filter_apps_with_restricted_ppi_or_cash_payment_systems()

    # Write the filtered data to an Excel file
    filtered_data_file_path = os.path.join(current_dir, 'filtered_data.xlsx')
    write_to_excel_file(second_month_data.data_frame, filtered_data_file_path)

    # Compare the data
    data_comparator = DataComparator(first_month_data, second_month_data)
    print(data_comparator.count_ci_id())

    # Publish the filtered data to Tableau Server
    # publish_to_tableau_server(filtered_data_file_path, 'PROJECT_ID', 'FilteredData')
