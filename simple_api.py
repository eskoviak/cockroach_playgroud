from budget import Budget
from flask import Flask

app = Flask(__name__)

@app.route('/coa')
def coa():
    budget = Budget()
    return budget.get_chart_of_accounts()

@app.route('/expense_categories')
def expense_categories():
    budget = Budget()
    return budget.get_expense_categories();