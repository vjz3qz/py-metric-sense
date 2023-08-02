class ArgumentHandler:
    @staticmethod
    def get_filter_type():
        print("Please select a filter type:")
        print("1. Restricted")
        print("2. Cash Payment")
        print("3. NFR")
        print("4. All")
        while True:
            user_input = int(input("Enter your choice (1-4): "))
            if 1 <= user_input <= 4:
                return user_input
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def get_sheet_name():
        sheet_name = input("Enter the name of the sheet to read from: ")
        return sheet_name
