"""module used to run various parts of budete

"""
from budget import Budget
#import json

budget = Budget()

#print(bulk_load(''))
#budget.add_expense(budget.bulk_load_('json/receipt.json'))

#print(json.dumps(budget.get_expense_categories()))

#print(json.dumps(budget.get_sub_categories('Personal')))

#print(budget.get_chart_of_accounts())
##print(json.dumps(budget.get_chart_of_accounts()))

#print(budget.validate_input(budget.bulk_load_csv('data/test/test-Budget Input_bad_cat.csv')))
#print(budget.validate_input(budget.bulk_load_csv('data/Budget Input.csv')))
#budget.add_expense(budget.bulk_load_csv('data/Budget Input.csv'))

#print(budget.get_sub_categories('Vehicle'))
#print(budget.get_chart_of_accounts())

print(budget.backup_database())
