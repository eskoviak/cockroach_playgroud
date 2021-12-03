import csv
import json
from models import Expense

with open('data/Budget Input.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    expenses = []
    for row in reader:
        detail = dict()
        detail["location"] = row["Location"]
        detail["vendor"] = row['Vendor']
        detail['mileage'] = row['Mileage']
        detail['gallons'] = row['Gallons']
        detail['vehicle'] = row['Vehicle']
        detail['balance on account'] = row['Balance_on_account']

        expense = dict()
        expense['expense_category'] = row['Category']
        expense['expense_sub_category'] = row['SubCategory']
        expense['expense_detail'] = json.dumps(detail)
        expense['date'] = row['Date']
        expense['amount'] = row['Amount']
        expense['tender'] = row['Tender']
        expense['memo'] = row['Memo']

        expenses.append(expense)

    print(expenses)
