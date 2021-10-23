import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy_cockroachdb import run_transaction

from models import Expense, Expense_category, Expense_sub_category, Expense_xref

def add_expense_category(session, cat, sub_cat):
        new_expense_cat = []
        new_expense_sub_cat = []
        new_expense_xref = []

        new_expense_cat.append(Expense_category(expense_category=cat))
        new_expense_sub_cat.append(Expense_sub_category(expense_sub_category=sub_cat))

        session.add_all(new_expense_cat)
        session.add_all(new_expense_sub_cat)

        exp_id = session.query(Expense_category).filter(Expense_category.expense_category ==cat).first()
        exp_sub_id = session.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category==sub_cat).first()

        new_expense_xref.append(Expense_xref(expense_category_id=exp_id.id, expense_sub_category_id=exp_sub_id.id))
        session.add_all(new_expense_xref)
 


if __name__ == '__main__':
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    run_transaction(sessionmaker(bind=engine),
        lambda s: add_expense_category(s, 'Misc', 'Grocery'))