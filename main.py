from utils.argument_handler import ArgumentHandler
from utils.data_filterer import DataFilterer
from utils.data_comparator import DataComparator
from utils.file_editor import FileEditor


# from utils.tableau_publisher import TableauPublisher


def get_filter_type():
    print("Please select a filter type:")
    print("1. Restricted")
    print("2. Cash Payment")
    print("3. NFR")
    print("4. All")
    options = {
        1: DataFilterer.filter_apps_with_restricted_ppi_or_cash_payment_systems,
        2: DataFilterer.filter_apps_with_restricted_ppi_or_cash_payment_systems,
        3: DataFilterer.filter_apps_with_restricted_ppi_or_cash_payment_systems,
        4: DataFilterer.filter_apps_with_restricted_ppi_or_cash_payment_systems
    }
    while True:
        user_input = int(input("Enter your choice (1-4): "))
        if user_input in options:
            return options[user_input]
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':

    # Get the file paths
    first_month_file_path = FileEditor.select_file("Select the Excel file for the first month")
    second_month_file_path = FileEditor.select_file("Select the Excel file for the second month")

    # Get the sheet names
    first_month_sheet_name = ArgumentHandler.get_sheet_name()
    second_month_sheet_name = ArgumentHandler.get_sheet_name()

    # Read the first month data
    first_month_df = FileEditor.read_excel_file(first_month_file_path, first_month_sheet_name) # sheet_name='Restricted'
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

    # Compare the data
    data_comparator = DataComparator(first_month_data, second_month_data)
    print(data_comparator.count_ci_id())

    # Publish the filtered data to Tableau Server
    # publish_to_tableau_server(filtered_data_file_path, 'PROJECT_ID', 'FilteredData')
