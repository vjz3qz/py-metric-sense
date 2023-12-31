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
    if ArgumentHandler.get_print_status():
        FileEditor.write_to_excel_file(first_month_data.get_data_frame(), 'first_month_data.xlsx')
        FileEditor.write_to_excel_file(second_month_data.get_data_frame(), 'second_month_data.xlsx')

    # Compare the data
    data_comparator = DataComparator(first_month_data, second_month_data)

    print("-----------------------------------")
    prev, curr, diff = data_comparator.count_ci_id()
    print("CI_IDs Comparison:")
    print(f"Number of CI_IDs in the first month: {prev}")
    print(f"Number of CI_IDs in the second month: {curr}")
    print(f"Number of CI_IDs that are different: {diff}")
    print("-----------------------------------")
    changes2 = data_comparator.compare_fields2()
    print("Field Comparison:")
    for field, change_dict in changes2.items():
        for (prev_value, curr_value), ci_ids in change_dict.items():
            print(f"For field '{field}', the value changed from '{prev_value}' to '{curr_value}' for CI_IDs: {ci_ids}")

    print("-----------------------------------")
    changes = data_comparator.compare_fields()
    print("Application Comparison:")
    for ci_id, ci_id_changes in changes.items():
        print(f"CI_ID: {ci_id}")
        for field, (prev_value, curr_value) in ci_id_changes.items():
            print(f"For field '{field}', the value changed from '{prev_value}' to '{curr_value}'")

    # Publish the filtered data to Tableau Server
    # publish_to_tableau_server(filtered_data_file_path, 'PROJECT_ID', 'FilteredData')


if __name__ == '__main__':
    main()
