import gspread
from google.oauth2.service_account import Credentials


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


def update_spreadsheet(data, worksheet):
    print(f"updating {worksheet} spreadsheet...\n")
    spreadsheet_to_update = SHEET.worksheet(worksheet)
    spreadsheet_to_update.append_row(data)
    print(f"{worksheet} Spreadsheet updated!\n")


def calculate_surplus_data(sales_row):
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):

    print("Calculating Stock Data...\n")

    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_spreadsheet(sales_data, "sales")
    calculate_surplus_data(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_spreadsheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_spreadsheet(stock_data, "stock")


main()
