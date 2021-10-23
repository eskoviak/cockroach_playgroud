from budget import Budget

budget = Budget()

#print(bulk_load(''))
budget.add_expense(budget.bulk_load('json/receipt.json'))

#print(get_expense_categories())

#print(get_sub_categories('Personal'))