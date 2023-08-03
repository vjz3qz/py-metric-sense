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