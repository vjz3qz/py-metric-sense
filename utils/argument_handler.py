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
    def get_filter_type(): # change these to actual names
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

    @staticmethod
    def get_print_status():
        while True:
            yes_or_no = input("Do you want to export the data to Excel sheets? (y/n): ")
            if yes_or_no.lower() == 'y':
                return True
            elif yes_or_no.lower() == 'n':
                return False
            else:
                print("Error: Invalid input. Please try again.")