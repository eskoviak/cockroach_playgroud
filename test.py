"""test.py

"""
from budget import Budget


budget = Budget()

#print(budget.add_expense((budget.bulk_load_s3('Data Sets/Budget Input.csv'))))

print(budget._archive_s3('Budget.csv'))


