from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy_cockroachdb import run_transaction

from models import Expense, Expense_category, Expense_sub_category

def add_fuel_receipt(session):
    new_expense = []

    expense_category = session.query(Expense_category).filter(Expense_category.expense_category =='Vehicle').first()
    expense_sub_category = session.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == 'Fuel').first()

    #print (expense_category.id,expense_sub_category.id)
    new_expense.append(Expense(date='2021-09-13T22:21:00', expense_category_id=expense_category.id, expense_sub_category_id=expense_sub_category.id,
        amount=51.79))
    session.add_all(new_expense)   


if __name__ == '__main__':
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    run_transaction(sessionmaker(bind=engine),
        lambda s: add_fuel_receipt(s))