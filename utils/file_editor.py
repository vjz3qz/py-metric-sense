import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog


class FileEditor:

    # Create a function to open a file dialog and return the selected file path
    @staticmethod
    def select_file(message):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title=message)  # Open the file dialog and get the selected file path
        return file_path

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
