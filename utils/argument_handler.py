class ArgumentHandler:
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
