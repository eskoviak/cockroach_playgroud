from budget import Budget
import json

budget = Budget()

#print(bulk_load(''))
#budget.add_expense(budget.bulk_load('json/receipt.json'))

#print(json.dumps(budget.get_expense_categories()))

print(json.dumps(budget.get_sub_categories('Personal')))

#print(budget.get_chart_of_accounts())
##print(json.dumps(budget.get_chart_of_accounts()))