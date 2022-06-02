import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('burger_maker')


def get_sales_data():
    """
    gather sales figures input from user
    """
    while True:

        print("Please input the sales data from the last Market")
        print("Data Should be 6 numbers seperated by commas as shown below:")
        print("Eg: 1, 2, 3, 4, 5, 6\n")

        data_str = input("Please enter data here:")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is Valid")
            break

    return sales_data


def validate_data(values):

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"You provided {len(values)}, However it can only be 6 values"
            )
    except ValueError as e:
        print(f"Error with Data {e}, please try again.\n")
        return False

    return True


def update_sales_spreadsheet(data):
    """
    update sales spreadsheet
    """
    print("updating sales spreadsheet...\n")
    sales_spreadsheet = SHEET.worksheet("sales")
    sales_spreadsheet.append_row(data)
    print("Sales Spreadsheet Updated correctly\n")


def calculate_surplus_data(sales_row):
    print("Calculating surplus data..\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_spreadsheet(sales_data)
    calculate_surplus_data(sales_data)


main()
