import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy_cockroachdb import run_transaction

from models import Expense, Expense_category, Expense_sub_category


def add_expense(session, detail):
    new_expense = []

    expense_category = session.query(Expense_category).filter(Expense_category.expense_category == detail.expense_category).first()
    expense_sub_category = session.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == detail.expnese_sub_category).first()

    new_expense.append(Expense(
        date = detail.date,
        expense_category_id = expense_category.id,
        expense_sub_category_id = expense_sub_category.id,
        amount = detail.amount,
        tender = detail.tender,
        expense_detail = json.dumps(detail.exp_detail)
    ))

    session.add_all(new_expense)

def add_fuel_receipt(session):
    detail = {'location' : 'Red Wing, MN', 'vendor': 'Family Fare'}
    #detail = {'mileage': 162030, 'location': 'Hastings, MN'}

    new_expense = []
    
    expense_category = session.query(Expense_category).filter(Expense_category.expense_category =='Misc').first()
    expense_sub_category = session.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == 'Grocery').first()

    #print (expense_category.id,expense_sub_category.id)
    new_expense.append(Expense(date='2021-09-26T19:41:00Z', expense_category_id=expense_category.id,
        expense_sub_category_id=expense_sub_category.id, amount=10.67, tender = 'amex inserted *8200', 
        expense_detail = json.dumps(detail)))
    session.add_all(new_expense)   


if __name__ == '__main__':
    detail = {
        'expense_category' : 'Misc',
        'expense_sub_category' : 'Grocery',
        'exp_detail' : {'location' : 'Red Wing, MN', 'vendor': 'Family Fare'},
        'date' : '2021-09-26T19:41:00Z',
        'amount' : 9999,
        'tender' : 'some form of tender'
    }
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    run_transaction(sessionmaker(bind=engine),
        lambda s : add_expense(s, detail))