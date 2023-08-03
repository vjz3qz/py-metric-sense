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
2. Implement additional data filters.
3. Integrate comprehensive error handling.
4. Develop more options for data comparison.
5. Expand support for comparison of more than two files.

6. Write a script to visualize data with Tableau.
7. Integrate a machine learning model for analysing the source of differences.
8. Connect the tool to Tableau for enhanced data visualization.
9. Broaden support for different data types.