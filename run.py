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
    print("Please input the sales data from the last Market")
    print("Data Should be 6 numbers seperated by commas as shown below:")
    print("Eg: 1, 2, 3, 4, 5, 6\n")

    data_str = input("Please enter data here:")
    print(f"the data you provided is {data_str}")


get_sales_data()
