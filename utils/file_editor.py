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
        parent_dir = os.path.dirname(current_dir)
        filtered_data_file_path = os.path.join(parent_dir, file_name)

        try:
            df.to_excel(filtered_data_file_path, index=False)

        except Exception as e:
            print(f"Error: An unexpected error occurred while writing to the file {filtered_data_file_path}. {str(e)}")
